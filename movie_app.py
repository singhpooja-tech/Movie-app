import statistics
import random
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def _exit_program():
    """Exit prompt"""
    print("Bye!")


def _press_to_continue():
    """Self-explanatory """
    print()
    input("Press anything to continue... \n")


class MovieApp:
    def __init__(self, storage):
        """Initializes MovieApp with storage objects"""
        self._storage = storage
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY not found. Check .env file")

    def _fetcher(self, title):
        """Fetching movie details from OMDb API"""
        api_url = f"http://www.omdbapi.com/?t={title}&apikey={self.api_key}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            movie_data = response.json()
            if movie_data.get("Response") == "False":
                print(f"Movie '{title}' not found in OMDb.")
                return None

            movie_details = {
                "title": movie_data.get("Title"),
                "year": movie_data.get("Year"),
                "rating": float(movie_data.get("imdbRating", 0)),
                "poster": movie_data.get("Poster"),
                "link": movie_data.get("imdbID")
            }
            return movie_details

        except requests.exceptions.RequestException as h:
            print(f"Error! {h}")
            return None

    def _list_movies(self):
        """1. Listing all the movies"""
        movies = self._storage.list_movies()
        total_movies = 0
        for _ in movies:
            total_movies += 1
        print(f"{total_movies} movies in total")
        for movie, details in movies.items():
            rating = details["rating"]
            year = details["year"]
            print(f"{movie} ({year}): {rating}")

    def _add_movie(self):
        """Adding Movie provided by the user
         fetching Movie details from OMDb API"""
        while True:
            title = input("Please enter title of the Movie: ")
            if len(title) == 0:
                print("Movie title can not be empty")

            else:
                movie_details = self._fetcher(title)

                if movie_details:
                    # Save to storage
                    self._storage.add_movie(
                        movie_details["title"],
                        movie_details["year"],
                        movie_details["rating"],
                        movie_details["poster"],
                        movie_details["link"]
                        )
                    print(f"\nMovie {title} successfully added to the database")
                    break
                else:
                    print("Could not add Movie. Try again!")

    def _delete_movie(self):
        """3. Deleting a movie, if the movie only exists."""

        delete = input("Which movie shall be deleted? ")

        self._storage.delete_movie(delete)

    def _update_movie(self):
        """Update the rating of an existing movie in the database"""

        title = input(f"Which movie shall be updated?: ")
        note = input(f"Please enter a note for '{title}': ")
        self._storage.update_movie(title, note)

    def _movie_stats(self):
        """Showing the user the statistics of the movie database such as
            average rating, median rating, best rated movie and the worst rated one"""
        movies = self._storage.get_movies()

        ratings = [details["rating"] for details in movies.values()]
        movie_names = list(movies.keys())

        average_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        best_movie = movie_names[ratings.index(max(ratings))]
        worst_movie = movie_names[ratings.index(min(ratings))]

        print(f"Average rating: {round(average_rating, 2)}")
        print(f"Median rating: {round(median_rating, 2)}")
        print(f"Best Movie: {best_movie}, {max(ratings)}")
        print(f"Worst Movie: {worst_movie}, {min(ratings)}")

    def _random_movie(self):
        """Picks a random movie for the user"""
        movies = self._storage.get_movies()
        movie, details = random.choice(list(movies.items()))

        rating = details["rating"]
        year = details["year"]
        print(f"Tonight's choice is: {movie} ({year}), rated at: {rating}")

    def _search_movie(self):
        """Searches a movie based of the users input, very sensitive"""
        movies = self._storage.get_movies()

        search_input = input("Please enter part of movie's name: ").lower()

        for movie, details in movies.items():
            rating = details["rating"]
            year = details["year"]
            if search_input in movie.lower():
                print(f"{movie} ({year}): {rating}")

    def _rating_sorted_movies(self):
        """ Display a sorted version of the ratings in the movie database in descending order
        bubble sorting, going through the rating over and over and pushing the lower rating at the end(descending)"""
        movies = self._storage.get_movies()

        movies_sorting = list(movies.items())

        for i in range(len(movies_sorting)):
            for j in range(len(movies_sorting) - 1):
                if movies_sorting[j][1]["rating"] < movies_sorting[j + 1][1]["rating"]:
                    movies_sorting[j], movies_sorting[j + 1] = movies_sorting[j + 1], movies_sorting[j]

        for movie, details in movies_sorting:
            print(f"{movie} ({details["year"]}), {details["rating"]}")

    def _year_sorted_movies(self):

        """ User asked what type of order he wants and program sorts them accordingly
        bubble sorting used, this time year is pushed around according to the users wishes"""
        movies = self._storage.get_movies()
        print("\nHow would you like the movies to be sorted?\n ")
        while True:  # not letting the user use any other form or number except the ints 1 and 2.
            try:

                user_choice = int(input("Press 1 for ascending order | Press 2 for descending order\n"))
                if user_choice != 1 and user_choice != 2:
                    print("Invalid input! Please enter a number between 1 & 2")
                else:
                    break

            except ValueError:
                print("Invalid Input! Please enter a number")

        movies_sorting = list(movies.items())

        for i in range(len(movies_sorting)):
            for j in range(len(movies_sorting) - 1):
                if user_choice == 1:
                    if movies_sorting[j][1]["year"] > movies_sorting[j + 1][1]["year"]:
                        movies_sorting[j], movies_sorting[j + 1] = movies_sorting[j + 1], movies_sorting[j]
                elif user_choice == 2:
                    if movies_sorting[j][1]["year"] < movies_sorting[j + 1][1]["year"]:
                        movies_sorting[j], movies_sorting[j + 1] = movies_sorting[j + 1], movies_sorting[j]

        for movie, details in movies_sorting:
            print(f"{movie} rated at: {details["rating"]}, made in {details["year"]}")

    def _generate_website(self):
        """Generate a website with the Movie's in our list"""
        with open("_static/index_template.html", "r", encoding="utf-8") as template_file:
            template = template_file.read()  # Loading the HTML file

            movies = self._storage.list_movies()
            movie_grid_html = ""
            for title, movie in movies.items():
                note = movie["note"]  # generating the note
                imdb_link = f"https://www.imdb.com/title/{movie["link"]}"  # Generating the imdb link
                movie_grid_html += f"""
                    <li>
                        <div class="movie">
                            <a href="{imdb_link}" target="_blank">
                            <img src="{movie['poster']}" alt="{title}" class="movie-poster" title="{note}">
                            </a>
                            <div class="movie-title">{title}</div>
                            <div class="movie-year">{movie['year']}</div>
                            <div class="movie-rating">{movie['rating']}</div>
                        </div>
                    </li>
                """
                # replacing the templates
                show_content_html = template.replace("__TEMPLATE_TITLE__", "Movie Project")
                show_content_html = show_content_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

                with open("data/index.html", "w") as target_file:  # writing the index.html
                    target_file.write(show_content_html)

        print("Website was generated successfully!")

    def run(self):
        """Command data structure, user picks a number of the action he wants to do
        Program is always running and updating with the users decisions.
        Press 0 to Exit
        Function Pointers used. User has to enter a valid number
        from 0 to 9 and only that to execute the action """
        menu_actions = {
            0: _exit_program,
            1: self._list_movies,
            2: self._add_movie,
            3: self._delete_movie,
            4: self._update_movie,
            5: self._movie_stats,
            6: self._random_movie,
            7: self._search_movie,
            8: self._rating_sorted_movies,
            9: self._year_sorted_movies,
            10: self._generate_website
        }

        while True:
            print("********** My Movies Database **********")
            print("")
            print("Menu:")
            print("0. Exit")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete Movie")
            print("4. Update movie")
            print("5. Stats")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("9. Movies sorted by year")
            print("10. Generate Webpage")
            print("")
            try:

                user_input = int(input("Enter Choice (0-10): "))
                print("")

                if user_input in menu_actions:

                    menu_actions[user_input]()

                    if user_input != 0:
                        _press_to_continue()
                    if user_input == 0:
                        break
                else:
                    print("Invalid choice, please enter a number between 0 and 10.")
                    _press_to_continue()

            except ValueError:
                print("\nInvalid input, please enter a number.\n")
                _press_to_continue()