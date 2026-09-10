import csv
from pathlib import Path
def load_rules() -> list[str]:
    path = Path("data/historical_rules.csv")
    with path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row["description"] for row in reader]
