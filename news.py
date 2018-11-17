
import psycopg2

DBNAME = "news"


def fetch_all(query):
    database = psycopg2.connect(database=DBNAME)
    conn = database.cursor()
    conn.execute(query)
    all_results = conn.fetchall()
    database.close()
    return all_results


def top_articles():
    article_query = 'SELECT * FROM best_three_articles;'
    result = fetch_all(article_query)
    output = '"%s"  --  %s  views\n'
    top_articles = "".join(output % (title, views) for title, views in result)
    print("\nThree Articles have been accessed the most are:\n ")
    print(top_articles)


def top_authors():
    author_query = 'SELECT * FROM best_authors;'
    result = fetch_all(author_query)
    output = '"%s"  --  %s  views\n'
    top_authors = "".join(output % (name, views) for name, views in result)
    print("\nThe Most Popular Authors' Articles of All Time Are: \n ")
    print(top_authors)


def percentage_error():
    error_query = 'SELECT * FROM percentage_error WHERE all_errors >=1;'
    result = fetch_all(error_query)
    view = '"%s"  --  %s errors\n'
    error = "".join(view % (date, format(err, '.2f')) for date, err in result)
    print("\nMore than one percent of requests lead to errors was on:\n ")
    print(error)


def main():
    top_articles()
    top_authors()
    percentage_error()


main()


