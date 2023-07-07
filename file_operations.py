import socket
import requests
import os
import datetime
import time
import pandas as pd


def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80))
        return True

    except OSError:
        pass

    return False


def download_file(url, file_name):
    current_time = datetime.datetime.now()

    while True:
        if os.path.isfile(file_name):
            with open("log.txt", "a", encoding="cp1250") as f:
                f.write(f"{current_time}: The file {file_name} already exists.\n")

            if not is_internet_available():
                with open("log.txt", "a", encoding="cp1250") as f:
                    f.write(
                        f"{current_time}: The file {file_name} was not downloaded from the address {url}. Internet is not available.\n"
                    )
                time.sleep(10)

            else:
                response = requests.get(url)
                new_file_name = file_name + "_new"
                with open(new_file_name, "wb") as f:
                    f.write(response.content)

                if compare_files(file_name, new_file_name):
                    with open("log.txt", "a", encoding="cp1250") as f:
                        f.write(
                            f"{current_time}: The file {file_name} already exists on disk and is up-to-date.\n"
                        )
                    os.remove(file_name)
                    os.rename(new_file_name, file_name)
                    return "up-to-date"

                else:
                    with open("log.txt", "a", encoding="cp1250") as f:
                        f.write(
                            f"{current_time}: The file {file_name} already exists on disk and has been restored to the current version.\n"
                        )
                    os.remove(file_name)
                    os.rename(new_file_name, file_name)
                    return "updated"
        else:
            if not is_internet_available():
                with open("log.txt", "a", encoding="cp1250") as f:
                    f.write(
                        f"{current_time}: The file {file_name} was not downloaded from the address {url}. Internet is not available.\n"
                    )
                time.sleep(10)

            else:
                response = requests.get(url)

                with open(file_name, "wb") as f:
                    f.write(response.content)
                with open("log.txt", "a", encoding="cp1250") as f:
                    f.write(
                        f"{current_time}: The file {file_name} was downloaded from the address {url}.\n"
                    )
                return "downloaded"


def compare_dataframes(main_column, df1, df2):
    existing_urls = set(df1[main_column])
    diff_rows = df2[~df2[main_column].isin(existing_urls)]
    diff_df = pd.DataFrame(diff_rows, columns=df1.columns)
    return diff_df


def read_csv_file(file_path, names, skip_rows=0, separator=None):
    if not separator:
        df = pd.read_csv(file_path, names=names, skiprows=skip_rows, engine="python")

    else:
        df = pd.read_csv(
            file_path, names=names, skiprows=skip_rows, sep=separator, engine="python"
        )

    return df


def compare_files(file1, file2):
    with open(file1, "r") as f1:
        content1 = f1.read()
    with open(file2, "r") as f2:
        content2 = f2.read()

    if content1 == content2:
        return True

    else:
        return False
