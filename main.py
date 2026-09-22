import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/kobis_movies.csv"
)

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    columns = [
        "movieCd",
        "movieNm",
        "openDt",
        "genre",
        "nation",
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10",
    ]

    df = df[columns].copy()

    # 여러 장르가 있는 경우 첫 번째 장르만 사용
    # 예: 액션|드라마 -> 액션
    df["genre_first"] = (
        df["genre"]
        .fillna("미분류")
        .astype(str)
        .str.split(r"[|/]", regex=True)
        .str[0]
        .str.strip()
    )

    df.loc[df["genre_first"] == "", "genre_first"] = "미분류"

    return df


df = load_data()


# ==================================================
# 그래프 1. 장르별 영화 편수
# ==================================================
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre_first"]
    .value_counts()
    .rename_axis("장르")
    .reset_index(name="편수")
)

fig1 = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.55,
    title="장르별 영화 편수",
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    ),
)

fig1.update_layout(
    legend_title_text="장르",
    margin=dict(t=60, l=20, r=20, b=20),
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "첫 번째 그래프의 내용을 한 문장으로 적어 보세요.",
    placeholder="예: 어떤 장르의 영화가 가장 많이 포함되어 있는지 알 수 있다.",
    key="graph1_note",
)


# ==================================================
# 그래프 2. 장르별 영화 트리맵
# ==================================================
st.header("2. 장르별 영화 트리맵")

treemap_df = df[
    ["genre_first", "movieNm", "total_audi"]
].copy()

treemap_df["total_audi"] = pd.to_numeric(
    treemap_df["total_audi"],
    errors="coerce",
).fillna(0)

treemap_df["movieNm"] = (
    treemap_df["movieNm"]
    .fillna("영화명 없음")
    .astype(str)
)

fig2 = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객",
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    ),
)

fig2.update_layout(
    margin=dict(t=60, l=20, r=20, b=20),
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "두 번째 그래프의 내용을 한 문장으로 적어 보세요.",
    placeholder="예: 장르별로 어떤 영화가 많은 관객을 모았는지 알 수 있다.",
    key="graph2_note",
)


# ==================================================
# 그래프 3. 총 관객 수 히스토그램
# ==================================================
st.header("3. 영화별 총 관객 수 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].copy()

hist_df["total_audi"] = pd.to_numeric(
    hist_df["total_audi"],
    errors="coerce",
)

hist_df = hist_df.dropna(
    subset=["total_audi"]
)

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
# 대부분의 영화가 몰려 있는 구간 계산
# --------------------------------------------------
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


# --------------------------------------------------
# 가장 관객이 많은 영화 계산
# --------------------------------------------------
max_idx = hist_df["total_audi"].idxmax()

max_movie = hist_df.loc[max_idx, "movieNm"]
max_audi = hist_df.loc[max_idx, "total_audi"]


st.divider()

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


# ==================================================
# 그래프 4. 개봉일 스크린 수와 총 관객의 관계
# ==================================================
st.header("4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df[
    ["movieNm", "genre_first", "first_scrn", "total_audi"]
].copy()

scatter_df["first_scrn"] = pd.to_numeric(
    scatter_df["first_scrn"],
    errors="coerce",
)

scatter_df["total_audi"] = pd.to_numeric(
    scatter_df["total_audi"],
    errors="coerce",
)

scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi"]
)

scatter_df["movieNm"] = (
    scatter_df["movieNm"]
    .fillna("영화명 없음")
    .astype(str)
)

scatter_df["genre_first"] = (
    scatter_df["genre_first"]
    .fillna("미분류")
    .astype(str)
)

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre_first": "장르",
    },
)

fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(
        size=9,
        opacity=0.75,
    ),
)

fig4.update_layout(
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    legend_title="장르",
    margin=dict(t=60, l=20, r=20, b=20),
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "네 번째 그래프의 내용을 한 문장으로 적어 보세요.",
    placeholder="예: 개봉일 스크린 수와 총 관객 수의 관계를 살펴볼 수 있다.",
    key="graph4_note",
)


# ==================================================
# 그래프 5. 장르별 총 관객 수 상자 그림
# ==================================================
st.header("5. 장르별 총 관객 수 분포")

box_df = df[
    ["movieNm", "genre_first", "total_audi"]
].copy()

# 총 관객 수를 숫자로 변환
box_df["total_audi"] = pd.to_numeric(
    box_df["total_audi"],
    errors="coerce",
)

# 필요한 값이 없는 행 제거
box_df = box_df.dropna(
    subset=["genre_first", "total_audi"]
)

# 영화명 결측값 처리
box_df["movieNm"] = (
    box_df["movieNm"]
    .fillna("영화명 없음")
    .astype(str)
)

# --------------------------------------------------
# 영화가 10편 이상인 장르만 선택
# --------------------------------------------------
genre_movie_counts = (
    box_df["genre_first"]
    .value_counts()
)

selected_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

box_df = box_df[
    box_df["genre_first"].isin(selected_genres)
].copy()


# --------------------------------------------------
# 상자 그림 생성
# --------------------------------------------------
fig5 = px.box(
    box_df,
    x="genre_first",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 수 분포",
    labels={
        "genre_first": "장르",
        "total_audi": "총 관객 수",
    },
)


# --------------------------------------------------
# 이상치에 마우스를 올렸을 때 영화명 표시
# --------------------------------------------------
fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    ),
)


fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    margin=dict(t=60, l=20, r=20, b=20),
)

st.plotly_chart(fig5, use_container_width=True)

st.divider()

st.markdown("**이 그래프로 알 수 있는 것**")

st.text_input(
    "다섯 번째 그래프의 내용을 한 문장으로 적어 보세요.",
    placeholder="예: 장르별 총 관객 수의 분포와 차이를 비교할 수 있다.",
    key="graph5_note",
)
