from collections import Counter
import plotly.express as px
import pandas as pd
from .codes import state_codes, country_codes, top_per_country, top_per_state
from dash import dcc

def generate_graph(figure, height='90vh'):
    return dcc.Graph(figure=figure, config={'displaylogo': False}, style={'width': '100%', 'height': height}, className="card")

def titleize(bad_list):
    return [item.title().replace("_", " ") for item in bad_list]

def make_most_common(df, column, count, recursive):
    common_list = []
    if recursive:
        for items in df[column].dropna().tolist():
            if items is not None:
                common_list += titleize(items)
    else:
        common_list = [item for item in titleize(df[column].dropna().tolist()) if item is not None]

    return Counter(common_list).most_common(count)

def counter_to_df(counter, xlabel, ylabel):
    return pd.DataFrame.from_records(list(dict(counter).items()), columns=[xlabel, ylabel])

def make_bar_chart(most_common, title, xlabel, ylabel):
    most_common = list(reversed(most_common))
    most_common = counter_to_df(most_common, xlabel, ylabel)

    fig = px.bar(most_common, x=ylabel, y=xlabel, orientation='h', title=title, height=750)
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    return fig

def make_pie_chart(most_common, title, xlabel, ylabel):
    # Convert counter to df
    most_common = pd.DataFrame.from_records(list(dict(most_common).items()), columns=[xlabel, ylabel])

    fig = px.pie(most_common, values=ylabel, names=xlabel, title=title)
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    return fig

def generic_most_common(df, count, chart_type, title, column, recursive, xlabel, ylabel):
    most_common = make_most_common(df, column, count, recursive)
    
    if chart_type == "bar":
        return make_bar_chart(most_common, title, xlabel, ylabel)
    else:
        return make_pie_chart(most_common, title, xlabel, ylabel)

def plot_map(thing_per_state, title, column_name, chart_type="USA"):
    states = chart_type == "USA"
    fig = None

    if states:
        fig = px.choropleth(
            thing_per_state,
            title=title,
            locations='state',
            locationmode='USA-states',
            scope='usa',
            color=column_name,
            color_continuous_scale="Viridis_r"
        )
    else:
        fig = px.choropleth(
            thing_per_state,
            projection='orthographic',
            title=title,
            locations='country', 
            locationmode="country names", 
            scope='world',
            color=column_name,
            color_continuous_scale="Viridis_r"
        )
    
    fig.update_layout(margin=dict(
        t=50, # 50px margin above graph to show image
        l=0,
        r=0,
        b=50, # 50px margin below graph
        pad=0
    ),
    autosize=True)

    return fig

def count_per_state(df):
    column_per_state = {}

    states = list(set(df['region'].tolist()))

    for state in states:
        people_in_state = df[df['region'] == state]
        column_per_state[state] = people_in_state.shape[0]

    column_per_state = {'state': [state_codes[state] for state in column_per_state if state in state_codes], 'count': [column_per_state[state] for state in column_per_state if state in state_codes]}
    count_per_state = pd.DataFrame(column_per_state)

    return plot_map(count_per_state, 'Count per state', 'count')

def count_per_country(df):
    column_per_country = {}

    countries = list(set(df['countryCode'].tolist()))

    for country in countries:
        people_in_country = df[df['countryCode'] == country]
        column_per_country[country] = people_in_country.shape[0]


    column_per_country = {'country': [country_codes[country] for country in column_per_country if country in country_codes], 'count': [column_per_country[country] for country in column_per_country if country in country_codes]}
    count_per_country = pd.DataFrame(column_per_country)
    return plot_map(count_per_country, 'Count per country', 'count', chart_type='world')

def generic_map(df, scope, column, recursive, title):
    thing_per_state = top_per_state(df, column, recursive) if scope == "USA" else top_per_country(df, column, recursive)
    return plot_map(thing_per_state, title, column, chart_type=scope)

def generic_histogram(df, column, title, cap=None, bins=50, getlen=False):
    # Modify column of strings to column of string lengths
    if getlen:
        df[column] = df[column].str.len()
    # Collect all points above specified value into one
    if cap:
        df[column] = df[column].apply(lambda item: item if item < cap else cap)

    fig = px.histogram(df, x=column, title=title, nbins=bins)

    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    return fig