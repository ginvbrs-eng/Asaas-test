"""OCR service abstraction."""

from __future__ import annotations


async def extract_text_from_image(image_bytes: bytes) -> str:
    """Extract text from image bytes using OCR provider."""
    # TODO: integrate pytesseract and pre-processing pipeline.
    _ = image_bytes
    return ""
