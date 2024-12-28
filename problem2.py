# This py file is for Problem 2 of Homework #6 MPCS 51042
#
# AKBAR SAPUTRA
#
# This file makes a movie search website from an open movie database API

"""
I use flask as my main library. I use urllib.request, json, and urllib.parse
libraries just as helpers.
IMPORTANT! There's a whole bunch of dependencies problems among flask, jinja2,
and Werkzeug. I spent so much time to update them at the latest update and
did extensive browsing to troubleshoot this. Both the app and the pytest work on
my linux1.cs.uchicago.edu machine, but just in case they don't work for my grade,
it might be required to update flask to the most up-to-date version
"""
from flask import (Flask, request, render_template, url_for)

from urllib.request import (Request, urlopen)
from json import loads
from urllib.parse import quote

"""
This app does three things:
- search movies by strings of the movie titles and returns at max 20 results,
- open details about movie (result of search), and
- list 20 trending movies of the week.
It's like a miniscule version of IMDb, if you will.

To do all these jobs, I use two sources of API: TheMovieDB.org (TMDB) and Open
Movie Database (OMDB). TMDB API is very comprehensive, and requires an extensive
use of URL requests and JSON parsing. I want this app to focus more on the use
of Flask library, so I use OMDB as another API source because OMDB provides a
more straightforward way to provide details about movies. The search result is
also maxed at 20 results because TMDB uses pages to return the result, and it will
require a more complicated JSON work.

I use TMDB when user search movies by titles and when user wants to find out the
trending movies of the week, and then I use OMDB when user click on a specific
movies based on the search result or based on the trending list. I can't do search
on OMDB because it requires user to enter the exact movie title, not any string
that matches any movie titles.
"""

def send_request(url, tmdb=True):
    """
    This is a helper method that handles all the API requests. TMDB requires
    headers in every request, so I have to make a flag if the request is intended
    to TMDB. If it is, I insert headers into the request.
    """
    if tmdb:
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMzRkZDk0MDFlODFmMmU1NGIwNzQ0YWJkNTQyYjAyMyIsInN1YiI6IjUyMzlkMzMyNzYwZWUzNzg2MDE3ZDcyZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.uNKPSLz_IHWAmGu30qmQZz2rYGJ5EDnWmh1dlm7L3IM"
        }
        request = Request(url, headers=headers)
    else:
        request = Request(url)
    with urlopen(request) as response:
        result = response.read()
    return result.decode("utf-8")

# I define 'web' as my Flask app name
web = Flask(__name__)

# The first endpoint is the homepage "/", where the homepage is and where the
# search result is showed. The default webpage for the homepage is "search.html".
# There are two methods defined: "POST" when user sends search request, and
# "GET" when user receives search results
@web.route("/", methods=("GET", "POST"))
def home():
    """
    This is the associated function for "/" route. This function will be called
    in the main() function, which is when the app was first initialized by user.
    """
    # If a search is requested, then this function sends an API request to TMDB
    if request.method == "POST":
        # Get the keyword from the "title" field input, or return "" if it's empty
        title = request.form.get("title", "")
        if title:
            # quote() is a method from urllib.parse library to help URLify
            # the search keyword (i.e. change " " to "%20%", etc.)
            title = quote(title)
            response_tmdb = send_request(f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US")
            result = loads(response_tmdb)
            # The search result is in the key "results" from the dict that is
            # returned by the API request (after JSON parsing)
            movies = result["results"]
        else:
            # If search keyword is empty, return nothing
            movies = None
        # Now I use "result.html" as a template, which is an extension of
        # "search.html", to show the search results
        return render_template("result.html", movies=movies)

    # If no search is requested, then show the default webpage
    else:
        return render_template("search.html")

# The second endpoint is the movie detail page, which involves a variable rule
# called "movie_id/<id>"" that shows the movie id.
# The movie detail page uses "movie.html" as a template.
# This endpoint only receives data and doesn't send anything, so there is
# only "GET" method defined.
@web.route("/movie_id/<id>", methods=("GET",))
def movie_detail(id):
    """
    This is the associated function of "/movie_id/<id>" route. This function will
    be called from the "result.html" as a link when user click on "Open details >>>"
    link provided on each movie in the search result. This function is called
    using "url_for" method from flask, through syntax in the html template
    provided by jinja2 library (which is included in flask)
    """
    if request.method == "GET":
        # If user request to see details of a movie, first we send an API request
        # to TMDB to retrieve a universal ID, which is IMDb movie ID
        response_tmdb = send_request(f"https://api.themoviedb.org/3/movie/{id}?language=en-US")
        movie = loads(response_tmdb)

        # Then send the IMDB movie ID as an API request to OMDB to retrieve
        # details about a movie
        response_omdb = send_request(f"https://www.omdbapi.com/?i={movie['imdb_id']}&apikey=56742269", tmdb=False)
        details = loads(response_omdb)
            # Get the keyword from the "title" field input, or return "" if it's empty
    else:
        # If this function is somehow accessed without any movie detail request,
        # return nothing
        movie = None
        details = None
    # Show both the result of TMDB and OMDB API request to "movie.html"
    # Why do both results of TMDB and OMDB have to be sent to "movie.html"?
    # This is to make sure that the details shown in the search results list
    # is similar to the details shown in the movie details page (especially
    # for the poster image, the backdrop, movie title, year, and summary)
    return render_template("movie.html", movie=movie, details=details)

# This is the third and final endpoint, which is the "/trending" route that
# shows a list of trending movies of the current week. TMDb provides this
# without any input argument. The trending page uses "trending.html" as a template
# This endpoint only receives data and doesn't send anything, so there is
# only "GET" method defined.
@web.route("/trending", methods=("GET", "POST"))
def trending():
    """
    This is the associated function of "/trending" route. This function will be
    called from the "search.html" as a link when user click on "Find trending
    movies this week" link provided next to the "Search" button in the homepage.
    This function is also called using "url_for" method from flask, through
    syntax in the html template provided by jinja2 library.
    """
    if request.method == "GET":
        # When user click on "Find trending movies this week" link in homepage,
        # the app sends request to TMDB and receives a list of trending movies
        # of the current week
        response_tmdb = send_request("https://api.themoviedb.org/3/trending/movie/week?language=en-US")
        result = loads(response_tmdb)
        movies = result["results"]
    elif request.method == "POST":
        title = request.form.get("title", "")
        if title:
            # quote() is a method from urllib.parse library to help URLify
            # the search keyword (i.e. change " " to "%20%", etc.)
            title = quote(title)
            response_tmdb = send_request(f"https://api.themoviedb.org/3/search/movie?query={title}&include_adult=false&language=en-US")
            result = loads(response_tmdb)
            # The search result is in the key "results" from the dict that is
            # returned by the API request (after JSON parsing)
            movies = result["results"]
        else:
            # If search keyword is empty, return nothing
            movies = None
        # Now I use "result.html" as a template, which is an extension of
        # "search.html", to show the search results
        return render_template("result.html", movies=movies)
    # Show the result from TMDB to "movie.html"
    return render_template("trending.html", movies=movies)

def main():
    """
    When the app was first started, the app showed the homepage, associated with
    the home() function
    """
    home

if __name__ == "__main__":
    # To run the app using "python problem2/problem2.py", flask requires the app
    # to be run in the debug mode.
    web.run(debug=True)