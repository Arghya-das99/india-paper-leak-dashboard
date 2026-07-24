import pandas as pd
import streamlit as st



@st.cache_data(show_spinner=False)
def load_data():
    """
    Load the paper leaks dataset.
    The original CSV is NEVER modified.
    Additional columns are created only in memory.
    """

    DATA_PATH = "data/paper_leaks.csv"
    try:
        df = pd.read_csv(DATA_PATH, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(DATA_PATH, encoding="cp1252")

    # -----------------------------
    # Basic cleanup
    # -----------------------------
    df.columns = df.columns.str.strip()

    # Remove duplicate records
    
    print("Rows before drop_duplicates:", len(df))

    df = df.drop_duplicates()

    print("Rows after drop_duplicates:", len(df))

    # -----------------------------
    # Date Processing
    # -----------------------------
    df["date"] = pd.to_datetime(
    df["date"],
    dayfirst=True,
    errors="coerce"
    )

    df["year"] = df["date"].dt.year

    df["month"] = df["date"].dt.month_name()

    # -----------------------------
    # Government Classification
    # -----------------------------
    def government(year):
        if pd.isna(year):
            return "Unknown"

        year = int(year)

        if 2004 <= year < 2014:
            return "UPA"
        elif year >= 2014:
            return "NDA"

        return "Unknown"

    df["government"] = df["year"].apply(government)

    # -----------------------------
    # Government Term
    # -----------------------------
    def government_term(year):
        if pd.isna(year):
            return "Unknown"

        year = int(year)

        if 2004 <= year <= 2008:
            return "UPA I"

        elif 2009 <= year <= 2013:
            return "UPA II"

        elif 2014 <= year <= 2018:
            return "NDA I"

        elif 2019 <= year <= 2023:
            return "NDA II"

        elif 2024 <= year <= 2026:
            return "NDA III"

        return "Unknown"

    df["government_term"] = df["year"].apply(government_term)

    # -----------------------------
    # Numeric Columns
    # -----------------------------
    numeric_columns = [
        "arrests",
        "convictions",
        "aspirants_affected",
        "linked_deaths",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # -----------------------------
    # Helper Columns
    # -----------------------------
    df["has_arrests"] = df["arrests"].fillna(0) > 0

    df["has_convictions"] = df["convictions"].fillna(0) > 0

    df["has_deaths"] = df["linked_deaths"].fillna(0) > 0

    df["incident_count"] = 1

    print(df["state"].value_counts(dropna=False))

    return df


