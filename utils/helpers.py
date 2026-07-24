import streamlit as st
from utils.calculations import calculate_kpis



import streamlit as st

def dashboard_header(df):
    total_incidents = len(df)
    start_year = int(df["year"].min())
    end_year = int(df["year"].max())

    st.markdown(
        f"""
<div class="dashboard-header">

<h1 class="dashboard-title">India Paper Leak Dashboard</h1>

<p class="dashboard-subtitle">
Interactive Analysis of Paper Leaks in India
</p>

<span class="stat-chip">📄 {total_incidents} Incidents</span>
<span class="stat-chip">📅 {start_year} - {end_year}</span>
<span class="stat-chip">🏛 UPA & NDA Analysis</span>
<span class="stat-chip">📊 Interactive Dashboard</span>

</div>
""",
        unsafe_allow_html=True,
    )







def overview_kpis(df):

    kpi = calculate_kpis(df)

    html = f"""

    <div class="kpi-grid">

    <div class="kpi-card">

    <div class="kpi-icon">📄</div>

    <div class="kpi-card blue">
    Paper Leaks
    </div>

    <div class="kpi-value">
    {kpi['total_incidents']}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-icon">👥</div>

    <div class="kpi-card purple">
    Aspirants Affected
    </div>

    <div class="kpi-value">
    {kpi['total_aspirants']:,}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-icon">🚔</div>

    <div class="kpi-card orange">
    Arrests
    </div>

    <div class="kpi-value">
    {kpi['total_arrests']}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-icon">⚖️</div>

    <div class="kpi-card green">
    Convictions
    </div>

    <div class="kpi-value">
    {kpi['total_convictions']}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-icon">💀</div>

    <div class="kpi-card red">
    Linked Deaths
    </div>

    <div class="kpi-value">
    {kpi['total_deaths']}
    </div>

    </div>

    <div class="kpi-card">

    <div class="kpi-icon">❌</div>

    <div class="kpi-card amber">
    Cancelled Exams
    </div>

    <div class="kpi-value">
    {kpi['cancelled_exams']}
    </div>

    </div>

    </div>

    """

    st.markdown(html, unsafe_allow_html=True)


def government_cards(df):

    from utils.calculations import government_summary

    summary = government_summary(df)

    upa = summary.get("UPA", {})
    nda = summary.get("NDA", {})

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🟦 UPA")

        st.metric("Paper Leaks", upa.get("incidents", 0))

        st.metric("Aspirants", f"{upa.get('aspirants',0):,}")

        st.metric("Arrests", upa.get("arrests", 0))

        st.metric("Convictions", upa.get("convictions", 0))

        st.metric("Deaths", upa.get("deaths", 0))

    with col2:

        st.subheader("🟧 NDA")

        st.metric("Paper Leaks", nda.get("incidents", 0))

        st.metric("Aspirants", f"{nda.get('aspirants',0):,}")

        st.metric("Arrests", nda.get("arrests", 0))

        st.metric("Convictions", nda.get("convictions", 0))

        st.metric("Deaths", nda.get("deaths", 0))


