# --------------------------------------------------
# 그래프 3. 총 관객 수 히스토그램
# --------------------------------------------------
st.header("3. 영화별 총 관객 수 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].copy()

# 총 관객 수를 숫자로 변환
hist_df["total_audi"] = pd.to_numeric(
    hist_df["total_audi"],
    errors="coerce",
)

# 결측값 제거
hist_df = hist_df.dropna(subset=["total_audi"])

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수",
    },
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 수: %{x:,.0f}명<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    ),
)

fig3.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=60, l=20, r=20, b=20),
)

st.plotly_chart(fig3, use_container_width=True)


# --------------------------------------------------
# 히스토그램에서 알 수 있는 내용
# --------------------------------------------------

# 가장 관객이 많은 영화
max_idx = hist_df["total_audi"].idxmax()
max_movie = hist_df.loc[max_idx, "movieNm"]
max_audi = hist_df.loc[max_idx, "total_audi"]

# 영화가 가장 많이 들어 있는 관객 구간 계산
counts, bin_edges = pd.cut(
    hist_df["total_audi"],
    bins=20,
    include_lowest=True,
    retbins=True,
)

bin_counts = counts.value_counts().sort_index()

most_common_bin = bin_counts.idxmax()

range_start = most_common_bin.left
range_end = most_common_bin.right

st.markdown("**이 그래프로 알 수 있는 것**")

st.write(
    f"대부분의 영화는 총 관객 수 "
    f"**{range_start:,.0f}명 ~ {range_end:,.0f}명** "
    f"구간에 몰려 있습니다."
)

st.write(
    f"총 관객이 가장 많은 영화는 **{max_movie}**로, "
    f"총 **{max_audi:,.0f}명**의 관객을 모았습니다."
)
