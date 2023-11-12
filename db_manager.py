import sqlite3
import pandas as pd

class TreasuryDatabaseManager:
    def __init__(self, db_name="treasury_data.db"):
        self.conn = sqlite3.connect(db_name)

    def create_table(self, df, table_name):
        # 将DataFrame的列类型转换为SQLite兼容的类型
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

    def write_data(self, df, table_name):
        # 写入数据到表
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)

    def read_data(self, table_name):
        # 从表中读取数据
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql_query(query, self.conn)

    def close(self):
        # 关闭数据库连接
        self.conn.close()
