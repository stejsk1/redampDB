# REDAMP
## 07/13/2023 (2)
### Refactoring, customization, reorganization
- **Refactoring:**
    - The entire project has been reorganized without altering its external behavior. 
        - This involves moving functions to class methods.
        
- **Customization:**
    - Two new directories are being created in the project.  
    The first one is `csv_data`, and the second one is `logs_data`.
        - The `csv_data` directory now contains or will contain newly downloaded CSV files upon the first execution of the program.

        - The "logs_data" directory will contain "logs.txt" and a new file called "profiling_results.txt," which includes the benchmark of the main code. 
            - You can find an example of the "profiling_results" file in the folder.  
            ***Please note that running the program will overwrite it with your values.***

- **Reorganization:**
    - The following file schema falls under code reorganization.
        - Old scheme: 
            - `main.py`
                - *def main():*
            - `utilities.py`
                - *def is_internet_available():*
                - *def get_ipv4_address(url, error_log):*
                - *def log_message(table_name, csv_status):*
                - *def log_error_message():*
            - `file_operations.py`
                - *def download_file(url, file_name):*
                - *def compare_dataframes(main_column, df1, df2):*
                - *def compare_files(file1, file2):*
            - `database.py`
                - *def connect_to_database():*
                - *def create_table_if_not_exists(conn, cur):*
                - *def fetchtable(cur, table_name):*
                - *def update_table(conn, cur, table_name, col_names, csv_status=None, url_csv_df=None):*
            - `authentication.py`
                - *def authenticate_user(max_attempts=5, cooldown_time=60):*
        - New scheme:
            - `main.py`
                - **class DataCollector:**
                    - *def \_\_init__(self):*
                    - *def run(self):*
                - **if \_\_name__ == "\_\_main__":**
            - `utilities.py`
                - **class NetworkHandler:**
                    - *def get_ipv4_address(url, error_log):*
                    - *def log_message(table_name, csv_status):*
                    - *def log_error_message(logs_path):*
            - `file_operations.py`
                - **class FileHandler:**
                    - *def \_\_init__(self, url, file_name):*
                    - *def is_internet_available():*
                    - *def download_file(self):*
                    - *def compare_dataframes(main_column, df1, df2):*
                    - *def compare_files(file1, file2):*
            - `database.py`
                - **class DatabaseHandler:**
                    - *def \_\_init__(self, dbname, user, password, host, port):*
                    - *def def create_table_if_not_exists(self):*
                    - *def fetchtable(self, table_name):*
                    - *def update_table(self, table_name, col_names, csv_status=None, url_csv_df=None):*
            - `authentication.py`
                - **class Authenticator:**
                    - *def \_\_init__(self, username="postgres", password="redamp", max_attempts=5, cooldown_time=60):*
                    - *def authenticate(self):*

## 07/13/2023 (1)
### Optimization, migration, customization
- **Optimization**:  
    - Upgrading the code to make more use of the numpy library and pandas to increase code efficiency.
        - Initial tests record total time: 2 minutes 37 seconds.
        - Final tests record total time: 41.8579 s
            - Depending on HW.
    - Correction of errors in code.
- **Migration**:
    - Code modification:
        - Switching from outdated versions of libraries to current ones.  
        See the `requirements.txt` file for more information.
    - Upgrading to the latest `python 3.11.4` version.
- **Customization**:
    - All descriptions will be in English. 
        - This also applies to the `README` file, which has been rewritten.  
        Its older version in Czech will be renamed to `CZ_README` and will not be the main `README` file for github.
