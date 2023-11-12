from scraper import TreasuryDataScraper
from db_manager import TreasuryDatabaseManager

if __name__ == '__main__':

    #
    scraper = TreasuryDataScraper()
    df_bills = scraper.get_df_bills()
    df_notes = scraper.get_df_notes()
    df_Bonds = scraper.get_df_Bonds()
    df_TIPS = scraper.get_df_TIPS()
    df_FRNs = scraper.get_df_FRNs()
    scraper.close_driver()

    # create database
    db_manager = TreasuryDatabaseManager()

    # create table
    db_manager.create_table(df_bills, "bills")
    db_manager.create_table(df_notes, "notes")
    db_manager.create_table(df_Bonds, "bonds")
    db_manager.create_table(df_TIPS, "tips")
    db_manager.create_table(df_FRNs, "frns")

    #
    df_bills_from_db = db_manager.read_data("bills")
    df_notes_from_db = db_manager.read_data("notes")

    #
    db_manager.close()
