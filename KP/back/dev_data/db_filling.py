import os
import pandas as pd
from sqlalchemy import create_engine


def main():
    engine = create_engine("postgresql://tournamentdb_owner:n7OlDfCm1SLV@ep-soft-dawn-a5fverwq.us-east-2.aws.neon.tech/tournamentdb?sslmode=require")
    for filename in sorted(os.listdir("dev_data/tables"), key=lambda x: int(x[0])):
        df = pd.read_csv(f"dev_data/tables/{filename}")
        table_name = filename.replace(".csv", "").split("-")[-1]
        df.to_sql(table_name, engine, if_exists="append", index=False)


if __name__ == "__main__":
    main()
