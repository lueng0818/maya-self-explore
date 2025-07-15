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
    /* 模擬 Tailwind utility */
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
    <style> /* 省略 CSS… */ </style>
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
    wealth_df   = pd.read_csv(os.path.join(DATA_DIR, "totem_wealth_view.csv"))
    emotion_df  = pd.read_csv(os.path.join(DATA_DIR, "totem_emotion.csv"))
except Exception as e:
    st.error(f"❌ 資料載入失敗：{e}")
    st.stop()

# ────────────── Sidebar Input ──────────────
st.sidebar.header("📅 查詢你的 Maya 印記")
year = st.sidebar.selectbox("西元年", sorted(kin_start.keys()), index=sorted(kin_start.keys()).index(1990))
month = st.sidebar.selectbox("月份", list(range(1,13)), index=0)
max_day = calendar.monthrange(year, month)[1]
day = st.sidebar.slider("日期", 1, max_day, 1)
category = st.sidebar.radio("🔍 主題", ["自我探索","金錢觀","情感議題"])

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
# ── 功能說明 區塊 ──
st.markdown("## 🔍 功能說明")

st.markdown("""
1. **輸入你的生日**  
   選擇西元年／月／日，精準算出你的 Maya 能量頻率（KIN）。

2. **一鍵生成印記**  
   系統自動計算並對應 20 種圖騰，並根據主題生成不同維度的深入解讀。  
""")

if category == "自我探索":
    st.markdown("""
3. **深入能量解讀：自我探索**  
   解鎖你的**天賦**（🎁 禮物）、**挑戰**（🚧 瓶頸）與**角色定位**（🙋 你是誰），  
   並附上具體日常練習建議（🪄 建議），幫助你在生活中自然發揮力量。
""")

elif category == "金錢觀":
    st.markdown("""
3. **深入能量解讀：金錢觀**  
   解析你的**金錢態度**（💰 我的金錢觀）、**盲點**（🚧 金錢盲點）、  
   以及累積財富的實戰方法（🌱 創造豐盛的方法、🗝️ 如何達到財富自由），  
   讓你從心態與行動兩面穩健累積資源。
""")

else:  # 情感議題
    st.markdown("""
3. **深入能量解讀：情感議題**  
   探索你的**情感特質**（💞 個人情感特質）、**相處盲點**（🚧 關係盲點）、  
   並提供**溝通與修復建議**（💡 改善關係的建議、🤝 伴侶需知），  
   幫助你在關係中更輕鬆自在地連結與成長。
""")

st.markdown("""
4. **分享與回饋**  
   將你的專屬印記海報分享到社群，或在底部留言，  
   幫助我們持續優化內容與體驗。
""")

st.markdown('</div>', unsafe_allow_html=True)

# ────────────── caption mapping ──────────────
descriptions = {
  "你是誰": "←描述你的個性或能量特質…",
  "最常遇到的瓶頸": "←代表你比較容易卡關…",
  "建議": "←提供簡單可行的提醒…",
  "擁有什麼樣的禮物": "←天生擁有的天賦…",
  "我的金錢觀": "←說明你怎麼看錢…",
  "金錢盲點": "←用錢時容易犯的錯…",
  "創造豐盛的方法": "←幫助累積財富的小事…",
  "如何達到財富自由": "←心態＋行動結合…",
  "個人情感特質": "←你在感情裡的樣子…",
  "情感關係中的盲點": "←相處障礙小陷阱…",
  "改善關係的建議": "←小方法改善溝通…",
  "需要伴侶了解的重點": "←希望對方知道的需求…",
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

# ────────────── 深度解讀 ──────────────
if category=="自我探索":
    df = self_df[self_df["圖騰"]==totem]
    if not df.empty:
        render_section(
            df,
            [("你是誰","🙋 你是誰"),("最常遇到的瓶頸","🚧 最常遇到的瓶頸"),
             ("建議","🪄 建議"),("擁有什麼樣的禮物","🎁 擁有什麼樣的禮物")],
            ["圖騰是你的角色原型，幫助你看見優勢與盲點。","內化這份能量，成為更完整的自己。"]
        )

elif category=="金錢觀":
    df = wealth_df[wealth_df["圖騰"]==totem]
    if not df.empty:
        render_section(
            df,
            [("我的金錢觀","💰 我的金錢觀"),("金錢盲點","🚧 金錢盲點"),
             ("創造豐盛的方法","🌱 創造豐盛的方法"),("如何達到財富自由","🗝️ 如何達到財富自由")],
            ["了解自己錢的能量，才不會重複踩雷。","調整心態＋實踐方法，累積財富自由。"]
        )

elif category=="情感議題":
    df = emotion_df[emotion_df["圖騰"]==totem]
    if not df.empty:
        render_section(
            df,
            [("個人情感特質","💞 個人情感特質"),("情感關係中的盲點","🚧 情感關係中的盲點"),
             ("改善關係的建議","💡 改善關係的建議"),("需要伴侶了解的重點","🤝 需要伴侶了解的重點")],
            ["先了解自身情感模式，才能有效調整。","告訴對方需求，共創穩定連結。"]
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

> **阿傑，28 歲｜設計師**  
> “系統操作非常直覺，不到十分鐘就完成。看到自己的挑戰角色後，給了我面對困難的新勇氣。”
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

- **能否下載解讀海報？**  
  正在開發中，敬請期待下次更新！
""")
st.markdown('</div>', unsafe_allow_html=True)

# ────────────── 固定 Footer ──────────────
st.markdown(
    """
    <footer class="footer">
      準備好體驗你的 Maya 力量了嗎？  
      <a href="#查詢你的印記">👉 一鍵查詢</a>  
      <a href="https://line.me/R/ti/p/%40690ZLAGN" target="_blank">👉 加入社群</a>
    </footer>
    """,
    unsafe_allow_html=True
)
