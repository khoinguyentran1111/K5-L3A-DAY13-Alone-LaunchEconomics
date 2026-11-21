"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm Alone (file nộp).
Chạy trong thư mục src/: python lab13.py   (cần pandas, scipy, statsmodels)
Không cần khoá API. Dữ liệu trong hai file CSV là giả lập.
Mọi số tính từ cột *_simulated được in kèm nhãn simulated.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import sys
from statistics import NormalDist

import pandas as pd
from scipy.stats import binom
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)
CO_DINH_THANG = 40_000_000   # chi phí cố định của trợ lý mỗi tháng
YC_THANG = 45_000            # số yêu cầu hoàn phí mỗi tháng
YC_NGAY = 1_500              # số yêu cầu hoàn phí mỗi ngày
SO_NHAN_VIEN = 40
PHAM_VI = ['noi_dia', 'hang_nang']   # phạm vi pilot, chọn từ kết quả A3


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, chay_lai, xem_lai, lam_lai, tong, thanh_cong, cps, hoa_don_moi_yc.
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × lương phút. Đây là số GIẢ LẬP (simulated).
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B; giữ mặc định ở A2.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    return dict(token=tien_token.sum(), tool=tien_tool.sum(),
                chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
                xem_lai=xem_lai, lam_lai=lam_lai, tong=tong, thanh_cong=thanh_cong,
                cps=tong / thanh_cong,
                hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs))


