import plotly.express as px
import plotly.graph_objects as go
import json
import plotly.express as px
from utils.calculations import state_summary

from utils.calculations import government_chart_data
import streamlit as st

# ==========================================================
# COMMON LAYOUT
# ==========================================================

def _apply_dark_theme(fig, title, height=450):
    """
    Apply a consistent dark theme to all Plotly charts.
    """

    fig.update_layout(
        title={
            "text": title,
            "x": 0.02,
            "xanchor": "left",
            "font": {
                "size": 20,
                "color": "#F8FAFC",
            },
        },
        template="plotly_dark",
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font={
            "color": "#F8FAFC",
            "size": 13,
        },
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
        height=height,
        legend=dict(
            orientation="h",
            y=1.08,
            x=0,
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
    )

    fig.update_yaxes(
        gridcolor="#334155",
        zeroline=False,
    )

    return fig


# ==========================================================
# YEARLY TREND
# ==========================================================

def yearly_trend_chart(df):

    if df.empty:
        return None

    yearly = (
        df.groupby("year")
        .size()
        .reset_index(name="Incidents")
    )

    fig = px.line(
        yearly,
        x="year",
        y="Incidents",
        markers=True,
    )

    fig.update_traces(
        line=dict(
            color="#3B82F6",
            width=4,
        ),
        marker=dict(
            size=8,
        ),
    )

    return _apply_dark_theme(
        fig,
        "Year-wise Paper Leak Trend",
    )


# ==========================================================
# GOVERNMENT COMPARISON
# ==========================================================

# def government_comparison_chart(df):

#     gov = government_chart_data(df)

#     if gov.empty:
#         return None

#     fig = go.Figure()

#     fig.add_trace(
#         go.Bar(
#             name="Incidents",
#             x=gov["government"],
#             y=gov["incidents"],
#             marker_color="#3B82F6",
#             text=gov["incidents"],
#             textposition="outside",
#         )
#     )

#     fig.update_yaxes(
#         title="Incidents"
#     )

#     return _apply_dark_theme(
#         fig,
#         "Paper Leak Incidents by Government",
#     )


def government_comparison_chart(df):

    gov = government_chart_data(df)

    if gov.empty:
        return None

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Incidents",
            x=gov["government"],
            y=gov["incidents"],
            text=gov["incidents"],
            textposition="outside",
        )
    )

    fig.add_trace(
        go.Bar(
            name="Arrests",
            x=gov["government"],
            y=gov["arrests"],
            text=gov["arrests"],
            textposition="outside",
        )
    )

    fig.add_trace(
        go.Bar(
            name="Convictions",
            x=gov["government"],
            y=gov["convictions"],
            text=gov["convictions"],
            textposition="outside",
        )
    )

    fig.update_layout(
        barmode="group"
    )

    return _apply_dark_theme(
        fig,
        "Government Comparison",
        height=500,
    )


def government_aspirants_chart(df):
    """
    Compare the number of affected aspirants under each government.
    """

    gov = government_chart_data(df)

    if gov.empty:
        return None

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=gov["government"],
            y=gov["aspirants"],
            text=[f"{int(x):,}" for x in gov["aspirants"]],
            textposition="outside",
            marker_color="#F59E0B",
            name="Aspirants Affected",
        )
    )

    fig.update_yaxes(title="Aspirants")

    return _apply_dark_theme(
        fig,
        "Aspirants Affected by Government",
        height=450,
    )


import plotly.express as px


def state_incidents_chart(df):
    """
    Top 10 states by paper leak incidents.
    """

    if df.empty:
        return None

    chart_df = (
        df.groupby("state")["incident_count"]
        .sum()
        .reset_index()
        .sort_values("incident_count", ascending=False)
        .head(10)
    )

    fig = px.bar(
        chart_df,
        x="incident_count",
        y="state",
        orientation="h",
        text="incident_count",
        color="incident_count",
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        title="Top 10 States by Paper Leak Incidents",
        xaxis_title="Number of Incidents",
        yaxis_title="",
        coloraxis_showscale=False,
        height=500,
        yaxis=dict(categoryorder="total ascending"),
    )

    fig.update_traces(textposition="outside")

    return _apply_dark_theme(fig, "")


def state_aspirants_chart(df):
    """
    Top 10 states by aspirants affected.
    """

    if df.empty:
        return None

    chart_df = (
        df.groupby("state")["aspirants_affected"]
        .sum()
        .fillna(0)
        .reset_index()
        .sort_values("aspirants_affected", ascending=False)
        .head(10)
    )

    fig = px.bar(
        chart_df,
        x="aspirants_affected",
        y="state",
        orientation="h",
        text="aspirants_affected",
        color="aspirants_affected",
        color_continuous_scale="Oranges",
    )

    fig.update_layout(
        title="Top 10 States by Aspirants Affected",
        xaxis_title="Aspirants",
        yaxis_title="",
        coloraxis_showscale=False,
        height=500,
        yaxis=dict(categoryorder="total ascending"),
    )

    fig.update_traces(textposition="outside")

    return _apply_dark_theme(fig, "")

