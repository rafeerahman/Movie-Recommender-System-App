""" File to process datasets
"""
import pandas as pd


def load_reviews_data(filename: str) -> None:
    """ Load the reviews dataset using a pandas dataframe.
    Columns Include:
    'review_id', 'reviewer', 'movie', 'rating', 'review_summary',
    'review_date', 'spoiler_tag', 'review_detail', 'helpful'

    load_reviews_data('sample_reviews.json')
    """
    reviews_df = pd.read_json(filename)
    # reviews_df.columns.to_list()
    movies = reviews_df['movie'].to_list()
    reviewer = reviews_df['reviewer'].to_list()
    ratings = reviews_df['rating'].to_list()

    # print(movies)
