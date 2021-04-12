"""CSC111 Winter 2021"""

from __future__ import annotations
import pandas as pd
from typing import Any, Union
import csv
import json


class _Vertex:
    """A vertex in a movie review graph, used to represent a reviewer or a movie.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'reviewer', 'movie'}
    """
    item: Any
    kind: str
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'reviewer', 'movie'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def reviewer_similarity_score(self, other: _Vertex):
        """Return the similarity score between this vertex and other.

        Similarity score is based on how many movies both reviewers rated, and if those scores are
        similar.

        Preconditions:
            - self.kind == 'reviewer'
            - other.kind == 'reviewer'
        """
        if self.degree == 0 or other.degree == 0:
            return 0.0
        else:
            set_1 = set(self.neighbours)
            set_2 = set(other.neighbours)
            same_neighbours = set.intersection(set_1, set_2)
            sim_score_so_far = 0

            for vertex in same_neighbours:
                # 'bothered reviewing' bonus:
                sim_score_so_far += 1
                # 'love' bonus
                if self.neighbours[vertex] >= 9 and other.neighbours[vertex] >= 9:
                    sim_score_so_far += 2
                # 'like' bonus
                elif self.neighbours[vertex] >= 7 and other.neighbours[vertex] >= 7:
                    sim_score_so_far += 1
                # 'dumpster dive' bonus
                elif self.neighbours[vertex] <= 4 and other.neighbours[vertex] <= 4:
                    sim_score_so_far += 1
                # 'great minds' bonus
                if self.neighbours[vertex] != 10 and \
                        self.neighbours[vertex] == other.neighbours[vertex]:
                    sim_score_so_far += 2

            return sim_score_so_far / min(self.degree(), other.degree())


class Graph:
    """A weighted graph used to represent a network of movie reviews which keeps track of ratings.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph, with no vertices or edges."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'reviewer', 'movie'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float]) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'reviewer', 'movie'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_similarity_score(self, reviewer1: Any, reviewer2: Any) -> float:
        """Return the similarity score between the two given reviewers in this graph.

        Raise a ValueError if reviewer1 or reviewer2 do not appear as vertices in this graph.
        """
        vertices = self.get_all_vertices()
        if reviewer1 not in vertices or reviewer2 not in vertices:
            raise ValueError
        else:
            v1 = self._vertices[reviewer1]
            v2 = self._vertices[reviewer2]
            return v1.reviewer_similarity_score(v2)


def load_review_graph_df(df: pd.DataFrame, threshold: int = 0) -> Graph:
    """Return a movie review graph from the given data set. Only includes reviewers with more
    reviews than the given threshold. Default threshold is 0.

    Preconditions:
        - df is a dataframe returned by clean_dataframe
    """
    graph = Graph()
    reviewers = {}

    for i in range(0, len(df['reviewer'])):
        reviewer = df['reviewer'][i]
        movie = df['movie'][i]
        rating = df['rating'][i]

        if reviewer not in reviewers:
            reviewers[reviewer] = [(movie, rating)]
        else:
            reviewers[reviewer].append((movie, rating))

    for reviewer in reviewers:
        if len(reviewers[reviewer]) > threshold:
            graph.add_vertex(reviewer, 'reviewer')
            for movie in reviewers[reviewer]:
                rating = int(movie[1])
                graph.add_vertex(movie[0], 'movie')
                graph.add_edge(reviewer, movie[0], rating)

    return graph


def create_json(df: pd.DataFrame) -> None:
    """ Create a csv file from the filtered dataframe
    Preconditions:
    - df is a dataframe created by calling the above functions
    """
    df.to_json("data/imdb_reviews.json", orient='split', index=False)


def load_review_graph_json(reviews_file: str, threshold: int = 0):
    """Return a movie review graph from the given data set. Only includes reviewers with more
    reviews than the given threshold. Default threshold is 0.

        Preconditions:
            - reviews_file is a JSON file returned by create_json
    """
    graph = Graph()
    reviewers = {}

    with open(reviews_file) as json_file:
        data = json.load(json_file)

        for review in data['data']:
            reviewer = review[0]
            movie = review[1]
            rating = int(review[2])

            if reviewer not in reviewers:
                reviewers[reviewer] = [(movie, rating)]
            else:
                reviewers[reviewer].append((movie, rating))

    for reviewer in reviewers:
        if len(reviewers[reviewer]) > threshold:
            graph.add_vertex(reviewer, 'reviewer')
            for movie in reviewers[reviewer]:
                rating = int(movie[1])
                graph.add_vertex(movie[0], 'movie')
                graph.add_edge(reviewer, movie[0], rating)

    return graph
