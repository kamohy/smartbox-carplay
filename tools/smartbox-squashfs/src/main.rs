//! Offline-only patcher. Original inodes and devices are read from the image.
use std::{env, error::Error, fs::{File, OpenOptions}, io::{BufReader, Cursor}, path::Path};
use backhand::{FilesystemReader, FilesystemWriter, NodeHeader};

fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 || (args.len() - 3) % 3 != 0 {
        return Err("usage: smartbox-squashfs INPUT OUTPUT [replace|add IMAGE_PATH SOURCE]...".into());
    }
    if Path::new(&args[2]).exists() { return Err("output already exists".into()); }
    let fs = FilesystemReader::from_reader(BufReader::new(File::open(&args[1])?))?;
    let mut writer = FilesystemWriter::from_fs_reader(&fs)?;
    // Preserve the source filesystem timestamp for deterministic rebuilding.
    for action in args[3..].chunks_exact(3) {
        if !action[1].starts_with("/ota/www/") || action[1].contains("..") {
            return Err("only files below /ota/www/ may be modified".into());
        }
        let bytes = Cursor::new(std::fs::read(&action[2])?);
        match action[0].as_str() {
            "replace" => writer.replace_file(&action[1], bytes)?,
            "add" => {
                let mode = if action[1] == "/ota/www/cgi-bin/bh-diagnostics.cgi" { 0o755 } else { 0o644 };
                writer.push_file(bytes, &action[1], NodeHeader::new(mode, 0, 0, 1768470083))?;
            },
            _ => return Err("action must be replace or add".into()),
        }
    }
    let mut output = OpenOptions::new().write(true).create_new(true).open(&args[2])?;
    writer.write(&mut output)?;
    println!("offline SquashFS written: {}", args[2]);
    Ok(())
}
