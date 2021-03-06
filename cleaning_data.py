"""CSC111 Winter 2021 Project: Cleaning the Data

Instructions
===============================
This Python module contains several functions that perform computations on
dataframes or create new dataframes for the given dataset. A JSON file is created
from the filtered dataframe.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021
Rafee Rahman, Michael Galorro, Kimiya Raminrad, Mojan Majid
"""
import json
import pandas as pd


def load_dataframe() -> pd.DataFrame:
    """ Return a dataframe for the 6 data files and print when you start or finish loading
    a file.
    Preconditions:
        - The 6 JSON files are located in a folder called 'data'
    """
    data_dir = 'data'
    file_names = ["part-01.json", "part-02.json", "part-03.json",
                  "part-04.json", "part-05.json", "part-06.json"]
    reviews_list = []
    for file in file_names:
        print(f"Started loading {file}...")
        with open(f"{data_dir}/{file}") as json_file:
            new_file = json.load(json_file)
            for review in new_file:
                reviews_list.append(review)
        print(f"Finished loading {file}")
    print("Loading complete")
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
    return df_not_na.reset_index(drop=True)


def remove_shows(df: pd.DataFrame) -> pd.DataFrame:
    """ Return a dataframe that has no tv show reviews. The year pattern decides if a
    review is for a TV show.
    Preconditions:
    - df is a dataframe returned by clean_dataframe
    """
    year_re = r'(?:\()(\d{4})(?!\-)?(?:\d{4})?(?:\sTV\sMovie)?' \
              r'(?:\sVideo)?(?:\s?\)$)(?!\sSeason\s\d+\,?\sEpisode\s\d+$)'
    movie_df = df[df["movie"].str.extract(year_re)[0].notna()]
    return movie_df.reset_index(drop=True)


def create_csv(df: pd.DataFrame) -> None:
    """ Create a csv file from the filtered dataframe
    Preconditions:
    - df is a dataframe created by calling the above functions
    """
    df.to_csv("data/imdb_reviews.csv", sep="\t", index=False)


def create_json(df: pd.DataFrame) -> None:
    """ Create a JSON file from the filtered dataframe
    Preconditions:
    - df is a dataframe created by calling the above functions
    """
    df.to_json("data/imdb_reviews.json", orient='split', index=False)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['json', 'pandas'],
        'allowed-io': ['load_dataframe', 'load_sample'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
