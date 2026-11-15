// Bai 2: DNA template -> mRNA -> amino acids (chi 24 codon trong bang de).
// De chinh thuc dam bao do dai DNA chia het cho 3. Neu du lieu ngoai de
// co 1-2 nucleotide le, vong lap khong tao codon thieu (robustness only).
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

int main() {
    // The official task (QTOJ p059) uses File IO. When PROTEIN.INP
    // exists, it is authoritative; PROTEIN.OUT must be produced. Only
    // use stdin/stdout in an environment without the official input file.
    // This prevents a judge's auxiliary stdin from overriding its .INP.
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ifstream fin("PROTEIN.INP");
#ifdef PROTEIN_FORCE_FILE_IO
    if (!fin.is_open()) return 1;
#endif
    const bool fileMode = fin.is_open();
    istream &in = fileMode ? static_cast<istream &>(fin) : cin;
    string dna;
    if (!(in >> dna)) return 0;

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
    if (fileMode) {
        ofstream fout("PROTEIN.OUT", ios::out | ios::trunc);
        if (!fout) return 1;
        fout << answer << '\n';
        if (!fout) return 1;
    } else {
        cout << answer << '\n';
    }
}
