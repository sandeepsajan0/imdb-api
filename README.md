# Imdb movies Project

## Setup and installation
    
    Use Python3.7
    
    1. Create a python virtualenv with command ```python3.7 -m venv  imdb_env```
    
    2. Activate virtual environment with command ```source imdb_env/bin/activate```
    
    3. Install required packages with ``` pip install -r requirements.txt```
    
    4. If you have SQLite file then run simply ```python manage.py runserver```
    
    5. Else run ```python manage.py migrate``` then run ```python manage.py runserver```.
    
    API DOC:
    
    /register/ : Post Request {"username":"sandeep", "password":"password"}
    
    /login/ : Post Request {"username":"sandeep", "password":"password"}
    
    /scrape_movies/ : Post Request {"url": "https://www.imdb.com/chart/top/"}
    
    /movies/list/ : Get Request param(for query) "search=<keyword>"
    
    movie/details/ : Get Request with body {"id":2}
    
    watchlist/movie/ : Post Request(to add) {"movie_id":2}, Get Request for listing
    
    watchlist/remove/ : Delete Request(to remove) {"movie_id":2}
    
    watchedlist/movie/ : Post Request(to add) {"movie_id":2}, Get Request for listing
    
    watchedlist/remove/ : Delete Request(to remove) {"movie_id":2}
    
If you have any query Please contact to sandeepsajan0@gmail.com or 6005030657.

