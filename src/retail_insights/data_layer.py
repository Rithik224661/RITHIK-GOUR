import duckdb
import pandas as pd
from typing import Optional


class DataLayer:
    """Handles loading CSVs and running analytical queries via DuckDB / Pandas."""

    def __init__(self):
        self.conn = duckdb.connect(database=':memory:')

    def load_csv(self, path: str, table_name: str = 'sales') -> pd.DataFrame:
        df = pd.read_csv(path)
        self.conn.register(table_name, df)
        return df

    def register_df(self, df: pd.DataFrame, table_name: str = 'sales') -> None:
        self.conn.register(table_name, df)

    def query(self, sql: str) -> pd.DataFrame:
        return self.conn.execute(sql).df()

    def sample_top_categories(self, limit: int = 5):
        q = f"SELECT category, SUM(sales) AS total_sales FROM sales GROUP BY category ORDER BY total_sales DESC LIMIT {limit};"
        return self.query(q)

    def total_sales_by_region(self):
        q = "SELECT region, SUM(sales) AS total_sales FROM sales GROUP BY region ORDER BY total_sales DESC;"
        return self.query(q)
