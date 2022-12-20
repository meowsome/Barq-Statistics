from functions.graph_generator import generic_most_common, generate_graph, generic_histogram, get_count, get_sona_count
from functions.codes import country_codes
import pickle
import json
from tqdm import tqdm

# df = get_altered_df()

# with open("barq.pkl", 'wb') as pickle_file:
#     pickle.dump(df, pickle_file)

with open("barq.pkl", "rb") as pickle_file:
    df = pickle.load(pickle_file)

# worldwide_graphs = [
#     generate_graph(figure=count_per_country(df)),
#     generate_graph(figure=generic_map(df, scope="world", column="sonas", recursive=True, title="Most popular fursona per country")),
#     generate_graph(figure=generic_map(df, scope="world", column="age", recursive=False, title="Most popular age per country")),
#     generate_graph(figure=count_per_state(df)),
#     generate_graph(figure=generic_map(df, scope="USA", column="sonas", recursive=True, title="Most popular fursona per state")),
#     generate_graph(figure=generic_map(df, scope="USA", column="age", recursive=False, title="Most popular age per state")),
#     generate_graph(figure=generic_map(df, scope="USA", column="groups", recursive=True, title="Most popular groups per state")),
# ]

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

countries = list(country_codes.keys()) + [None]
counts = {country: {"total": None, "species": None} for country in countries}
for country in tqdm(countries):
    for graph in generate_country_graphs(country_code=country):
        with open(f"pickle/{graph.figure['layout']['title']['text']}.pkl", 'wb') as pickle_file:
            pickle.dump(graph, pickle_file)
    counts[country]['total'] = get_count(df, country)
    counts[country]['species'] = get_sona_count(df, country)

with open("data/counts.json", "w") as data_file:
    json.dump(counts, data_file)