from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models.models import db, Anime, Season, Episode, User, UserAnimeRating, UserAnimeProgress, DevilFruit
from flask_sqlalchemy import SQLAlchemy
import json
from flask import g
from flask import jsonify, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# ================== ФУНКЦІЯ ІМПОРТУ ДАНИХ ==================

def load_anime_data():
    with open("static/js/episods.json", "r", encoding="utf-8") as f:
        anime_data = json.load(f)

    # Очищення тільки таблиць аніме, сезонів та епізодів
    Episode.query.delete()
    Season.query.delete()
    Anime.query.delete()
    db.session.commit()

    for key, anime in anime_data.items():
        new_anime = Anime(
            key=anime["key"],
            title=anime["title"],
            description=anime["description"],
            cover=anime["cover"],
            genres=",".join(anime["genres"])
        )
        db.session.add(new_anime)
        db.session.flush()  # отримати id, не комітячи

        for season_index, season in enumerate(anime["seasons"], start=1):
            new_season = Season(
                anime_id=new_anime.id,
                season_number=season_index
            )
            db.session.add(new_season)
            db.session.flush()

            if isinstance(season["episodes"], list):
                for episode in season["episodes"]:
                    db.session.add(Episode(
                        season_id=new_season.id,
                        episode_number=episode["number"],
                        video=episode["video"]
                    ))
            else:
                for episode_num in range(1, season["episodes"] + 1):
                    db.session.add(Episode(
                        season_id=new_season.id,
                        episode_number=episode_num,
                        video=f"Video/{key}/{key}_trailer.mp4"
                    ))

    db.session.commit()
    print("✅ Аніме дані успішно імпортовано!")

def load_devil_fruits_data():
    with open("static/js/devil_fruits.json", "r", encoding="utf-8") as f:
        fruits_data = json.load(f)

    # Очистити таблицю devil_fruits
    DevilFruit.query.delete()
    db.session.commit()

    for fruit_key, fruit in fruits_data.items():
        new_fruit = DevilFruit(
            key=fruit.get("key", fruit_key),
            title=fruit.get("title") or fruit.get("name") or "Без назви",
            description=fruit.get("description", ""),
            fruit_type=fruit.get("type", "Невідомий"),
            cover=fruit.get("cover", "")
        )
        db.session.add(new_fruit)

    db.session.commit()
    print("✅ Дані про диявольські фрукти успішно імпортовані!")


# ================== МАРШРУТИ ==================

@app.route('/')
def main_page():
    last_seen = []
    is_guest = g.user is None

    if g.user:
        progress = (
            db.session.query(UserAnimeProgress, Anime, Season, Episode)
            .join(Anime, UserAnimeProgress.anime_id == Anime.id)
            .join(Season, UserAnimeProgress.season_id == Season.id)
            .join(Episode, UserAnimeProgress.episode_id == Episode.id)
            .filter(UserAnimeProgress.user_id == g.user.id)
            .order_by(UserAnimeProgress.last_watched_at.desc())
            .limit(4)
            .all()
        )

        last_seen = [{
            "anime_title": anime.title,
            "season_number": season.season_number,
            "episode_number": episode.episode_number,
            "cover": anime.cover,
            "anime_key": anime.key
        } for progress, anime, season, episode in progress]

    return render_template('Main_Page.html', last_seen=last_seen, is_guest=is_guest)


@app.route('/anime')
def anime():
    animes = Anime.query.all()
    return render_template('Anime.html', animes=animes)

@app.route('/anime/<key>')
def anime_episodes(key):
    anime = Anime.query.filter_by(key=key).first_or_404()

    user_rating = None
    if g.user:
        rating_record = UserAnimeRating.query.filter_by(user_id=g.user.id, anime_id=anime.id).first()
        if rating_record:
            user_rating = rating_record.rating

    return render_template('anime_episodes.html', anime=anime, user_rating=user_rating)

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    # Отримати всі оцінки користувача
    ratings = UserAnimeRating.query.filter_by(user_id=g.user.id).all()

    # Отримати відповідні аніме та сформувати список карток
    rated_animes = [(Anime.query.get(r.anime_id), r.rating) for r in ratings]

    return render_template('profile.html', rated_animes=rated_animes)


