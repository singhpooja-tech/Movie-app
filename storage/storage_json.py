from storage.istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        """Initializes the storage path to the json file"""
        self.file_path = file_path

    def get_movies(self):
        """Loads the movie database from the JSON file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Error loading movie database.")
            return {}

    def save_movies(self, movies):
        """Saves the movie database to the JSON file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(movies, file, indent=4)

    def list_movies(self):
        """Returns a dic of the movies."""
        return self.get_movies()

    def add_movie(self, title, year, rating, poster, link):
        """Adds a movie to JSON database."""
        movies = self.get_movies()
        movies[title] = {"year": year, "rating": rating, "poster": poster, "note": "", "link": link}
        self.save_movies(movies)

    def delete_movie(self, title):
        """Deletes a Movie from the JSON database."""
        movies = self.get_movies()
        if title in movies:
            del movies[title]
            print(f"\nMovie {title} deleted successfully")
            self.save_movies(movies)
        else:
            print(f"No movie with title '{title}' found in the database")

    def update_movie(self, title, note):
        """Updates a movie's note in the JSON database."""
        movies = self.get_movies()
        if title in movies:
            movies[title]["note"] = note
            print(f"Note for '{title}' is successfully updated")
            self.save_movies(movies)

        else:
            print(f"Movie '{title}' not found!")