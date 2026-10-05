class Movie:
    def __init__(self, title):
        self.title = title
        self.ratings = []

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.ratings.append(rating)
        else:
            print("Rating must be between 1 and 5")

    def average_rating(self):
        if not self.ratings:
            return 0

        return sum(self.ratings) / len(self.ratings)

    def show_details(self):
        print(f"Movie: {self.title}")
        print(f"Average Rating: {self.average_rating():.1f}/5")


movie = Movie("Interstellar")

movie.add_rating(5)
movie.add_rating(4)
movie.add_rating(5)
movie.add_rating(4)

movie.show_details()