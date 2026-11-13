// Bai 5: Dem cac cay khong danh nhan n dinh, bac <= 4 (alkane structural isomers).
// Su dung multiset generating functions va dinh ly dissymmetry cho cay.
#include <bits/stdc++.h>
using namespace std;

using i64 = long long;
constexpr int N = 20;
using Poly = array<i64, N + 1>;
using Multi = array<Poly, 5>;

// H[k](z): so cach chon mot multiset gom dung k cay 'planted'.
// k H_k(z) = sum_{j=1..k} A(z^j) H_{k-j}(z).
Multi multisets(const Poly &a) {
    Multi h{};
    h[0][0] = 1;
    for (int k = 1; k <= 4; ++k) {
        for (int degree = 1; degree <= N; ++degree) {
            i64 sum = 0;
            for (int j = 1; j <= k; ++j) {
                for (int size = 1; j * size <= degree; ++size) {
                    sum += a[size] * h[k - j][degree - j * size];
                }
            }
            assert(sum % k == 0);
            h[k][degree] = sum / k;
        }
    }
    return h;
}

int main() {
    if (FILE *f = fopen("ALKANE.INP", "r")) {
        fclose(f);
        freopen("ALKANE.INP", "r", stdin);
        freopen("ALKANE.OUT", "w", stdout);
    }
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    if (n < 1 || n > N) return 0;

    // A(z) = z * (H_0 + H_1 + H_2 + H_3):
    // o goc, mot canh danh cho cha => toi da 3 nhanh con.
    Poly a{};
    for (int size = 1; size <= N; ++size) {
        Multi h = multisets(a);
        for (int k = 0; k <= 3; ++k) a[size] += h[k][size - 1];
    }

    Multi h = multisets(a);
    Poly rooted{}, orderedEdge{};
    for (int size = 1; size <= N; ++size) {
        for (int k = 0; k <= 4; ++k) rooted[size] += h[k][size - 1];
        for (int left = 1; left < size; ++left) {
            orderedEdge[size] += a[left] * a[size - left];
        }
    }

    // Cay khong goc = cay co danh dau dinh + cay danh dau canh
    //                - cay co canh duoc dinh huong.
    // H_2 la cay danh dau canh khong dinh huong, A*A danh dau canh co huong.
    cout << rooted[n] + h[2][n] - orderedEdge[n] << '\n';
}
