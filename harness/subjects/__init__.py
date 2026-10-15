"""
Pluggable Subject Pack Registry for AI Bootcamp.
Allows any subject teacher (Mathematics, Science, Humanities, Economics, or custom tracks)
to experience the full 4-sprint architecture using authentic student work, domain rubrics,
and subject-relevant misconceptions.
"""
from harness.subjects.registry import (
    SUBJECT_PACKS,
    get_active_subject,
    set_active_subject,
    get_subject_pack,
    list_subject_packs,
)

__all__ = [
    "SUBJECT_PACKS",
    "get_active_subject",
    "set_active_subject",
    "get_subject_pack",
    "list_subject_packs",
]
