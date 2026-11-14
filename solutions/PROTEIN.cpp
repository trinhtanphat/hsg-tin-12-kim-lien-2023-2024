// Bai 2: DNA template -> mRNA -> amino acids (chi 24 codon trong bang de).
// De chinh thuc dam bao do dai DNA chia het cho 3. Neu du lieu ngoai de
// co 1-2 nucleotide le, vong lap khong tao codon thieu (robustness only).
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

int main() {
    // Online judges may provide stdin even when a stale PROTEIN.INP exists.
    // Prefer stdin; fall back to official file input only at EOF.
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string dna;
    bool fromFile = false;
#ifdef PROTEIN_FORCE_FILE_IO
    {
        ifstream fin("PROTEIN.INP");
        if (!(fin >> dna)) return 0;
        fromFile = true;
    }
#else
    if (!(cin >> dna)) {
        ifstream fin("PROTEIN.INP");
        if (!(fin >> dna)) return 0;
        fromFile = true;
    }
#endif
    auto complement = [](char c) -> char {
        switch (c) {
            case 'A': return 'U';
            case 'T': return 'A';
            case 'C': return 'G';
            case 'G': return 'C';
            default: return '?';
        }
    };
    const unordered_map<string, string> amino = {
        {"UCA", "Ser"}, {"UCU", "Ser"}, {"UCC", "Ser"}, {"UCG", "Ser"},
        {"ACA", "Thr"}, {"ACU", "Thr"}, {"ACC", "Thr"}, {"ACG", "Thr"},
        {"CGA", "Arg"}, {"CGU", "Arg"}, {"CGC", "Arg"}, {"CGG", "Arg"},
        {"GGA", "Gly"}, {"GGU", "Gly"}, {"GGC", "Gly"}, {"GGG", "Gly"},
        {"UAU", "Tyr"}, {"UAC", "Tyr"}, {"CAU", "His"}, {"CAC", "His"},
        {"CCU", "Pro"}, {"CCA", "Pro"}, {"CCC", "Pro"}, {"CCG", "Pro"}
    };

    string answer;
    answer.reserve(dna.size() * 2);
    bool first = true;
    for (size_t i = 0; i + 2 < dna.size(); i += 3) {
        string codon;
        for (int j = 0; j < 3; ++j) codon += complement(dna[i + j]);
        auto it = amino.find(codon);
        if (!first) answer.push_back('-');
        first = false;
        answer += (it == amino.end() ? "Unk" : it->second);
    }
    cout << answer << '\n';

    // Mirror results to the official .OUT file when a .INP file exists.
    // Do not make stdout-only grading fail if the output directory is read-only.
    ifstream check("PROTEIN.INP");
    if (fromFile || check.good()) {
        ofstream fout("PROTEIN.OUT");
        if (fout) fout << answer << '\n';
        else if (fromFile) return 1;
    }
}
