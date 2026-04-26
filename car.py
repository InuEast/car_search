import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="차종 검색", layout="wide")

# 데이터 로드
df = pd.read_csv('cars.csv', encoding='utf-8-sig')

st.title("🚗 차종 검색 시스템")

search_model = st.text_input("차종을 입력하세요 (예: 아반떼)")

def copy_to_clipboard(text):
    components.html(f"""
        <script>
        function copyText() {{
            navigator.clipboard.writeText("{text}");
            const msg = document.getElementById("msg");
            msg.style.display = "block";
            setTimeout(() => {{
                msg.style.display = "none";
            }}, 1500);
        }}
        </script>

        <button onclick="copyText()" 
        style="
            background-color:#4CAF50;
            color:white;
            border:none;
            padding:6px 10px;
            border-radius:6px;
            cursor:pointer;">
            복사
        </button>

        <div id="msg" style="display:none; color:green; font-size:12px;">
            복사됨!
        </div>
    """, height=60)

if search_model.strip():
    result = df[df['차종'].str.contains(search_model, case=False, na=False)]

    if not result.empty:
        st.markdown(f"### 🔍 검색 결과 ({len(result)}건)")

        result_display = result.copy()
        result_display["Product id"] = result_display["Product id"].astype(str).str.replace(",", "")

        # 헤더
        col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])
        col1.markdown("**제조사**")
        col2.markdown("**차종**")
        col3.markdown("**호수**")
        col4.markdown("**Product ID**")
        col5.markdown("**복사**")

        st.divider()

        # 데이터 출력
        for i, row in result_display.iterrows():
            col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])

            col1.write(row['제조사'])
            col2.write(row['차종'])
            col3.write(row['호수'])

            # Product ID 클릭해도 복사 가능하게
            col4.markdown(f"""
                <span style="cursor:pointer; color:#1f77b4;"
                onclick="navigator.clipboard.writeText('{row['Product id']}')">
                {row['Product id']}
                </span>
            """, unsafe_allow_html=True)

            with col5:
                copy_to_clipboard(row['Product id'])

    else:
        st.warning("❌ 해당 차종을 찾을 수 없습니다.")