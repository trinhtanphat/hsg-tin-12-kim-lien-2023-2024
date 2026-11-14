# Đối chứng độc lập cho DIVIDE — 15/11/2026

## Tại sao bổ sung?

Các trường hợp ngẫu nhiên ngắn được đối chiếu bằng vét cạn, nhưng phép đối chứng cho dữ liệu dài trước đó phần lớn sử dụng lại quy hoạch động 11 số dư. Hai chương trình có thể cùng mắc một lỗi khái niệm. Bộ hồi quy đã thêm **hai phép đối chứng đóng** ở giới hạn `n = 100000`, không tái sử dụng công thức DP.

Với các thẻ có giá trị giống nhau, mỗi tập vị trí được chọn là một cách đếm riêng — kể cả khi tạo thành cùng một số.

## Chứng minh và kết quả kỳ vọng

**Các thẻ đều là 11:** mọi dãy con khác rỗng ghép lại vẫn chia hết cho 11. Số đáp án là `(2^n - 1) mod 1_000_000_007`. Ca này đã có từ trước.

**Các thẻ đều là 1:** chọn `k` thẻ tạo số gồm `k` chữ số 1. Theo tiêu chuẩn chia hết cho 11, nó chia hết khi và chỉ khi `k` chẵn. Với `n >= 1`, tổng số cách chọn `k` chẵn, không tính `k = 0`, bằng `2^(n-1) - 1`. Bộ test kiểm chứng với `n = 100000`.

**Các thẻ đều là 10:** chọn `k` thẻ tạo số `10 + 10×100 + ... + 10×100^(k-1)`. Vì `100 ≡ 1 (mod 11)`, giá trị số đó đồng dư `10k (mod 11)`, nên chia hết cho 11 khi `k` là bội dương của 11. Đáp án là tổng `C(n,k)` theo `k = 11,22,... <= n`, tính bằng giai thừa và nghịch đảo modulo (vì `n < 1_000_000_007`). Không có quy hoạch động 11 trạng thái trong oracle này.

Các phép đồng nhất thức được kiểm tra trên **giới hạn số lượng thẻ lớn nhất** với các số thẻ đều hợp lệ (`1`, `10`, `11`).

## Phạm vi và mức độ độc lập

- Các ca `1` và `10` có giá trị kỳ vọng tính bằng công thức tổ hợp, tách khỏi phần triển khai DP trong `solutions/DIVIDE.cpp`.
- Các phép đếm vẫn dựa trên **cách hiểu cùng đặc tả** là chọn tập vị trí, giữ nguyên thứ tự. Nếu cách hiểu đề sai thì tất cả đối chứng cũng có thể sai; cần kiểm tra lại đề gốc.
- Đây là cải thiện độ đa dạng của oracle, **không chứng minh đúng 100% trên mọi đầu vào**.
- Có thể kiểm thử tiếp với đối chứng meet-in-the-middle cho `n` trung bình; cần thêm dữ liệu thực nghiệm từ học sinh để đo độ phân hóa của đề.

## Chạy lại

```powershell
# Trên máy có Python 3 và compiler C++17:
python tests/run_tests.py
```

Không sử dụng GitHub Actions; QA được chạy trên máy riêng. Khi báo cáo PASS, cần ghi mã commit, môi trường, lệnh và mã thoát thực tế.
