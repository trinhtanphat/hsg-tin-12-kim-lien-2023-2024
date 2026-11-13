"""Release audit for three user scans, Word/PDF and local Pages assets."""
from __future__ import annotations
import hashlib, re, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs"
EXPECTED={
 "page-1.png":"c7c03c1992e9b5238c9e12b96ce0015d0273c8c2c5b0016108074c4852194c6c",
 "page-2.png":"4b8095f7f1df8f678dd233427b0f7a095741aaaa3d126e5e06bfa993c54df6c7",
 "page-3.png":"c43c502d47ec3fd596e8cdafb68de55678f2fe229448e69f38affa46cd3c8467",
}
for filename,sha in EXPECTED.items():
    path=DOCS/"assets/exam/original"/filename
    assert path.is_file(),path
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    assert actual==sha,(filename,actual)
    assert (DOCS/"assets/exam"/filename).is_file()
    print("ORIGINAL_SCAN_PASS",filename)
for filename in ("De-thi-Kim-Lien-2023-2024-scan.docx","De-thi-tom-tat-bien-tap.docx"):
    path=DOCS/"downloads"/filename
    assert path.is_file()
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        names=set(z.namelist())
        assert "[Content_Types].xml" in names and "word/document.xml" in names
        media=[n for n in names if n.startswith("word/media/")]
        assert len(media)>=3,(filename,len(media))
        xml=z.read("word/document.xml")
        if "bien-tap" in filename:
            for token in ("PRIME","PROTEIN","BILLARD","DIVIDE","ALKANE"):
                assert token.encode() in xml,token
    print("DOCX_PASS",filename)
pdf=DOCS/"downloads"/"De-thi-Kim-Lien-2023-2024-scan.pdf"
assert pdf.is_file() and pdf.read_bytes()[:5]==b"%PDF-"
assert pdf.stat().st_size>100000
print("PDF_SCAN_PASS",pdf.stat().st_size)
readme=(ROOT/"README.md").read_text(encoding="utf-8")
outside=readme.split("```")[::2]
assert all("\\n" not in chunk for chunk in outside),"literal backslash-n outside code fence"
print("README_LINK_FORMAT_PASS")
html=(DOCS/"index.html").read_text(encoding="utf-8")
links=re.findall(r'(?:href|src)="(\./[^"]+)"',html)
for link in links:
    assert not link.startswith("../")
    local=DOCS/link[2:]
    assert local.is_file(),f"Broken local link: {link}"
print("LOCAL_LINKS_PASS",len(links))
print("RELEASE_ASSET_AUDIT_PASS")
