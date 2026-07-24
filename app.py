import streamlit as st

from config import *
from utils.data_loader import load_data
from utils.filters import sidebar_filters
from utils.charts import (
    yearly_trend_chart,
    government_comparison_chart,
    government_aspirants_chart,
    state_incidents_chart,
    state_aspirants_chart,
    exam_category_chart,
    conducting_body_category_chart,
    conducting_body_treemap,
    body_type_chart,
)

from utils.helpers import (
    dashboard_header,
    overview_kpis,
    government_cards,
    government_insights,
)
from utils.calculations import state_summary
from utils.helpers import conducting_body_card
from utils.calculations import top_conducting_bodies
from utils.calculations import state_wise_analytics
from utils.charts import state_wise_chart
from utils.calculations import state_insights
from utils.calculations import major_incidents_timeline
from utils.helpers import timeline_card


import streamlit as st

st.set_page_config(
    page_title="India Paper Leak Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>

.body-card{
    background:#1E293B;
    border-left:6px solid #FFD700;
    padding:18px;
    border-radius:12px;
    margin-bottom:18px;
}

.body-title{
    color:white;
    font-size:22px;
    font-weight:700;
    margin-bottom:12px;
}

.body-text{
    color:#E5E7EB;
    font-size:16px;
    line-height:1.8;
}
            
.insights-card {
    background: #1E293B;
    border-left: 6px solid #3B82F6;
    border-radius: 12px;
    padding: 20px;
    margin-top: 15px;
    margin-bottom: 20px;
}

.insights-title {
    color: white;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 15px;
}

.insights-item {
    color: #E5E7EB;
    font-size: 16px;
    line-height: 1.8;
    margin-bottom: 8px;
}
            
.timeline-card{
    background:#1E293B;
    border-left:6px solid #F59E0B;
    padding:18px;
    border-radius:12px;
    margin-bottom:18px;
}

.timeline-date{
    color:#FBBF24;
    font-size:15px;
    font-weight:700;
    margin-bottom:8px;
}

.timeline-title{
    color:white;
    font-size:20px;
    font-weight:700;
    margin-bottom:10px;
}

.timeline-body{
    color:#E5E7EB;
    font-size:15px;
    line-height:1.7;
}
</style>
""", unsafe_allow_html=True)

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

df = load_data()

filtered_df = sidebar_filters(df)

dashboard_header(filtered_df)

st.divider()

# ----------------------------
# KPI Placeholder
# ----------------------------

st.header("📊 Overview")

overview_kpis(filtered_df)

st.divider()

# ----------------------------
# Trend Placeholder
# ----------------------------

st.header("📈 Trend Analysis")

trend_container = st.container(border=True)

with trend_container:

    fig = yearly_trend_chart(filtered_df)

    if fig is not None:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )
    else:
        st.warning("No data available for the selected filters.")

st.divider()

# ----------------------------
# Government Comparison
# ----------------------------

st.header("🏛 UPA vs NDA Analysis")

government_cards(filtered_df)

st.divider()

st.header("🏛 Government Comparison")

col1, col2 = st.columns(2)

with col1:
    fig = government_comparison_chart(filtered_df)

    if fig is not None:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

with col2:
    fig = government_aspirants_chart(filtered_df)

    if fig is not None:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )
    else:
        st.warning("No government comparison data available.")

st.divider()

government_insights(filtered_df)




# ----------------------------
# Map
# ----------------------------

st.divider()
st.header("🗺️ Geographic Analysis")

fig = state_incidents_chart(filtered_df)

col1, col2 = st.columns(2)

with col1:
    fig = state_incidents_chart(filtered_df)

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = state_aspirants_chart(filtered_df)

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)


st.divider()

st.header("🏛️ Conducting Body Analysis")

col1, col2 = st.columns(2)

with col1:


    fig = conducting_body_treemap(filtered_df)

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = body_type_chart(filtered_df)

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)

st.divider()


st.subheader("🏆 Top Conducting Body Categories")

top_bodies = top_conducting_bodies(filtered_df)

for i in range(0, len(top_bodies), 2):

    col1, col2 = st.columns(2)

    with col1:
        conducting_body_card(i + 1, top_bodies.iloc[i])

    if i + 1 < len(top_bodies):
        with col2:
            conducting_body_card(i + 2, top_bodies.iloc[i + 1])


st.divider()

st.subheader("📍 State-wise Analytics")

state_df = state_wise_analytics(filtered_df)

st.dataframe(state_df, use_container_width=True)

state_wise_chart(state_df)

insights = state_insights(state_df)

st.subheader("💡 Key Insights")

for insight in insights:
    st.info(insight)

st.divider()




st.header("📅 Major Paper Leak Timeline")

timeline_df = major_incidents_timeline(filtered_df)


for _, row in timeline_df.iterrows():
    timeline_card(row)

st.divider()

st.header("📝 Exam Analysis")

fig = exam_category_chart(filtered_df)

if fig is not None:
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------------------------
# Explorer
# ----------------------------

st.header("🔍 Incident Explorer")

st.data_editor(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    disabled=True,
)


st.divider()

st.markdown(
    """
    <div style="
        background-color:#111827;
        padding:12px 18px;
        border-radius:10px;
        text-align:center;
        color:#D1D5DB;
        font-size:12px;
        line-height:1.5;
        margin-top:15px;
    ">

    <div style="font-size:16px;font-weight:600;color:white;margin-bottom:6px;">
        India Paper Leak Dashboard (2004–2026)
    </div>

    Built with ❤️ using <b>Streamlit</b>, <b>Python</b>, <b>Pandas</b> & <b>Plotly</b>

    

    📂 Dataset: <b>India Paper Leaks from 2004 to 2026</b> by <b>Sujay Nadkarni (Kaggle)</b>

    

    Independent analysis • Open Source • MIT License

    

    <a href="https://github.com/Arghya-das99/india-paper-leak-dashboard" target="_blank" style="text-decoration:none;">
        GitHub
    </a>
    &nbsp;|&nbsp;
    <a href="https://www.linkedin.com/in/arghya-das-60a118193" target="_blank" style="text-decoration:none;">
        LinkedIn
    </a>

    <br>

    <span style="font-size:11px;color:#9CA3AF;">
        © 2026 Arghya Das
    </span>

    </div>
    """,
    unsafe_allow_html=True,
)
