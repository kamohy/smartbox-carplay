#!/usr/bin/env python3
"""RV32 disassembly and GP-reference search for SmartBox Andes binaries.

Encoding reference: Andes XAndesPerf binutils patch (2025-11-26),
https://sourceware.org/pipermail/binutils/2025-November/145934.html
The GP word-load/store immediates are signed 19-bit values.
"""

from __future__ import annotations

import argparse
import re
import struct
from pathlib import Path

from capstone import CS_ARCH_RISCV, CS_MODE_RISCVC, CS_MODE_RISCV32, Cs
from elftools.elf.elffile import ELFFile


REGISTERS = [
    "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
    "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
    "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
    "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
]


def sign_extend(value: int, bits: int) -> int:
    sign = 1 << (bits - 1)
    return (value ^ sign) - sign


def addigp(opcode: int) -> tuple[int, int] | None:
    if opcode & 0x307F != 0x100B:
        return None
    immediate = (
        ((opcode >> 21) & 0x3FF) << 1
        | ((opcode >> 20) & 1) << 11
        | ((opcode >> 17) & 7) << 12
        | ((opcode >> 15) & 3) << 15
        | ((opcode >> 31) & 1) << 17
        | ((opcode >> 14) & 1)
    )
    return (opcode >> 7) & 0x1F, sign_extend(immediate, 18)


def gp_memory(opcode: int) -> tuple[str, int, int] | None:
    """Return mnemonic, data register and signed byte offset for Andes GP ops."""
    kind = opcode & 0x707F
    byte_kind = opcode & 0x307F
    if byte_kind in (0x000B, 0x200B, 0x300B):
        store = byte_kind == 0x300B
        name = {0x000B: "nds.lbgp", 0x200B: "nds.lbugp", 0x300B: "nds.sbgp"}[byte_kind]
        width = 1
    elif kind in (0x102B, 0x502B, 0x002B, 0x202B, 0x402B):
        store = kind in (0x002B, 0x402B)
        name = {0x102B: "nds.lhgp", 0x502B: "nds.lhugp", 0x002B: "nds.shgp",
                0x202B: "nds.lwgp", 0x402B: "nds.swgp"}[kind]
        width = 4 if kind in (0x202B, 0x402B) else 2
    else:
        return None
    common = ((opcode >> 17) & 7) << 12 | ((opcode >> 15) & 3) << 15
    if store:
        immediate = ((opcode >> 25) & 0x3F) << 5 | ((opcode >> 7) & 1) << 11 | common
        if width == 4:
            immediate |= ((opcode >> 9) & 7) << 2 | ((opcode >> 8) & 1) << 17 | ((opcode >> 31) & 1) << 18
        else:
            immediate |= ((opcode >> 8) & 0xF) << 1 | ((opcode >> 31) & 1) << 17
            if width == 1:
                immediate |= (opcode >> 14) & 1
        register = (opcode >> 20) & 0x1F
    else:
        immediate = ((opcode >> 20) & 1) << 11 | common
        if width == 4:
            immediate |= ((opcode >> 22) & 0x1FF) << 2 | ((opcode >> 21) & 1) << 17 | ((opcode >> 31) & 1) << 18
        else:
            immediate |= ((opcode >> 21) & 0x3FF) << 1 | ((opcode >> 31) & 1) << 17
            if width == 1:
                immediate |= (opcode >> 14) & 1
        register = (opcode >> 7) & 0x1F
    return name, register, sign_extend(immediate, 19 if width == 4 else 18)


