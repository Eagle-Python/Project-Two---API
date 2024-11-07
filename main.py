import requests
from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ['API_KEY']


url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
img_url = "https://image.tmdb.org/t/p/w500"

youtube_url = "https://api.themoviedb.org/3/movie/movie_id/videos?language=en-US"
watch_url = "https://www.youtube.com/watch?v="

search_url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"

app = Flask(__name__)


@app.route("/")
def home():
    now_playing_url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"

    popular_url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    query = {
        "api_key": API_KEY
    }

    now_playing_respond = requests.get(url=now_playing_url, params=query)
    all_movie = now_playing_respond.json()['results']

    popular_respond = requests.get(url=popular_url, params=query)
    popular_movies = popular_respond.json()['results']

    return render_template("home.html", all_movie=all_movie, popular=popular_movies, photo_path=img_url)


@app.route("/search", methods=["Get", "POST"])
def search():
    search_params = {
        "api_key": API_KEY,
        "query": request.form['search_data'],
        "include_adult": "true",
        "language": "en-US",
        "page": "1",

    }
    if request.method == "POST":
        search_url = f"https://api.themoviedb.org/3/search/movie"
        search_request = requests.get(url=search_url, params=search_params)
        # request_id = search_request.json()
        search_data = search_request.json()['results']
        return render_template("search_movie.html", data=search_data, photo=img_url)
    return render_template("home.html")


@app.route("/search_movie_detail/<int:m_id>", methods=["GET", "POST"])
def search_movie_detail(m_id):
    movie_id = m_id
    detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    youtube = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US"
    query = {
        "api_key": API_KEY
    }
    youtube_respond = requests.get(url=youtube, params=query)
    if "results" not in youtube_respond.json():
        return render_template("no_data.html")
    data = youtube_respond.json()['results'][-1]
    use_url = ""
    if data:
        use_url = data['key']
    detail_respond = requests.get(url=detail_url, params=query)
    detail_data = detail_respond.json()
    return render_template("search_movie_detail.html", all_movie=data, all_data=detail_data, image=img_url, y_url=use_url, y_path=watch_url)


@app.route("/actor")
def actor_name():
    actor_url = "https://api.themoviedb.org/3/person/popular?language=en-US&page=8"
    query = {
        "api_key": API_KEY
    }
    actor_respond = requests.get(url=actor_url, params=query)
    data = actor_respond.json()['results']
    return render_template('actor.html', data=data, image_path=img_url)


@app.route("/actor_detail/<string:actor_id>")
def actor_detail(actor_id):
    actor_detail_url = f"https://api.themoviedb.org/3/person/{actor_id}?language=en-US"
    query = {
        "api_key": API_KEY
    }
    actor_detail_respond = requests.get(url=actor_detail_url, params=query)
    data = actor_detail_respond.json()
    return render_template('actor_detail.html', data=data, image_path=img_url)


@app.route("/actor_search", methods=["GET", "POST"])
def actor_search():
    actor_search_url = "https://api.themoviedb.org/3/search/person"
    query = {
        "api_key": API_KEY,
        "query": request.form["search_data"],
        "include_adult": 'true',
        'language': 'en-US',
        'page': '1'
    }
    actor_search_respond = requests.get(url=actor_search_url, params=query)
    data = actor_search_respond.json()['results']
    return render_template('search_actor.html', data=data, image_path=img_url)


@app.route("/series")
def series():
    query = {
        "api_key": API_KEY,
    }
    popular_series_url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
    popular_series_respond = requests.get(url=popular_series_url, params=query)
    popular_series = popular_series_respond.json()['results']

    playing_url = "https://api.themoviedb.org/3/tv/airing_today?language=en-US&page=1"
    playing_respond = requests.get(url=playing_url, params=query)
    playing_series = playing_respond.json()['results']

    return render_template("home.html", popular=popular_series, photo_path=img_url, all_movie=playing_series)


@app.route("/job")
def job():
    query = {
        "api_key": API_KEY,
    }
    job_url = "https://api.themoviedb.org/3/configuration/jobs"
    job_respond = requests.get(url=job_url, params=query)
    job_data = job_respond.json()
    job_datas = []
    for job_detail in job_data:
        job_datas.append(job_detail['jobs'])
    return render_template("job.html", job_data=job_data, data=job_datas)


if __name__ == "__main__":
    app.run(debug=True)
