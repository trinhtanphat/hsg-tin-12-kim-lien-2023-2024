"""Verify 420 published INP/OUT pairs by compiling/running all C++17 solutions."""
from __future__ import annotations
import hashlib, json, sys, tempfile, zipfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_tests import compile_all, run
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"docs/assets/test-manifest.json").read_text(encoding="utf-8"))
expected={"PRIME":100,"PROTEIN":100,"BILLARD":100,"DIVIDE":100,"ALKANE":20}
assert data["official_constraints_only"] is True
assert {k:v["count"] for k,v in data["problems"].items()}==expected
checked=0
with tempfile.TemporaryDirectory(prefix="kim-lien-bank-check-") as tmp:
    bins=compile_all(Path(tmp))
    for name,amount in expected.items():
        base=ROOT/"tests/generated"/name
        meta=json.loads((base/"manifest.json").read_text(encoding="utf-8"))
        assert meta["count"]==amount
        archive=ROOT/"docs"/data["problems"][name]["zip"]
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==data["problems"][name]["zip_sha256"]
        with zipfile.ZipFile(archive) as z:
            bad=z.testzip()
            assert bad is None,(archive,bad)
            assert len([x for x in z.namelist() if x.endswith(".INP")])==amount
        for row in meta["cases"]:
            folder=base/row["id"]
            inp=(folder/(name+".INP")).read_text(encoding="utf-8")
            out=(folder/(name+".OUT")).read_text(encoding="utf-8")
            assert hashlib.sha256(inp.encode()).hexdigest()==row["input_sha256"]
            assert hashlib.sha256(out.encode()).hexdigest()==row["output_sha256"]
            actual=run(bins[name],inp,timeout=20)
            assert actual==out.strip(),f"{name} {row['id']} mismatch: {actual[:50]!r} != {out[:50]!r}"
            checked+=1
        print(f"PASS {name}: {amount}/{amount} generated cases",flush=True)
assert checked==420
print("PASS GENERATED CASE BANK: 420/420; SHA-256 + ZIP CRC + C++17 output verified")
