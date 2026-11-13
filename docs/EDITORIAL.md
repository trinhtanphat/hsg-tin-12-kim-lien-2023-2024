# Editorial — lời giải chi tiết 5 bài (C++17)

> Nguồn yêu cầu: 3 trang đề chọn đội tuyển HSG Tin học lớp 12 Hà Nội 2023–2024, Trường THPT Kim Liên, ngày 30/08/2023. Đây là lời giải độc lập.

## Bài 1. PRIME — Tích ba số nguyên tố (5 điểm)

**Bài toán.** Với số nguyên dương `n`, kiểm tra `n = p*q*r` với `p,q,r` là số nguyên tố, có thể trùng nhau.

**Ý tưởng.** Phân tích `n` thành thừa số nguyên tố và **đếm số lượng theo bội số** (đếm `2` ba lần nếu `n=8`). Đáp án `YES` khi và chỉ khi tổng số thừa số nguyên tố bằng 3.

1. Lặp chia hết cho 2 và tăng `count`.
2. Thử `d = 3, 5, 7,...` đến khi `d*d > n` hiện tại; mỗi lần chia hết lại tăng `count`.
3. Sau vòng lặp, nếu `n>1`, chính nó là thừa số nguyên tố cuối cùng.
4. In `YES` đúng khi `count=3`, ngược lại `NO`.

**Chứng minh.** Mỗi lần chia loại bỏ đúng một thừa số nguyên tố. Khi hết các ước `d <= sqrt(n)` của số còn lại, số còn lại lớn hơn 1 phải là số nguyên tố. Như vậy `count` bằng tổng số thừa số nguyên tố kể cả lặp (tính duy nhất của phân tích thừa số nguyên tố), chính là điều kiện đề bài.

**Độ phức tạp.** `O(sqrt(n))` phép thử chia trong trường hợp xấu nhất, `O(1)` bộ nhớ; `n <= 10^14` trong phân bố test của đề, thử chia là khả thi bằng C++17. Dùng `d <= n/d` để tránh tràn số khi kiểm tra căn bậc hai.

**Bẫy.** `n=1 -> NO`, `n=8 -> YES`, `n=12 -> YES`, `n=30 -> YES`, `n=16 -> NO`.

## Bài 2. PROTEIN — Tổng hợp amino acid (5 điểm)

**Bài toán.** Chuyển dãy DNA mẫu sang mRNA bằng cặp bổ sung `A→U`, `T→A`, `C→G`, `G→C`. Cứ 3 nucleotide của mRNA tạo một bộ ba, tra bảng để sinh tên amino acid hoặc `Unk`, nối bằng `-`.

**Ý tưởng.** Duyệt từng nhóm 3 ký tự **đầy đủ** của DNA, chuyển mỗi ký tự tương ứng sang mRNA, tra `unordered_map` gồm 24 bộ ba quy định trong bảng; mọi bộ ba còn lại là `Unk`.

**Chứng minh.** Quy tắc bổ sung ánh xạ từng ký tự DNA sang đúng nucleotide mRNA. Các nhóm 3 liên tiếp không chồng lấn khớp thứ tự dịch mã. Bảng tra chính xác theo bộ ba mRNA, nên kết quả từng nhóm và thứ tự toàn chuỗi đều đúng.

**Độ phức tạp.** `O(L)` thời gian, `O(1)` bộ nhớ bổ sung trừ chuỗi đầu vào `O(L)`, với `L<=10^5`.

**Bẫy.** Bộ ba ngoài bảng (`Unk`), phân biệt DNA với mRNA (không tra trực tiếp trên DNA), codon ở cuối có 1–2 ký tự. **Giả định hợp lý:** chỉ codon hoàn chỉnh được đọc; 1–2 nucleotide còn dư không tạo amino acid. Tuy nhiên đề chưa quy định rõ đối với độ dài không chia hết cho 3; đề chính thức cần nêu quy tắc chính xác nếu chấm các test như vậy.

## Bài 3. BILLARD — Bàn bi-a (4 điểm)

**Bài toán.** Viên bi xuất phát ở `(x,y)` trong hình chữ nhật `[0,m]×[0,n]`, di chuyển với vận tốc `(v1,v2)`, phản xạ đàn hồi lý tưởng ở thành; tính tọa độ sau `t` giây.

