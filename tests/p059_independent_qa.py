"""Independent, file-mode-aware QTOJ p059 PROTEIN differential audit.

Oracle uses a *DNA-triplet-to-amino* table derived manually from the exam
instead of the solution's mRNA table or tests/run_tests.py CODONS mapping.

This tests the published specification, NOT QTOJ's undisclosed test #14.
"""
from __future__ import annotations

import hashlib
import itertools
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_tests import compile_all

# Derived independently by applying DNA->mRNA complementation to each
# codon on the original exam's printed table.
DNA_CODONS = {
    "Ser": ("AGT", "AGA", "AGG", "AGC"),
    "Thr": ("TGT", "TGA", "TGG", "TGC"),
    "Arg": ("GCT", "GCA", "GCG", "GCC"),
    "Gly": ("CCT", "CCA", "CCG", "CCC"),
    "Tyr": ("ATA", "ATG"),
    "His": ("GTA", "GTG"),
    "Pro": ("GGA", "GGT", "GGG", "GGC"),
}
TO_AMINO = {triplet: name for name, codes in DNA_CODONS.items() for triplet in codes}
assert len(TO_AMINO) == 24

ALL = ["".join(p) for p in itertools.product("ATCG", repeat=3)]
assert len(ALL) == 64 and len(set(ALL)) == 64
RNG = random.Random(20261115)


def reference(dna: str) -> str:
    assert 0 < len(dna) <= 100000 and len(dna) % 3 == 0
    assert all(c in "ATCG" for c in dna)
    return "-".join(TO_AMINO.get(dna[i:i + 3], "Unk")
                    for i in range(0, len(dna), 3)) + "\n"


def check_file_mode(binary: Path, dna: str, case: str) -> None:
    with tempfile.TemporaryDirectory(prefix="p059-file-qa-") as folder:
        cwd = Path(folder)
        (cwd / "PROTEIN.INP").write_text(dna + "\n", encoding="ascii")
        start = time.perf_counter()
        run = subprocess.run([str(binary)], cwd=cwd, input="AGT\n",
                             capture_output=True, text=True, timeout=3, check=True)
        elapsed = time.perf_counter() - start
        got = (cwd / "PROTEIN.OUT").read_text(encoding="ascii")
        expected = reference(dna)
        if got != expected:
            position = next((i for i, (a, b) in enumerate(zip(got, expected))
                             if a != b), min(len(got), len(expected)))
            raise AssertionError(
                f"{case}: mismatch at output offset {position}; "
                f"lengths got={len(got)}, expected={len(expected)}; "
                f"got={got[max(position-20, 0):position+35]!r}; "
                f"expected={expected[max(position-20, 0):position+35]!r}")
        assert run.stdout == "", f"{case}: unexpected stdout in file mode"
        print(f"PASS {case}: DNA={len(dna)} output={len(got)} "
              f"sha256={hashlib.sha256(got.encode()).hexdigest()[:12]} "
              f"duration_ms={elapsed*1000:.1f}", flush=True)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="p059-compile-qa-") as td:
        binary = compile_all(Path(td))["PROTEIN"]

        # Every pair of the 64 possible DNA triplets appears adjacently.
        # The whole 64*64 pair enumeration fits well within official bounds.
        pairs = "".join(x + y for x in ALL for y in ALL)
        check_file_mode(binary, pairs, "all-4096-codon-pairs")

        # Overlapping mixed mappings, unknown codons and length boundary.
        cases = {
            "max-random": "".join(RNG.choices(ALL, k=33333)),
            "max-all-unrecognized": "AAA" * 33333,
            "max-all-His": "GTA" * 33333,
            "max-His-Unk": "".join(RNG.choices(("GTA", "GTG", "AAA", "TCT"), k=33333)),
            "max-all-codons-cycled": "".join(ALL[i % 64] for i in range(33333)),
            "max-sample-pattern": "AGTAGGGTAGCACCT" * 6666 + "AGTAGGGTAGCACCT"[:9],
        }
        for name, dna in cases.items():
            if len(dna) > 100000 or len(dna) % 3:
                raise AssertionError(f"{name}: generated input outside exam bounds")
            check_file_mode(binary, dna, name)

        # Check stdin/stdout fallback only when the official file does not exist.
        with tempfile.TemporaryDirectory(prefix="p059-stdin-qa-") as folder:
            data = "AGTAGGGTAGCACCT"
            p = subprocess.run([str(binary)], input=data + "\n", text=True,
                               capture_output=True, cwd=folder, check=True, timeout=3)
            assert p.stdout == reference(data), "stdin fallback mismatch"

    print("PASS: independent DNA codon oracle, 4096 adjacent pairs, "
          "six long file cases, file priority and stdin fallback", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("FAIL:", repr(e), file=sys.stderr)
        raise
