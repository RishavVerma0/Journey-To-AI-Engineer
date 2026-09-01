class Movie:
    def __init__(self, movie_id, title, genres):
        self.movie_id = movie_id
        self.title = title
        self.genres = set(genres)
        self.ratings = []

    def add_rating(self, rating):
        if rating < 1 or rating > 5:
            raise ValueError(
                "Rating must be between 1 and 5"
            )

        self.ratings.append(rating)

    def average_rating(self):
        if not self.ratings:
            return 0

        return sum(self.ratings) / len(self.ratings)

    def display(self):
        print("-" * 45)
        print(f"ID       : {self.movie_id}")
        print(f"Title    : {self.title}")
        print(f"Genres   : {', '.join(self.genres)}")
        print(f"Ratings  : {self.ratings}")
        print(
            f"Average  : "
            f"{self.average_rating():.2f}"
        )


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.watched_movies = set()
        self.rated_movies = {}

    def watch_movie(self, movie_id):
        self.watched_movies.add(movie_id)

    def rate_movie(self, movie_id, rating):
        self.rated_movies[movie_id] = rating


class MoviePlatform:
    def __init__(self):
        self.movies = {}
        self.users = {}

    def add_movie(self, movie):
        if movie.movie_id in self.movies:
            raise ValueError("Movie already exists")

        self.movies[movie.movie_id] = movie

    def add_user(self, user):
        if user.user_id in self.users:
            raise ValueError("User already exists")

        self.users[user.user_id] = user

    def watch_movie(self, user_id, movie_id):
        if user_id not in self.users:
            raise ValueError("User not found")

        if movie_id not in self.movies:
            raise ValueError("Movie not found")

        self.users[user_id].watch_movie(movie_id)

    def rate_movie(self, user_id, movie_id, rating):
        if user_id not in self.users:
            raise ValueError("User not found")

        if movie_id not in self.movies:
            raise ValueError("Movie not found")

        movie = self.movies[movie_id]
        user = self.users[user_id]

        movie.add_rating(rating)
        user.rate_movie(movie_id, rating)

    def top_rated_movies(self, minimum_ratings=1):
        movies = [
            movie
            for movie in self.movies.values()
            if len(movie.ratings) >= minimum_ratings
        ]

        return sorted(
            movies,
            key=lambda movie: movie.average_rating(),
            reverse=True
        )

    def recommend_by_genre(self, genre):
        recommendations = []

        for movie in self.movies.values():
            if genre.lower() in {
                g.lower() for g in movie.genres
            }:
                recommendations.append(movie)

        return sorted(
            recommendations,
            key=lambda movie: movie.average_rating(),
            reverse=True
        )

    def most_popular_movie(self):
        if not self.movies:
            return None

        watch_count = {}

        for user in self.users.values():
            for movie_id in user.watched_movies:
                watch_count[movie_id] = (
                    watch_count.get(movie_id, 0) + 1
                )

        if not watch_count:
            return None

        popular_id = max(
            watch_count,
            key=watch_count.get # type: ignore
        ) # type: ignore

        return self.movies[popular_id]

    def genre_statistics(self):
        statistics = {}

        for movie in self.movies.values():
            for genre in movie.genres:

                if genre not in statistics:
                    statistics[genre] = {
                        "movies": 0,
                        "ratings": 0
                    }

                statistics[genre]["movies"] += 1
                statistics[genre]["ratings"] += len(
                    movie.ratings
                )

        return statistics


platform = MoviePlatform()


movies = [
    Movie(
        1,
        "Inception",
        ["Sci-Fi", "Thriller"]
    ),
    Movie(
        2,
        "Interstellar",
        ["Sci-Fi", "Drama"]
    ),
    Movie(
        3,
        "The Dark Knight",
        ["Action", "Drama"]
    ),
    Movie(
        4,
        "The Hangover",
        ["Comedy"]
    ),
    Movie(
        5,
        "Avengers",
        ["Action", "Sci-Fi"]
    )
]


for movie in movies:
    platform.add_movie(movie)


users = [
    User(101, "Rishav"),
    User(102, "Rahul"),
    User(103, "Priya"),
]


for user in users:
    platform.add_user(user)


platform.watch_movie(101, 1)
platform.watch_movie(101, 2)
platform.watch_movie(102, 1)
platform.watch_movie(102, 3)
platform.watch_movie(103, 1)
platform.watch_movie(103, 5)


platform.rate_movie(101, 1, 5)
platform.rate_movie(102, 1, 4)
platform.rate_movie(103, 1, 5)

platform.rate_movie(101, 2, 5)
platform.rate_movie(102, 3, 5)
platform.rate_movie(103, 5, 4)


print("\nTOP RATED MOVIES")

for movie in platform.top_rated_movies():
    movie.display()


print("\nSCI-FI RECOMMENDATIONS")

for movie in platform.recommend_by_genre("Sci-Fi"):
    movie.display()


print("\nMOST POPULAR MOVIE")

popular = platform.most_popular_movie()

if popular:
    popular.display()


print("\nGENRE STATISTICS")

statistics = platform.genre_statistics()

for genre, data in statistics.items():
    print(
        f"{genre}: "
        f"{data['movies']} movies | "
        f"{data['ratings']} ratings"
    )