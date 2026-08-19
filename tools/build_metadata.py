#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClassicAssist-Macros metadata.json uretici/duzenleyici.

Macros/ klasoru altindaki tum *.py makro dosyalarini tarar, mevcut
metadata.json'daki kayitlarla birlestirir ve guncel metadata.json uretir.

Davranis:
  - Mevcut kayitlar YENIDEN YAZILMAZ: Id, SHA1, Size, ModifiedDate, Name,
    Author, Era, Description korunur (mevcut metadata'daki degerler asildir).
  - Diskte var olup metadata'da OLMAYAN yeni bir .py gorulurse eklenir:
      Name        -> dosya adindan (uzanti atilmis, ilk harf buyuk) VEYA "# Name:" yorumundan
      Description -> "# Description:" yorumundan (yoksa bos)
      Author      -> "# Author:" yorumundan (yoksa "beyhano")
      Era         -> "# Era:" yorumundan (yoksa "Custom")
      Categories  -> diskteki ust klasor adi  (ornek: Custom)
      FileName    -> klasore gore yol, backslash ayiriciyla
      Size        -> dosyanin byte boyutu
      SHA1        -> dosyanin SHA-1'i (buyuk harf hex)
      Id          -> rastgele UUID v4
      ModifiedDate-> dosya mtime
  - metadata'da gorunen ama diske karsiligi OLMAYAN bir kayit YENIDEN YAZILIR
    YERINE birebir korunur (silmez), boylece eski kayitlar kaybolmaz.

Kullanim:
  python3 tools/build_metadata.py
"""

import hashlib
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MACROS_DIR = ROOT / "Macros"
METADATA_PATH = MACROS_DIR / "metadata.json"


def dedent_comment(value: str) -> str:
    """Yorum satirinin '#' sonrasi boslugunu temizle."""
    return value.strip()


def read_header_comment(path: Path) -> dict:
    """Dosyanin basindaki yorumlardan Name/Description/Author/Era/Shard al."""
    result = {}
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
            for _ in range(40):
                line = fh.readline()
                if not line:
                    break
                if not line.lstrip().startswith("#"):
                    # yorumlar sadece dosyanin baskindadir; ilk kod satirinda dur
                    if "#" not in line:
                        continue
                m = re.match(r"^\s*#\s*([A-Za-z]+)\s*:\s*(.*)$", line)
                if m:
                    key = m.group(1).lower()
                    value = dedent_comment(m.group(2))
                    if key in ("name", "description", "author", "era", "shard"):
                        result[key] = value
    except OSError:
        pass
    return result


def sha1_of(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def name_from_header_or_file(path: Path) -> str:
    header = read_header_comment(path)
    if header.get("name"):
        return header["name"].strip()
    stem = path.stem.replace("-", " ").replace("_", " ").strip()
    return " ".join(word.capitalize() for word in stem.split()) if stem else path.stem


def main() -> int:
    if not MACROS_DIR.exists():
        print(f"HATA: {MACROS_DIR} bulunamadi")
        return 1

    # Mevcut metadata
    existing = []
    if METADATA_PATH.exists():
        try:
            with open(METADATA_PATH, "r", encoding="utf-8-sig") as fh:
                existing = json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"UYARI: mevcut metadata okunamadi ({exc}), sifirdan olusturuyorum")
            existing = []

    # Dosyadan diske gore kayitlari eşle
    by_file = {mac["FileName"]: mac for mac in existing if mac.get("FileName")}

    # Disk taramasi
    py_files = sorted(MACROS_DIR.rglob("*.py"))

    # Yeni eklenen makrolar (diskte var, metadata'da yok)
    added = 0
    updated = 0
    for path in py_files:
        rel = path.relative_to(MACROS_DIR)
        fname = str(rel).replace("/", "\\")

        if fname in by_file:
            # surede guncelleme: boyut ve hash degisti mi? (sadece bilgi amaci)
            existing_rec = by_file[fname]
            try:
                size = path.stat().st_size
                if existing_rec.get("Size") != size:
                    existing_rec["Size"] = size
                digest = sha1_of(path)
                if existing_rec.get("SHA1") != digest:
                    existing_rec["SHA1"] = digest
                updated += 1
            except OSError:
                pass
            continue

        # Yeni kayit olustur
        try:
            size = path.stat().st_size
        except OSError as exc:
            print(f"UYARI: {rel} okunamadi ({exc})")
            continue

        header = read_header_comment(path)
        category = rel.parts[0] if len(rel.parts) > 1 else "Misc"
        name = header.get("name") or name_from_header_or_file(path)

        rec = {
            "Name": name,
            "Description": header.get("description", ""),
            "Author": header.get("author", "beyhano"),
            "Era": header.get("era", "Custom"),
            "Id": str(uuid.uuid4()),
            "Categories": category,
            "FileName": fname,
            "Size": size,
            "SHA1": sha1_of(path),
            "ModifiedDate": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "+00:00"),
        }
        existing.append(rec)
        by_file[fname] = rec
        added += 1
        print(f"+ {fname}  ({name})")

    # metadata'da olup diske karsiligi olmayanlar: korunur (not duser)
    missing_on_disk = [f for f in by_file if not (MACROS_DIR / f.replace("\\", "/")).exists()]
    if missing_on_disk:
        print(f"BILGI: {len(missing_on_disk)} kayit diskte yok, metadata'da korundu.")

    # Siralama: Kategori -> Name
    # Categories bazi eski kayitlarda liste olabilir (CategoriesConverter), normalize et
    def cat_key(rec):
        c = rec.get("Categories", "")
        if isinstance(c, list):
            c = c[0] if c else ""
        return str(c), str(rec.get("Name", ""))

    existing.sort(key=cat_key)

    with open(METADATA_PATH, "w", encoding="utf-8") as fh:
        json.dump(existing, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print(f"Tamam: {len(existing)} kayit (yeni: {added}, boyut/hash guncel: {updated}) -> {METADATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())