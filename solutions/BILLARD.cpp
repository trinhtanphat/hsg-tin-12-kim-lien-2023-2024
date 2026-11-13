// Bai 3: Ban bi-a. Trai phep phan xa trong hinh chu nhat thanh chuyen dong tren duong thang.
#include <algorithm>
#include <cstdio>
#include <iostream>
using namespace std;

long long coordinate(long long length, long long start,
                     long long velocity, long long seconds) {
    const long long period = 2 * length;
    // Lay modulo truoc khi nhan de an toan ca voi t va v lon.
    long long unfolded = (start + (velocity % period) * (seconds % period)) % period;
    if (unfolded < 0) unfolded += period;
    return min(unfolded, period - unfolded);
}

int main() {
    if (FILE *f = fopen("BILLARD.INP", "r")) {
        fclose(f);
        freopen("BILLARD.INP", "r", stdin);
        freopen("BILLARD.OUT", "w", stdout);
    }
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long m, n, x, y, vx, vy, t;
    if (!(cin >> m >> n >> x >> y >> vx >> vy >> t)) return 0;
    cout << coordinate(m, x, vx, t) << ' '
         << coordinate(n, y, vy, t) << '\n';
}
