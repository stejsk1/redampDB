import socket
import requests
import os
import datetime
import time
import pandas as pd


class FileHandler:
    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name

    @staticmethod
    def is_internet_available():
        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            pass
        return False

    def download_file(self):
        current_time = datetime.datetime.now()
        csv_data_dir = "csv_data"
        log_dir = "logs_data"

        if not os.path.exists(csv_data_dir):
            os.makedirs(csv_data_dir)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_path = os.path.join(csv_data_dir, self.file_name)
        logs_path = os.path.join(log_dir, "log.txt")

        while True:
            if os.path.isfile(file_path):
                with open(logs_path, "a", encoding="cp1250") as f:
                    f.write(f"{current_time}: The file {file_path} already exists.\n")

                if not self.is_internet_available():
                    with open(logs_path, "a", encoding="cp1250") as f:
                        f.write(
                            f"{current_time}: The file {self.file_name} was not downloaded from the address {self.url}. Internet is not available.\n"
                        )
                    time.sleep(10)
                else:
                    response = requests.get(self.url)
                    new_file_path = os.path.join(csv_data_dir, self.file_name + "_new")
                    with open(new_file_path, "wb") as f:
                        f.write(response.content)

                    if self.compare_files(file_path, new_file_path):
                        with open(logs_path, "a", encoding="cp1250") as f:
                            f.write(
                                f"{current_time}: The file {file_path} already exists on disk and is up-to-date.\n"
                            )
                        os.remove(file_path)
                        os.rename(new_file_path, file_path)
                        return "up-to-date"
                    else:
                        with open(logs_path, "a", encoding="cp1250") as f:
                            f.write(
                                f"{current_time}: The file {file_path} already exists on disk and has been restored to the current version.\n"
                            )
                        os.remove(file_path)
                        os.rename(new_file_path, file_path)
                        return "updated"
            else:
                if not self.is_internet_available():
                    with open(logs_path, "a", encoding="cp1250") as f:
                        f.write(
                            f"{current_time}: The file {self.file_name} was not downloaded from the address {self.url}. Internet is not available.\n"
                        )
                    time.sleep(10)
                else:
                    response = requests.get(self.url)

                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    with open(logs_path, "a", encoding="cp1250") as f:
                        f.write(
                            f"{current_time}: The file {file_path} was downloaded from the address {self.url}.\n"
                        )
                    return "downloaded"

    @staticmethod
    def compare_files(file1, file2):
        with open(file1, "r") as f1:
            content1 = f1.read()
        with open(file2, "r") as f2:
            content2 = f2.read()

        if content1 == content2:
            return True
        else:
            return False

    def compare_dataframes(main_column, df1, df2):
        existing_urls = set(df1[main_column])
        diff_rows = df2[~df2[main_column].isin(existing_urls)]
        diff_df = pd.DataFrame(diff_rows, columns=df1.columns)
        return diff_df
