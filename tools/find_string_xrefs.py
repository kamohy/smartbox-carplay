#!/usr/bin/env python3
"""Find simple RISC-V AUIPC/ADDI references to a string in an ELF file."""

from __future__ import annotations

import argparse
from pathlib import Path

from capstone import CS_ARCH_RISCV, CS_MODE_RISCVC, CS_MODE_RISCV32, Cs
from capstone.riscv import RISCV_OP_IMM, RISCV_OP_REG
from elftools.elf.elffile import ELFFile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf", type=Path)
    parser.add_argument("string")
    parser.add_argument("--context", type=int, default=10)
    args = parser.parse_args()

    needle = args.string.encode("utf-8") + b"\0"
    blob = args.elf.read_bytes()
    offsets: list[int] = []
    start = 0
    while (found := blob.find(needle, start)) >= 0:
        offsets.append(found)
        start = found + 1
    if not offsets:
        parser.error("string not found")

    with args.elf.open("rb") as fh:
        elf = ELFFile(fh)
        if elf["e_machine"] != "EM_RISCV" or elf.elfclass != 32:
            parser.error("only 32-bit RISC-V ELF files are supported")

        targets: list[int] = []
        for offset in offsets:
            for segment in elf.iter_segments():
                begin = int(segment["p_offset"])
                end = begin + int(segment["p_filesz"])
                if segment["p_type"] == "PT_LOAD" and begin <= offset < end:
                    targets.append(int(segment["p_vaddr"]) + offset - begin)
                    break

        text = elf.get_section_by_name(".text")
        code = text.data()
        base = int(text["sh_addr"])

    decoder = Cs(CS_ARCH_RISCV, CS_MODE_RISCV32 | CS_MODE_RISCVC)
    decoder.detail = True
    decoder.skipdata = True
    instructions = list(decoder.disasm(code, base))
    matches: list[int] = []
    for index, instruction in enumerate(instructions):
        if instruction.mnemonic != "auipc" or len(instruction.operands) != 2:
            continue
        rd, immediate = instruction.operands
        if rd.type != RISCV_OP_REG or immediate.type != RISCV_OP_IMM:
            continue
        high = immediate.imm
        if high >= 0x80000:
            high -= 1 << 20
        partial = instruction.address + (high << 12)
        for following in instructions[index + 1 : index + 5]:
            if following.mnemonic not in {"addi", "c.addi"} or len(following.operands) < 2:
                continue
            operands = following.operands
            if following.mnemonic == "addi" and len(operands) == 3:
                dest, source, addend = operands
                if (
                    dest.type == RISCV_OP_REG
                    and source.type == RISCV_OP_REG
                    and addend.type == RISCV_OP_IMM
                    and dest.reg == rd.reg
                    and source.reg == rd.reg
                    and partial + addend.imm in targets
                ):
                    matches.append(index)

    print(f"string={args.string!r} targets={','.join(hex(value) for value in targets)} xrefs={len(matches)}")
    for match in matches:
        first = max(0, match - args.context)
        last = min(len(instructions), match + args.context + 5)
        print(f"\n--- xref near 0x{instructions[match].address:X} ---")
        for instruction in instructions[first:last]:
            marker = ">" if instruction.address == instructions[match].address else " "
            print(f"{marker} 0x{instruction.address:08X}: {instruction.mnemonic:8} {instruction.op_str}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
