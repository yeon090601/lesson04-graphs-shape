# --------------------------------------------------
# 그래프 2. 장르별 영화 트리맵
# --------------------------------------------------
st.header("2. 장르별 영화 트리맵")

# 트리맵에 사용할 데이터
treemap_df = df[
    ["genre_first", "movieNm", "total_audi"]
].copy()

# 총 관객 수가 숫자로 처리되도록 변환
treemap_df["total_audi"] = pd.to_numeric(
    treemap_df["total_audi"],
    errors="coerce",
).fillna(0)

# 영화명이 비어 있는 경우를 대비
treemap_df["movieNm"] = (
    treemap_df["movieNm"]
    .fillna("영화명 없음")
    .astype(str)
)

fig_treemap = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객",
)

fig_treemap.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    ),
)

fig_treemap.update_layout(
    margin=dict(t=60, l=20, r=20, b=20),
)

st.plotly_chart(fig_treemap, use_container_width=True)

st.divider()

st.markdown("**이 그래프로 알 수 있는 것**")
st.text_input(
    "한 문장으로 적어 보세요.",
    placeholder="예: 장르별로 어떤 영화가 많은 관객을 모았는지 알 수 있다.",
    label_visibility="collapsed",
    key="graph2_note",
)
