"""Extraction en masse du texte de `documents/` vers `build/terrain/` (git-ignoré).

Utilitaire d'analyse, pas une commande `just` : sert à parcourir des dossiers
réels (dossiers de camp, UA de cours) sans les ingérer comme sources.

    uv run python -I scripts/terrain.py [documents/sous-dossier ...]

Écrit, pour chaque fichier porteur de texte, `build/terrain/<chemin>.md` et un
manifeste `build/terrain/manifest.tsv` (chemin, ext, octets, mots, statut).
Les médias (images, vidéos, audio) sont listés mais pas convertis.
Les formats anciens (.doc, .xls, .odt, .rtf, .pages, .dot) passent par
LibreOffice headless avant markitdown.
"""

from __future__ import annotations

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "documents"
OUT = ROOT / "build" / "terrain"

TEXT_EXT = {".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".md", ".csv", ".html", ".xml"}
SOFFICE_EXT = {".doc": "docx", ".dot": "docx", ".dotx": "docx", ".dotm": "docx", ".xls": "xlsx",
               ".xlt": "xlsx", ".xltx": "xlsx", ".odt": "docx", ".ods": "xlsx", ".odp": "pptx",
               ".rtf": "docx", ".pages": "docx", ".numbers": "xlsx"}
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".gif", ".heic", ".tiff", ".bmp", ".jfif", ".svg", ".eps",
             ".mp4", ".mov", ".mkv", ".m4a", ".dng", ".afpub", ".afdesign", ".afphoto", ".indd",
             ".zip", ".url", ".webloc", ".plist", ".rels", ".gpx", ".kml", ".excalidraw",
             ".ds_store", ".mxdl"}
MAX_BYTES = 150 * 1024 * 1024
FILE_TIMEOUT = 90  # secondes par fichier (xlsx à formules, pptx lourds)


class Timeout(Exception):
    pass


def _alarm(signum, frame):
    raise Timeout()


def pdf_text(path: Path) -> str:
    import pymupdf

    parts = []
    with pymupdf.open(path) as doc:
        for i, page in enumerate(doc, start=1):
            parts.append(f"<!-- p.{i} -->\n{page.get_text()}")
    return "\n".join(parts)


def office_text(path: Path) -> str:
    from markitdown import MarkItDown

    return MarkItDown().convert(str(path)).text_content


def soffice_text(path: Path, target: str) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", target, "--outdir", tmp, str(path)],
            check=True, capture_output=True, timeout=180,
        )
        produced = list(Path(tmp).glob(f"*.{target}"))
        if not produced:
            raise RuntimeError("soffice: aucune sortie")
        return office_text(produced[0])


def extract(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return pdf_text(path)
    if ext in {".txt", ".md", ".csv", ".xml", ".html"}:
        return path.read_text(errors="replace")
    if ext in SOFFICE_EXT:
        return soffice_text(path, SOFFICE_EXT[ext])
    return office_text(path)


def main(targets: list[str]) -> None:
    roots = [Path(t).resolve() for t in targets] if targets else [DOCS]
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = OUT / "manifest.tsv"
    done = set()
    if manifest.exists():
        done = {line.split("\t")[0] for line in manifest.read_text().splitlines()[1:]}
    else:
        manifest.write_text("path\text\tbytes\twords\tstatus\n")
    with manifest.open("a") as mf:
        for root in roots:
            for path in sorted(p for p in root.rglob("*") if p.is_file()):
                rel = path.relative_to(DOCS)
                if str(rel) in done:
                    continue
                ext = path.suffix.lower()
                size = path.stat().st_size
                status, words = "skipped", 0
                if ext in MEDIA_EXT or (ext not in TEXT_EXT and ext not in SOFFICE_EXT):
                    status = "media" if ext in MEDIA_EXT else "unknown"
                elif size > MAX_BYTES:
                    status = "too-big"
                else:
                    signal.signal(signal.SIGALRM, _alarm)
                    signal.alarm(FILE_TIMEOUT)
                    try:
                        text = extract(path)
                        words = len(text.split())
                        dest = OUT / rel.with_suffix(rel.suffix + ".md")
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_text(text)
                        status = "ok" if words >= 20 else "empty"
                    except Exception as exc:  # noqa: BLE001
                        status = f"error:{type(exc).__name__}"
                    finally:
                        signal.alarm(0)
                mf.write(f"{rel}\t{ext}\t{size}\t{words}\t{status}\n")
                mf.flush()
    print(f"manifeste : {manifest}")


if __name__ == "__main__":
    main(sys.argv[1:])
