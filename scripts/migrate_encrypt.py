#!/usr/bin/env python3
"""Migration helper: encrypt existing plaintext CA private keys.

Default behavior: create a new file `<orig>`.enc and copy a backup `<orig>`.bak
Optionally replace the original in-place with encrypted bytes using `--inplace`.

Requires `CA_KEK` environment variable (base64-encoded key) or `--kek` argument.
"""
import argparse
import base64
import os
import shutil
import sys
from pathlib import Path

from crypto_utils import encrypt_bytes, decrypt_bytes, get_kek_from_env, MAGIC


def find_candidates(root: Path):
    exts = {".key", ".pem"}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() in exts or "private" in p.name.lower():
            yield p


def load_kek_from_arg_or_env(kek_arg: str | None):
    if os.getenv("CA_KEK"):
        return get_kek_from_env()
    if kek_arg:
        try:
            return base64.b64decode(kek_arg)
        except Exception as e:
            raise RuntimeError("Provided --kek value is not valid base64") from e
    raise RuntimeError("No KEK provided. Set CA_KEK env or pass --kek")


def migrate(path: Path, kek: bytes, inplace: bool, dry_run: bool):
    for p in find_candidates(path):
        data = p.read_bytes()
        if data.startswith(MAGIC):
            print(f"Skipping already-encrypted: {p}")
            continue
        if b"PRIVATE KEY" not in data:
            # skip non-key files
            continue

        enc_bytes = encrypt_bytes(data, kek)

        if inplace:
            backup = p.with_suffix(p.suffix + ".bak")
            if not backup.exists():
                shutil.copy2(p, backup)
                print(f"Backup created: {backup}")
            if not dry_run:
                p.write_bytes(enc_bytes)
                print(f"Replaced {p} with encrypted data (in-place)")
        else:
            target = Path(str(p) + ".enc")
            backup = Path(str(p) + ".bak")
            if not backup.exists():
                shutil.copy2(p, backup)
                print(f"Backup created: {backup}")
            if target.exists():
                print(f"Encrypted target already exists, skipping: {target}")
                continue
            if not dry_run:
                target.write_bytes(enc_bytes)
                print(f"Wrote encrypted file: {target}")

        # verification
        try:
            dec = decrypt_bytes(enc_bytes, kek)
            if dec != data:
                raise RuntimeError(f"Verification failed for {p}")
        except Exception as e:
            print(f"ERROR: verification failed for {p}: {e}", file=sys.stderr)
            # attempt rollback if inplace
            if inplace and backup.exists():
                shutil.copy2(backup, p)
                print(f"Rolled back {p} from {backup}")
            raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", default="data", help="Root data path to scan")
    parser.add_argument("--kek", help="Base64-encoded KEK (optional, otherwise CA_KEK env is used)")
    parser.add_argument("--inplace", action="store_true", help="Replace original files with encrypted bytes (create .bak)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without writing files")
    args = parser.parse_args()

    try:
        kek = load_kek_from_arg_or_env(args.kek)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    root = Path(args.path)
    if not root.exists():
        print(f"Path does not exist: {root}", file=sys.stderr)
        sys.exit(2)

    try:
        migrate(root, kek, args.inplace, args.dry_run)
    except Exception as e:
        print(f"Migration failed: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
