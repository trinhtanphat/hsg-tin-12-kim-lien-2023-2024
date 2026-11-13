# Lời giải trọn bộ đề chọn đội tuyển HSG Tin học 12 Hà Nội — 2023–2024

Đề chính thức của **Trường THPT Kim Liên**, kỳ thi chọn đội tuyển thi học sinh giỏi thành phố Hà Nội lớp 12, năm học 2023–2024; ngày 30/08/2023; thời gian 180 phút. Đây là dự án lời giải tham khảo độc lập (không phải đáp án chính thức của trường).

## Website GitHub Pages

**[Mở website tương tác và xem đề 3 trang](https://trinhtanphat.github.io/hsg-tin-12-kim-lien-2023-2024/)** — minh họa 5 bài, mô phỏng, 420 test trong 5 gói ZIP, tài liệu Word/PDF và ảnh scan.

## 5 bài, 20 điểm

| Bài | Tên | Điểm | Mã C++17 | Ý tưởng |
| --- | --- | ---: | --- | --- |
| 1 | Tích ba số nguyên tố | 5 | [PRIME.cpp](solutions/PRIME.cpp) | Phân tích thừa số nguyên tố, đếm theo bội số |
| 2 | Tổng hợp amino acid | 5 | [PROTEIN.cpp](solutions/PROTEIN.cpp) | Bổ sung nucleotide rồi dịch từng bộ ba |
| 3 | Bàn bi-a | 4 | [BILLARD.cpp](solutions/BILLARD.cpp) | Trải gương, lấy tọa độ modulo chu kỳ `2m`, `2n` |
| 4 | Chia hết cho 11 | 3 | [DIVIDE.cpp](solutions/DIVIDE.cpp) | DP 11 số dư, chọn/bỏ thẻ, đếm modulo `1e9+7` |
| 5 | Alkane | 3 | [ALKANE.cpp](solutions/ALKANE.cpp) | Hàm sinh đa tập cây không nhãn + định lý dissymmetry |

**Mỗi file có `main()` độc lập; không có phụ thuộc bên ngoài.** Compile và chạy bằng stdin/stdout hoặc đặt `PRIME.INP`, `PROTEIN.INP`, `BILLARD.INP`, `DIVIDE.INP`, `ALKANE.INP` trong thư mục làm việc để chương trình tự ghi đúng tệp `.OUT`. Không kích hoạt GitHub Actions; toàn bộ QA chạy ở máy local.

## Chạy nhanh

```bash
g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic solutions/PRIME.cpp -o prime
printf '12\n' | ./prime   # YES

g++ -std=c++17 -O2 solutions/ALKANE.cpp -o alkane
printf '20\n' | ./alkane  # 366319

python tests/run_tests.py  # QA trên cả 5 bài, random + brute-force
```

Trên Windows (PowerShell), biên dịch với `g++ ... -o PRIME.exe`, sau đó dùng file `PRIME.INP` và chạy `./PRIME.exe`; kết quả ở `PRIME.OUT`. Bộ test cũng hỗ trợ `clang++` hoặc Zig `zig c++` thông qua biến `ZIG_EXE` (lệnh chạy được xác thực trên WIN11-181). Bạn cũng có thể dùng [scripts/local_qa.ps1](scripts/local_qa.ps1).

## Tài liệu

- [Tóm tắt đầy đủ đầu vào/đầu ra/ràng buộc từ ba trang đề](docs/DE_BAI_TOM_TAT.md)
- [Editorial: phân tích thuật toán + chứng minh + độ phức tạp cả 5 bài](docs/EDITORIAL.md)
- [Đánh giá đề và những điểm chưa chặt chẽ](docs/DANH_GIA_DE.md)
- [Bộ kiểm thử tự động](tests/run_tests.py)
- [Ngân hàng 420 test, bộ sinh và SHA-256](tests/TEST_BANK_README.md)
- [GitHub Pages và nguồn website](docs/PAGES_README.md)
- [Bằng chứng QA 1.194/1.194 PASS trên WIN11-181 + G++ + Clang++](docs/QA_EVIDENCE.md)
- [Kiểm toán cuối: sanitizer, benchmark, ZIP và phạm vi nghiệm thu](docs/AUDIT_FINAL.md)
- [Test mẫu](samples/)

### Lưu ý về cách hiểu đề

- **PRIME:** `8 = 2 × 2 × 2` phải cho `YES`; số nguyên tố được phép trùng.
- **PROTEIN:** đề **đã yêu cầu độ dài DNA chia hết cho 3** (trang 2), nên tất cả ký tự hợp lệ đều thuộc một bộ ba hoàn chỉnh. Chương trình cũng bỏ qua nhóm cuối thiếu 1–2 ký tự nếu thử dữ liệu ngoài phạm vi đề.
- **BILLARD:** `v1`, `v2` có thể âm hoặc bằng 0; phản xạ đúng ngay cả khi chạm góc.
- **DIVIDE:** đếm **các tập vị trí được chọn**, không gộp các thẻ trùng giá trị; không chọn thẻ nào không được tính.
- **ALKANE:** đếm **đồng phân cấu tạo mạch carbon** (cây không gắn nhãn bậc ≤4), **không** đếm đồng phân lập thể.

### Điểm cần đối chiếu với đề gốc

Trong bảng tổng quan ở trang 1, hàng Bài 5 ghi tên tệp kết quả là `ALKANE.INP`. Đây nhiều khả năng là lỗi đánh máy: phần mô tả chi tiết của Bài 5 nêu rõ `ALKANE.OUT`. Repository thống nhất dùng `ALKANE.OUT`.

## Nguồn kiểm chứng Bài 5

- OEIS [A000602](https://oeis.org/A000602): số cây không gắn nhãn, tối đa 4 cạnh kề ở mỗi đỉnh; chính là số đồng phân alkane bỏ qua đồng phân lập thể.
- Đại học Bayreuth, [Isomers of Alkanes](https://www.mathe2.uni-bayreuth.de/sascha/oeis/alkane.html), bảng n = 1..50.

## Phạm vi QA

Các bài được kiểm thử bằng mẫu đề, trường hợp biên, kiểm thử ngẫu nhiên với đối chứng brute force / mô phỏng và kiểm tra toàn bộ dãy alkane n=1..20. Dùng `python tests/run_tests.py` để tái chạy và xem số kiểm thử cụ thể. Trạng thái QA tại thời điểm publish phải căn cứ vào log chạy thực tế, không coi việc có test file là đã chạy PASS.

## License

Mã và tài liệu lời giải tham khảo: MIT ([LICENSE](LICENSE)). Đề gốc thuộc về đơn vị ra đề; repository không tái bản nguyên văn đề hoặc hình ảnh đề.
