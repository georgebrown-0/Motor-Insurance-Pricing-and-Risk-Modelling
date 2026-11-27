from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import URL, create_engine

sql_path_freq = Path(__file__).resolve().parents[1] / "sql" / "extract_frequency.sql"
query_freq = sql_path_freq.read_text(encoding="utf-8")

sql_path_sev = Path(__file__).resolve().parents[1] / "sql" / "extract_severity.sql"
query_sev = sql_path_sev.read_text(encoding="utf-8")


def load_frequency(connection):
    return pd.read_sql_query(query_freq, connection)


def load_severity(connection):
    return pd.read_sql_query(query_sev, connection)

if __name__ == "__main__":
    database_url = URL.create(
        drivername="mysql+pymysql",
        username="motor_user",
        password=getpass("MySQL password for motor_user: "),
        host="127.0.0.1",
        port=3307,
        database="motor_insurance",
    )
    engine = create_engine(database_url)

    with engine.connect() as connection:
        frequency = load_frequency(connection)
        severity = load_severity(connection)

    print("Frequency rows:", len(frequency))
    print("Frequency IDs unique:", frequency["IDpol"].is_unique)
    print("Zero-claim policies:", (frequency["ClaimNb"] == 0).sum())
    print("Severity rows:", len(severity))
    print(severity.loc[severity["IDpol"] == 424, ["IDpol", "ClaimAmount"]])
