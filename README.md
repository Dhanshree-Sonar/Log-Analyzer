# Log-Analyzer

This is an internal reporting tool for newspaper site. It retrieves log from the database and generates the report, which provides analysis such as most popular articles and most popular authors.

## Prerequisites

- Install [VirtuaBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- Install [Vagrant](https://www.vagrantup.com/downloads.html)
- Download [FSND-Virtual-Machine](https://github.com/udacity/fullstack-nanodegree-vm)
- Download [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- log_analyzer.py

## Initial setup

1. On terminal change directory to your downloads and perform `cd FSND-Virtual-Machine/vagrant`
2. Run `vagrant up`. This command will take a while for the first time.
3. Run `vagrant ssh`
4. Place `newsdata.sql` into `vagrant` directory, which is shared with your virtual machine
5. On terminal change directory to `vagrant` directory and run `psql -d news -f newsdata.sql`

## Built with

1. Python
2. PostgreSQL
3. psycopg2 python module to connect to database

## Create VIEWS, which are required for successful execution of log_analyzer.py
1. View to count the number of hits to the path
`CREATE VIEW path_visits AS
SELECT path, count(*) as visits
FROM log
GROUP BY path;`

2. View to retrieve maximum used columns from a log table
`CREATE VIEW log_data AS
SELECT path, status, time
FROM log;`

3. View to count number of hits per day 
`CREATE VIEW all_load AS
SELECT to_char(time, 'Month DD, YYYY') AS date, count(*) AS visits
FROM log_data
GROUP BY date;`

4. View to count number of load errors per day
`CREATE VIEW error_load AS
SELECT to_char(time, 'Month DD, YYYY') AS date, count(*) AS visits
FROM log_data
WHERE status = '404 NOT FOUND'
GROUP BY date;`

## How to run the analyzer

1. Place `log_analyzer.py` into `vagrant` directory.(Perform this just for the first time, no need to copy file every time you run the code)
2. On terminal change directory to `vagrant` directory and run `vagrant up`.
3. Run `vagrant ssh`.
4. Run the analyzer file `python2.7 log_analyzer.py`.

## Analysis description

This analyzer provides 4 answers:
1. Provides list of articles, which have most visitors. This will help to find the most popular articles.
2. Provides list of authors, whose articles are most viewed. This will help to find the most popular authors.
3. Provide list of dates, when load errors are more than 1%. This will help to find out when site users faced more issues.
4. Provides day of the week, which has the most visits. This will help to find on which day more user visits site, so upload interesting articles on that day will target maximum audience.

## Enhancement

`log_analyzer.py` contains `run_analysis()` method, which provides all the analysis. You can improve report by creating more functions and calling those function in `run_analysis()` method.