@app.route('/devil_fruits')
def devil_fruits():
    fruits = DevilFruit.query.all()
    return render_template('Devil_Fruits.html', fruits=fruits)
    
@app.route('/episode')
def episode():
    return render_template('episode.html')

@app.route('/news')
def news():
    animes = Anime.query.all()
    return render_template('News.html', animes=animes)

from flask import session

@app.route('/register', methods=['GET','POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    if User.query.filter_by(email=email).first():
        flash("Користувач з таким email вже існує!")
        return render_template('profile.html', show_modal=True, show_login=False)

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Зберегти користувача в сесії
    session['user_id'] = new_user.id
    flash("Реєстрація успішна!")
    return redirect(url_for('profile'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Будь ласка, введіть email та пароль", 400

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            return "Неправильний логін або пароль", 401

    return render_template('profile.html')  # GET-запит


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@app.route('/logout')
def logout():
    session.clear()
    flash("Ви вийшли з акаунту.")
    return render_template('profile.html')  # GET-запит

@app.route('/rate_anime', methods=['POST'])
def rate_anime():
    print(">>> POST на /rate_anime")
    print(">>> g.user:", g.user)

    if g.user is None:
        return jsonify({"error": "Користувач не авторизований"}), 401


    data = request.get_json()
    anime_id = data.get("anime_id")
    rating = data.get("rating")

    if not anime_id or not rating:
        return jsonify({"error": "Неправильні дані"}), 400

    # Перевірка чи існує запис
    existing_rating = UserAnimeRating.query.filter_by(user_id=g.user.id, anime_id=anime_id).first()
    if existing_rating:
        existing_rating.rating = rating
    else:
        new_rating = UserAnimeRating(user_id=g.user.id, anime_id=anime_id, rating=rating)
        db.session.add(new_rating)

    db.session.commit()
    return jsonify({"message": "Оцінка збережена успішно!"})

# ================== API ==================

@app.route('/api/anime')
def api_anime_list():
    animes = Anime.query.all()
    data = {
        a.key: {
            "title": a.title,
            "description": a.description,
            "cover": a.cover,
            "genres": a.genres.split(","),
            "seasons": [
                {"seasonTitle": s.season_title, "episodes": s.episodes}
                for s in a.seasons
            ]
        } for a in animes
    }
    return jsonify(data)

@app.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    anime = Anime.query.get_or_404(anime_id)

    user_rating = None
    if g.user:
        rating_record = UserAnimeRating.query.filter_by(user_id=g.user.id, anime_id=anime_id).first()
        if rating_record:
            user_rating = rating_record.rating

    return render_template("anime_detail.html", anime=anime, user_rating=user_rating)

@app.route('/anime/<key>/season/<int:season_number>/episode/<int:episode_number>')
def view_episode(key, season_number, episode_number):
    anime = Anime.query.filter_by(key=key).first_or_404()
    season = Season.query.filter_by(anime_id=anime.id, season_number=season_number).first_or_404()
    episode = Episode.query.filter_by(season_id=season.id, episode_number=episode_number).first_or_404()

    # Якщо користувач авторизований — оновлюємо/додаємо прогрес
    if g.user:
        progress = UserAnimeProgress.query.filter_by(
            user_id=g.user.id,
            anime_id=anime.id
        ).first()

        if progress:
            progress.season_id = season.id
            progress.episode_id = episode.id
            progress.last_watched_at = datetime.utcnow()
        else:
            new_progress = UserAnimeProgress(
                user_id=g.user.id,
                anime_id=anime.id,
                season_id=season.id,
                episode_id=episode.id,
                last_watched_at=datetime.utcnow()
            )
            db.session.add(new_progress)

        db.session.commit()

    return render_template('episode.html', anime=anime, season=season, episode=episode)
# ================== СТАРТ ==================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_devil_fruits_data()
        load_anime_data()  # <== перезаписує дані аніме
    app.run(debug=True)
