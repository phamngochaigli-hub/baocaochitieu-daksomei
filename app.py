import streamlit as st
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import datetime

# Indicators data from the updated document
data = {
    'Mã chỉ tiêu': ['KT01', 'KT01a', 'KT01b', 'KT01b1', 'KT01b2', 'KT01c', 'KT02', 'KT03', 'KT04', 'KT05', 'KT06', 'KT07', 'KT08', 'KT09', 'KT09a', 'KT10', 'KT11', 'KT12', 'QP01', 'QP02', 'XD01', 'XD02', 'XD03', 'XD04'],
    'Nhóm': ['I Về kinh tế - xã hội'] * 18 + ['II Về quốc phòng - an ninh'] * 2 + ['III Xây dựng Đảng và hệ thống chính trị'] * 4,
    'Chỉ tiêu chủ yếu': [
        'Tốc độ tăng giá trị sản phẩm', 'Nông, lâm, thủy sản', 'Công nghiệp và xây dựng', 'Công nghiệp', 'Xây dựng', 'Dịch vụ',
        'Tổng thu ngân sách trên địa bàn đến năm 2030', 'Doanh thu bán lẻ hàng hóa và dịch vụ', 'Tỷ lệ dân số tham gia bảo hiểm y tế',
        'Giảm tỷ lệ hộ nghèo đa chiều', 'Bảo hiểm xã hội tự nguyện', 'Đào tạo nghề lao động nông thôn', 'Tỷ lệ che phủ rừng',
        'Tỷ lệ dân cư nông thôn sử dụng nước hợp vệ sinh', 'Trong đó: Tỷ lệ sử dụng nước sạch', 'Tỷ lệ chất thải rắn ở nông thôn được thu gom',
        'Tỷ lệ giải ngân vốn đầu tư công so với kế hoạch HĐND tỉnh giao', 'Tỷ lệ trường đạt chuẩn quốc gia', 'Tỷ lệ giao quân hằng năm',
        'Xếp loại về quốc phòng – an ninh hằng năm', 'Tỷ lệ phát triển đảng viên mới hằng năm (so với đảng viên đầu nhiệm kỳ)',
        'Tỷ lệ đảng viên hoàn thành tốt nhiệm vụ hằng năm', 'Tỷ lệ chi bộ hoàn thành tốt nhiệm vụ hằng năm',
        'Hằng năm Đảng bộ phân đấu xếp loại hoàn thành tốt nhiệm vụ: xây dựng Chính quyền, Mặt trận và các tổ chức chính trị - xã hội xã được xếp loại hoàn thành tốt nhiệm vụ'
    ],
    'ĐƠN VỊ TÍNH': ['%', '%', '%', '%', '%', '%', 'Triệu đồng', 'Tỷ đồng', '%', '%', 'Người', 'Người', '%', '%', '%', '%', '%', '%', '%', 'Đạt xã vững mạnh', '%', '%', '%', '%'],
    'NĂM 2026': [10.3, 4.5, 9.0, 17.8, 8.5, 14.5, 800.0, 300.0, 100.0, 4.88, 157.0, 90.0, 48.5, 82.0, 0.5, 23.0, 93.0, 16.66, 100.0, float('nan'), 4.0, 85.0, 90.0, 80.0],
    'NĂM 2027': [10.2, 4.5, 9.0, 17.5, 8.5, 14.4, 850.0, 350.0, 100.0, 4.88, 165.0, 90.0, 48.8, 83.0, 0.7, 24.0, 95.0, 16.66, 100.0, float('nan'), 4.0, 85.0, 90.0, 80.0],
    'NĂM 2028': [10.4, 4.3, 8.8, 17.4, 8.3, 14.3, 900.0, 370.0, 100.0, 4.88, 173.0, 90.0, 49.0, 84.0, 0.8, 25.0, 95.0, 17.0, 100.0, float('nan'), 4.0, 85.0, 90.0, 80.0],
    'NĂM 2029': [10.1, 4.2, 8.4, 17.2, 8.2, 14.3, 950.0, 381.0, 100.0, 4.88, 182.0, 90.0, 49.1, 84.5, 0.9, 26.0, 96.0, 33.33, 100.0, float('nan'), 4.0, 85.0, 90.0, 80.0],
    'NĂM 2030': [10.0, 4.0, 8.3, 17.1, 8.0, 14.0, 1000.0, 381.0, 100.0, 4.88, 190.0, 90.0, 49.2, 85.0, 1.0, 27.0, 96.0, 50.0, 100.0, float('nan'), 4.0, 85.0, 90.0, 80.0],
    'Giai đoạn 2026 - 2030': [10.2, 4.3, 8.7, 17.4, 8.3, 14.3, 4500.0, 1782.0, 100.0, 4.88, 190.0, 450.0, 49.09, 85.0, 1.0, 26.0, 95.0, 50.0, 100.0, float('nan'), float('nan'), float('nan'), float('nan'), float('nan')],
    'CHỦ TRÌ': [
        'Phòng kinh tế', 'Phòng kinh tế', 'Phòng kinh tế', 'Phòng kinh tế', 'Phòng kinh tế', 'Phòng kinh tế', 'Phòng kinh tế', 'Phòng kinh tế',
        'Phòng Văn hóa - xã hội', 'Phòng kinh tế', 'Phòng Văn hóa – xã hội', 'Phòng Văn hóa – xã hội', 'Phòng kinh tế', 'Phòng kinh tế',
        'Phòng kinh tế', 'Phòng kinh tế', 'Phòng kinh tế', 'Phòng Văn hóa – xã hội', 'Ban Chỉ huy Quân sự; Công an xã', 'Ban Chỉ huy Quân sự; Công an xã',
        'Ban Xây dựng Đảng, các chi bộ trực thuộc', 'Ban Xây dựng Đảng, các chi bộ trực thuộc', 'các chi bộ trực thuộc', ''
    ]
}
indicators = pd.DataFrame(data)

