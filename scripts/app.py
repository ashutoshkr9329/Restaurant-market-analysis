# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
# from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
# Incorporate data
df = pd.read_csv('Restaurants_clean.csv')


'''Columns: ['Outlet', 'Restaurant Name', 'City', 'Address', 'Coordinates',
       'Latitude', 'Longitude', 'Dine In - Yearly Revenue',
       'Dine In - Yearly Cost', 'Dine In - Yearly Total Number of Orders',
       'Home Delivery - Yearly Revenue', 'Home Delivery - Yearly Cost',
       'Home Delivery - Yearly Total Number of Orders', 'Total Yearly Revenue',
       'Total Yearly Cost', 'Total Yearly Number of Orders', 'Total Revenue / Cost Ratio']'''

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


fig2 = px.scatter(df, x="Total Yearly Revenue", y="Total Yearly Cost",
                 size="Total Yearly Number of Orders", color="Restaurant Name", hover_name="Outlet",
                 log_x=True, size_max=60, title="Bubble Chart Distribution")

fig3 = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Total Revenue / Cost Ratio', radius=10,
                        center=dict(lat=28.63, lon=77.21), zoom=11,
                        mapbox_style="stamen-terrain", title="Revenue/Cost HeatMap", color_continuous_scale='YlOrRd')
fig4 = px.density_mapbox(df, lat='Latitude', lon='Longitude', z='Total Yearly Number of Orders', radius=20,
                        center=dict(lat=28.63, lon=77.21), zoom=11,
                        mapbox_style="stamen-terrain", title="Total Yearly Number of Orders HeatMap",
                         color_continuous_scale='YlOrRd')


fig7 = px.histogram(df, x="Restaurant Name", color="City",
                   title="Restaurant Wise City Distribution",
                   nbins=20, barmode='group',
                   labels={'Restaurant Name': 'Restaurant Name', 'count': 'Count', 'City': 'City'})
fig8 = px.histogram(df, x="City", color="Restaurant Name",
                   title="City Wise Restaurant Distribution",
                   nbins=20, barmode='group',
                   labels={'City': 'City', 'count': 'Count', 'Restaurant Name': 'Restaurant Name'})


@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):

    fig = px.histogram(df, x='Restaurant Name', y=col_chosen, histfunc='sum', title="Selection Chart/Comparative Graph")
    fig.update_yaxes(tickprefix='₹',tickformat='.0f')
    return fig


@callback(
    Output(component_id='controls-and-graph2', component_property='figure'),
    Input(component_id='controls-and-radio-item2', component_property='value')
)
def update_graph2(col_chosen):
    fig5 = px.scatter(df, x="Total Yearly Revenue", y=col_chosen, animation_frame="Restaurant Name",
                      animation_group="Restaurant Name", size="Total Yearly Number of Orders", color="City",
                      hover_name="Outlet", log_x=True, size_max=55, range_x=[10000000, 1000000000],
                      range_y=[1000000, 100000000], title="Data Distribution")
    fig5.update_yaxes(tickprefix='₹', tickformat='.0f')

    return fig5



# App layout
app.layout = html.Div([
    html.Div(children='Statistical App with Data, Graph, and Controls'),
    html.Hr(),
    dcc.RadioItems(options=['Total Yearly Revenue','Total Yearly Cost',
                            'Dine In - Yearly Revenue','Dine In - Yearly Cost',
                            'Dine In - Yearly Total Number of Orders','Home Delivery - Yearly Revenue',
                            'Home Delivery - Yearly Cost','Home Delivery - Yearly Total Number of Orders',
                            'Total Yearly Number of Orders'],
                   value='Total Yearly Revenue', id='controls-and-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph'),
    # dcc.Graph(
    #     id='AutoPlay Map',
    #     figure=fig5
    # ),
    dcc.RadioItems(options=['Total Yearly Revenue', 'Total Yearly Cost',
                            'Dine In - Yearly Revenue', 'Dine In - Yearly Cost',
                            'Dine In - Yearly Total Number of Orders', 'Home Delivery - Yearly Revenue',
                            'Home Delivery - Yearly Cost', 'Home Delivery - Yearly Total Number of Orders',
                            'Total Yearly Number of Orders'],
                   value='Total Yearly Revenue', id='controls-and-radio-item2'),
    dcc.Graph(
        id='controls-and-graph2',
        figure={}
    ),
    dcc.Graph(
        id='rest_groupby_bar',
        figure=fig7
    ),
    dcc.Graph(
        id='city_groupby_bar',
        figure=fig8
    ),
    dcc.Graph(
        id='density_mapbox',
        figure=fig3
    ),
    dcc.Graph(
        id='orders_mapbox',
        figure=fig4
    )
])
#


if __name__ == '__main__':
    print("Running")
    app.run_server()


