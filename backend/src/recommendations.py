from app import *
from init import app, db
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

class KNNModel(object):
    def __init__(self, user_id):
        self.db = db
        self.genres = None
        self.genre_indices = None
        self.books = None
        self.user_id = user_id

    def generate_n_dimensional_space(self):
        # Fetch all books in the database
        self.books = self.db.get_all_books()

        # Get all unique genres
        self.genres = set()
        for book in self.books:
            book_genres = self.db.get_book_genres(book['id'])
            for genre in book_genres:
                self.genres.add(genre)

        # Map genres to indices
        self.genre_indices = {genre: i for i, genre in enumerate(self.genres)}

        # Initialize n-dimensional space with zeros
        n_dimensions = len(self.genres) + 1  # Ratings plus genres
        n_space = np.zeros((len(self.books), n_dimensions))

        # Fill n-dimensional space
        for i, book in enumerate(self.books):
            book_genres = self.db.get_book_genres(book['id'])
            avg_rating = self.db.get_average_rating(book['id'])
            n_space[i][0] = avg_rating  # Rating as the first dimension
            for genre in book_genres:
                genre_index = self.genre_indices[genre]
                n_space[i][genre_index + 1] = 1  # Set genre index to 1

        # Visualize the n-dimensional space
        pca = PCA(n_components=3)
        n_space_pca = pca.fit_transform(n_space)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(n_space_pca[:, 0], n_space_pca[:, 1], n_space_pca[:, 2])
        ax.set_xlabel('PCA Component 1')
        ax.set_ylabel('PCA Component 2')
        ax.set_zlabel('PCA Component 3')
        plt.show()

    def recommendation_algorithm(self):
        # Check if genres and genre_indices are initialized
        if self.genres is None or self.genre_indices is None or self.books is None:
            raise ValueError("Genres, genre_indices, or books are not initialized. Run generate_n_dimensional_space first.")

        # Using the user_id, fetch their favorite books
        favorite_books = self.db.get_user_favorites(self.user_id)

        # Create a vector for the user's favorite genres
        user_genre_vector = np.zeros(len(self.genres))
        for book_id in favorite_books:
            book_genres = self.db.get_book_genres(book_id)
            for genre in book_genres:
                if genre in self.genre_indices:
                    user_genre_vector[self.genre_indices[genre]] = 1

        # Create a vector for the user's average rating
        user_avg_rating = np.mean([self.db.get_rating(book_id) for book_id in favorite_books])

        # Find nearby books with a slight bias towards higher-rated books of the same genre(s)
        recommended_books = []
        for i, book in enumerate(self.books):
            book_genres = self.db.get_book_genres(book['id'])
            book_rating = self.db.get_rating(book['id'])
            book_genre_vector = np.zeros(len(self.genres))
            for genre in book_genres:
                if genre in self.genre_indices:
                    book_genre_vector[self.genre_indices[genre]] = 1
            # Calculate distance between the user's vector and the book's vector
            genre_distance = np.linalg.norm(user_genre_vector - book_genre_vector)
            rating_distance = abs(user_avg_rating - book_rating)
            distance = genre_distance + 0.1 * rating_distance  # Bias towards higher-rated books
            recommended_books.append((book['id'], distance))

        # Sort recommended books by distance and return
        recommended_books.sort(key=lambda x: x[1])
        return recommended_books
