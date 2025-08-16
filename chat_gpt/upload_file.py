# upload_file.py
import os
import time
import csv
from typing import Iterable, List, Tuple, Optional
from openai import OpenAI

RECORD_FILE = "file_id_record.csv"
CSV_HEADERS = ["file_id", "path", "timestamp"]


# ── CSV helpers ────────────────────────────────────────────────────────────────

def ensure_file_id_record():
    if not os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()

def append_record(file_id: str, path: str):
    ensure_file_id_record()
    with open(RECORD_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writerow({"file_id": file_id, "path": os.path.abspath(path), "timestamp": str(int(time.time()))})


# ── Upload / Delete files ─────────────────────────────────────────────────────

def upload_file(client: OpenAI, path: str) -> str:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ File not found: {path}")
    with open(path, "rb") as fh:
        up = client.files.create(file=fh, purpose="assistants")  # still valid for Vector Stores
    append_record(up.id, path)
    return up.id

def upload_files(paths: Iterable[str]) -> List[str]:
    # NB: The OpenAI client is created in main; import get_api_key or pass a client?
    # We'll pass a client from main for better reuse—but to keep a simple signature
    # that matches the earlier code, we lazy-create a client here only if needed.
    from get_api_key import get_api_key
    client = OpenAI(api_key=get_api_key())

    file_ids: List[str] = []
    for p in paths:
        p = p.strip()
        if not p:
            continue
        try:
            fid = upload_file(client, p)
            file_ids.append(fid)
        except Exception as e:
            print(f"❌ Failed to upload '{p}': {e}")
    return file_ids

def delete_file_by_id(client: OpenAI, file_id: str) -> bool:
    try:
        client.files.delete(file_id)
        # Also clean CSV
        try:
            rows = []
            with open(RECORD_FILE, "r", newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            rows = [r for r in rows if r.get("file_id") != file_id]
            with open(RECORD_FILE, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                w.writeheader()
                w.writerows(rows)
        except Exception:
            pass
        return True
    except Exception as e:
        print(f"⚠️ Failed to delete '{file_id}': {e}")
        return False


# ── Vector store helpers for File Search ──────────────────────────────────────
# Docs: File Search with Responses API uses vector stores. :contentReference[oaicite:1]{index=1}

VEC_STORE_FILE = "vector_store_id.txt"

def _save_vs_id(vs_id: str, session_name: str):
    os.makedirs(".state", exist_ok=True)
    with open(os.path.join(".state", f"{session_name}_{VEC_STORE_FILE}"), "w", encoding="utf-8") as f:
        f.write(vs_id)

def _load_vs_id(session_name: str) -> Optional[str]:
    path = os.path.join(".state", f"{session_name}_{VEC_STORE_FILE}")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() or None
    return None

def ensure_or_create_vector_store(client: OpenAI, session_name: str, file_ids: List[str]) -> str:
    """
    Create (or reuse) a vector store for this session and ingest the given files.
    Returns vector_store_id.
    """
    vs_id = _load_vs_id(session_name)
    if not vs_id:
        vs = client.vector_stores.create(name=f"vs:{session_name}")
        vs_id = vs.id
        _save_vs_id(vs_id, session_name)

    # Add files and wait for ingestion to finish
    try:
        client.vector_stores.file_batches.create_and_poll(
            vector_store_id=vs_id,
            file_ids=file_ids
        )
    except Exception as e:
        print(f"⚠️ Ingestion failed for some files: {e}")
    return vs_id


# ── Input parsing ─────────────────────────────────────────────────────────────

def parse_paths_and_ids(raw: str) -> Tuple[List[str], List[str]]:
    """
    Split comma-separated input into (paths_to_upload, existing_file_ids).
    Accepts both file-... and file_... id prefixes.
    """
    paths: List[str] = []
    ids: List[str] = []
    if not raw:
        return paths, ids

    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        if item.startswith(("file-", "file_")):
            ids.append(item)
        elif os.path.isfile(item):
            paths.append(item)
        else:
            print(f"⚠️ Skipped invalid input (not a file path or file_id): '{item}'")
    return paths, ids
