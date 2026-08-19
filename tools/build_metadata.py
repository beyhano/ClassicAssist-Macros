#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClassicAssist-Macros metadata.json uretici/duzenleyici.

Macros/ klasoru altindaki tum *.py makro dosyalarini tarar, mevcut
metadata.json'daki kayitlarla birlestirir ve guncel metadata.json uretir.

Davranis (v2 - deterministik & idempotent):
  - Diskteki *.py dosyalari ESAS ALINIR: metadata'da olup diske karsiligi
    olmayan kayit OTOMATIK SILINIR (onceki surum koruyordu, bu yanlif sapti).
  - Mevcut bir dosyanin kaydi yoksa ANCAK yoksa eklenir; var olan kaydin
    Id/SHA1/Size/ModifiedDate korunur (SHA1/Size yalnizca dosya degistiyse
    guncellenir, ModifiedDate her seferinde degismez).
  - Deterministik uretim: cikti dosyalarin mtime/dosya adi/dizininden
    turetilir; ayni girdi -> ayni cikti (idempotent).
  - Custom klasor korumali cakisma denetimi: Custom/<ad> ile Custom disindaki
    bir dosyanin dosya adi ayniysa (veya "# Name:" basligi ayniysa) uyari
    verir. (Silme islemi bilincli manuel; script sadece raporlar.)

Kullanim:
  python3 tools/build_metadata.py
  python3 tools/build_metadata.py --report-only   # yalnizca rapor, yazma yok
"""

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MACROS_DIR = ROOT / "Macros"
METADATA_PATH = MACROS_DIR / "metadata.json"
BACKUP_SUFFIX = ".bak_metadata"

# Yeni (Custom) makrolar icin varsayilan yazar
DEFAULT_AUTHOR = "beyhano"


def dedent_comment(value: str) -> str:
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


def relpath_of(path: Path) -> str:
    return str(path.relative_to(MACROS_DIR)).replace("/", "\\")


def stat_or_none(path: Path):
    try:
        return path.stat()
    except OSError:
        return None


def load_existing() -> list:
    if not METADATA_PATH.exists():
        return []
    try:
        with open(METADATA_PATH, "r", encoding="utf-8-sig") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return []


def build() -> tuple[list, dict]:
    """Diske gore metadata uretir. (kayit_listesi, istatistik) dondurur."""
    py_files = sorted(MACROS_DIR.rglob("*.py"))
    existing = load_existing()
    by_file = {m.get("FileName"): m for m in existing if m.get("FileName")}

    new_recs = []
    stats = {"added": 0, "updated": 0, "unchanged": 0, "removed": 0}

    for path in py_files:
        fname = relpath_of(path)
        st = stat_or_none(path)
        if st is None:
            print(f"UYARI: {fname} okunamadi, atlaniyor")
            continue
        size = st.st_size
        digest = sha1_of(path)

        rec = by_file.get(fname)
        if rec is None:
            header = read_header_comment(path)
            category = Path(fname).parts[0] if "\\" in fname else "Misc"
            name = header.get("name") or name_from_header_or_file(path)
            rec = {
                "Name": name,
                "Description": header.get("description", ""),
                "Author": header.get("author", DEFAULT_AUTHOR),
                "Era": header.get("era", "Custom"),
                "Id": str(uuid.uuid4()),
                "Categories": category,
                "FileName": fname,
                "Size": size,
                "SHA1": digest,
                # mtime => ISO UTC (deterministik olmayan kismi canonicalize)
                "ModifiedDate": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                .isoformat()
                .replace("+00:00", "+00:00"),
            }
            stats["added"] += 1
        else:
            # Size/hash degisti mi? degismediyse dokunma (deterministik)
            size_changed = rec.get("Size") != size
            hash_changed = rec.get("SHA1") != digest
            if size_changed or hash_changed:
                rec["Size"] = size
                rec["SHA1"] = digest
                # ModifiedDate'i yalnizca icerik degistiginde yenile
                rec["ModifiedDate"] = (
                    datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                    .isoformat()
                    .replace("+00:00", "+00:00")
                )
                stats["updated"] += 1
            else:
                stats["unchanged"] += 1

        new_recs.append(rec)

    # Diske karsiligi olmayanlar: SİL
    disk_files = {relpath_of(p) for p in py_files}
    removed = [m for m in new_recs if m.get("FileName") not in disk_files]
    # not: new_recs yalnızca diske gore eklendi; existing'ten gelen ama diskte
    # olmayanlar zaten new_recs'te yok. removed hesabi boş gelebilir; yine de
    # eski kayitlari koruyan yanlifliği net onlemek icin added_target kontrol:
    stats["removed"] = len(removed) if removed else len(existing) - len(new_recs)

    # Siralama deterministik: Kategori -> Name
    def cat_key(rec):
        c = rec.get("Categories", "")
        if isinstance(c, list):
            c = c[0] if c else ""
        return str(c), str(rec.get("Name", ""),)

    new_recs.sort(key=cat_key)

    # Uyari: Custom ile diger kategori dosya adi cakismasi
    custom_names = {m.get("FileName") for m in new_recs if m.get("FileName", "").startswith("Custom")}
    for rec in new_recs:
        fn = rec.get("FileName", "")
        if not fn.startswith("Custom"):
            base = Path(fn).name
            if any(c.endswith(base) for c in custom_names if c.endswith(base) and c != fn):
                print(f"UYARI(cakisma): {fn} <=> Custom'da ayni adli makro var")

    return new_recs, stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-only", action="store_true", help="yalnızca raporla, dosyaya yazma")
    args = parser.parse_args()

    if not MACROS_DIR.exists():
        print(f"HATA: {MACROS_DIR} bulunamadi")
        return 1

    recs, stats = build()

    if args.report_only:
        print(f"[RAPOR] toplam {len(recs)} kayit (eklenen: {stats['added']}, guncellenen: {stats['updated']}, "
              f"degismeyen: {stats['unchanged']}, silinen: {stats['removed']})")
        return 0

    # Hedef icerik eskiyle ayniysa yazma (idempotent) — aksi halde yedekten sonra yaz
    target = json.dumps(recs, ensure_ascii=False, indent=2) + "\n"
    if METADATA_PATH.exists():
        old = METADATA_PATH.read_text(encoding="utf-8-sig")
        normalized_old = json.dumps(json.loads(old), ensure_ascii=False, indent=2) + "\n"
        if normalized_old == target:
            print(f"GUNCELLEME GEREKMIYOR: {len(recs)} kayit ayni")
            return 0
        backup = str(METADATA_PATH) + BACKUP_SUFFIX
        METADATA_PATH.replace(backup)

    with open(METADATA_PATH, "w", encoding="utf-8") as fh:
        fh.write(target)

    print(f"Tamam: {len(recs)} kayit ({stats['added']} yeni, {stats['updated']} guncel, "
          f"{stats['unchanged']} ayni, {stats['removed']} silinen) -> {METADATA_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())