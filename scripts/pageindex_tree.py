"""Arbre PageIndex Flash d'un PDF, sans LLM ni réseau, en json sur stdout.

Lancé par `index --pageindex` dans le venv dédié :
    .venv-pageindex/bin/python -I scripts/pageindex_tree.py <pdf>
Installation : `just install-pageindex` (pageindex 0.4.1 en --no-deps + 6 paquets, 18 Mo).
Sortie : liste plate [{title, page, level}] ; les nœuds synthétiques « Preface »
et « … (intro) » sont retirés, les titres fusionnés par « ; » séparés.
"""

from __future__ import annotations

import json
import os
import socket
import sys


def _forbid_network() -> None:
    os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
    for key in list(os.environ):
        if key.endswith("_API_KEY"):
            del os.environ[key]

    def deny(*_a, **_k):
        raise RuntimeError("pageindex_tree : appel réseau interdit")

    socket.socket.connect = deny  # type: ignore[method-assign]
    socket.create_connection = deny  # type: ignore[assignment]
    socket.getaddrinfo = deny  # type: ignore[assignment]


def flatten(nodes: list[dict], depth: int = 1) -> list[dict]:
    out: list[dict] = []
    for n in nodes:
        title = (n.get("title") or "").strip()
        synthetic = title == "Preface" or title.endswith("(intro)")
        if title and not synthetic:
            for part in title.split("; "):
                out.append({"title": part.strip(), "page": int(n.get("start_index") or 0), "level": depth})
        out.extend(flatten(n.get("nodes") or [], depth + 1))
    return out


def main(pdf: str) -> None:
    _forbid_network()
    from pageindex.flash import page_index_flash

    res = page_index_flash(pdf, summary=False, optimize="merge", use_embedded_toc=False)
    json.dump(flatten(res.get("structure") or []), sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage : pageindex_tree.py <pdf>")
    main(sys.argv[1])