**Trải gương.** Thay vì phản xạ vận tốc ở tường, tưởng tượng phản chiếu các bản sao hình chữ nhật. Trong mặt phẳng trải, viên bi đi thẳng tới `(x+v1*t, y+v2*t)`. Mỗi trục độc lập có chu kỳ `2*length`:

```
r = ((start + velocity*t) % (2*length) + 2*length) % (2*length)
answer = min(r, 2*length - r)
```

Trong code lấy modulo `velocity` và `t` **trước khi nhân** để giảm rủi ro tràn. Công thức hoạt động với vận tốc âm, vận tốc bằng 0 và cả va chạm đúng ở góc.

**Chứng minh.** Mỗi lần qua một đường biên trong mặt phẳng trải tương ứng với phản xạ của vận tốc thành phần vuông góc đường biên trong bàn thật. Gấp lại hai hình chữ nhật liên tiếp cho ánh xạ tam giác trong chu kỳ `2*length`. Hai tọa độ độc lập, nên áp dụng công thức cho x và y cho đúng vị trí cuối cùng.

**Độ phức tạp.** `O(1)` thời gian, `O(1)` bộ nhớ; `long long` dùng cho các đại lượng nguyên.

## Bài 4. DIVIDE — Chia hết cho 11 (3 điểm)

**Bài toán.** Cho dãy `a[1..n]`, chọn một tập con **không rỗng** các vị trí (không đổi thứ tự), ghép biểu diễn thập phân của các số được chọn; đếm số cách cho số mới chia hết cho 11 modulo `10^9+7`.

**Nhận xét.** Nếu đang có giá trị `z`, nối `a` có `d` chữ số tạo `z' = z*10^d + a`, do đó

```
z' mod 11 = ((z mod 11) * (10^d mod 11) + a mod 11) mod 11.
```

Vì `10 ≡ -1 (mod 11)`, thừa số `10^d mod 11` chỉ là `10` khi `d` lẻ, hoặc `1` khi `d` chẵn.

**DP.** `dp[r]` = số cách chọn từ các phần tử đã xét cho chuỗi ghép có số dư `r`, **bao gồm dãy rỗng** (`dp[0]=1` ban đầu). Với mỗi `a`:

- Không chọn `a`: giữ nguyên `dp[r]`.
- Chọn `a`: cộng `dp[r]` vào `next[(r*(10^d mod 11)+a%11)%11]`.

Mỗi bước dùng `next` riêng, tránh dùng lại một thẻ nhiều lần. Cuối cùng in `(dp[0]-1+MOD)%MOD` để bỏ dãy rỗng.

**Chứng minh.** Với mỗi dãy con của tiền tố, quyết định duy nhất ở phần tử mới là chọn hoặc không chọn. Hai nhóm rời nhau, bao phủ mọi dãy con; công thức cập nhật số dư theo phép nối thập phân là chính xác. Quy nạp theo số phần tử chứng minh toàn bộ `dp` đúng; bỏ đi dãy rỗng nhận đúng kết quả.

**Độ phức tạp.** `O(11n + 10n)` (đếm chữ số) = `O(n)` thời gian, `O(11)` bộ nhớ; `n<=10^5`, `a[i]<=10^9`.

**Bẫy.** Các thẻ cùng giá trị vẫn khác **vị trí**, có thể chọn một hoặc nhiều thẻ; `11` một mình phải đếm là một cách; tuyệt đối không đếm dãy rỗng.

## Bài 5. ALKANE — Đồng phân mạch carbon (3 điểm)

**Bài toán.** Đếm cây không gắn nhãn (unlabeled free trees) có đúng `n` đỉnh, bậc mỗi đỉnh không vượt quá 4. Hai cây tương đương nếu đẳng cấu. `1<=n<=20`. Không tính đồng phân lập thể.

Phương pháp **Pólya + định lý dissymmetry cho cây** giải thích được vì sao không đếm thừa các nhánh đối xứng.

### 1. Cây planted (cây gốc có một cạnh dành cho cha)

