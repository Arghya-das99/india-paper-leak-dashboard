import streamlit as st


def sidebar_filters(df):

    st.sidebar.header("🎛 Dashboard Filters")

    # -------------------------
    # Search
    # -------------------------
    search = st.sidebar.text_input(
        "🔍 Search Exam",
        placeholder="Type exam name..."
    )

    st.sidebar.divider()

    # -------------------------
    # Year
    # -------------------------
    years = sorted(df["year"].dropna().unique())

    selected_years = st.sidebar.multiselect(
        "📅 Year",
        years,
        default=years
    )

    # -------------------------
    # Government
    # -------------------------
    governments = sorted(df["government"].dropna().unique())

    selected_governments = st.sidebar.multiselect(
        "🏛 Government",
        governments,
        default=governments
    )

    # -------------------------
    # Body Type
    # -------------------------
    body_types = sorted(df["body_type"].dropna().unique())

    selected_body_types = st.sidebar.multiselect(
        "🏢 Body Type",
        body_types,
        default=body_types
    )

    # -------------------------
    # Conducting Body
    # -------------------------
    bodies = sorted(df["conducting_body"].dropna().unique())

    selected_bodies = st.sidebar.multiselect(
        "📚 Conducting Body",
        bodies,
        default=bodies
    )

    # -------------------------
    # Area
    # -------------------------
    areas = sorted(df["state"].dropna().unique())

    selected_areas = st.sidebar.multiselect(
        "📍 State",
        areas,
        default=areas
    )

    # -------------------------
    # Leak Status
    # -------------------------
    status = sorted(df["leak_status"].dropna().unique())

    selected_status = st.sidebar.multiselect(
        "📄 Leak Status",
        status,
        default=status
    )

    # -------------------------
    # Confidence
    # -------------------------
    confidence = sorted(df["confidence"].dropna().unique())

    selected_confidence = st.sidebar.multiselect(
        "✅ Confidence",
        confidence,
        default=confidence
    )

    # -------------------------
    # Apply Filters
    # -------------------------

    filtered = df[
        (df["year"].isin(selected_years))
        & (df["government"].isin(selected_governments))
        & (df["body_type"].isin(selected_body_types))
        & (df["conducting_body"].isin(selected_bodies))
        & (df["state"].isin(selected_areas))
        & (df["leak_status"].isin(selected_status))
        & (df["confidence"].isin(selected_confidence))
    ]

    if search:

        filtered = filtered[
            filtered["exam_name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.sidebar.divider()

    st.sidebar.success(
        f"Showing {len(filtered)} of {len(df)} incidents"
    )

    return filtered