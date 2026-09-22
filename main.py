import pandas as pd
import plotly.express as px
import streamlit as st


DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화 데이터를 살펴봅니다.")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 필요한 열만 사용
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

    # 장르가 여러 개 적힌 경우 첫 번째 장르만 사용
    # 예: "액션|드라마" -> "액션"
    #     "액션/드라마" -> "액션"
    df["genre_first"] = (
        df["genre"]
        .fillna("미분류")
        .astype(str)
        .str.split(r"[|/]", regex=True)
        .str[0]
        .str.strip()
    )

    df.loc[df["genre_first"].eq(""), "genre_first"] = "미분류"

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

fig = px.pie(
    genre_counts,
    names="장르",
    values="편수",
    hole=0.55,
    title="장르별 영화 편수",
)

fig.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    ),
)

fig.update_layout(
    legend_title_text="장르",
    margin=dict(t=60, l=20, r=20, b=20),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown("**이 그래프로 알 수 있는 것**")
st.text_input(
    "한 문장으로 적어 보세요.",
    placeholder="예: 어떤 장르의 영화가 가장 많이 포함되어 있는지 알 수 있다.",
    label_visibility="collapsed",
    key="graph1_note",
)
