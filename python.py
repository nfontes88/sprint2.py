import sys

import requests
import secrets
import sqlite3


def get_top_250_data() -> list[dict]:
    api_query = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secret_key}"
    response = requests.get(api_query)
    if response.status_code != 200:  # if we don't get an ok response we have trouble
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)
    # jsonresponse is a kinda useless dictionary, but the items element has what we need
    jsonresponse = response.json()
    show_list = jsonresponse["items"]
    return show_list


def report_results(data_to_write: list[dict]):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def get_ratings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_queries = []
    base_query = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/"
    wheel_of_time_query = f"{base_query}tt7462410"
    api_queries.append(wheel_of_time_query)
    first_query = f"{base_query}{top_show_data[0]['id']}"
    api_queries.append(first_query)
    fifty_query = f"{base_query}{top_show_data[49]['id']}"
    api_queries.append(fifty_query)
    hundred_query = f"{base_query}{top_show_data[99]['id']}"
    api_queries.append(hundred_query)
    two_hundered = f"{base_query}{top_show_data[199]['id']}"
    api_queries.append(two_hundered)
    for query in api_queries:
        response = requests.get(query)
        if response.status_code != 200:  # if we don't get an ok response we have trouble, skip it
            print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
            continue
        rating_data = response.json()
        results.append(rating_data)
    return results


def main():
    top_show_data = get_top_250_data()
    ratings_data = get_ratings(top_show_data)
    report_results(ratings_data)
    report_results(top_show_data)


conn = sqlite3.connect('tables.db')
c = conn.cursor()


def create_table1():
    c.execute('''CREATE TABLE IF NOT EXISTS top250_tv_shows(the id INT, the title TEXT, the full title TEXT, the year INT, crew TEXT, imdb rating INT, imdbrating count INT)''')
    print(sqlite3.version)


def data_entry():
    c.execute('''INSERT INTO top250_tv_shows VALUES'''("https://imdb-api.com/en/API/Top250TVs"))
    conn.commit()
    c.close()
    conn.close()


def create_table2():
    c.execute('''CREATE TABLE IF NOT EXISTS user_ratings(imdbId INT, total rating INT, total rating votes INT, 10 rating % INT, 10 rating votes INT, 9 rating % INT, 9 rating votes INT, 8 rating % INT, 8 rating votes INT, 7 rating % INT, 7 rating votes INT, 6 rating % INT, 6 rating votes INT, 5 rating % INT, 5 rating votes INT, 4 rating % INT, 4 rating votes INT, 3 rating % INT, 3 rating votes INT, 2 rating % INT, 2 rating votes INT, 1 rating % INT, 1 rating votes INT)''')
    print(sqlite3.version)


def data_entry():
    c.execute('''INSERT INTO user_ratings VALUES'''("https://imdb-api.com/en/API/UserRatings"))
    conn.commit()
    c.close()
    conn.close()


create_table()
data_entry()


if __name__ == '__main__':
    main()