def exam_category_chart(df):
    """
    Top 10 exams with the highest number of paper leak incidents.
    """

    if df.empty:
        return None

    chart_df = (
        df.groupby("exam_category")
        .agg(
            incidents=("incident_id", "count"),
            aspirants=("aspirants_affected", "sum"),
        )
        .fillna(0)
        .sort_values("incidents", ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        chart_df,
        x="incidents",
        y="exam_category",
        orientation="h",
        color="incidents",
        text="incidents",
        color_continuous_scale="Viridis",
        hover_data={
            "aspirants": ":,",
        },
    )

    fig.update_layout(
        title="Top Exam Categories by Paper Leak Incidents",
        xaxis_title="Incidents",
        yaxis_title="",
        height=550,
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),
    )

    fig.update_traces(textposition="outside")

    return _apply_dark_theme(fig, "")


def conducting_body_category_chart(df):
    """
    Paper leak incidents by conducting body category.
    """

    if df.empty:
        return None

    chart_df = (
        df.groupby("conducting_body_category")
        .agg(
            incidents=("incident_id", "count"),
            aspirants=("aspirants_affected", "sum"),
            arrests=("arrests", "sum"),
            convictions=("convictions", "sum"),
        )
        .fillna(0)
        .reset_index()
        .sort_values("incidents", ascending=False)
    )

    fig = px.bar(
        chart_df,
        x="conducting_body_category",
        y="incidents",
        color="incidents",
        text="incidents",
        color_continuous_scale="Blues",
        hover_data={
            "aspirants": ":,",
            "arrests": True,
            "convictions": True,
        },
    )

    fig.update_layout(
        title="Paper Leak Incidents by Conducting Body Category",
        xaxis_title="",
        yaxis_title="Incidents",
        coloraxis_showscale=False,
        height=500,
    )

    fig.update_traces(textposition="outside")

    return _apply_dark_theme(fig, "")

def body_type_chart(df):
    """
    Paper leak incidents by body type.
    """

    if df.empty:
        return None

    chart_df = (
        df.groupby("body_type")
        .agg(
            incidents=("incident_id", "count"),
            aspirants=("aspirants_affected", "sum"),
            arrests=("arrests", "sum"),
            convictions=("convictions", "sum"),
        )
        .fillna(0)
        .reset_index()
        .sort_values("incidents", ascending=False)
    )

    fig = px.pie(
        chart_df,
        names="body_type",
        values="incidents",
        hole=0.55,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    fig.update_layout(
        title="Incidents by Body Type",
        height=500,
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font=dict(color="white"),
    )

    return fig


def conducting_body_treemap(df):
    """
    Treemap of paper leak incidents by conducting body category.
    Rectangle Size  -> Number of incidents
    Rectangle Color -> Aspirants affected
    """

    if df.empty:
        return None

    chart_df = (
        df.groupby("conducting_body_category")
        .agg(
            incidents=("incident_id", "count"),
            aspirants=("aspirants_affected", "sum"),
            arrests=("arrests", "sum"),
            convictions=("convictions", "sum"),
            deaths=("linked_deaths", "sum"),
        )
        .fillna(0)
        .reset_index()
    )

    fig = px.treemap(
        chart_df,
        path=["conducting_body_category"],
        values="incidents",
        color="aspirants",
        color_continuous_scale="Reds",
        hover_data={
            "incidents": True,
            "aspirants": ":,",
            "arrests": True,
            "convictions": True,
            "deaths": True,
        },
    )

    fig.update_layout(
        title="Paper Leak Incidents by Conducting Body Category",
        margin=dict(t=50, l=10, r=10, b=10),
        height=550,
        coloraxis_colorbar=dict(
            title="Aspirants Affected"
        ),
    )

    fig.update_traces(
        textinfo="label+value+percent root",
        root_color="#0F172A",
    )

    return _apply_dark_theme(fig, "")




import plotly.express as px
import streamlit as st


def state_wise_chart(state_df):
    fig = px.bar(
        state_df,
        x="incidents",
        y="state",
        orientation="h",
        text="incidents",
        color="incidents",
        color_continuous_scale="Blues",
        custom_data=[
            "aspirants",
            "arrests",
            "convictions"
        ],
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
        yaxis=dict(title=""),
        xaxis=dict(title="Incidents"),
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="""
    <b>%{y}</b><br><br>

    📄 Incidents: %{x}<br>
    👥 Aspirants: %{customdata[0]:,.0f}<br>
    🚔 Arrests: %{customdata[1]}<br>
    ⚖️ Convictions: %{customdata[2]}

    <extra></extra>
    """
    )

    fig.update_yaxes(categoryorder="total ascending")

    st.plotly_chart(fig, use_container_width=True)