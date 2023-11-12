from scraper import TreasuryDataScraper
from db_manager import TreasuryDatabaseManager

def daily_example():
    # scrape data
    scraper = TreasuryDataScraper()
    df_bills = scraper.get_df_bills()
    df_notes = scraper.get_df_notes()
    df_Bonds = scraper.get_df_Bonds()
    df_TIPS = scraper.get_df_TIPS()
    df_FRNs = scraper.get_df_FRNs()
    scraper.close_driver()

    # cache to csv
    df_bills.to_csv("treasury_cache/bills.csv", index=False)
    df_notes.to_csv("treasury_cache/notes.csv", index=False)
    df_Bonds.to_csv("treasury_cache/bonds.csv", index=False)
    df_TIPS.to_csv("treasury_cache/tips.csv", index=False)
    df_FRNs.to_csv("treasury_cache/frns.csv", index=False)

    # create database
    db_manager = TreasuryDatabaseManager()

    # create table
    db_manager.write_data(df_bills, "bills")
    db_manager.write_data(df_notes, "notes")
    db_manager.write_data(df_Bonds, "bonds")
    db_manager.write_data(df_TIPS, "tips")
    db_manager.write_data(df_FRNs, "frns")

    # read table
    df_bills_from_db = db_manager.read_data("bills")
    print(df_bills_from_db)
    df_notes_from_db = db_manager.read_data("notes")
    print(df_notes_from_db)

    # close database
    db_manager.close()

if __name__ == '__main__':
    daily_example()