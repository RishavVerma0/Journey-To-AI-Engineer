"""Program 3: Library
Demonstrates: composition (a Library "has" Books), class methods,
and __repr__ / __len__ special methods.
"""


class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
        self.is_available = True

    def __repr__(self):
        status = "available" if self.is_available else "checked out"
        return f"'{self.title}' by {self.author} ({self.year}) - {status}"


class Library:
    def __init__(self, name):
        self.name = name
        self._books = []  # composition: the library holds Book objects

    def __len__(self):
        return len(self._books)

    def add_book(self, book):
        self._books.append(book)
        print(f"Added: {book.title}")

    def find_by_author(self, author):
        return [b for b in self._books if b.author.lower() == author.lower()]

    def checkout(self, title):
        for book in self._books:
            if book.title.lower() == title.lower():
                if not book.is_available:
                    print(f"Sorry, '{book.title}' is already checked out.")
                    return
                book.is_available = False
                print(f"You checked out '{book.title}'.")
                return
        print(f"'{title}' is not in the library.")

    def return_book(self, title):
        for book in self._books:
            if book.title.lower() == title.lower():
                book.is_available = True
                print(f"Thanks for returning '{book.title}'.")
                return
        print(f"'{title}' does not belong to this library.")

    def show_catalog(self):
        print(f"\n{self.name} catalog ({len(self)} books):")
        for book in self._books:
            print(f"  {book!r}")


if __name__ == "__main__":
    lib = Library("City Library")

    lib.add_book(Book("Gitanjali", "Rabindranath Tagore", 1910))
    lib.add_book(Book("Godan", "Munshi Premchand", 1936))
    lib.add_book(Book("Malgudi Days", "R. K. Narayan", 1943))
    lib.add_book(Book("Swami and Friends", "R. K. Narayan", 1935))

    lib.show_catalog()

    print()
    lib.checkout("Godan")
    lib.checkout("Godan")        # already checked out
    lib.checkout("Unknown Book")  # not in library

    print("\nBooks by R. K. Narayan:")
    for book in lib.find_by_author("r. k. narayan"):
        print(f"  {book!r}")

    print()
    lib.return_book("Godan")
    lib.show_catalog()