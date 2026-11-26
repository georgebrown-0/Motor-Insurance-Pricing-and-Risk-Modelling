from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import URL, create_engine

database_url = URL.create(
    drivername="mysql+pymysql",
    username="motor_user",
    password=getpass("MySQL password for motor_user: "),
    host="127.0.0.1",
    port=3307,
    database="motor_insurance",
)

engine = create_engine(database_url)

sql_path = Path(__file__).resolve().parents[1] / "sql" / "extract_severity.sql"
query = sql_path.read_text(encoding="utf-8")

with engine.connect() as connection:
    severity = pd.read_sql_query(query, connection)

print("Dataset shape:", severity.shape)
print(severity.loc[severity["IDpol"] == 424, ["IDpol", "ClaimAmount"]])