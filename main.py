import multiprocessing
import os
import traceback
import sys
from utilities import NetworkHandler
from file_operations import FileHandler
from database import DatabaseHandler
from authentication import Authenticator
from line_profiler import LineProfiler


class DataCollector:
    def __init__(self):
        self.authenticator = Authenticator()
        self.urls = [
            (),
            ("https://urlhaus.abuse.ch/downloads/csv_recent/", "urlhaus.csv"),
            ("http://reputation.alienvault.com/reputation.data", "alienvault.csv"),
            ("https://openphish.com/feed.txt", "openphish.csv"),
        ]

        self.table_names = ["base", "urlhaus", "alienvault", "openphish"]

        self.col_names = {
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

        self.data_handler = DatabaseHandler(
            dbname="postgres",
            user="postgres",
            password="redamp",
            host="localhost",
            port="5432",
        )

    def run(self):
        if not self.authenticator.authenticate():
            return

        DatabaseHandler.create_table_if_not_exists(self.data_handler)
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            for table_name in self.table_names:
                if table_name == "base":
                    continue

                for key, value in self.col_names.items():
                    if table_name == key:
                        url = self.urls[list(self.col_names.keys()).index(key)]
                        file_handler = FileHandler(url[0], url[1])
                        csv_status = pool.starmap(file_handler.download_file, [()])[0]

                        if csv_status == "updated" or csv_status == "downloaded":
                            self.data_handler.update_table(
                                table_name,
                                self.col_names,
                                csv_status=csv_status,
                            )

                        network_handler = NetworkHandler()
                        network_handler.log_message(table_name, csv_status)


def exception_hook(exctype, value, tb):
    log_dir = "logs_data"
    logs_path = os.path.join(log_dir, "error_log.txt")
    with open(logs_path, "a") as f:
        f.write(f"Type of exception: {exctype}\n")
        f.write(f"Value: {value}\n")
        traceback.print_tb(tb, file=f)
        f.write("\n")
    print("Type of exception: ", exctype)
    print("Value: ", value)
    print("Traceback: ", "".join(traceback.format_tb(tb)))
    sys.exit()


sys.excepthook = exception_hook

if __name__ == "__main__":
    collector = DataCollector()

    profiler = LineProfiler()
    profiler.add_function(DataCollector.run)
    profiler.enable_by_count()
    run_data_collector_wrapper = profiler(collector.run)

    run_data_collector_wrapper()

    log_dir = "logs_data"
    logs_path = os.path.join(log_dir, "profiling_results.txt")
    with open(logs_path, "w") as f:
        profiler.print_stats(stream=f)
