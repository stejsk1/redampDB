import socket
import numpy as np
import pandas as pd
import datetime
import os
from urllib.parse import urlparse


class NetworkHandler:
    @staticmethod
    def get_ipv4_address(url, error_log):
        try:
            ip_address = socket.gethostbyname(urlparse(url).hostname)
            return ip_address
        except socket.gaierror:
            error_log.append(f"Error getting an IPv4 address for a URL {url}\n")
            return np.nan

    @staticmethod
    def log_message(table_name, csv_status):
        log_dir = "logs_data"
        logs_path = os.path.join(log_dir, "log.txt")
        status_messages = {
            "updated": f"The table {table_name} is {csv_status}.",
            "downloaded": f"The table {table_name} is {csv_status}.",
            "up-to-date": f"The table {table_name} is {csv_status}.",
        }

        if csv_status in status_messages:
            current_time = datetime.datetime.now()
            message = status_messages[csv_status] + "\n"
            with open(logs_path, "a", encoding="cp1250") as f:
                f.write(f"{current_time}: {message}")
            print(f"{current_time}: {message}")
        else:
            NetworkHandler.log_error_message(logs_path)

    @staticmethod
    def log_error_message(logs_path):
        current_time = datetime.datetime.now()
        error_message = "The state of the database is corrupted."

        with open(logs_path, "a", encoding="cp1250") as f:
            f.write(f"{current_time}: {error_message}\n")
        print(f"{current_time}: {error_message}\n")
