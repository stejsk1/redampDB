import psycopg2
import pandas as pd
import numpy as np
import itertools
from utilities import convert_datetimetostrf, get_ipv4_address
from file_operations import compare_dataframes
import concurrent.futures


def connect_to_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="redamp",
        host="localhost",
        port="5432",
    )
    return conn


def create_table_if_not_exists(conn, cur):
    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS BASE (
            base_id SERIAL PRIMARY KEY,
            Source VARCHAR(20),
            IP VARCHAR(50),
            URL TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS URLHAUS (
            ID SERIAL PRIMARY KEY,
            base_id INTEGER,
            id_incident INTEGER,
            DateAdded TIMESTAMP,
            URL TEXT,
            URL_Status VARCHAR(20),
            Last_Online TIMESTAMP,
            Threat VARCHAR(20),
            Tags VARCHAR(500),
            URLhaus_Link VARCHAR(500),
            Reporter VARCHAR(100),
            FOREIGN KEY (base_id) REFERENCES BASE(base_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ALIENVAULT (
            ID SERIAL PRIMARY KEY,
            base_id INTEGER,
            IP VARCHAR(50),
            Risk INTEGER,
            Reliability INTEGER,
            Activity VARCHAR(50),
            Country VARCHAR(50),
            City VARCHAR(50),
            Latitude FLOAT,
            Longitude FLOAT,
            Occurrences INTEGER,
            FOREIGN KEY (base_id) REFERENCES BASE(base_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS OPENPHISH (
            ID SERIAL PRIMARY KEY,
            base_id INTEGER,
            URL TEXT,
            FOREIGN KEY (base_id) REFERENCES BASE(base_id)
        )
        """,
    ]
    index_queries = [
        """
        CREATE INDEX IF NOT EXISTS idx_urlhaus_base_id ON URLHAUS (base_id)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_alienvault_base_id ON ALIENVAULT (base_id)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_openphish_base_id ON OPENPHISH (base_id)
        """,
    ]

    for query in table_queries:
        cur.execute(query)

    for query in index_queries:
        cur.execute(query)

    conn.commit()


def fetchtable(cur, table_name):
    cur.execute(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';"
    )
    column_names = [result[0] for result in cur.fetchall()]
    columns_str = ", ".join(column_names)
    query_data = f"SELECT {columns_str} FROM {table_name};"
    cur.execute(query_data)
    table_data = pd.DataFrame(cur.fetchall(), columns=column_names)
    return table_data


def update_table(conn, cur, table_name, col_names, csv_status=None, url_csv_df=None):
    if csv_status:
        base = "base"

        if table_name + ".csv" == "urlhaus.csv":
            url_csv_df = pd.read_csv(
                table_name + ".csv",
                names=col_names[table_name],
                skiprows=9,
                sep=",",
                engine="python",
            )

            """ url_csv_df["last_online"] = pd.to_datetime(
                url_csv_df["last_online"].apply(convert_datetimetostrf), errors="coerce"
            )
            url_csv_df["dateadded"] = pd.to_datetime(
                url_csv_df["dateadded"].apply(convert_datetimetostrf), errors="coerce"
            ) """

            url_csv_df["last_online"] = pd.to_datetime(
                url_csv_df["last_online"], errors="coerce"
            )
            url_csv_df["last_online"] = np.where(
                ~url_csv_df["last_online"].isnull(),
                url_csv_df["last_online"].dt.strftime("%Y-%m-%d %H:%M:%S"),
                np.datetime64("NaT"),
            )

            url_csv_df["dateadded"] = pd.to_datetime(
                url_csv_df["dateadded"], errors="coerce"
            )
            url_csv_df["dateadded"] = np.where(
                ~url_csv_df["dateadded"].isnull(),
                url_csv_df["dateadded"].dt.strftime("%Y-%m-%d %H:%M:%S"),
                np.datetime64("NaT"),
            )

            main_column = "url"

        elif table_name + ".csv" == "alienvault.csv":
            url_csv_df = pd.read_csv(
                table_name + ".csv",
                names=col_names[table_name],
                sep="#|,",
                engine="python",
            )

            url_csv_df["risk"] = np.where(
                np.isnan(url_csv_df["risk"]), None, url_csv_df["risk"].astype(int)
            )
            url_csv_df["reliability"] = np.where(
                np.isnan(url_csv_df["reliability"]),
                None,
                url_csv_df["reliability"].astype(int),
            )
            url_csv_df["occurrences"] = np.where(
                np.isnan(url_csv_df["occurrences"]),
                None,
                url_csv_df["occurrences"].astype(int),
            )

            main_column = "ip"

        elif table_name + ".csv" == "openphish.csv":
            with open(table_name + ".csv", "r") as file:
                lines = file.readlines()

            data = [line.strip() for line in lines]
            url_csv_df = pd.DataFrame(data, columns=col_names[table_name])

            main_column = "url"

        table_data = fetchtable(cur, table_name)
        url_csv_df = compare_dataframes(main_column, table_data, url_csv_df)

        if table_name != "alienvault":
            error_log = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(
                    get_ipv4_address,
                    url_csv_df["url"].tolist(),
                    itertools.repeat(error_log),
                )
            url_csv_df["ip"] = list(results)
            with open("log.txt", "a", encoding="cp1250") as f:
                f.writelines(error_log)

        else:
            url_csv_df["url"] = None

        url_csv_df["ip"] = np.where(
            url_csv_df["ip"].apply(isinstance, args=(str,)), url_csv_df["ip"], None
        )
        url_csv_df["url"] = np.where(
            url_csv_df["url"].apply(isinstance, args=(str,)), url_csv_df["url"], None
        )

        url_csv_df["source"] = table_name
        update_table(conn, cur, base, col_names, url_csv_df=url_csv_df)

    sql_query = "INSERT INTO {} ({}) VALUES ({})".format(
        table_name,
        ", ".join(col_names[table_name]),
        ", ".join(["%s"] * len(col_names[table_name])),
    )
    values = [
        url_csv_df[column].replace({np.NaN: None}) for column in col_names[table_name]
    ]

    cur.executemany(sql_query, zip(*values))
    conn.commit()

    if csv_status:
        update_query = f"""
        UPDATE {table_name}
        SET base_id = BASE.base_id
        FROM BASE
        WHERE {table_name}.base_id IS NULL AND {table_name}.{main_column} = BASE.{main_column};
        """

        cur.execute(update_query)
        conn.commit()
