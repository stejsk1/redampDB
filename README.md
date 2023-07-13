# REDAMP
## Getting started
- execute `pip install -r requirements.txt`
- execute `python3 main.py`

### Database data:
- user: postgres
- pw: redamp  
    - In the `main.py` file, within the `DataCollector` class, there are the database connection details.  
    If needed, the connection variables can be modified to connect to a different database.  
    `self.data_handler = DatabaseHandler(
            dbname="postgres",
            user="postgres",
            password="redamp",
            host="localhost",
            port="5432",
        )`

## Changelogs
- A new file `changelog.md` has been added that explains the changes to the program.

## About the project
In general, the project serves as a data collection and processing system with the following key features:

- Authentication: The project includes an authentication mechanism to ensure secure access and manipulation of the data, allowing only authorized users to interact with the system.

- File Download: It enables the downloading of CSV files from specified URLs. Existing files are checked, and a comparison is performed to determine if an update is needed based on the newly downloaded data.

- Efficient Data Comparison and Update: By leveraging the `numpy` and `pandas` libraries, the project optimizes data comparison operations. It efficiently compares the downloaded CSV data with the existing records in the `PostgreSQL` database, identifying new or updated entries for accurate and streamlined updates.

- Data Retrieval: The project facilitates data retrieval from the `PostgreSQL` database, enabling users to obtain specific information based on their requirements.

- Logging and Error Handling: Throughout the data collection and processing stages, the project maintains a log file that captures important events and any encountered errors. This logging mechanism aids in troubleshooting and monitoring the system's performance.

- Performance Profiling: The project incorporates profiling capabilities to measure and analyze the performance of its data collection and processing tasks. Profiling results are recorded in a separate file, allowing developers to identify potential bottlenecks and optimize the code for enhanced efficiency.

In summary, the project offers a comprehensive solution for automated data collection, efficient comparison and updating of records in a `PostgreSQL` database, seamless data retrieval, logging of events and errors, and performance profiling for continuous optimization.

## Theoretical test
The path to the czech theory test is located in the `doc` folder, which also contains the initial brainstorming of the project.

## Conclusion
For reasons I was told at the interview that I should learn the database when taking this test,
I decided to use the "Everything else depends on your imagination" point from the assignment and created a more complex structure than just three tables.

I created the following code to behave universally for urlhaus, alienvault and openphish, which use the same functions for downloading and updating.

The course of my brainstorming gave me a basic idea of what this project should look like, but I had to rework it several times during development to achieve the most efficiency.
Fortunately, my knowledge of the pandas library made my job much easier and helped me optimize the code.
* I used parameterization to prevent SQL injection, even though it's not the most effective form of protection.
* For Brute Force prevention, I also added user authentication as a precaution.