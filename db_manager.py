import sqlite3
import pandas as pd
from datetime import datetime


class TreasuryDatabaseManager:
    """
    A class to manage the SQLite database for treasury data.
    It handles creating tables, appending data, and reading data.
    """

    def __init__(self, db_name="treasury_data.db"):
        """
        Initializes the database manager and connects to the SQLite database.
        :param db_name: Name of the SQLite database file.
        """
        self.conn = sqlite3.connect(db_name)

    def add_timestamp(self, df):
        """
        Adds a timestamp column to a DataFrame.
        :param df: DataFrame to which the timestamp will be added.
        :return: DataFrame with timestamp column.
        """
        df['timestamp'] = datetime.now().strftime("%Y-%m-%d")
        return df

    def write_data(self, df, table_name):
        """
        Writes data to a specified table in the database. Appends data to existing table.
        :param df: DataFrame containing the data to be written.
        :param table_name: Name of the table in the database.
        """
        df = self.add_timestamp(df)
        df.to_sql(table_name, self.conn, if_exists='append', index=False)

    def read_data(self, table_name, date=None):
        """
        Reads data from a specified table. Can optionally filter data by a specific date.
        :param table_name: Name of the table to read data from.
        :param date: Specific date to filter data (format: 'YYYY-MM-DD').
        :return: DataFrame with the read data.
        """
        query = f"SELECT * FROM {table_name}"
        if date:
            query += f" WHERE timestamp = '{date}'"
        return pd.read_sql_query(query, self.conn)

    def close(self):
        """
        Closes the connection to the SQLite database.
        """
        self.conn.close()


if __name__ == '__main__':
    # Example usage:
    # db_manager = TreasuryDatabaseManager()
    # db_manager.write_data(df_bills, "bills")  # Assuming df_bills is a DataFrame you want to write
    # db_manager.write_data(df_notes, "notes")  # Repeat for other DataFrames
    # ...
    # df_bills_nov12 = db_manager.read_data("bills", "2023-11-12")  # Reading data for a specific date
    # db_manager.close()
    pass
