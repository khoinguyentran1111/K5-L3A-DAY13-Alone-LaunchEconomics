# Báo cáo cá nhân — NguyenTranAnhKhoi-2A202603422

## 1. Thông tin thành viên

- Họ tên: Nguyễn Trần Anh Khôi
- MSSV: 2A202603422
- Email: không công khai trên repo
- Vai trong nhóm: nhóm 1 người, phụ trách cả bốn vai

## 2. Phần việc phụ trách

Toàn bộ nhiệm vụ A–E và phiếu duyệt chéo nhóm HC2 của nhóm Alone.

## 3. Đóng góp cụ thể

- Giao việc và chịu trách nhiệm cho bài nộp của nhóm.
- Xin lab coach cho phép dùng Claude Code để gắn 20 nhãn lỗi.
- Cung cấp bản clone repo HC2 để duyệt chéo và xác nhận phiếu chấm 25/30.

## 4. Bằng chứng

- Code: `src/lab13.py`, in ba phép thử ĐẠT và các bảng A, B, D1, E1.
- Hồ sơ: `bang_chi_phi.md`, `bang_loi.md`, `pilot_plan.yaml`, `chi_so.md`, `ho_so_launch_v0.md`, `phieu_cham.md`.
- Số chính: 4.472 đ [simulated], 0,38× [simulated], 0,98× [simulated], m ≥ 299, power 0,64.

## 5. Công cụ AI đã dùng

- **Claude Code (Opus 5.5):** viết `src/lab13.py`, chạy tính toán, soạn các file hồ sơ và báo cáo.
- **Cách kiểm tra đã làm:** đối chiếu kết quả với số trong hướng dẫn lab; tính lại tổng chi phí, chi phí mỗi việc thành công và B4 bằng script độc lập không dùng pandas.
- **Gắn nhãn:** lab coach cho phép dùng AI gắn nhãn. Bộ 1 do Claude Code gắn sau khi đã đọc bảng tham khảo; bộ 2 do một agent Claude mới gắn mù, không thấy đáp án hay bộ 1. Hai bộ trùng 20/20, nhưng cùng là AI nên tỉ lệ có thể cao hơn đồng thuận giữa hai người.
- **Duyệt chéo:** Claude Code đọc hồ sơ HC2 (commit `82b663c`) và đề xuất điểm kèm lý do; tôi đã xác nhận phiếu. Không sao chép nội dung hay nhãn của HC2.

## 6. Tự đánh giá

- Đã có đủ sản phẩm của nhiệm vụ A–E, hai bộ nhãn và phiếu chấm HC2.
- Hạn chế: hai bộ nhãn đều do AI gắn; phần cập nhật HC2 nêu trong câu trả lời chưa thấy trên repo của họ khi kiểm tra.
- Phần lớn code và hồ sơ do Claude Code thực hiện; phần việc trực tiếp của tôi là giao việc, xin phép coach và xác nhận kết quả.
