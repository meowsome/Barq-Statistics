from dash import Dash, html, dcc
from functions.retrieve_data import get_altered_df
from functions.graph_generator import generic_most_common, count_per_state, count_per_country, generic_map

app = Dash(__name__)

# df = get_altered_df()

import pickle

# with open("barq.pkl", 'wb') as pickle_file:
#     pickle.dump(df, pickle_file)

with open("barq.pkl", "rb") as pickle_file:
    df = pickle.load(pickle_file)

print("Starting app")

app.layout = html.Div(children=[
    html.H1(children='Barq Scraping Statistics'),


    html.Div(children=[
        dcc.Graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Top Fursonas", column="sonas", recursive=True, xlabel="Fursona", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=50, chart_type="bar", title="Top States", column="region", recursive=False, xlabel="State", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Orientation Breakdown", column="sexualOrientation", recursive=False, xlabel="Orientation", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Gender Breakdown", column="genders", recursive=True, xlabel="Gender", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Relationship Breakdown", column="relationshipStatus", recursive=False, xlabel="Relationship", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Location Type Breakdown", column="type", recursive=False, xlabel="Location Type", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Group Breakdown", column="groups", recursive=True, xlabel="Group", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=20, chart_type="bar", title="Event Breakdown", column="events", recursive=True, xlabel="Event", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Language Breakdown", column="languages", recursive=True, xlabel="Language", ylabel="Count")),
        dcc.Graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Kink Breakdown", column="kinks", recursive=True, xlabel="Kink", ylabel="Count")),
        dcc.Graph(figure=count_per_state(df)),
        dcc.Graph(figure=count_per_country(df)),
        dcc.Graph(figure=generic_map(df, scope="USA", column="sonas", recursive=True, title="Most popular fursona per state")),
        dcc.Graph(figure=generic_map(df, scope="world", column="sonas", recursive=True, title="Most popular fursona per country")),
        dcc.Graph(figure=generic_map(df, scope="USA", column="events", recursive=True, title="Most popular event per state")),
        dcc.Graph(figure=generic_map(df, scope="USA", column="groups", recursive=True, title="Most popular groups per state")),
        dcc.Graph(figure=generic_map(df, scope="USA", column="age", recursive=False, title="Most popular age per state")),
        dcc.Graph(figure=generic_map(df, scope="world", column="age", recursive=False, title="Most popular age per country")),

        # Histogram of age
        # Most Common Social Accounts
        # Histogram of count of fursonas people have
        

    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)