import socket
import numpy as np
import pandas as pd
import datetime
from urllib.parse import urlparse


def get_ipv4_address(url):
    try:
        ip_address = socket.gethostbyname(urlparse(url).hostname)
        return ip_address

    except socket.gaierror:
        with open("log.txt", "a", encoding="cp1250") as f:
            f.write(f"Error getting an IPv4 address for a URL {url}\n")
        return np.nan


def convert_datetimetostrf(date):
    if isinstance(date, (float, int)):
        if not np.isnan(date):
            date = pd.to_datetime(date, unit="s").strftime("%Y-%m-%d %H:%M:%S")

        else:
            date = ""

    elif isinstance(date, str):
        date = pd.to_datetime(date).strftime("%Y-%m-%d %H:%M:%S")

    return date


def log_message(table_name, csv_status):
    status_messages = {
        "updated": f"The table {table_name} is {csv_status}.",
        "downloaded": f"The table {table_name} is {csv_status}.",
        "up-to-date": f"The table {table_name} is {csv_status}.",
    }

    if csv_status in status_messages:
        current_time = datetime.datetime.now()
        message = status_messages[csv_status] + "\n"
        with open("log.txt", "a", encoding="cp1250") as f:
            f.write(f"{current_time}: {message}")
        print(f"{current_time}: {message}")

    else:
        log_error_message()


def log_error_message():
    current_time = datetime.datetime.now()
    error_message = "The state of the database is corrupted."

    with open("log.txt", "a", encoding="cp1250") as f:
        f.write(f"{current_time}: {error_message}\n")
    print(f"{current_time}: {error_message}\n")