def government_insights(df):
    """
    Display automatically generated insights for UPA vs NDA.
    """

    from utils.calculations import government_summary

    summary = government_summary(df)

    if len(summary) < 2:
        st.info("Government comparison requires data from both UPA and NDA.")
        return

    upa = summary.get("UPA", {})
    nda = summary.get("NDA", {})

    st.markdown("### 📌 Government Wise Key Insights")

    insights = []

    # -------------------------
    # Incidents
    # -------------------------
    upa_incidents = upa.get("incidents", 0)
    nda_incidents = nda.get("incidents", 0)

    if nda_incidents > upa_incidents:
        diff = nda_incidents - upa_incidents
        insights.append(
            f"• **Incidents:** NDA recorded **{nda_incidents:,}** paper leak incidents compared to **{upa_incidents:,}** under UPA (**+{diff:,}**)."
        )
    elif upa_incidents > nda_incidents:
        diff = upa_incidents - nda_incidents
        insights.append(
            f"• **Incidents:** UPA recorded **{upa_incidents:,}** paper leak incidents compared to **{nda_incidents:,}** under NDA (**+{diff:,}**)."
        )
    else:
        insights.append(
            f"• **Incidents:** Both governments recorded **{upa_incidents:,}** paper leak incidents."
        )

    # -------------------------
    # Aspirants
    # -------------------------
    upa_asp = upa.get("aspirants", 0)
    nda_asp = nda.get("aspirants", 0)

    if nda_asp > upa_asp:
        diff = nda_asp - upa_asp
        insights.append(
            f"• **Aspirants Affected:** **{nda_asp:,}** during NDA compared to **{upa_asp:,}** during UPA (**+{diff:,}**)."
        )
    elif upa_asp > nda_asp:
        diff = upa_asp - nda_asp
        insights.append(
            f"• **Aspirants Affected:** **{upa_asp:,}** during UPA compared to **{nda_asp:,}** during NDA (**+{diff:,}**)."
        )
    else:
        insights.append(
            f"• **Aspirants Affected:** Both governments affected **{upa_asp:,}** aspirants."
        )

    # -------------------------
    # Arrests
    # -------------------------
    upa_arrests = upa.get("arrests", 0)
    nda_arrests = nda.get("arrests", 0)

    if nda_arrests > upa_arrests:
        diff = nda_arrests - upa_arrests
        insights.append(
            f"• **Arrests:** NDA recorded **{nda_arrests:,}** arrests compared to **{upa_arrests:,}** under UPA (**+{diff:,}**)."
        )
    elif upa_arrests > nda_arrests:
        diff = upa_arrests - nda_arrests
        insights.append(
            f"• **Arrests:** UPA recorded **{upa_arrests:,}** arrests compared to **{nda_arrests:,}** under NDA (**+{diff:,}**)."
        )
    else:
        insights.append(
            f"• **Arrests:** Both governments recorded **{upa_arrests:,}** arrests."
        )

    # -------------------------
    # Convictions
    # -------------------------
    upa_conv = upa.get("convictions", 0)
    nda_conv = nda.get("convictions", 0)

    if nda_conv > upa_conv:
        diff = nda_conv - upa_conv
        insights.append(
            f"• **Convictions:** NDA recorded **{nda_conv:,}** convictions compared to **{upa_conv:,}** under UPA (**+{diff:,}**)."
        )
    elif upa_conv > nda_conv:
        diff = upa_conv - nda_conv
        insights.append(
            f"• **Convictions:** UPA recorded **{upa_conv:,}** convictions compared to **{nda_conv:,}** under NDA (**+{diff:,}**)."
        )
    else:
        insights.append(
            f"• **Convictions:** Both governments recorded **{upa_conv:,}** convictions."
        )

    # -------------------------
    # Deaths
    # -------------------------
    upa_deaths = upa.get("deaths", 0)
    nda_deaths = nda.get("deaths", 0)

    if nda_deaths > upa_deaths:
        diff = nda_deaths - upa_deaths
        insights.append(
            f"• **Linked Deaths:** NDA reported **{nda_deaths:,}** linked deaths compared to **{upa_deaths:,}** under UPA (**+{diff:,}**)."
        )
    elif upa_deaths > nda_deaths:
        diff = upa_deaths - nda_deaths
        insights.append(
            f"• **Linked Deaths:** UPA reported **{upa_deaths:,}** linked deaths compared to **{nda_deaths:,}** under NDA (**+{diff:,}**)."
        )
    else:
        insights.append(
            f"• **Linked Deaths:** Both governments reported **{upa_deaths:,}** linked deaths."
        )

    # -------------------------
    # Cancelled Exams
    # -------------------------
    upa_cancelled = upa.get("cancelled", 0)
    nda_cancelled = nda.get("cancelled", 0)

    if nda_cancelled > upa_cancelled:
        diff = nda_cancelled - upa_cancelled
        insights.append(
            f"• **Cancelled Exams:** **{nda_cancelled:,}** exams were cancelled during NDA compared to **{upa_cancelled:,}** during UPA (**+{diff:,}**)."
        )
    elif upa_cancelled > nda_cancelled:
        diff = upa_cancelled - nda_cancelled
        insights.append(
            f"• **Cancelled Exams:** **{upa_cancelled:,}** exams were cancelled during UPA compared to **{nda_cancelled:,}** during NDA (**+{diff:,}**)."
        )
    else:
        insights.append(
            f"• **Cancelled Exams:** Both governments cancelled **{upa_cancelled:,}** exams."
        )

    for insight in insights:
        st.info(insight)



import streamlit as st


def conducting_body_card(rank, row):

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    medal = medals.get(rank, f"#{rank}")

    st.markdown(f"""
<div class="body-card">

<div class="body-title">
{medal} {row["conducting_body_category"]}
</div>

<div class="body-text">

📄 <b>Incidents:</b> {int(row["incidents"])} ({row["percentage"]}%)
👥 <b>Aspirants:</b> {int(row["aspirants"]):,}<br>
🚔 <b>Arrests:</b> {int(row["arrests"])}<br>
⚖️ <b>Convictions:</b> {int(row["convictions"])}

</div>

</div>
""", unsafe_allow_html=True)
    




import pandas as pd
import streamlit as st


def timeline_card(row):
    aspirants = (
        f"{int(row['aspirants_affected']):,}"
        if pd.notna(row["aspirants_affected"])
        else "N/A"
    )

    deaths = (
        str(int(row["linked_deaths"]))
        if pd.notna(row["linked_deaths"]) and row["linked_deaths"] > 0
        else "None Reported"
    )

    st.markdown(
        f"""
<div class="timeline-card">
<div class="timeline-date">{row['date']}</div>
<div class="timeline-title">{row['exam_name']}</div>
<div class="timeline-body">
<b>📍 State:</b> {row['state']}<br>
<b>🏛 Conducting Body:</b> {row['conducting_body_category']}<br>
<b>👥 Aspirants Affected:</b> {aspirants}<br>
<b>🕊️ Linked Deaths:</b> {deaths}
</div>
</div>
""",
        unsafe_allow_html=True,
    )