from abc import ABC, abstractmethod


class IStorage(ABC):
    """Interface for movie storage with CRUD operations."""

    @abstractmethod
    def list_movies(self):
        """Returns a dictionary of movies from storage."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster, link):
        """Adds a movie to storage."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Deletes a movie from storage by title."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Updates a movie's rating in storage."""
        pass