def andes_branch(opcode: int) -> tuple[str, int, int, int] | None:
    kind = opcode & 0x707F
    if kind not in (0x505B, 0x605B, 0x705B):
        return None
    register = (opcode >> 15) & 0x1F
    immediate = (opcode >> 20) & 0x1F | ((opcode >> 7) & 1) << 5
    offset = ((opcode >> 8) & 0xF) << 1 | ((opcode >> 25) & 0x1F) << 5 | ((opcode >> 31) & 1) << 10
    if kind == 0x705B:
        name = "nds.bbs" if opcode & (1 << 30) else "nds.bbc"
    else:
        immediate |= ((opcode >> 30) & 1) << 6
        name = "nds.beqc" if kind == 0x505B else "nds.bnec"
    return name, register, immediate, sign_extend(offset, 11)


def read_string(blob: bytes, virtual_address: int, segments: list[tuple[int, int, int]]) -> str | None:
    for file_offset, address, size in segments:
        if address <= virtual_address < address + size:
            offset = file_offset + virtual_address - address
            match = re.match(rb"[\x09-\x0d\x20-\x7e]{4,}\0", blob[offset:offset + 512])
            if match:
                return match.group()[:-1].decode("ascii")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", type=Path)
    parser.add_argument("--start", type=lambda value: int(value, 0))
    parser.add_argument("--length", default=0x100, type=lambda value: int(value, 0))
    parser.add_argument("--gp", type=lambda value: int(value, 0), help="explicit global pointer, if known")
    parser.add_argument("--find-gp-address", "--find-address", type=lambda value: int(value, 0), help="scan .text for GP, PC-relative and direct branch/call references to this address")
    args = parser.parse_args()

    blob = args.elf.read_bytes()
    with args.elf.open("rb") as fh:
        elf = ELFFile(fh)
        text = elf.get_section_by_name(".text")
        text_address = int(text["sh_addr"])
        text_data = text.data()
        segments = [
            (int(segment["p_offset"]), int(segment["p_vaddr"]), int(segment["p_filesz"]))
            for segment in elf.iter_segments()
            if segment["p_type"] == "PT_LOAD"
        ]
        symbols = {}
        for section in elf.iter_sections():
            if section["sh_type"] in ("SHT_DYNSYM", "SHT_SYMTAB"):
                for symbol in section.iter_symbols():
                    if symbol["st_value"] and symbol.name:
                        symbols[int(symbol["st_value"])] = symbol.name
        plt = elf.get_section_by_name(".plt")
        relocations = elf.get_section_by_name(".rela.plt")
        if plt is not None and relocations is not None:
            dynamic = elf.get_section(relocations["sh_link"])
            for index, relocation in enumerate(relocations.iter_relocations()):
                symbols[int(plt["sh_addr"]) + 32 + index * 16] = dynamic.get_symbol(relocation["r_info_sym"]).name + "@plt"

    if args.start is None and args.find_gp_address is None:
        parser.error("--start or --find-gp-address is required")
    if args.start is not None and not (text_address <= args.start < text_address + len(text_data)):
        parser.error("start address is outside .text")

    gp = args.gp
    decoder = Cs(CS_ARCH_RISCV, CS_MODE_RISCV32 | CS_MODE_RISCVC)
    for candidate in range(0, len(text_data) - 8, 2) if gp is None else ():
        instruction = next(decoder.disasm(text_data[candidate : candidate + 4], text_address + candidate, count=1), None)
        if instruction and instruction.mnemonic == "auipc" and instruction.op_str.startswith("gp, "):
            high = int(instruction.op_str.split(",", 1)[1], 0)
            next_offset = candidate + instruction.size
            following = next(decoder.disasm(text_data[next_offset : next_offset + 4], instruction.address + instruction.size, count=1), None)
            if following and following.mnemonic == "addi" and following.op_str.startswith("gp, gp, "):
                low = int(following.op_str.rsplit(",", 1)[1], 0)
                gp = instruction.address + (sign_extend(high, 20) << 12) + low
                break
    position = args.start - text_address if args.start is not None else 0
    end = min(len(text_data), position + args.length) if args.find_gp_address is None else len(text_data)
    register_values = {}
    while position < end:
        address = text_address + position
        halfword = struct.unpack_from("<H", text_data, position)[0]
        size = 4 if halfword & 0x3 == 0x3 else 2
        chunk = text_data[position : position + size]
        if len(chunk) < size:
            break
        annotation = ""
        decoded = addigp(int.from_bytes(chunk, "little")) if size == 4 else None
        memory = gp_memory(int.from_bytes(chunk, "little")) if size == 4 else None
        branch = andes_branch(int.from_bytes(chunk, "little")) if size == 4 else None
        target = None
        if gp is not None and decoded:
            register_values.clear()
            register, immediate = decoded
            target = gp + immediate
            value = read_string(blob, target, segments)
            mnemonic = "nds.addigp"
            operands = f"{REGISTERS[register]}, {immediate:+#x}  # 0x{target:X}"
            if value is not None:
                annotation = f" {value!r}"
            if target in symbols:
                annotation += f" <{symbols[target]}>"
        elif gp is not None and memory:
            register_values.clear()
            mnemonic, register, immediate = memory
            target = gp + immediate
            operands = f"{REGISTERS[register]}, {immediate:+#x}(gp)  # 0x{target:X}"
            if target in symbols:
                annotation = f" <{symbols[target]}>"
        elif branch:
            register_values.clear()
            mnemonic, register, constant, offset = branch
            target = address + offset
            operands = f"{REGISTERS[register]}, {constant}, {offset:+#x}"
            annotation = f" # 0x{target:X}"
        else:
            instruction = next(decoder.disasm(chunk, address, count=1), None)
            if instruction is None:
                mnemonic = ".word" if size == 4 else ".hword"
                operands = f"0x{int.from_bytes(chunk, 'little'):0{size * 2}X}"
            else:
                mnemonic = instruction.mnemonic
                operands = instruction.op_str
                if gp is not None and (gp_operand := re.search(r"(-?(?:0x[0-9a-f]+|\d+))\(gp\)", operands)):
                    target = gp + int(gp_operand.group(1), 0)
                    annotation = f" # 0x{target:X}"
                if mnemonic in ("jal", "c.jal", "j", "c.j"):
                    destination = address + int(operands.rsplit(",", 1)[-1].strip(), 0)
                    target = destination
                    annotation = f" # 0x{destination:X}"
                    if destination in symbols:
                        annotation += f" <{symbols[destination]}>"
                if mnemonic == "auipc":
                    register, high = operands.split(", ")
                    register_values[register] = address + (sign_extend(int(high, 0), 20) << 12)
                elif mnemonic == "addi" and len(parts := operands.split(", ")) == 3 and parts[1] in register_values:
                    target = register_values[parts[1]] + int(parts[2], 0)
                    annotation = f" # 0x{target:X}"
                    if (value := read_string(blob, target, segments)) is not None:
                        annotation += f" {value!r}"
                    if target in symbols:
                        annotation += f" <{symbols[target]}>"
                    register_values.clear()
                elif mnemonic == "jalr":
                    parts = operands.split(", ")
                    if len(parts) == 3 and parts[1] in register_values:
                        destination = register_values[parts[1]] + int(parts[2], 0)
                        target = destination
                        annotation = f" # 0x{destination:X}"
                        if destination in symbols:
                            annotation += f" <{symbols[destination]}>"
                    register_values.clear()
                elif (memory_operand := re.search(r"(-?(?:0x[0-9a-f]+|\d+))\(([a-z][a-z0-9]*)\)", operands)) and memory_operand.group(2) in register_values:
                    target = register_values[memory_operand.group(2)] + int(memory_operand.group(1), 0)
                    annotation = f" # 0x{target:X}"
                    if target in symbols:
                        annotation += f" <{symbols[target]}>"
                    register_values.clear()
                else:
                    register_values.clear()
        if args.find_gp_address is None or target == args.find_gp_address:
            print(f"0x{address:08X}: {chunk.hex():8}  {mnemonic:12} {operands}{annotation}")
        position += size
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
