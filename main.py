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
    #     액션/드라마 -> 액션
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


# --------------------------------------------------
# 그래프 1. 장르별 영화 편수
# --------------------------------------------------
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


# --------------------------------------------------
# 그래프 2. 장르별 영화 트리맵
# --------------------------------------------------
st.header("2. 장르별 영화 트리맵")

treemap_df = df[
    ["genre_first", "movieNm", "total_audi"]
].copy()

# 총 관객 수를 숫자로 변환
treemap_df["total_audi"] = pd.to_numeric(
    treemap_df["total_audi"],
    errors="coerce",
).fillna(0)

# 영화명이 없는 경우 처리
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