# Users (same as before)
users = {
    "phongkinhte": {"role": "Phòng kinh tế", "password": "123"},
    "phongvanhua": {"role": "Phòng Văn hóa - xã hội", "password": "123"},
    "phongvanhua2": {"role": "Phòng Văn hóa – xã hội", "password": "123"},
    "banchqs": {"role": "Ban Chỉ huy Quân sự; Công an xã", "password": "123"},
    "banxaydung": {"role": "Ban Xây dựng Đảng, các chi bộ trực thuộc", "password": "123"},
    "admin": {"role": "Admin", "password": "admin"}
}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user = None
if 'results' not in st.session_state:
    st.session_state.results = {year: pd.DataFrame(columns=['Mã chỉ tiêu', 'Giá_trị_thực_hiện', 'Ghi_chú', 'Người_nhập', 'Thời_điểm', 'Trạng_thái']) for year in range(2026, 2031)}
if 'locked_years' not in st.session_state:
    st.session_state.locked_years = []

# Login logic (same as before)
if not st.session_state.logged_in:
    st.title("Đăng nhập")
    user = st.text_input("Username")
    passw = st.text_input("Password", type="password")
    if st.button("Đăng nhập"):
        if user in users and users[user]["password"] == passw:
            st.session_state.logged_in = True
            st.session_state.role = users[user]["role"]
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Sai username/password")
else:
    role = st.session_state.role
    st.title(f"Báo cáo Chỉ tiêu - {role}")
    if st.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.rerun()

    # Filter indicators by role
    filtered_indicators = indicators if role == "Admin" else indicators[indicators["CHỦ TRÌ"].str.contains(role.replace(" – ", " - "), na=False, case=False)]

    year = st.selectbox("Năm báo cáo", list(range(2026, 2031)) + ["Giai đoạn"])

    if year != "Giai đoạn":
        results = st.session_state.results[year]
        df = filtered_indicators.merge(results, left_on='Mã chỉ tiêu', right_on='Mã chỉ tiêu', how='left')
        df["Tỷ lệ %"] = (df["Giá_trị_thực_hiện"] / df[f"NĂM {year}"]) * 100
        df["Màu"] = df["Tỷ lệ %"].apply(lambda x: 'green' if x >= 100 else 'yellow' if x >= 90 else 'red' if pd.notna(x) else '')

        if role != "Admin" and year not in st.session_state.locked_years:
            st.subheader("Nhập báo cáo")
            for idx, row in df.iterrows():
                col1, col2 = st.columns(2)
                with col1:
                    st.text(f"{row['Mã chỉ tiêu']} - {row['Chỉ tiêu chủ yếu']} ({row['ĐƠN VỊ TÍNH']})")
                with col2:
                    value = st.number_input("Giá trị thực hiện", value=row.get("Giá_trị_thực_hiện", 0.0), key=f"val_{idx}_{year}")
                    note = st.text_input("Ghi chú", value=row.get("Ghi_chú", ""), key=f"note_{idx}_{year}")
                if st.button("Lưu", key=f"save_{idx}_{year}"):
                    new_row = pd.DataFrame({
                        'Mã chỉ tiêu': [row['Mã chỉ tiêu']],
                        'Giá_trị_thực_hiện': [value],
                        'Ghi_chú': [note],
                        'Người_nhập': [st.session_state.user],
                        'Thời_điểm': [datetime.datetime.now().isoformat()],
                        'Trạng_thái': ['Nháp']
                    })
                    st.session_state.results[year] = pd.concat([results[results['Mã chỉ tiêu'] != row['Mã chỉ tiêu']], new_row])
                    st.success("Đã lưu")

            if st.button("Gửi báo cáo"):
                st.session_state.results[year].loc[st.session_state.results[year]['Người_nhập'] == st.session_state.user, 'Trạng_thái'] = 'Đã gửi'
                st.success("Đã gửi, không sửa được nữa")

        st.dataframe(df.style.apply(lambda x: ['background-color: ' + x['Màu']] * len(x) if 'Màu' in x.name else None, axis=1))

    else:
        # Giai đoạn summary (aggregate from years)
        st.subheader("Theo dõi giai đoạn")
        agg_real = pd.DataFrame({'Mã chỉ tiêu': indicators['Mã chỉ tiêu']})
        for y in range(2026, 2031):
            res = st.session_state.results[y][['Mã chỉ tiêu', 'Giá_trị_thực_hiện']].rename(columns={'Giá_trị_thực_hiện': f'Real_{y}'})
            agg_real = agg_real.merge(res, how="left")
        agg_real['Total Real'] = agg_real.iloc[:, 1:].sum(axis=1)
        agg_df = indicators.merge(agg_real, on='Mã chỉ tiêu')
        fig, ax = plt.subplots()
        # Example plot; customize as needed
        ax.bar(agg_df['Mã chỉ tiêu'][:5], agg_df['Total Real'][:5])
        st.pyplot(fig)

    if role == "Admin":
        st.subheader("Tiến độ nộp")
        progress = {}
        for u in users:
            if u != "admin":
                count = len(st.session_state.results[year]) if year != "Giai đoạn" else 0  # Simplify for demo
                progress[u] = "Đã nộp" if count > 0 else "Chưa nộp"
        st.write(progress)

        if st.button("Khóa năm"):
            st.session_state.locked_years.append(year)
            st.success(f"Đã khóa năm {year}")

        # Export functions (same as before)
        def to_excel(df):
            out = BytesIO()
            with pd.ExcelWriter(out, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Tổng hợp')
            return out.getvalue()

        st.download_button("Xuất Excel", to_excel(df), "baocao.xlsx")

        def to_pdf(df):
            out = BytesIO()
            doc = SimpleDocTemplate(out, pagesize=letter)
            table_data = [df.columns] + df.values.tolist()
            table = Table(table_data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey), ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            doc.build([table])
            return out.getvalue()

        st.download_button("Xuất PDF", to_pdf(df), "baocao.pdf")
