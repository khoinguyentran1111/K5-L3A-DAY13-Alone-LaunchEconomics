# Phiếu chấm hội đồng Gate 2a

Nhóm số n chấm nhóm số n + 1; nhóm cuối chấm nhóm 1. Chấm theo bằng chứng trong hồ sơ, không theo cách trình bày: một đề xuất No-go có lý do bằng số được điểm cao hơn một đề xuất Go bỏ qua con số bất lợi.

> **Trạng thái: Nguyễn Trần Anh Khôi đã xác nhận.** Điểm do Claude Code đề xuất từ hồ sơ HC2 tại commit `82b663c`. Chưa có buổi trình bày trực tiếp nên chưa có câu trả lời của HC2.

- Nhóm chấm (hội đồng): Alone
- Nhóm được chấm: HC2

| Tiêu chí | 0 điểm | 5 điểm | 10 điểm | Điểm | Lý do (có số) |
| --- | --- | --- | --- | ---: | --- |
| Đề xuất khớp bằng chứng | Mâu thuẫn với số của chính nhóm | Khớp nhưng bỏ qua một con số bất lợi | Khớp, nêu cả con số bất lợi và cách xử lý | 10 | Go có điều kiện khớp 0,38× [simulated]; nêu power 0,64 và xem lại 100% tốn 11.743 đ [simulated], mỗi điểm có người xử lý. Lưu ý: mọi điều kiện cùng hạn 2027-01-05, trùng ngày quyết định |
| Số giả lập và phạm vi | Không nhãn; phạm vi "mọi yêu cầu" | Có nhãn hoặc có thu hẹp phạm vi | Nhãn ở mọi số giả lập; phạm vi thu hẹp có lý do bằng số | 10 | Hồ sơ gắn nhãn ở các mục 1, 2, 3, 7; phạm vi loại quoc_te (1,88×) và doi_tac (0,85×) [simulated]. Nên thêm nhãn riêng cho 92,5% và mức hoà vốn 5,1 phút trong `bang_chi_phi.md` |
| Pilot ra được quyết định | Không đối chứng hoặc thiếu cỡ mẫu | Đủ cỡ mẫu, luật dừng chung chung | Tách được tác động, đủ mẫu, luật dừng có ngưỡng, thời hạn, người có quyền dừng | 5 | Có đối chứng, 20 cụm mỗi nhóm, luật có ngưỡng. Nhưng bước 50% chạy 7 ngày chỉ được m ≈ 215 < 299, n hiệu dụng 814 < 859 (power 0,78). Luật mở lại 7 ngày không đo được trong 3 ngày; xem lại 100% (11.743 đ [simulated]) tự vượt ngưỡng chi phí 8.000 đ |
| **Tổng** | | | | **25 / 30** | |

**Quyết định của hội đồng:** Go có điều kiện

**Lý do:** Số liệu và phạm vi của HC2 vững, đề xuất nêu đúng các con số bất lợi. Trước khi bắt đầu cần kéo bước 50% lên ít nhất 10 ngày (m ≈ 307, n hiệu dụng 862), viết lại luật mở lại theo cohort đủ 7 ngày, và nêu rõ luật chi phí áp dụng từ tuần nào.

**Một câu hỏi cho đội trình:** Bước 50% chạy 1 tuần chỉ được khoảng 215 yêu cầu mỗi nhân viên, vậy nhóm kéo dài bao lâu để đạt 299, và ngày quyết định 2027-01-05 có còn đủ 7 ngày theo dõi mở lại không?

**Câu trả lời của đội trình (ghi lại tại buổi):** Chưa có, ghi khi HC2 trả lời.
