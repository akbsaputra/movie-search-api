import pytest
from problem2 import web

@pytest.fixture
def app():
    """
    This method creates an instance of the flask app directly
    """
    app = web  
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(app):
    """
    This method creates a client instance of the flask app. This is necessary
    so that I can simulate an HTTP request ("GET" or "POST") to the app for
    testing purposes 
    """
    return app.test_client()

def test_home_page_status_code(client):
    """
    This method tests that the root endpoint ("/") returns a 200 status code,
    meaning that the request is successful
    """
    response = client.get("/")
    assert response.status_code == 200

def test_home_page_template(client):
    """
    This method tests that the "/" endpoint uses the correct template, which is
    the "search.html". I test that the response should have:
    - a "search.html" text I put as a comment in the html document,
    - a "Title" input field, and
    - a "Search" button.
    This might not necessarily be a good test (because any html file with 
    those texts in it would pass the test), but this is sufficient.
    """
    response = client.get("/")
    assert b"search.html" in response.data 
    assert b"Title" in response.data
    assert b"Search" in response.data

def test_result_page(client):
    """
    This method tests that the result page at "/" route returns a 200 status code,
    and returns the correct result when I tried to search the movie "Inception"
    """
    response = client.post("/", data={"title": "Inception"})
    assert response.status_code == 200
    assert b"Results" in response.data
    assert b"Inception" in response.data

def test_movie_detail_page(client):
    """
    This method tests that the movie detail page ("/movie_id/<id>") returns a
    200 status code, as well as the correct details for the "Avatar" movie when
    it is run using the "Avatar" movie id on TMDB (which is 19995)
    """
    movie_id = 19995
    response = client.get(f"/movie_id/{movie_id}")
    assert response.status_code == 200
    # The response should have the text "Avatar" and "Pandora" in it
    assert b"Avatar" in response.data 
    assert b"Pandora" in response.data

def test_trending_page(client):
    """
    This method tests that the trending page ("/trending") returns a 200 status
    code, as well as the movie "The Marvels" which, on Nov 15 2023, is still
    trending on TMDB. This can be changed as time goes by, and I hope at least
    next week "The Marvels" is still trending on TMDB because otherwise this
    test will fail :/
    """
    response = client.get("/trending")
    assert response.status_code == 200
    assert b"Trending Movies" in response.data
    assert b"The Marvels" in response.data

if __name__ == "__main__":
    pytest.main()
