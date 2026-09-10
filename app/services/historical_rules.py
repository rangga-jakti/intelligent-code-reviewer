import csv
from pathlib import Path


def load_rules() -> list[dict[str, str]]:
    path = Path("data/historical_rules.csv")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != ["id", "type", "description"]:
            raise ValueError(f"Invalid CSV header: {reader.fieldnames}")

        return [
            {
                "id": row["id"],
                "type": row["type"],
                "description": row["description"],
            }
            for row in reader
        ]
