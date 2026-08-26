import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(
    page_title="서울 기온 데이터 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 기온 데이터 분석")
st.write("서울의 일별 기온 데이터를 이용해 요약통계와 연평균 기온 변화를 살펴봅니다.")

# 데이터 주소
url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 불러오기
df = pd.read_csv(url)

# -----------------------------------
# 1. 원본 데이터
# -----------------------------------
st.subheader("1. 원본 데이터")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------------
# 2. 요약통계
# -----------------------------------
st.subheader("2. 요약통계")

st.dataframe(
    df.describe(),
    use_container_width=True
)

# -----------------------------------
# 3. 날짜 처리
# -----------------------------------
df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

# 연도 만들기
df["연도"] = df["날짜"].dt.year

# -----------------------------------
# 4. 연평균 기온 계산
# -----------------------------------
annual_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

# 1907년 이후
annual_temp = annual_temp[
    annual_temp["연도"] >= 1907
]

# -----------------------------------
# 5. 선 그래프
# -----------------------------------
st.subheader("3. 서울의 연평균 기온 변화")

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    annual_temp["연도"],
    annual_temp["평균기온"],
    linewidth=1.5
)

ax.set_xlabel("Year")
ax.set_ylabel("Average Temperature (°C)")
ax.set_title("Annual Average Temperature in Seoul (1907-Present)")

ax.grid(True, alpha=0.3)

plt.tight_layout()

st.pyplot(fig, use_container_width=True)

# -----------------------------------
# 6. 연도별 데이터
# -----------------------------------
st.subheader("4. 연도별 평균기온")

st.dataframe(
    annual_temp,
    use_container_width=True
)
