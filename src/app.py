from pathlib import Path
import sqlite3

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "crm.db"


@st.cache_data
def load_data():
    if not DB_PATH.exists():
        st.error("db/crm.db がありません。先に python src/generate_sample_data.py と python src/etl.py を実行してください。")
        st.stop()

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM opportunities", conn)

    return df


def main():
    st.set_page_config(
        page_title="CRM KPI Dashboard",
        layout="wide",
    )

    st.title("CRM KPI Dashboard")
    st.caption("CRM商談データをPython・SQLite・SQL・Streamlitで可視化するダッシュボード")

    df = load_data()

    st.sidebar.header("フィルター")

    owners = sorted(df["owner"].unique())
    stages = sorted(df["stage"].unique())
    industries = sorted(df["industry"].unique())

    selected_owners = st.sidebar.multiselect("担当者", owners, default=owners)
    selected_stages = st.sidebar.multiselect("商談ステージ", stages, default=stages)
    selected_industries = st.sidebar.multiselect("業界", industries, default=industries)

    filtered_df = df[
        df["owner"].isin(selected_owners)
        & df["stage"].isin(selected_stages)
        & df["industry"].isin(selected_industries)
    ]

    total_amount = filtered_df["amount"].sum()
    opportunity_count = len(filtered_df)

    closed_df = filtered_df[filtered_df["is_closed"] == 1]
    if len(closed_df) > 0:
        win_rate = closed_df["is_won"].sum() / len(closed_df)
    else:
        win_rate = 0

    average_amount = filtered_df["amount"].mean() if len(filtered_df) > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("売上合計", f"¥{total_amount:,.0f}")
    col2.metric("商談件数", f"{opportunity_count:,}件")
    col3.metric("受注率", f"{win_rate:.1%}")
    col4.metric("平均商談金額", f"¥{average_amount:,.0f}")

    st.divider()

    monthly_sales = (
        filtered_df.groupby("close_month", as_index=False)["amount"]
        .sum()
        .sort_values("close_month")
    )

    owner_sales = (
        filtered_df.groupby("owner", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )

    stage_amount = (
        filtered_df.groupby("stage", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        st.subheader("月別売上推移")
        st.line_chart(monthly_sales, x="close_month", y="amount")

    with right:
        st.subheader("担当者別売上")
        st.bar_chart(owner_sales, x="owner", y="amount")

    st.subheader("ステージ別商談金額")
    st.bar_chart(stage_amount, x="stage", y="amount")

    st.subheader("商談データ一覧")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
