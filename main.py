import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 읽기
df = pd.read_csv(url, encoding="utf-8-sig")
df["날짜"] = pd.to_datetime(df["날짜"])
df["연도"] = df["날짜"].dt.year

# 요약통계
print(df.describe())

# 연평균 기온
annual_temp = df.groupby("연도")["평균기온"].mean()

# 전체 연도 범위
all_years = range(df["연도"].min(), df["연도"].max() + 1)

# 아예 값이 없는 연도 찾기
missing_years = []
for y in all_years:
    year_data = df[df["연도"] == y]["평균기온"]
    if year_data.notna().sum() == 0:
        missing_years.append(y)

# 유난히 낮은 연도 찾기(IQR 기준)
q1 = annual_temp.quantile(0.25)
q3 = annual_temp.quantile(0.75)
iqr = q3 - q1
low_cut = q1 - 1.5 * iqr
low_years = annual_temp[annual_temp < low_cut]

# 그래프
plt.figure(figsize=(14, 6))
plt.plot(annual_temp.index, annual_temp.values, marker="o", markersize=2, linewidth=1)

# 비어 있는 연도 강조
for y in missing_years:
    plt.axvspan(y - 0.5, y + 0.5, alpha=0.2)
    plt.text(y, annual_temp.min(), f"{y}\n자료 없음", ha="center", va="bottom")

# 유난히 낮은 연도 강조
plt.scatter(low_years.index, low_years.values, s=80)
for y, v in low_years.items():
    plt.text(y, v, f"{y}: {v:.2f}℃", ha="center", va="bottom")

# 1907년은 부분 연도라 참고 표시
if 1907 in annual_temp.index:
    plt.text(1907, annual_temp.loc[1907], "1907\n(10월 시작)", ha="center", va="top")

plt.title("서울 연평균 기온 추세 (비어 있는 연도·유난히 낮은 연도 강조)")
plt.xlabel("연도")
plt.ylabel("연평균기온(℃)")
plt.grid(True)
plt.show()

print("값이 비어 있는 연도:", missing_years)
print("유난히 낮은 연도:", list(low_years.index))
