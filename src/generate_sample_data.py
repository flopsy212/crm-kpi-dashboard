from datetime import date, timedelta
from pathlib import Path
import random

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_CSV_PATH = DATA_DIR / "raw_crm_opportunities.csv"


def random_date(start: date, end: date) -> date:
    days = (end - start).days
    return start + timedelta(days=random.randint(0, days))


def main():
    random.seed(42)

    DATA_DIR.mkdir(exist_ok=True)

    owners = ["Sato", "Suzuki", "Takahashi", "Tanaka", "Kawasaki"]
    industries = ["IT", "Manufacturing", "Retail", "Finance", "Healthcare"]
    regions = ["Tokyo", "Osaka", "Nagoya", "Fukuoka", "Sapporo"]
    stages = ["Lead", "Proposal", "Negotiation", "Won", "Lost"]

    rows = []

    start_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)

    for i in range(1, 301):
        stage = random.choices(
            stages,
            weights=[20, 25, 20, 25, 10],
            k=1
        )[0]

        amount = random.randint(30, 800) * 10000

        close_date = random_date(start_date, end_date)
        created_date = close_date - timedelta(days=random.randint(10, 120))

        rows.append({
            "opportunity_id": f"OPP-{i:04d}",
            "customer_name": f"Customer-{random.randint(1, 80):03d}",
            "industry": random.choice(industries),
            "region": random.choice(regions),
            "owner": random.choice(owners),
            "stage": stage,
            "amount": amount,
            "created_date": created_date.isoformat(),
            "close_date": close_date.isoformat(),
        })

    df = pd.DataFrame(rows)
    df.to_csv(RAW_CSV_PATH, index=False, encoding="utf-8-sig")

    print(f"CSVを作成しました: {RAW_CSV_PATH}")
    print(f"件数: {len(df)}")


if __name__ == "__main__":
    main()