# -*- coding: utf-8 -*-
"""Render buku ID -> Surviving_the_Future_ID.pdf"""
import book_pdf

if __name__ == "__main__":
    pages, chapters, tables = book_pdf.render(
        "/home/user/SetyoWisodo/book_id.md",
        "/home/user/SetyoWisodo/Surviving_the_Future_ID.pdf",
        lang="id",
    )
    print("PDF written: %d pages, %d chapters, %d tables" % (pages, len(chapters), len(tables)))
    for label, pg in list(chapters.items())[:3]:
        print("   ", label, "->", pg)
