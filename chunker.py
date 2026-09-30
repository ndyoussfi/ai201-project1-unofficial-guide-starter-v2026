"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks

def split_into_paragraphs(text: str) -> list[str]:
    """
    One piece per paragraph, with the document's title repeated on each.

    The title line is the only place a hall or course is named, so without it a
    laundry paragraph from housing_morrow_house.txt would not say "Morrow House"
    anywhere and would be indistinguishable from six other halls.
    """
    lines = text.split("\n")
    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()
    paragraphs = [paragraph.strip() for paragraph in body.split("\n\n") if paragraph.strip()]

    if not paragraphs:
        return [text]

    return [f"{title}\n\n{paragraph}" for paragraph in paragraphs]

def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    One chunk per paragraph, with the title repeated on each.

    Unit 1 kept every post whole. 23 of the 88 chunks that produced covered four
    or five topics at once, so they matched every question a little and no
    question well. This splits each post at its paragraph breaks and carries the
    title onto every piece, so a chunk covers one topic and still names what it
    is about.
    """

    chunks: list[Chunk] = []
    
    for document in documents:
        text = document.text.strip()

        if not text:
            continue

        pieces = split_into_paragraphs(text)

        for index, piece in enumerate(pieces):
            chunks.append(Chunk(
                text=piece,
                source=document.source,
                index=index,
                produced_by="chunker.py::split_documents"
            ))

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
