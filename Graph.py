"""CSC111 Winter 2021"""

from __future__ import annotations
import pandas as pd
from typing import Any, Union


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


def load_review_graph(df: pd.DataFrame) -> Graph:
    """Return a movie review graph from the given data set.

    Preconditions:
        - df is a dataframe returned by clean_dataframe
    """
    graph = Graph()

    for i in range(0, len(df['reviewer'])):
        reviewer = df['reviewer'][i]
        movie = df['movie'][i]
        rating = df['rating'][i]
        graph.add_vertex(reviewer, 'reviewer')
        graph.add_vertex(movie, 'movie')
        graph.add_edge(reviewer, movie, rating)

    return graph
