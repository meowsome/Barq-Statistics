from dash import Dash, html, dcc, Output, Input
from datetime import date
from functions.codes import country_codes
import json
import pickle

external_stylesheets = [{
    'href': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'rel': 'stylesheet',
    'crossorigin': 'anonymous'
}]

app = Dash(
    __name__,
    title="Barq Statistics",
    external_stylesheets=external_stylesheets,
    meta_tags=[{
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }, {
        'name': 'description',
        'content': 'Statistics on furries around the world'
    }, {
        'property': 'og:title',
        'content': 'Barq Statistics'
    }, {
        'property': 'og:description',
        'content': 'Statistics on furries around the world'
    }, {
        'property': 'og:url',
        'content': 'https://barq.meowso.me'
    }, {
        'property': 'og:type',
        'content': 'website'
    }, {
        'property': 'og:image',
        'content': 'https://barq.meowso.me/assets/logo.png'
    }]
)

print("Starting app")

def fetch_worldwide_graph(title):
    with open(f"pickle/{title}.pkl", "rb") as pickle_file:
        return pickle.load(pickle_file)

def generate_worldwide_graphs(country_code=None):
    graphs = [
        fetch_worldwide_graph("Most popular fursona per country"),
        fetch_worldwide_graph("Most popular age per country")
    ]

    if country_code == "US":
        graphs += [
            fetch_worldwide_graph("Most popular fursona per state"),
            fetch_worldwide_graph("Most popular age per state"),
            fetch_worldwide_graph("Most popular groups per state")
        ]

    return graphs

def fetch_stat(data_type, country_code):
    country = country_code if country_code else "null"
    with open(f"data/counts.json", "r") as data_file:
        data_dict = json.loads(data_file.read())
        return data_dict[country][data_type]

def generate_stat_cards(country_code=False):
    return [
        stat_card_generator("Total Furries", fetch_stat("total", country_code)),
        stat_card_generator("Unique Sona Species", fetch_stat("species", country_code))
    ]

def fetch_graph(title, country_code):
    country = f"in {country_codes[country_code]}" if country_code else "Worldwide"
    with open(f"pickle/{title} {country}.pkl", "rb") as pickle_file:
        return pickle.load(pickle_file)

def generate_country_graphs(country_code=False):
    country_graphs = [
        fetch_graph("Top Fursonas", country_code),
        fetch_graph("Orientation Breakdown", country_code),
        fetch_graph("Gender Breakdown", country_code),
        fetch_graph("Relationship Breakdown", country_code),
        fetch_graph("Location Type Breakdown", country_code),
        fetch_graph("Group Breakdown", country_code),
        fetch_graph("Language Breakdown", country_code),
        fetch_graph("Kink Breakdown", country_code),
        fetch_graph("Social Accounts Breakdown", country_code),
        fetch_graph("Distribution of ages capped at 100", country_code),
        fetch_graph("Distribution of sona counts", country_code)
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
            html.Div(id="worldwide-graphs", className="w10 wrapper-vertical", children=generate_worldwide_graphs())
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
    output=[Output('graphs', 'children'), Output('stat-cards', 'children'), Output('worldwide-graphs', 'children')],
    inputs=[Input('country_code', 'value')]
)
def update_output(value):
    return [generate_country_graphs(country_code=value), generate_stat_cards(country_code=value), generate_worldwide_graphs(country_code=value)]

if __name__ == '__main__':
    app.run_server(debug=True)