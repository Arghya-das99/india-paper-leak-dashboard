import pandas as pd


def calculate_kpis(df):
    """
    Calculate overall dashboard KPIs.
    """

    cancelled_exams = (
        df["action_taken"]
        .fillna("")
        .str.contains("cancel", case=False)
        .sum()
    )

    return {
        "total_incidents": len(df),
        "total_aspirants": int(df["aspirants_affected"].fillna(0).sum()),
        "total_arrests": int(df["arrests"].fillna(0).sum()),
        "total_convictions": int(df["convictions"].fillna(0).sum()),
        "total_deaths": int(df["linked_deaths"].fillna(0).sum()),
        "cancelled_exams": int(cancelled_exams),
    }


def government_summary(df):
    """
    Returns government-wise summary for KPI cards.

    Output:
    {
        "UPA": {...},
        "NDA": {...}
    }
    """

    summary = (
        df.groupby("government")
        .agg(
            incidents=("incident_id", "count"),
            aspirants=("aspirants_affected", "sum"),
            arrests=("arrests", "sum"),
            convictions=("convictions", "sum"),
            deaths=("linked_deaths", "sum"),
            cancelled=(
                "action_taken",
                lambda x: x.fillna("").str.contains(
                    "cancel",
                    case=False,
                ).sum(),
            ),
        )
        .fillna(0)
    )

    return summary.to_dict("index")


def government_chart_data(df):
    """
    Returns dataframe for charts.
    """

    chart_df = (
        df.groupby("government")
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

    return chart_df


def state_summary(df):
    chart_df = (
        df[df["state"].notna()]
        .query("state != 'Unknown'")
        .copy()
    )

    summary = (
        chart_df.groupby("state")
        .agg(
            incidents=("incident_id", "count"),
            aspirants=("aspirants_affected", "sum"),
            arrests=("arrests", "sum"),
            convictions=("convictions", "sum"),
            deaths=("linked_deaths", "sum"),
        )
        .fillna(0)
        .reset_index()
        .sort_values("incidents", ascending=False)
    )

    return summary


import pandas as pd


def top_conducting_bodies(df, top_n=10):
    """
    Returns top conducting bodies ranked by paper leak incidents.
    """

    result = (
        df.groupby("conducting_body_category", as_index=False)
        .agg(
            incidents=("incident_count", "sum"),
            aspirants=("aspirants_affected", "sum"),
            arrests=("arrests", "sum"),
            convictions=("convictions", "sum"),
        )
        .sort_values("incidents", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    total_incidents = result["incidents"].sum()

    result["percentage"] = (
        result["incidents"] / total_incidents * 100
    ).round(1)

    return result


def state_wise_analytics(df, top_n=10):
    """
    Returns top states by paper leak incidents.
    """

    result = (
        df.groupby("state", as_index=False)
        .agg(
            incidents=("incident_count", "sum"),
            aspirants=("aspirants_affected", "sum"),
            arrests=("arrests", "sum"),
            convictions=("convictions", "sum"),
        )
        .sort_values("incidents", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return result


def state_insights(state_df):
    """
    Generate key insights for the state-wise analytics section.
    Excludes 'All India' from all calculations.
    """

    # Remove "All India" row
    state_only_df = state_df[
        state_df["state"].str.strip().str.lower() != "all india"
    ].copy()

    if state_only_df.empty:
        return []

    insights = []

    # 1. State with highest incidents
    top_state = state_only_df.iloc[0]

    insights.append(
        f"🏆 **{top_state['state']}** recorded the highest number of paper leak incidents (**{int(top_state['incidents'])}**)."
    )

    # 2. Top 3 states contribution
    total_incidents = state_only_df["incidents"].sum()
    top3_incidents = state_only_df.head(3)["incidents"].sum()

    top3_percentage = (top3_incidents / total_incidents) * 100

    insights.append(
        f"📊 The **Top 3 states** account for **{top3_percentage:.1f}%** of all state-wise paper leak incidents."
    )

    # 3. State affecting the highest number of aspirants
    aspirants_state = state_only_df.loc[
        state_only_df["aspirants"].idxmax()
    ]

    insights.append(
        f"👥 **{aspirants_state['state']}** affected the highest number of aspirants (**{int(aspirants_state['aspirants']):,}**)."
    )

    # 4. State with highest arrests
    arrests_state = state_only_df.loc[
        state_only_df["arrests"].idxmax()
    ]

    insights.append(
        f"🚔 **{arrests_state['state']}** recorded the highest number of arrests (**{int(arrests_state['arrests'])}**)."
    )

    # 5. State with highest convictions
    convictions_state = state_only_df.loc[
        state_only_df["convictions"].idxmax()
    ]

    insights.append(
        f"⚖️ **{convictions_state['state']}** recorded the highest number of convictions (**{int(convictions_state['convictions'])}**)."
    )

    return insights


def major_incidents_timeline(df, top_n=10):
    """
    Returns the top N major paper leak incidents based on
    aspirants affected. If aspirants are equal or missing,
    more recent incidents are prioritized.
    """

    timeline_df = (
        df.sort_values(
            by=["aspirants_affected", "date"],
            ascending=[False, False],
            na_position="last",
        )
        .head(top_n)
        .copy()
    )

    timeline_df["date"] = timeline_df["date"].dt.strftime("%d %b %Y")

    return timeline_df[
        [
            "date",
            "exam_name",
            "state",
            "conducting_body_category",
            "aspirants_affected",
            "linked_deaths",
        ]
    ]