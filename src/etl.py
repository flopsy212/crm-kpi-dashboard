from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "db"

RAW_CSV_PATH = DATA_DIR / "raw_crm_opportunities.csv"
PROCESSED_CSV_PATH = DATA_DIR / "processed_crm_opportunities.csv"
DB_PATH = DB_DIR / "crm.db"

TABLE_NAME = "opportunities"


def load_raw_data():
    """CSVを読み込む"""
    return pd.read_csv(RAW_CSV_PATH)


def transform_data(df):
    """分析しやすい形にデータを整形する"""

    # 元データを壊さないようにコピーする
    transformed = df.copy()

    # 日付をdatetime型に変換
    transformed["created_date"] = pd.to_datetime(transformed["created_date"])
    transformed["close_date"] = pd.to_datetime(transformed["close_date"])

    # 金額を数値型に変換
    transformed["amount"] = pd.to_numeric(transformed["amount"], errors="coerce").fillna(0)

    # 月別集計用のカラムを追加
    transformed["close_month"] = transformed["close_date"].dt.strftime("%Y-%m")

    # 受注・失注・完了フラグを追加
    transformed["is_won"] = (transformed["stage"] == "Won").astype(int)
    transformed["is_lost"] = (transformed["stage"] == "Lost").astype(int)
    transformed["is_closed"] = transformed["stage"].isin(["Won", "Lost"]).astype(int)

    # 商談作成日からクローズ日までの日数
    transformed["lead_time_days"] = (
        transformed["close_date"] - transformed["created_date"]
    ).dt.days

    return transformed


def save_to_csv(df):
    """整形後CSVを保存する"""
    df.to_csv(PROCESSED_CSV_PATH, index=False, encoding="utf-8-sig")


def save_to_sqlite(df):
    """整形後データをSQLiteに保存する"""

    DB_DIR.mkdir(exist_ok=True)

    # SQLiteに入れやすいように日付を文字列に戻す
    db_df = df.copy()
    db_df["created_date"] = db_df["created_date"].dt.strftime("%Y-%m-%d")
    db_df["close_date"] = db_df["close_date"].dt.strftime("%Y-%m-%d")

    with sqlite3.connect(DB_PATH) as conn:
        db_df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

        # 集計でよく使う列にインデックスを作る
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_opportunities_close_month "
            "ON opportunities(close_month)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_opportunities_owner "
            "ON opportunities(owner)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_opportunities_stage "
            "ON opportunities(stage)"
        )


def main():
    raw_df = load_raw_data()
    transformed_df = transform_data(raw_df)

    save_to_csv(transformed_df)
    save_to_sqlite(transformed_df)

    print(f"元データ件数: {len(raw_df)}")
    print(f"整形後CSVを作成しました: {PROCESSED_CSV_PATH}")
    print(f"SQLite DBを作成しました: {DB_PATH}")


if __name__ == "__main__":
    main()