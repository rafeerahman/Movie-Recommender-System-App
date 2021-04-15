"""CSC111 Winter 2021 Project Code

Instructions
===============================

This Python module uses University of Toronto's CSC111's assignment 3
visualization code, and adds some UI variable/UI changes.

The link to assignment 3 can be found here,
https://www.teach.cs.toronto.edu/~csc111h/winter/assignments/a3/handout/

Copyright and Usage Information
===============================

This file is Copyright (c) 2021
Rafee Rahman, Michael Galorro, Kimiya Raminrad, Mojan Majid
"""
import networkx as nx
from plotly.graph_objs import Scatter, Figure
import graph_construction

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
MOVIE_COLOUR = 'rgb(89, 205, 105)'
USER_COLOUR = 'rgb(105, 89, 205)'


def visualize_graph(graph: graph_construction.Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 1000) -> Figure:
    """ This code was written by following code from University of Toronto's
    CSC111, Assignment 3 code. More information can be found in our project report.

    Use plotly and networkx to visualize the given graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """
    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    kinds = [graph_nx.nodes[k]['kind'] for k in graph_nx.nodes]

    colours = [MOVIE_COLOUR if kind == 'movie' else USER_COLOUR for kind in kinds]

    x_edges = []
    y_edges = []
    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace3 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines',
                     name='edges',
                     line=dict(color=LINE_COLOUR, width=1),
                     hoverinfo='none',
                     )
    trace4 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker=dict(symbol='circle-dot',
                                 size=5,
                                 color=colours,
                                 line=dict(color=VERTEX_BORDER_COLOUR, width=0.5)
                                 ),
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data1 = [trace3, trace4]
    fig = Figure(data=data1)
    fig.update_layout(font=dict(color='white'),
                      paper_bgcolor='#191919',
                      plot_bgcolor='#191919', showlegend=False)
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    return fig


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['networkx', 'plotly.graph_objs', 'graph_construction'],
        'allowed-io': ['load_review_graph_json'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
