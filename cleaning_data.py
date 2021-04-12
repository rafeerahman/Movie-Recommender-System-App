"""
This Python module contains several functions that perform computations on
dataframes or create new dataframes for the given dataset.
"""
import json
import pandas as pd
import time


def load_dataframe() -> pd.DataFrame:
    """ Return a dataframe for the 6 data files and print when you start or finish loading
    a file and how much time it the loading takes.
    Preconditions:
        - The 6 JSON files are located in a folder called 'data'
    """
    data_dir = 'data'
    file_names = ["part-01.json", "part-02.json", "part-03.json",
                  "part-04.json", "part-05.json", "part-06.json"]
    start_time = time.time()
    reviews_list = []
    for file in file_names:
        print(f"Started loading {file}...")
        with open(f"{data_dir}/{file}") as json_file:
            new_file = json.load(json_file)
            for review in new_file:
                reviews_list.append(review)
        print(f"Finished loading {file} at {time.time() - start_time:.2f} total seconds elapsed")
    total_time = time.time() - start_time
    total_len = len(reviews_list)
    print(
        f"Loading complete after {total_time:.2f} seconds, "f"{total_len:,} items in reviews_list")
    return pd.DataFrame(reviews_list)


def load_sample(file: str) -> pd.DataFrame:
    """ Return a dataframe for the given sample data. The returned dataframe is used for
    testing purposes.
    Preconditions:
        - The file is located in a folder called 'data'
    """
    data_dir = 'data'
    reviews_list = []
    with open(f"{data_dir}/{file}") as json_file:
        new_file = json.load(json_file)
        for review in new_file:
            reviews_list.append(review)
    return pd.DataFrame(reviews_list)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """ Return a dataframe that only contains the columns of reviewer, movie, and rating
    and no null ratings. The data type of ratings in the returned data frame is int.
    Preconditions:
    - df is either the dataframe returned by load_dataframe or sample_dataframe
    """
    df = df[['reviewer', 'movie', 'rating']]
    df_not_na = df[df["rating"].notna()]
    df_not_na["rating"] = df_not_na["rating"].astype(int)
    return df_not_na.reset_index(drop=True)


def get_movie_titles() -> list[str]:
    """ Return all the movie titles. """
    df = load_sample('sample_reviews.json') # CHANGE TO 'load_dataframe' when done
    new_df = clean_dataframe(df)
    return new_df['movie'].to_list()





