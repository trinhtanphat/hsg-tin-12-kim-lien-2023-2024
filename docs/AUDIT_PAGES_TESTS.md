# Kiểm toán website, tài liệu và ngân hàng đề (13/11/2026)

## Phạm vi phát hành

- GitHub Pages: `https://trinhtanphat.github.io/hsg-tin-12-kim-lien-2023-2024/`
- Nguồn: `main/docs`, web HTML + CSS + JavaScript, không có backend, không cần GitHub Actions.
- Năm bài C++17 riêng biệt; mô phỏng tương tác độc lập bằng JavaScript; sơ đồ SVG giải thích PRIME, PROTEIN, BILLARD, DIVIDE và ALKANE.
- Bài thi scan nguyên bản: `docs/assets/exam/original/page-1.png` tới `page-3.png`. Ảnh preview tối ưu (nhỏ hơn) ở `docs/assets/exam/page-{1,2,3}.png`.
- Bản PDF 3 trang giữ nguyên hình ảnh; DOCX 3 trang scan giữ bố cục; DOCX biên tập văn bản có thể chỉnh sửa nhưng là **bản tóm tắt**, không phải bản chép nguyên văn.
- Giấy phép MIT chỉ áp dụng cho mã nguồn và tài liệu lời giải độc lập, không tự động cấp phép lại ảnh đề gốc.

## Ngân hàng test phát hành

| Bài | Case | Cặp đầu vào trùng lặp | Phạm vi kiểm tra |
|---|---:|---:|---|
| PRIME | 100 | 0 | n=1, n=10^14, số nguyên tố, lũy thừa, ba thừa số có lặp, YES/NO |
| PROTEIN | 100 | 0 | 64/64 codon mRNA, Ser/Thr/Arg/Gly/Tyr/His/Pro/Unk, chuỗi 99.999 ký tự |
| BILLARD | 100 | 0 | 9/9 cặp vận tốc -1/0/1, phản xạ cạnh/góc, t=1 và t=10^9 |
| DIVIDE | 100 | 0 | n=1 và n=100.000, trùng giá trị, độ dài chữ số khác nhau, đối chứng brute-force |
| ALKANE | 20 | 0 | Toàn bộ miền n=1..20, đối chiếu dãy cây không gắn nhãn bậc ≤4 |
| **Tổng** | **420** | **0** | Tất cả thuộc ràng buộc đề |

**Giới hạn trung thực:** 100 bộ test không thể bao hàm mọi đầu vào cho các bài có miền rất lớn. Bộ test được thiết kế để bao phủ các lớp tương đương, biên, phân nhóm và dữ liệu lớn; không phải bộ chấm bí mật của nhà trường.

## Chạy lại độc lập trên WIN11-181

```powershell
$env:ZIG_EXE = 'C:\Temp\HSG-KimLien-2023-2024\toolchain\zig-x86_64-windows-0.17.1\zig.exe'
$py = 'C:\Temp\HSG-KimLien-2023-2024\toolchain\python\python.exe'
& $py tests/generate_cases.py
& $py tests/coverage_audit.py
& $py tests/check_generated.py
& $py tests/run_tests.py
node tests/site_smoke.cjs
```

- Máy kiểm thử: `WIN11-181`, portable Zig C++17 + Python 3.13, không đụng Session 2 hoặc production.
- Bộ 420 cặp `.INP/.OUT`: **420/420 PASS**, xác minh SHA-256 file, SHA-256 ZIP, CRC và đầu ra từ binary thật.
- Hồi quy 5 bài: **1.194/1.194 PASS**.
- Bộ test xuất bản **420 đầu vào duy nhất** (0 test bị lặp).
- Generator có seed cố định 20261113; các ZIP được tạo với timestamp, thứ tự file và quyền truy cập cố định để build lặp lại ra cùng SHA-256.
- Chrome headless dùng profile riêng: 5 thẻ bài giải + 5 tab mô phỏng, 5/5 ví dụ, nút sáng/tối, ảnh gốc, không có lỗi runtime. Kiểm tra responsive: viewport 1440px/390px; mobile không tràn ngang.
- Xác minh 3 ảnh gốc khớp hash của ảnh do người dùng gửi:
  - trang 1: `c7c03c1992e9b5238c9e12b96ce0015d0273c8c2c5b0016108074c4852194c6c`
  - trang 2: `4b8095f7f1df8f678dd233427b0f7a095741aaaa3d126e5e06bfa993c54df6c7`
  - trang 3: `c43c502d47ec3fd596e8cdafb68de55678f2fe229448e69f38affa46cd3c8467`

## Kiểm tra cấu trúc văn bản

- Word scan gồm 3 ảnh và giữ bố cục A4; PDF scan đúng 3 trang A4.
- DOCX biên tập chứa mô tả chính của 5 bài, bảng phạm vi và phần phụ lục 3 ảnh; có thể sửa phần văn bản.
- README đã sửa lỗi ký tự `\\n` hiển thị trong danh sách liên kết. `\\n` còn xuất hiện hợp lệ trong các lệnh `printf` ở code fence, không phải lỗi hiển thị.

## Kết luận và giới hạn

Đã nghiệm thu GitHub Pages và 5 chương trình qua bộ test công khai cùng kiểm thử nội bộ. **Không công bố đạt AC chính thức 20/20** do không có kết quả từ hệ thống chấm bí mật. Đánh giá độ khó trong website là nhận xét chuyên môn chủ quan.


## Bổ sung kiểm tra hồi quy ngày 14/11/2026

Chỉ số 1.194/1.194 trong biên bản kiểm toán website ngày 13/11 ở trên là kết quả lịch sử. Sau PR #1, WIN11-181 đã tái chạy trên commit `15c36be6`: **1.207/1.207 PASS** (5/5 C++17) và **420/420 test công khai PASS**, kiểm tra SHA-256 và ZIP CRC. Xem [QA_EVIDENCE.md](QA_EVIDENCE.md) để không nhầm số liệu QA của hai phiên bản.
