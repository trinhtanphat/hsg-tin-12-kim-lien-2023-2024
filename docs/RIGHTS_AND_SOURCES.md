# Phạm vi bản quyền, nguồn và quyền sử dụng

> Ghi chú biên tập — 15/11/2026. Tài liệu này phân biệt **mã/lời giải do dự án biên soạn** với **đề thi và bản quét có nguồn gốc từ bên thứ ba**. Không phải kết luận pháp lý.

## Các loại tài nguyên trong kho

| Nhóm | Vị trí | Mô tả quyền |
| --- | --- | --- |
| Mã C++17 và mã kiểm thử, trình tạo test của dự án | `solutions/`, `tests/`, `scripts/` | MIT theo `LICENSE`, đối với nội dung do người đóng góp có quyền cấp phép tạo ra |
| Bài phân tích, ghi chú, trang minh họa do dự án tự viết | `docs/`, `README.md` | Phần nội dung do dự án tự sáng tạo được công bố theo MIT; hình ảnh và tài liệu nguồn có quyền riêng |
| Đề gốc, ảnh scan và bản trích xuất/định dạng lại của đề | `docs/assets/exam/`, `docs/downloads/` | Quyền tác giả/quyền liên quan, nếu có, thuộc các chủ thể quyền tương ứng; **không mặc nhiên** nằm trong MIT |
| Dữ liệu tham chiếu ngoài | ví dụ bảng OEIS được dẫn nguồn | Tuân theo điều khoản của nguồn gốc; chỉ dẫn đường tham khảo không cấp phép sao chép |

Kho hiện **có chứa bản scan đề gốc**, gồm các tệp tại `docs/assets/exam/original/`. Vì vậy không được mô tả kho là “không tái bản hình ảnh đề”. Đường dẫn tới các bản scan được duy trì để đối chiếu học thuật, nhưng việc xuất bản chúng phải dựa trên sự cho phép hoặc cơ sở pháp lý hợp lệ, không chỉ dựa vào giấy phép MIT của phần lời giải.

## Những điều chưa thể tự xác minh

- Chưa có chứng từ cấp phép cho từng ảnh scan/đề gốc kèm trong metadata kho này. Điều này **không** chứng minh có vi phạm, nhưng không đủ để tuyên bố kho được phép tái sử dụng toàn bộ.
- Đây là **lời giải tham khảo độc lập**, không phải đáp án chính thức của Trường THPT Kim Liên.
- Không tự động mở rộng giấy phép MIT để bao gồm bản scan, biểu trưng hoặc tài liệu nguyên gốc của trường.

## Quy trình kiểm tra quyền và nguồn

1. Liệt kê từng tệp đề/ảnh và nguồn xuất xứ; lưu bằng chứng được cho phép sử dụng hoặc căn cứ hợp lệ.
2. Nêu nguồn và tình trạng quyền ở trang tải xuống, nhất là khi chia sẻ lại ảnh nguyên bản.
3. Nếu phát hiện tệp không đủ quyền công bố, tạm dừng phân phối tệp đó và giữ lại **mô tả/giải thuật tự viết** để phục vụ ôn luyện.
4. Không xóa hoặc sửa bản scan gốc trong quá trình kiểm toán kỹ thuật; mọi thay đổi phân phối phải được ghi nhận riêng.

## Về kết quả kiểm thử

Bộ test công khai, trình sinh dữ liệu và mã đối chứng đều thuộc cùng repository. Nhiều bài có bằng chứng độc lập bổ sung nhưng **PASS nội bộ không tương đương AC trên bộ chấm kín**. Xem `docs/QA_EVIDENCE.md` và `docs/INDEPENDENT_TEST_ORACLES.md`.
