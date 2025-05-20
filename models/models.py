from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Anime(db.Model):
    __tablename__ = 'anime'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    cover = db.Column(db.String, nullable=False)  # URL або шлях
    genres = db.Column(db.String, nullable=False)
    key = db.Column(db.String, nullable=False, unique=True) 

    seasons = db.relationship('Season', backref='anime', cascade="all, delete-orphan")

class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)

    episodes = db.relationship('Episode', backref='season', cascade="all, delete-orphan")

class Episode(db.Model):
    __tablename__ = 'episodes'
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    video = db.Column(db.String, nullable=False)

class UserAnimeProgress(db.Model):
    __tablename__ = 'user_anime_progress'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'), primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), primary_key=True)
    last_watched_at = db.Column(db.DateTime)

class UserAnimeRating(db.Model):
    __tablename__ = 'user_anime_rating'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

class DevilFruit(db.Model):
    __tablename__ = 'devil_fruits'
    id = db.Column(db.Integer, primary_key=True)       # ID для унікальності в базі
    key = db.Column(db.String(50), unique=True, nullable=False)      # унікальний ключ (як "doru_doru_no_mi")
    title = db.Column(db.String(255), nullable=False)   # назва фрукта (наприклад, "Фрукт Дору Дору но Мі")
    description = db.Column(db.Text, nullable=False)    # детальний опис
    fruit_type = db.Column(db.String(50), nullable=False)  # тип фрукту (Парамеція, Зоан тощо)
    cover = db.Column(db.String(255), nullable=True)    # посилання або шлях до картинки

    def __repr__(self):
        return f"<DevilFruit {self.title}>"
