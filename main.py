import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="서울 기온 데이터 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 데이터 분석")
st.write("서울의 일별 기온 데이터를 이용해 요약통계와 연평균 기온 변화를 살펴봅니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

df = pd.read_csv(url, encoding="cp949")

st.subheader("1. 원본 데이터")
st.dataframe(df)

# -----------------------------
# 요약통계
# -----------------------------
st.subheader("2. 기온 데이터 요약통계")

summary = df.describe()

st.dataframe(summary)

# -----------------------------
# 날짜 데이터 처리
# -----------------------------
df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

# 연도 추출
df["연도"] = df["날짜"].dt.year

# -----------------------------
# 일별 평균기온 → 연평균 기온
# -----------------------------
annual_temp = (
    df.groupby("연도")["평균기온(℃)"]
    .mean()
    .reset_index()
)

# 1907년 이후만 사용
annual_temp = annual_temp[annual_temp["연도"] >= 1907]

# -----------------------------
# 연평균 기온 그래프
# -----------------------------
st.subheader("3. 서울의 연평균 기온 변화")

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    annual_temp["연도"],
    annual_temp["평균기온(℃)"],
    linewidth=1.5
)

ax.set_title("서울의 연평균 기온 변화 (1907년~현재)", fontsize=16)
ax.set_xlabel("연도")
ax.set_ylabel("연평균 기온 (℃)")
ax.grid(alpha=0.3)

st.pyplot(fig)

# -----------------------------
# 연평균 데이터 확인
# -----------------------------
st.subheader("4. 연도별 평균기온 데이터")

st.dataframe(
    annual_temp,
    use_container_width=True
)
