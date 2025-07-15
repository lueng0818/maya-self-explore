import streamlit as st
from utils import compute_kin, fetch_self_info

st.title("自我探索查詢")
year = st.number_input("年", 1900, 2100, 1990)
month = st.number_input("月", 1, 12, 6)
day = st.number_input("日", 1, 31, 13)

kin = compute_kin(year, month, day)
info = fetch_self_info(kin)

st.header(f"KIN {kin} - {info['圖騰']}")
for key, val in info.items():
    if key not in ['KIN', '圖騰']:
        st.write(f"**{key}**: {val}")
