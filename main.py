import pandas as pd
import multiprocessing
from database import create_table_if_not_exists, connect_to_database, update_table
from file_operations import download_file
from authentication import authenticate_user
from utilities import log_message


def main():
    authenticated = authenticate_user()

    if authenticated:
        conn = connect_to_database()
        cur = conn.cursor()
        create_table_if_not_exists(conn, cur)

        urlhaus_url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
        alienvault_url = "http://reputation.alienvault.com/reputation.data"
        openphish_url = "https://openphish.com/feed.txt"

        urls = [
            (),
            (urlhaus_url, "urlhaus.csv"),
            (alienvault_url, "alienvault.csv"),
            (openphish_url, "openphish.csv"),
        ]

        table_names = ["base", "urlhaus", "alienvault", "openphish"]

        col_names = {
            "base": ["source", "ip", "url"],
            "urlhaus": [
                "id_incident",
                "dateadded",
                "url",
                "url_status",
                "last_online",
                "threat",
                "tags",
                "urlhaus_link",
                "reporter",
            ],
            "alienvault": [
                "ip",
                "risk",
                "reliability",
                "activity",
                "country",
                "city",
                "latitude",
                "longitude",
                "occurrences",
            ],
            "openphish": ["url"],
        }

        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            for table_name in table_names:
                if table_name == "base":
                    continue

                for key, value in col_names.items():
                    if table_name == key:
                        url = urls[list(col_names.keys()).index(key)]
                        csv_status = pool.starmap(download_file, [url])[0]

                        if csv_status == "updated" or csv_status == "downloaded":
                            update_table(conn, cur, table_name, col_names, csv_status)

                        log_message(table_name, csv_status)
    else:
        print("Authentication failed. Terminating program.")
        return


if __name__ == "__main__":
    main()
