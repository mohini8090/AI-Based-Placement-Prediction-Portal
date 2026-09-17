"""
MongoDB documents use `_id` (an ObjectId, not JSON-serializable). This
converts that into a plain string `id` field, which is what every
schema in schemas.py expects.
"""
from typing import Optional


def serialize_doc(doc: Optional[dict]) -> Optional[dict]:
    if doc is None:
        return None
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc
