from dash import Dash, html, dcc, Output, Input, DiskcacheManager
from functions.retrieve_data import get_altered_df
from functions.graph_generator import generic_most_common, count_per_state, count_per_country, generic_map, generate_graph, generic_histogram, get_count, get_sona_count
from datetime import date
from functions.codes import country_codes
import diskcache

external_stylesheets = [{
    'href': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'rel': 'stylesheet',
    'crossorigin': 'anonymous'
}]

app = Dash(
    __name__,
    background_callback_manager=DiskcacheManager(diskcache.Cache("./cache")),
    title="Barq Statistics",
    external_stylesheets=external_stylesheets
)

# df = get_altered_df()

import pickle

# with open("barq.pkl", 'wb') as pickle_file:
#     pickle.dump(df, pickle_file)

with open("barq.pkl", "rb") as pickle_file:
    df = pickle.load(pickle_file)

print("Starting app")

# worldwide_graphs = [
#     generate_graph(figure=count_per_country(df)),
#     generate_graph(figure=generic_map(df, scope="world", column="sonas", recursive=True, title="Most popular fursona per country")),
#     generate_graph(figure=generic_map(df, scope="world", column="age", recursive=False, title="Most popular age per country")),
#     generate_graph(figure=count_per_state(df)),
#     generate_graph(figure=generic_map(df, scope="USA", column="sonas", recursive=True, title="Most popular fursona per state")),
#     generate_graph(figure=generic_map(df, scope="USA", column="age", recursive=False, title="Most popular age per state")),
#     generate_graph(figure=generic_map(df, scope="USA", column="groups", recursive=True, title="Most popular groups per state")),
# ]

def generate_stat_cards(country_code=False):
    return [
        stat_card_generator("Total Furries", get_count(df, country_code=country_code), country_code=country_code),
        stat_card_generator("Unique Sona Species", get_sona_count(df, country_code=country_code), country_code=country_code)
    ]

def generate_country_graphs(country_code=False):
    country_graphs = [
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Top Fursonas", column="sonas", recursive=True, xlabel="Fursona", ylabel="Count", country_code=country_code), height='150vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Orientation Breakdown", column="sexualOrientation", recursive=False, xlabel="Orientation", ylabel="Count", country_code=country_code), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Gender Breakdown", column="genders", recursive=True, xlabel="Gender", ylabel="Count", country_code=country_code), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Relationship Breakdown", column="relationshipStatus", recursive=False, xlabel="Relationship", ylabel="Count", country_code=country_code), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=10, chart_type="pie", title="Location Type Breakdown", column="type", recursive=False, xlabel="Location Type", ylabel="Count", country_code=country_code), height='100vh'),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Group Breakdown", column="groups", recursive=True, xlabel="Group", ylabel="Count", country_code=country_code), height='150vh'),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Language Breakdown", column="languages", recursive=True, xlabel="Language", ylabel="Count", country_code=country_code), height='150vh'),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Kink Breakdown", column="kinks", recursive=True, xlabel="Kink", ylabel="Count", country_code=country_code), height='150vh'),
        generate_graph(figure=generic_most_common(df, count=30, chart_type="bar", title="Social Accounts Breakdown", column="socialAccounts", recursive=True, xlabel="Service", ylabel="Count", country_code=country_code)),
        generate_graph(figure=generic_histogram(df, column="age", title="Distribution of ages capped at 100", cap=100, country_code=country_code)),
        generate_graph(figure=generic_histogram(df, column="sonas", title="Distribution of sona counts", cap=100, bins=75, getlen=True, country_code=country_code)),
    ]

    return country_graphs

def stat_card_generator(title, stat, country_code=False):
    if country_code:
        title += f" in {country_codes[country_code]}"

    return html.Div(className="card w3", children=[
        html.Div(className="wrapper-vertical center p1", children=[
            html.H1(stat, className="center"),
            html.H4(title, className="center")
        ])
    ])

app.layout = html.Div(children=[
    html.Header(className="p1 left wrapper-vertical", children=[
        html.Div(className="wrapper-horizontal center left", children=[
            html.Img(src="/assets/logo.png"),
            html.H2("Barq Scraping Statistics")
        ]),
    ]),
    html.Div(className="card w5", children=[
        html.Div(className="p1 left wrapper-vertical", children=[
            html.Div(children=[
                html.H3("Information"),
                html.P("Barq is an app for furries to connect with one another based on location. For this project, profile information was collected for a subset of all Barq users. This information was used to perform analytics and statistics. No individual user was singled out in this project.")
            ]),
            html.A(href="#info", className="href-button", children=["Click here to read more"])
        ])
    ]),

    html.Div(className="wrapper-vertical w10", children=[
        html.Div(className="card", children=[
            html.Div(className="p1", children=[
                html.H3("Specify Country"),
                dcc.Dropdown(id="country_code", options=country_codes, searchable=True, clearable=True)
            ])
        ]),

        html.Div(id="loading", className="hidden", children=[
            html.Div(className="wrapper-horizontal center w10", children=[
                html.I(className="fa-3x fa fa-paw fa-spin p3")
            ])
        ]),

        html.Div(id="graphs-wrapper", children=[
            html.Div(id="stat-cards", className="w10 wrapper-horizontal", children=generate_stat_cards()),
            html.Div(id="graphs", className="w10 wrapper-vertical", children=generate_country_graphs()),
            # html.Div(id="worldwide-graphs", className="w10 wrapper-vertical", children=worldwide_graphs)
        ]),

        html.Div(id="info", className="card w5", children=[
            html.Div(className="p1 left wrapper-vertical", children=[
                html.Div(children=[
                    html.H3("Scraping Process"),
                    html.P("Some tools that were used: Android Studio, Charles, Plotly, Pandas, Numpy"),
                    html.Ol(children=[
                        html.Li("Android Studio was used used to run the Barq app on a desktop environment"),
                        html.Li("Charles was used to sniff packets sent to the Barq API from the Barq app"),
                        html.Li("The Barq API URLs were analyzed to determine their inputs and outputs"),
                        html.Li("A set of popular locations in the U.S. and other regions around the world were created"),
                        html.Li("For each location, IDs of 10,000 users in the surrounding area were saved"),
                        html.Li("A Raspberry Pi was set up with a fresh Barq account to send GET requests using the algorithm described above"),
                        html.Li("All data was combined and cleaned, and duplicate users were removed")
                    ])
                ]),
                html.Div(children=[
                    html.H3("Why?"),
                    html.P("Barq accounts contain information for real furs around the world. By performing statistics on this data, unique geographical and other patterns can be observed for real furs.")
                ]),
                html.Div(children=[
                    html.H3("Ethics"),
                    html.P("All data was collected legally and user profiles are stored anonymously by removing usernames and user IDs after all data was collected. Statistics are kept broad. No particular user was singled out in these statistics. All data collected was publicly accessible data")
                ])
            ])
        ])
    ]),

    html.Footer(className="w5 wrapper-vertical left", children=[
        html.Div(className="p1", children=[
            html.A(className="center left", href="https://meowso.me", target="_blank", children=[
                f"Barq Statistics © {date.today().year}",
                html.Img(src="/assets/meowsome.png"),
                "meowsome studio",
            ]),
            html.P(f"Barq © {date.today().year} barq.app")
        ])
    ])
])

# Toggle the "hidden" class name for the interactive and image maps 
@app.callback(
    output=[Output('graphs', 'children'), Output('stat-cards', 'children')],
    inputs=[Input('country_code', 'value')],
    background=True,
    running=[
        (Output("country_code", "disabled"), True, False), # ID, attribute, running action, finished action
        (Output("graphs-wrapper", "className"), "hidden", ""),
        (Output("loading", "className"), "", "hidden")
    ]
)
def update_output(value):
    return [generate_country_graphs(country_code=value), generate_stat_cards(country_code=value)]

if __name__ == '__main__':
    app.run_server(debug=True)