# ---------- Nhiệm vụ D1 · Cỡ mẫu ----------
def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Cỡ mẫu mỗi nhóm khi so hai tỉ lệ."""
    za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)


def he_so_thiet_ke(m, icc=0.02):
    return 1 + (m - 1) * icc


def n_hieu_dung(c, m, icc=0.02):
    return c * m / he_so_thiet_ke(m, icc)


def m_toi_thieu(n, c, icc=0.02):
    """m nhỏ nhất để c cụm đạt cỡ mẫu hiệu dụng n; None nếu không thể đạt."""
    mau = c - n * icc
    return None if mau <= 0 else math.ceil(n * (1 - icc) / mau)


# ---------- In kết quả từng nhiệm vụ ----------
def in_muc(ten):
    print(f'\n=== {ten} ===')


def nv_a(runs, reqs):
    in_muc('A2 · Mô hình chi phí (xem lại, làm lại, tổng, cps là simulated)')
    g = mo_hinh(runs, reqs)
    for ten, gia_tri in g.items():
        print(f'{ten:16s} {gia_tri:>14,.1f}')
    print(f'cps / hoá đơn mỗi yêu cầu = {g["cps"] / g["hoa_don_moi_yc"]:.2f} lần [simulated]')
    for khoan in ['token', 'tool', 'xem_lai', 'lam_lai']:
        print(f'tỉ trọng {khoan:8s} {g[khoan] / g["tong"]:6.1%}')
    print(f'giờ nhân viên chiếm {(g["xem_lai"] + g["lam_lai"]) / g["tong"]:.1%} [simulated]')
    khong_tc = len(reqs) - g['thanh_cong']
    he_thong = (g['tong'] + khong_tc * BASELINE) / len(reqs)
    print(f'cả hệ thống / yêu cầu = {he_thong:,.0f} đ = {he_thong / BASELINE:.2f}× [simulated]')

    in_muc('A3 · Theo loại yêu cầu (cps là simulated)')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        con = reqs[reqs['loai'] == loai]
        kq = mo_hinh(runs, con)
        so_run = runs['request_id'].isin(con['request_id']).sum()
        print(f'{loai:10s} n={len(con):4d} tc={kq["thanh_cong"] / len(con):6.1%} '
              f'run/yc={so_run / len(con):.2f} cps={kq["cps"]:>8,.0f} = {kq["cps"] / BASELINE:.2f}×')
    gop = runs.merge(reqs[['request_id', 'loai']], on='request_id')
    gop['ok'] = (gop['status'] == 'ok').astype(int)
    print('Tỉ lệ ok theo lần thử:')
    print(gop.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean').round(3))

    in_muc('A4 · Cộng chi phí cố định, phạm vi noi_dia + hang_nang [simulated]')
    pv = reqs[reqs['loai'].isin(PHAM_VI)]
    kq = mo_hinh(runs, pv)
    print(f'phạm vi: {len(pv)} yêu cầu, {kq["thanh_cong"]} thành công, '
          f'tổng {kq["tong"]:,.0f}, cps {kq["cps"]:,.0f}')
    for ten, ti_le in [('100% khối lượng', 1), ('50% khối lượng', .5),
                       ('25% khối lượng', .25), ('10% khối lượng', .1)]:
        viec = YC_THANG * ti_le * kq['thanh_cong'] / len(reqs)
        co_dinh = CO_DINH_THANG / viec
        print(f'{ten:16s} việc/tháng={viec:>8,.0f} cố định/việc={co_dinh:>7,.0f} '
              f'cps+cố định={kq["cps"] + co_dinh:>7,.0f} = {(kq["cps"] + co_dinh) / BASELINE:.2f}×')


def nv_b(runs, reqs):
    in_muc('B1 · Độ nhạy (mọi cps là simulated)')
    goc = mo_hinh(runs, reqs)['cps']
    kich_ban = {
        'Giá token gấp đôi': dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa': dict(gia_vao=13, gia_ra=65),
        'Xem lại gấp đôi': dict(he_so_xem_lai=2),
        'Xem lại giảm một nửa': dict(he_so_xem_lai=0.5),
        'Làm lại gấp đôi': dict(he_so_lam_lai=2),
        'Làm lại giảm một nửa': dict(he_so_lam_lai=0.5),
        'Lương tăng 25%': dict(luong_phut=2500),
        'Tối đa 2 lần chạy': dict(max_lan_chay=2),
        'Chỉ 1 lần chạy': dict(max_lan_chay=1),
    }
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        print(f'{ten:25s} {cps:8,.0f} {(cps / goc - 1) * 100:+6.1f}%')

    in_muc('B2 · Token gấp đôi + xem lại gấp đôi [simulated]')
    cps = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    print(f'{cps:,.0f} đ ({(cps / goc - 1) * 100:+.1f}%)')

    in_muc('B3 · Giới hạn số lần chạy [simulated]')
    for k in [1, 2, 3]:
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - kq['thanh_cong']
        print(f'{k} lần: trợ lý {kq["tong"]:>10,.0f}  không TC {khong_tc:3d}  '
              f'cả hệ thống {kq["tong"] + khong_tc * BASELINE:>10,.0f}  cps {kq["cps"]:,.0f}')

    in_muc('B4 · Xem lại 100%, phạm vi noi_dia + hang_nang [simulated]')
    pv = reqs[reqs['loai'].isin(PHAM_VI)]
    runs_pv = runs[runs['request_id'].isin(pv['request_id'])]
    co_ok = runs_pv.loc[runs_pv['status'] == 'ok', 'request_id'].nunique()
    so_lam_lai = int((pv['ket_qua'] == 'lam_lai').sum())
    tc = int((pv['ket_qua'] == 'thanh_cong').sum())
    may = (runs_pv['tokens_in'] / 1000 * GIA_VAO + runs_pv['tokens_out'] / 1000 * GIA_RA
           + runs_pv['tool_calls'] * GIA_TOOL).sum()
    phut_ll = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated']
    print(f'có ok={co_ok}, lam_lai={so_lam_lai}, thành công={tc}, token+tool={may:,.0f}')
    print(f'phút làm lại / ca toàn mẫu: TB {phut_ll.mean():.2f}, trung vị {phut_ll.median():.1f}')
    for nhan, phut in [('9 phút (đề)', 9), ('15,3 phút (dữ liệu)', 15.3)]:
        tong = may + co_ok * 5 * LUONG_PHUT + so_lam_lai * phut * LUONG_PHUT
        hoa_von = (BASELINE * tc - may - so_lam_lai * phut * LUONG_PHUT) / (co_ok * LUONG_PHUT)
        print(f'{nhan:20s} tổng {tong:>11,.0f}  cps {tong / tc:>7,.0f} = {tong / tc / BASELINE:.2f}×  '
              f'hoà vốn khi xem lại ≤ {hoa_von:.2f} phút')
    print('Lộ trình giảm xem lại (làm lại 9 phút, giữ nguyên số ca):')
    for r in [1, .75, .5, .25]:
        c = (may + r * co_ok * 5 * LUONG_PHUT + so_lam_lai * 9 * LUONG_PHUT) / tc
        print(f'  xem lại {r:4.0%}: cps {c:>7,.0f} = {c / BASELINE:.2f}×')
    xem = pv[pv['duoc_xem_lai'] == 1]
    print(f'đợt chạy thử trong phạm vi: xem lại {len(xem)}/{len(pv)} = {len(xem) / len(pv):.1%}, '
          f'TB {xem["phut_xem_lai_simulated"].mean():.2f} phút/lần, '
          f'sửa+bỏ {xem["quyet_dinh_xem_lai"].isin(["sua", "bo"]).mean():.1%}')


def nv_d(reqs):
    in_muc('D1 · Cỡ mẫu (baseline 0,70; alpha 0,05; power 0,8; ICC 0,02)')
    n5, n6 = co_mau(.70, .75), co_mau(.70, .76)
    de75 = he_so_thiet_ke(75)
    nb = math.ceil(n5 * de75)
    print(f'a) theo yêu cầu: {n5} mỗi nhóm')
    print(f'b) m=75: DE={de75:.2f}, n={nb}, {math.ceil(nb / 75)} người mỗi nhóm, '
          f'tổng {2 * math.ceil(nb / 75)} > {SO_NHAN_VIEN}: không đủ người')
    print(f'c) 20 nhân viên: trần {20 / .02:.0f} < {n5}: không đạt')
    print(f'd) 6 depot: trần {6 / .02:.0f}')
    m = m_toi_thieu(n6, 20)
    print(f'e) 6 điểm cần {n6}/nhóm: m ≥ {m}, DE={he_so_thiet_ke(m):.2f}, '
          f'n hiệu dụng={n_hieu_dung(20, m):.1f}, thô {20 * m:,} yêu cầu/nhóm')
    h = proportion_effectsize(.75, .70)
    print(f'power nếu tác động thật chỉ 5 điểm, n={n6}: '
          f'{NormalIndPower().power(effect_size=h, nobs1=n6, alpha=.05, ratio=1):.3f}')

    in_muc('D3 · Kiểm tra tính khả thi của lịch pilot')
    ti_le_pv = reqs['loai'].isin(PHAM_VI).mean()
    moi_nv = YC_NGAY * ti_le_pv / SO_NHAN_VIEN
    print(f'yêu cầu trong phạm vi/nhân viên/ngày = {moi_nv:.2f}')
    print(f'số ngày ở bước 0.50 để đạt m={m}: {math.ceil(m / moi_nv)} ngày; '
          f'1 tuần chỉ được {moi_nv * 7:.0f}/người; 14 ngày được {moi_nv * 14:.0f}/người')
    mo_lai = reqs.loc[reqs['loai'].isin(PHAM_VI), 'mo_lai_trong_7_ngay'].mean()
    print(f'mở lại 7 ngày: toàn mẫu {reqs["mo_lai_trong_7_ngay"].mean():.2%}, phạm vi {mo_lai:.2%}')
    for nv in [4, 10, 20]:
        n = round(nv * moi_nv * 7)
        nguong = math.ceil(.06 * n)
        print(f'  {nv:2d} nhân viên, cohort 7 ngày n={n}: '
              f'P(vượt trần 6% khi tỉ lệ thật {mo_lai:.2%}) = {binom.sf(nguong, n, mo_lai):.4f}')


def nv_e(reqs):
    in_muc('E1 · Chỉ số trong đợt chạy thử')
    for ten, df in [('toàn mẫu', reqs), ('phạm vi pilot', reqs[reqs['loai'].isin(PHAM_VI)])]:
        chinh = (df['dong_trong_24h'] == 1) & (df['mo_lai_trong_7_ngay'] == 0)
        xem = df[df['duoc_xem_lai'] == 1]
        bo_qua = xem['quyet_dinh_xem_lai'].isin(['sua', 'bo'])
        an_toan = df['mo_lai_trong_7_ngay'] == 1
        print(f'{ten:14s} chính {chinh.sum()}/{len(df)} = {chinh.mean():.2%} · '
              f'bỏ qua {bo_qua.sum()}/{len(xem)} = {bo_qua.mean():.2%} · '
              f'an toàn {an_toan.sum()}/{len(df)} = {an_toan.mean():.2%}')
    ll = reqs[reqs['loai'].isin(PHAM_VI)]['ket_qua'].eq('lam_lai').mean()
    print(f'tỉ lệ làm lại trong phạm vi: {ll:.2%}')
    print(f'depot trong mẫu: {reqs["depot"].nunique()}, nhân viên trong mẫu: {reqs["staff_id"].nunique()}')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')   # để in được tiếng Việt trên Windows
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    nv_a(runs, reqs)
    nv_b(runs, reqs)
    nv_d(reqs)
    nv_e(reqs)
