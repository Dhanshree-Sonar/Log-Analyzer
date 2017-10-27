#!/usr/bin/env python2.7

import psycopg2


class LogAnalyser():
    """This class is used to analyze the newpaper site logs."""

    def __init__(self):
        """Initializes the newpaper site log's DB name and DB connection."""
        self.db_name = "news"
        self.db, self.db_cursor = self.db_open_connection()
        
    def __del__(self):
        """Closes DB connection after required analysis has done."""
        try:
            self.db.close()
        except psycopg2.Error as e:
            print("Unable to close DB connection.. \n")
            print e.pgerror
            print e.diag.message_detail
            sys.exit(1)
        else:
            print("DB connection closed successfully.. \n")
            
    def run_analysis(self):
        """
        This method performs the analysis on log data using different methods,
        search_popular_articles(), search_popular_authors(),
        error_request_percentile() and most_people_visit()
        """
        print("Most popular 3 articles of all time: \n")
        result = self.search_popular_articles(3)
        print(result)
        print("------------------------------------------------------------\n")

        print("Most popular article authors of all time: \n")
        result = self.search_popular_authors(4)
        print(result)
        print("------------------------------------------------------------\n")

        print("Day(s) on which more than 1% of requests lead to errors: \n")
        result = self.error_request_percentile()
        print(result)
        print("------------------------------------------------------------\n")

        print("Day of the week, when most people visited the site: \n")
        result = self.most_people_visit()
        print(result)
        print("------------------------------------------------------------\n")

    def db_open_connection(self):
        """Opens DB connection."""
        try:
            db = psycopg2.connect(database=self.db_name)
        except psycopg2.Error as e:
            print("Unable to open DB connection.. \n")
            print e.pgerror
            print e.diag.message_detail
            sys.exit(1)
        else:
            db_cursor = db.cursor()
            print("DB connection opened successfully.. \n")
            return db, db_cursor

    def search_popular_articles(self, count):
        """Provides list of articles which have most visitors."""
        sql_statement = """
            SELECT articles.title, visits
            FROM articles, path_visits
            WHERE articles.slug LIKE
                substring(path_visits.path FROM '/article/#"%#"' for '#')
            ORDER BY visits DESC
            LIMIT """ + str(count) + ";"

        # Executing SQL statement to retrive popular articles
        self.db_cursor.execute(sql_statement)
        article_list = self.db_cursor.fetchall()

        # Looping through query result to display it in required format
        result = ""
        for list in article_list:
            result += list[0] + "  --  " + str(list[1]) + " views\n"

        return result

    def search_popular_authors(self, count):
        """Provides list of authors, whose articles are most viewed."""
        sql_statement = """
            SELECT authors.name, SUM(visits) AS visit_count
            FROM articles, authors, path_visits
            WHERE articles.slug LIKE
                substring(path_visits.path FROM '/article/#"%#"' for '#')
                AND  authors.id = articles.author
            GROUP BY authors.name
            ORDER BY visit_count DESC
            LIMIT """ + str(count) + ";"

        # Executing SQL statement to retrive popular authors
        self.db_cursor.execute(sql_statement)
        author_list = self.db_cursor.fetchall()

        # Looping through query result to display it in required format
        result = ""
        for list in author_list:
            result += list[0] + "  --  " + str(list[1]) + " views\n"

        return result

    def error_request_percentile(self):
        """Provide list of dates, when load errors are more than 1%."""
        sql_statement = """
            SELECT error_load.date, (
                error_load.visits * 100.0 / all_load.visits) AS percentile
            FROM error_load LEFT JOIN all_load
                ON (error_load.date = all_load.date)
            WHERE (error_load.visits * 100.0 / all_load.visits) > 1;
        """

        # Executing SQL query to retrive dates which had > 1% load errors.
        self.db_cursor.execute(sql_statement)
        error_day_list = self.db_cursor.fetchall()

        # Looping through query result to display it in required format
        result = ""
        for list in error_day_list:
            result += list[0] + "  --  " + str("%.2f" % list[1]) + "% errors\n"

        return result

    def most_people_visit(self):
        """Provides day which has most visits"""
        sql_statement = """
            SELECT to_char(time, 'Day') AS day , count(*) AS visits
            FROM log_data
            GROUP BY day
            ORDER BY visits DESC
            LIMIT 1;
        """

        # Executing SQL statement to retrive day which has most visitors
        self.db_cursor.execute(sql_statement)
        most_visit_day = self.db_cursor.fetchall()

        # Formatting query result in required style
        result = most_visit_day[0][0] + "  --  " + str(most_visit_day[0][1])
        result += " visits\n"

        return result


# Creating object of LogAnalyser class.
log_analysis = LogAnalyser()
# Starting log analysis.
log_analysis.run_analysis()
