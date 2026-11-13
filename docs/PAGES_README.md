# GitHub Pages
- **Nguồn xuất bản:** nhánh `main`, thư mục `/docs` (site tĩnh, không cần bước build).
- **Trang chính:** [Website minh họa và mô phỏng 5 bài](https://trinhtanphat.github.io/hsg-tin-12-kim-lien-2023-2024/).
- **Tài nguyên:** `docs/styles.css`, `docs/site.js`, `docs/assets/exam/page-[1..3].png`.
- **Test tải về:** `docs/downloads/*_tests.zip` với SHA trong `docs/assets/test-manifest.json`.
- **Tài liệu:** `docs/downloads/*.pdf`, `docs/downloads/*.docx`.
- **Triển khai:** cấu hình Pages nhánh `main /docs`. Không tạo workflow GitHub Actions tùy chỉnh.
- **Bảo mật:** toàn bộ JavaScript chạy trong trình duyệt, không gửi dữ liệu đầu vào người dùng đến máy chủ; không có cơ sở dữ liệu hay API nội bộ.
- **Đối chiếu:** test tương tác chỉ mang tính minh họa; dùng C++17 + kho test để chấm đầu ra.
