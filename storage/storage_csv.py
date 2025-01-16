from storage.istorage import IStorage
import csv
import os


class StorageCsv(IStorage):
    def __init__(self, file_path):
        """If csv file doesn't exist, one is automatically created"""
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                fieldnames = ["title", "year", "rating", "poster", "note", "link"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

    def get_movies(self):
        """Loads movies from CSV file and returns dict
        Making sure Row exists.
        Making sure row is dict for us to use get()
        and not misinterpret it as an 'str'"""
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='') as file:
                data = csv.DictReader(file)
                for row in data:
                    if row:
                        if isinstance(row, dict):
                            title = row.get("title")
                            if title:
                                movies[title] = {
                                    "year": int(row.get("year", 0)),
                                    "rating": float(row.get("rating", 0.0)),
                                    "poster": row.get("poster", ""),
                                    "note": row.get("note", ""),
                                    "link": row.get("link", "")
                                }
            return movies
        except FileNotFoundError:
            print("Error loading movie database")
        return {}

    def save_movies(self, data):
        """Saves the movie database to CSV file"""
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ["title", "year", "rating", "poster", "note", "link"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in data.items():
                writer.writerow({"title": title,
                                 "year": details["year"],
                                 "rating": details["rating"],
                                 "poster": details["poster"],
                                 "note": details["note"],
                                 "link": details["link"]
                                 })

    def list_movies(self):
        """Returns dict of movies from the csv file"""
        return self.get_movies()

    def add_movie(self, title, year, rating, poster, link):
        """Adds movie to the CSV file"""
        movies = self.get_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster, "note": "", "link": link}
        self.save_movies(movies)

    def delete_movie(self, title):
        """Deletes a Movie from the CSV file"""
        movies = self.get_movies()
        if title in movies:
            del movies[title]
            print(f"\nMovie {title} deleted successfully")
            self.save_movies(movies)
        else:
            print(f"No movie with title '{title}' found in the database")

    def update_movie(self, title, note):
        """Updates a movie's note in the CSV database"""
        movies = self.get_movies()
        if title in movies:
            movies[title]["note"] = note
            print(f"Note for '{title}' is successfully updated")
            self.save_movies(movies)

        else:
            print(f"Movie '{title}' not found!")