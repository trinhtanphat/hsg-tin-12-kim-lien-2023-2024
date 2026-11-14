# Kiểm toán độc lập bổ sung — 13/11/2026

## Phạm vi nghiệm thu
Đối chiếu cả 5 đề bài trong 3 ảnh được cung cấp, mã C++17, mô tả thuật toán, các tệp `.INP/.OUT`, kiểm thử ngẫu nhiên và tập kiểm thử brute-force. Không sử dụng GitHub Actions; không thao tác Session 2 hay production.

## Kết quả đã chạy thực tế
| Hạng mục | Phương pháp | Kết quả |
|---|---|---|
| 5 ví dụ trong đề | Chạy trực tiếp cả 5 binary | PASS |
| Bộ test tổng hợp GNU GCC 14.2.0 | `python tests/run_tests.py` | 1194/1194 PASS |
| Bộ test tổng hợp Clang 17.0.0 | `CXX=clang++ python tests/run_tests.py` | 1194/1194 PASS |
| Biên dịch với bộ phát hiện lỗi | `clang++ -std=c++17 -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer` | Biên dịch thành công 5/5 |
| Chạy binary có sanitizer | PRIME hai trường hợp lớn; PROTEIN 100001 ký tự input; BILLARD thời gian 10^9; DIVIDE n=10^5 và số 10^9; ALKANE n=20 | 6/6 kết thúc mã 0, không có thông báo lỗi sanitizer |
| Bài 5 ALKANE | Đối chiếu dãy n=1..20 và vét cạn cây không nhãn n=1..8 | PASS, n=20 được 366319 |
| Hai gói ZIP bàn giao | Kiểm tra CRC và so nội dung của 25 tệp mã nguồn/tài liệu | PASS |
| Ba ảnh đề trong bản ZIP đầy đủ | So sánh byte-by-byte với 3 ảnh đính kèm ban đầu | 3/3 trùng |

Cảnh báo: chạy không phát sinh sanitizer report **không** phải chứng minh tuyệt đối rằng mọi đầu vào đều không có lỗi. Cũng chưa có quyền truy cập hệ thống chấm bí mật của trường.

## Kết luận theo từng bài
- **PRIME:** đếm đúng số thừa số nguyên tố có lặp; chia thử tới sqrt(n), không cần ba số khác nhau.
- **PROTEIN:** đúng phép bổ sung DNA→mRNA và 24 codon được bảng cung cấp; 40 codon còn lại trả `Unk`. Đề đã yêu cầu chiều dài DNA chia hết cho 3.
- **BILLARD:** phép phản xạ qua modulo theo từng trục đúng cho v âm/0 và t lớn. Trang 2 có lỗi đánh máy tọa độ đỉnh cuối của hình chữ nhật.
- **DIVIDE:** quy hoạch động 11 số dư tính các tập vị trí khác nhau; loại bỏ dãy rỗng, lấy modulo 10^9+7.
- **ALKANE:** đếm cây không nhãn bậc ≤4, không đếm đồng phân lập thể; dãy kết quả trùng đối chứng.

## Cách tái hiện
```bash
python tests/run_tests.py
CXX=clang++ python tests/run_tests.py
```

Trên Windows không có compiler hệ thống, xem `docs/QA_EVIDENCE.md` để chạy qua công cụ Zig và Python portable trên WIN11-181.

## Phạm vi hoàn tất
Hoàn tất giải thuật, mã nguồn, kiểm thử tự động, đối chứng độc lập, tài liệu đánh giá và gói tải về. Điểm AC chính thức **chưa xác minh** vì không có bộ test/hệ thống chấm chính thức.


## Lưu ý bổ sung về miền dữ liệu PROTEIN (14/11/2026)

Thử `100001` ký tự được nêu trong bảng sanitizer phía trên là thử **ngoài miền đề chính thức**, không được dùng để chứng minh độ đúng trên miền dữ liệu hợp lệ. Với ràng buộc dài không quá `100000` và chia hết cho `3`, đầu vào hợp lệ lớn nhất có `99999` ký tự. Kiểm thử chính thức phải dùng chuỗi có độ dài chia hết cho 3. Xem [kiểm toán PROTEIN](PROTEIN_AUDIT.md).


## Kiểm thử cập nhật thực chạy ngày 14/11/2026

Sau khi merge [PR #1](https://github.com/trinhtanphat/hsg-tin-12-kim-lien-2023-2024/pull/1), commit `15c36be6` đã được chạy lại trên **WIN11-181** bằng Python portable 3.13.9 và Zig C++17 0.13.0: **1.207/1.207 khẳng định PASS**, **5/5 chương trình biên dịch**, kiểm toán độ bao phủ PASS, và **420/420 cặp test công khai PASS** kèm kiểm tra SHA-256 và CRC ZIP. Đây là lần chạy mới, tách biệt với kiểm toán 1.194 khẳng định ngày 13/11. Chi tiết tại [QA_EVIDENCE.md](QA_EVIDENCE.md).


## Bổ sung QA bản sửa I/O PROTEIN (14/11/2026)

Commit `89f8d568` kiểm tra trên WIN11-181: **1.209/1.209 PASS**, **5/5 chương trình C++17 biên dịch thành công**; 420/420 bộ test công khai PASS, SHA-256/ZIP CRC PASS; tiến trình kết thúc mã 0. Hai ca mới bắt lỗi ưu tiên nguồn I/O trong `PROTEIN.cpp`. Đây là kiểm thử hồi quy nội bộ; chưa có AC từ máy chấm ngoài. Xem [QA_EVIDENCE.md](QA_EVIDENCE.md).
