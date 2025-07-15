import os
import calendar
from PIL import Image

import pandas as pd
import streamlit as st

# ────────────── Path Setup ──────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR  = os.path.join(BASE_DIR, "images")

# ────────────── Page Config & CSS ──────────────
st.set_page_config(page_title="Maya 生命印記解碼", layout="wide")
st.markdown(
    """<style>
    .hero {padding:4rem 2rem; text-align:center; background:#f0f5f9;}
    .hero h1 {font-size:3rem; font-weight:700; margin-bottom:0.5rem;}
    .hero p  {font-size:1.25rem; margin-bottom:1.5rem;}
    .btn-primary {background:#1d4ed8; color:white; padding:0.75rem 1.5rem; border-radius:0.375rem; text-decoration:none;}
    .features, .example, .testimonials, .faq {padding:2rem;}
    .footer {position:fixed; bottom:0; width:100%; background:#1f2937; color:white; text-align:center; padding:1rem;}
    .footer a {color:#60a5fa; text-decoration:none; margin:0 0.5rem;}
    </style>""",
    unsafe_allow_html=True,
)

# ────────────── Hero Section ──────────────
st.markdown(
    """
    <section class="hero">
      <h1>立即解碼你的 Maya 生命印記，喚醒宇宙支持能量</h1>
      <p>只要輸入出生日期，一鍵探索你的專屬靈性密碼，並獲得實踐建議──無需下載、馬上操作。</p>
      <p><em>請從左側面板輸入你的西元生日，即可立即查看。</em></p>
    </section>
    """,
    unsafe_allow_html=True,
)

# ────────────── Load Data ──────────────
try:
    kin_start   = pd.read_csv(os.path.join(DATA_DIR, "kin_start_year.csv"), index_col="年份")["起始KIN"].to_dict()
    month_accum = pd.read_csv(os.path.join(DATA_DIR, "month_day_accum.csv"),   index_col="月份")["累積天數"].to_dict()
    kin_basic   = pd.read_csv(os.path.join(DATA_DIR, "kin_basic_info.csv"))
    self_df     = pd.read_csv(os.path.join(DATA_DIR, "totem_interpretation_new.csv"))
except Exception as e:
    st.error(f"❌ 資料載入失敗：{e}")
    st.stop()

# ────────────── Sidebar Input ──────────────
st.sidebar.header("📅 查詢你的 Maya 印記")
year = st.sidebar.selectbox("西元年", sorted(kin_start.keys()), index=sorted(kin_start.keys()).index(1990))
month = st.sidebar.selectbox("月份", list(range(1,13)), index=0)
max_day = calendar.monthrange(year, month)[1]
day = st.sidebar.slider("日期", 1, max_day, 1)

# ────────────── KIN 計算 ──────────────
start_kin = kin_start.get(year)
if start_kin is None:
    st.sidebar.error("⚠️ 此年份無起始 KIN")
    st.stop()
raw = start_kin + month_accum.get(month,0) + day
mod = raw % 260
kin = 260 if mod==0 else mod

# ────────────── 顯示基本 KIN 與圖騰 ──────────────
subset = kin_basic[kin_basic["KIN"]==kin]
if subset.empty:
    st.error(f"❓ 找不到 KIN {kin} 資料")
    st.stop()
info = subset.iloc[0]
totem = info["圖騰"]

st.markdown(f"## 🔢 你的 KIN：{kin} ｜ {info['主印記']} — {totem}", unsafe_allow_html=True)
img_file = os.path.join(IMG_DIR, f"{totem}.png")
if os.path.exists(img_file):
    st.image(Image.open(img_file), width=120)

# ────────────── 功能說明 ──────────────
st.markdown("## 🔍 功能說明")
st.markdown("""
1. **輸入你的生日**  
   選擇西元年／月／日，精準算出你的 Maya 能量頻率（KIN）。

2. **一鍵生成印記**  
   系統自動計算並對應 20 種圖騰，並根據主題生成不同維度的深入解讀。  

3. **深入能量解讀：自我探索**  
   解鎖你的**天賦**（🎁 禮物）、**挑戰**（🚧 瓶頸）與**角色定位**（🙋 你是誰），  
   並附上具體日常練習建議（🪄 建議），幫助你在生活中自然發揮力量。

4. **分享與回饋**  
   將你的專屬印記海報分享到社群，或在底部留言，  
   幫助我們持續優化內容與體驗。
""")

# ────────────── caption mapping ──────────────
descriptions = {
  "你是誰": "←描述你的個性或能量特質…",
  "最常遇到的瓶頸": "←代表你比較容易卡關…",
  "建議": "←提供簡單可行的提醒…",
  "擁有什麼樣的禮物": "←天生擁有的天賦…",
}

def render_section(df, items, edu_pts):
    for pt in edu_pts:
        st.info(pt)
    row = df.iloc[0]
    for col, label in items:
        if col not in row: continue
        st.markdown(f"### {label}")
        cap = descriptions.get(col)
        if cap: st.caption(cap)
        st.write(row[col])

# ────────────── 深度解讀：自我探索 ──────────────
df = self_df[self_df["圖騰"]==totem]
if not df.empty:
    render_section(
        df,
        [("你是誰","🙋 你是誰"),("最常遇到的瓶頸","🚧 最常遇到的瓶頸"),
         ("建議","🪄 建議"),("擁有什麼樣的禮物","🎁 擁有什麼樣的禮物")],
        ["圖騰是你的角色原型，幫助你看見優勢與盲點。","內化這份能量，成為更完整的自己。"]
    )

# ────────────── 深度解讀範例 ──────────────
st.markdown('<div class="example">', unsafe_allow_html=True)
st.markdown("### 深度解讀範例")
st.markdown("""
- **圖騰：** 白狗  
- **核心能量：** 護佑、守護、內在安定  
- **建議實踐：** 每日冥想前，點蠟燭並呼吸三分鐘，想像溫暖的火焰保障你的安全。  
- **背後故事：** 白狗象徵夜晚的守護神，牠引領靈魂穿越黑暗，回到自我中心。
""")
st.markdown('</div>', unsafe_allow_html=True)

# ────────────── 案例分享 ──────────────
st.markdown('<div class="testimonials">', unsafe_allow_html=True)
st.markdown("### 案例分享")
st.markdown("""
> **小芸，35 歲｜自由工作者**  
> “第一次查到『藍鷹』印記，就驚覺自己其實一直渴望自由翱翔。照著建議練習後，一個月內順利接下夢想案子！”
""")
st.markdown('</div>', unsafe_allow_html=True)

# ────────────── 常見問題 ──────────────
st.markdown('<div class="faq">', unsafe_allow_html=True)
st.markdown("### 常見問題")
st.markdown("""
- **為什麼查不到我的印記？**  
  請確認輸入格式（西元），或嘗試切換瀏覽器。  

- **一天可以查幾次？**  
  建議每次間隔 24 小時，以穩定能量頻率。  
""")
st.markdown('</div>', unsafe_allow_html=True)

# ────────────── 固定 Footer ──────────────
st.markdown(
    """
    <footer class="footer">
      <a href="https://www.facebook.com/soulclean1413/" target="_blank">👉 加入粉專</a> 
      <a href="https://www.instagram.com/tilandky/" target="_blank">👉 追蹤IG</a>
      <a href="https://line.me/R/ti/p/%40690ZLAGN" target="_blank">👉 加入社群</a>
    </footer>
    """,
    unsafe_allow_html=True
)
