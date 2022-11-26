from dash import Dash, html
from functions.retrieve_data import get_altered_df
from functions.graph_generator import generic_most_common, count_per_state, count_per_country, generic_map, generate_graph, generic_histogram
from datetime import date

app = Dash(__name__)

# df = get_altered_df()

import pickle

# with open("barq.pkl", 'wb') as pickle_file:
#     pickle.dump(df, pickle_file)

with open("barq.pkl", "rb") as pickle_file:
    df = pickle.load(pickle_file)

print("Starting app")

def stat_card_generator(title, stat):
    return html.Div(className="card w3", children=[
        html.Div(className="wrapper-vertical center", children=[
            html.H2(stat, className="center"),
            html.H4(title, className="center")
        ])
    ])

app.layout = html.Div(children=[
    html.H1(children='Barq Scraping Statistics'),

    html.Div(className="wrapper-vertical w10", children=[
        html.Div(className="wrapper-horizontal", children=[
            stat_card_generator("Total Furries", df.shape[0]),
            stat_card_generator("Unique Sona Species", df['sonas'].explode().nunique()),
            stat_card_generator("Countries with Furs", f"{df['countryCode'].nunique()} / 195")
        ]),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Top Fursonas", column="sonas", recursive=True, xlabel="Fursona", ylabel="Count"), height='150vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Orientation Breakdown", column="sexualOrientation", recursive=False, xlabel="Orientation", ylabel="Count"), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Gender Breakdown", column="genders", recursive=True, xlabel="Gender", ylabel="Count"), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Relationship Breakdown", column="relationshipStatus", recursive=False, xlabel="Relationship", ylabel="Count"), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Location Type Breakdown", column="type", recursive=False, xlabel="Location Type", ylabel="Count"), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Group Breakdown", column="groups", recursive=True, xlabel="Group", ylabel="Count"), height='150vh'),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Language Breakdown", column="languages", recursive=True, xlabel="Language", ylabel="Count"), height='150vh'),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Kink Breakdown", column="kinks", recursive=True, xlabel="Kink", ylabel="Count"), height='150vh'),
        generate_graph(figure=count_per_state(df)),
        generate_graph(figure=count_per_country(df)),
        generate_graph(figure=generic_map(df, scope="USA", column="sonas", recursive=True, title="Most popular fursona per state")),
        generate_graph(figure=generic_map(df, scope="world", column="sonas", recursive=True, title="Most popular fursona per country")),
        generate_graph(figure=generic_map(df, scope="USA", column="groups", recursive=True, title="Most popular groups per state")),
        generate_graph(figure=generic_map(df, scope="USA", column="age", recursive=False, title="Most popular age per state")),
        generate_graph(figure=generic_map(df, scope="world", column="age", recursive=False, title="Most popular age per country")),
        generate_graph(figure=generic_histogram(df, column="age", title="Distribution of ages capped at 100", cap=100)),
        generate_graph(figure=generic_histogram(df, column="sonas", title="Distribution of sona counts", cap=100, bins=75, getlen=True)),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Social Accounts Breakdown", column="socialAccounts", recursive=True, xlabel="Service", ylabel="Count")),
    ]),

    html.Footer(className="w5 wrapper-vertical left", children=[
        html.Div(className="p1", children=[
            html.A(className="center left", href="https://meowso.me", target="_blank", children=[
                f"Barq Statistics © {date.today().year}",
                html.Img(src="/assets/meowsome.png"),
                "meowsome studio",
            ]),
            html.P(f"Barq © {date.today().year} <insert name here>")
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)