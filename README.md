# First Project
# Logs Analysis Internal Reporting Tools
	
	This project contain python code to Database API with postgresql database using psycopg2 module.
	"The database contains newspaper articles, as well as the web server log for the site.
	The log has a database row for each time a reader loaded a web page.  
	it will connect to that database, use SQL queries to analyze the log data, and print out the answers to 3 questions."
	1. What are the most popular three articles of all time?
	2. Who are the most popular article authors of all time?
	3. On which days did more than 1% of requests lead to errors?

## Steps to run the software(vagrant and newsdata in postgresql database) and python codes:
	1. Install Git-Bash Unix-Style Terminal for Windows
	2. Install Vagrant Tools to turn on Virtual Machine and Connect to Virtual Box
	3. Install VirtualBox
	4. Download the VM configuration called FSND-Virtual-Machine
	5. Download the database file called newsdata.sql and put it in dircetory (log-analysis-project)
	6. Open Git-Bash cd to FSND-Virtual-Machine Directory and Type Vagrant up; Vagrant SSH
	7. Connect to database newsdata.sql from Step 5; cd into /vagrant directory and /log-analysis-project then use the command psql -d news -f newsdata.sql
	8. Connect to database using psql -d news or psql news
	9. Write queries -Create View- into connected database (new=>) 
	10. To quit type \q right after (news=>)
	11. Go to shared file by cd /vagrant and use the command (python news.py) to get the results
	
## Create Views in the database
#1. best_three_articles
	CREATE VIEW  best_three_articles AS SELECT articles.title, count(log.id) AS views 
	FROM articles left JOIN log on log.path like concat('%',articles.slug) 
	GROUP BY articles.title ORDER BY views desc limit 3;	
	
#2. best_authors
	CREATE VIEW best_authors AS SELECT authors.name, count(log.path) AS most_page_views
	FROM authors, articles, log WHERE articles.author = authors.id and log.path like concat('%',articles.slug,'%') 
	and status like '%200%' GROUP BY authors.name ORDER BY most_page_views desc;
	
#3. status_errors
	CREATE VIEW status_errors AS SELECT date(time) AS date, count(status) AS errors FROM
	log WHERE status like '%404%' GROUP BY date;
	
#4. status_ok
	CREATE VIEW status_ok AS SELECT date(time) AS date, count(status) AS status_200 
	FROM log WHERE status like '%200%' GROUP BY date;
	
#5. percentage_error
	CREATE VIEW percentage_error AS SELECT status_errors.date, 
	cast(float8 (sum(status_errors.errors)/(sum(status_errors.errors) + sum(status_ok.status_200)))*100 AS numeric) AS all_errors
	FROM status_errors FULL JOIN status_ok on status_errors.date = status_ok.date GROUP BY status_errors.date ORDER BY all_errors desc;