Đặt `A(z) = sum_{s>=1} a[s] z^s`, trong đó `a[s]` đếm cây với `s` đỉnh, gốc dành sẵn 1 cạnh nối lên cha và vì thế gốc có **tối đa 3 nhánh con**. Mỗi nhánh con lại là một cây planted. Các nhánh con không có thứ tự; mọi phép hoán đổi nhánh giống nhau không làm thành một cấu trúc mới.

Gọi `H_k(z)` là hàm sinh của **đa tập gồm đúng k** cây planted. `H_0(z)=1`. Nhận dạng đa tập theo chu trình cho công thức:

```
k * H_k(z) = sum_{j=1..k} A(z^j) * H_{k-j}(z).
A(z) = z * (H_0(z) + H_1(z) + H_2(z) + H_3(z)).
```

Công thức thứ hai: chọn một đỉnh gốc (nhân `z`), rồi chọn 0..3 nhánh không thứ tự. Khi tính hệ số `a[s]`, chỉ cần các hệ số `a[1..s-1]`; do đó tính lần lượt `s = 1..20` được, không có vòng lặp phụ thuộc tương lai.

Dùng công thức hệ số của `H_k`:

```
H[k][d] = (1/k) * sum_{j=1..k} sum_{s>=1, j*s<=d}
                                  a[s] * H[k-j][d-j*s].
```

Tất cả phép chia `k` đều là chia hết trên số nguyên do đây là hệ số đếm đa tập.

### 2. Đếm cây không gốc bằng dissymmetry

- `V(z) = z * sum_{k=0..4} H_k(z)` đếm cây **đánh dấu một đỉnh** (đỉnh gốc có tối đa 4 nhánh).
- `E(z) = H_2(z)` đếm cây **đánh dấu một cạnh không hướng** (ghép hai cây planted, không phân biệt hai đầu).
- `D(z) = A(z)^2` đếm cây **đánh dấu một cạnh có hướng** (ghép hai cây planted có phân biệt đầu thứ nhất và thứ hai).

Định lý dissymmetry cho cây:

```
T(z) = V(z) + E(z) - D(z).
answer[n] = [z^n] T(z).
```

**Vì sao đúng?** Mỗi cây có một tâm tự nhiên là đỉnh hoặc cạnh, bất biến dưới tự đẳng cấu. Các loại dấu đỉnh/cạnh/cạnh hướng tạo thành một phép ghép-hủy bỏ có dấu: các cách đánh dấu lệch tâm được bắt cặp (đỉnh và cạnh kề trên đường đến tâm, tương ứng với hướng trên cạnh), chỉ còn một đại diện tại tâm. Công thức vì vậy đếm mỗi lớp đẳng cấu đúng một lần.

**Độ phức tạp.** Với bậc tối đa 4 là hằng số, cài đặt đơn giản tái tính `H` khi mở rộng mỗi `a[s]`: `O(N^3)` thời gian, `O(N)` bộ nhớ, `N=20`; rất nhỏ.

**Đối chứng độc lập.** `n=5 -> 3`, `n=10 -> 75`, `n=20 -> 366319`, khớp [OEIS A000602](https://oeis.org/A000602) và [bảng Bayreuth](https://www.mathe2.uni-bayreuth.de/sascha/oeis/alkane.html).

### Bảng kết quả n = 1..20

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Đáp án | 1 | 1 | 1 | 2 | 3 | 5 | 9 | 18 | 35 | 75 |

| n | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Đáp án | 159 | 355 | 802 | 1858 | 4347 | 10359 | 24894 | 60523 | 148284 | 366319 |

## Tổng kết

| Bài | Thuật toán | Thời gian | Bộ nhớ |
| --- | --- | --- | --- |
| PRIME | Phân tích thừa số | `O(√n)` | `O(1)` |
| PROTEIN | Duyệt nhóm 3 + bảng tra | `O(L)` | `O(L)` kể cả input |
| BILLARD | Gấp tọa độ | `O(1)` | `O(1)` |
| DIVIDE | DP 11 phần dư | `O(n)` | `O(1)` |
| ALKANE | Pólya/dissymmetry | `O(N³)`, `N=20` | `O(N)` |
