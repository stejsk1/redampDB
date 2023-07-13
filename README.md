# REDAMP
## Getting started
- execute `pip install -r requirements.txt`
- execute `python3 main.py`

### Database data:
- user: postgres
- pw: redamp  
    - The `connect_to_database()` function holds the database connection information, if needed the database connection variables can be changed.

## Changelogs
- A new file `changelog.md` has been added that explains the changes to the program.

## About the project
The `urlhaus`, `alienvault` and `openphish` tables are linked to the `base` table using foreign keys.  
The `base` table is the control (parent) table,
from which I then retrieve additional information based on the `base_id` and `source` from the other tables. 
For the `alientvault` column names, the names used are those contained in the official documentation:  
`IP` - IPv4 address  
`Risk` - how risky is the target (1-10)  
`Reliability` - how reliable is the rating (1-10)  
`Activity` - what type of host is it  
`Country` - what is the IPv4 country of origin  
`City` - what is the IPv4 city of origin  
`Latitude` - geolocated latitude of the IPv4  
`Longitude` - geolocated longitude of the IPv4  
`Occurrences` - these refer to the amount of occurrences reported to OTX.3  

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