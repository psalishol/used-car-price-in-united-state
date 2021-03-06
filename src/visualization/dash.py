from logging import debug
import pgeocode
import os
import dash
import numpy as np
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State

# For making longitude and Latitude from zip code
nomi = pgeocode.Nominatim('us')

app = dash.Dash(__name__)
server = app.server


#--------- Loading the dataset ---------------#
def concat_data(FILE_DIR):
    N_SAMPLE = len(os.listdir(FILE_DIR))
    data = pd.read_csv(os.path.join(FILE_DIR,"used_data_0.csv"), delimiter=",")
    for i in range(1, N_SAMPLE):
        new_data = pd.read_csv(os.path.join(FILE_DIR,"used_data_{}.csv".format(i)), delimiter=",")
        data = pd.concat([data,new_data],axis=0)
        
    return data


##------- Creating data for the dashboard ----------##
FILEPATH = r"..\Data\Dashboard data"
data_ = concat_data(FILEPATH)


# Model list for the vehicle
make_list = [feature for feature in sorted(list(data_["make_name"].unique()),reverse=False) 
                    if len(data_[data_["make_name"] == feature]) > 1000]
#----> App layout

app.layout = html.Div(
    [
        dcc.Store(id='aggregate_data'),
        html.Div(
            [
                html.Div(
                    [
                        html.H2("Value Insight", id="header-text"),
        
                    ],
                )
            ],
            className= "header"
        ),
        
        html.Div(
            [
                html.Div(
                    [
                        # Dropdown for selecting Vehicle make
                        html.Label("Vehicle Make",id="make_label"),
                        dcc.Dropdown(
                            id="dropdown_make",
                            options = [{"label":i,"value":i} for i in make_list],
                            className="dcc_control"
                        ),
                        
                        # Dropdown for selecting Feature to compare price with
                        html.Label("Choose Feature to Compare",id="feature_label"),
                        dcc.Dropdown(
                            id="dropdown_comp",
                            options=[{"label": i,"value": i} for i in data_.columns 
                                            if data_[i].dtype == object],
                            value="Transmission",
                            className="dcc_control"
                        ),
                    ]
                )
            ]
        ),
        
        html.Div(
            [
                # For Model slot
                html.Div(
                    [
                        html.P("Make", id="make_text"),
                        html.H6(
                            id="model_text",
                            className= "info_text"
                        )
                    ],
                    id="model",
                    className="container_card"
                ),
        
        
                # For displaying the Avg price
                html.Div(
                    [
                        html.P("Avg Price", id="card-detail"),
                        html.H6(
                            id="avg_price_text",
                            className= "info_text"
                        )
                    ],
                    id="avg_price",
                    className= "container_card"
                )
        
            ],
            className = "row"
        ),
    
        # For plotting the second row
        html.Div(
            [
                # Plotting the bar graph
                html.Div(
                    [
                        dcc.Graph(id="lineplot_graph")
                    ],
                    className="container second col"
                )
            ],
            className="row"
        ),
    
        # For ploting barplot and barplot
        html.Div(
            [
                
                # Plotting the pieplot
                html.Div(
                    [
                        html.Label("Year", id="year_label"),
                        dcc.Dropdown(
                            id="select_year_dropdown",
                            options= [{"label": int(i), "value": int(i) } for i in 
                                      sorted([feature for feature in data_["listed_year"].unique()], reverse=False)],
                            value= 2020
                            ),
                        dcc.Graph(id="pieplot_graph")
                    ],
                    className="container first col"
                ),

                # Plotting the bar graph
                html.Div(
                    [
                        dcc.Graph(id="barplot_graph")
                    ],
                    className="container second col"
                ),
            ],
            className="row"
        ),
    
        # For Displaying Geographical Location
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="satelite_view")
                    ]
                )
            ]
        ),


        # For Plotting all make with price
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="make_price")
                    ],
                    className ="container last row"
                )
            ],
            className= "row2"
        )
    ]
)



#----> Helper functions
@app.callback(Output("model_text","children"),
              [Input("dropdown_make","value")])
def update_avg_price(value):
    if value is None:
        return "None"
    else:
        return value

#----> Updating the Card

@app.callback(Output("avg_price_text","children"),
              [Input("dropdown_make","value")])
def update_price_text(value):
    if value is None:
        return "0"
    else:
        name = data_.groupby("make_name")["price"].mean().to_frame()
        val = str(int(name[data_.groupby("make_name")["price"].mean().index == value].values))
        # formating the Price
        if len(val) == 5:
            return val[0:2]+","+val[2:]
        elif len(val) == 6:
            return val[0:3]+","+val[3:]
        elif len(val) == 7:
            return val[0]+","+val[1:4]+","+val[4:]  
 
        
#----> Callback for Barplot for features

@app.callback(Output("lineplot_graph","figure"),
              [Input("dropdown_make","value"),
               Input("dropdown_comp","value")]
              )
def update_barplot(selected_make,selected_comp):
    data_filtered = data_[data_["make_name"] == selected_make]
    # If nothing is selected
    if selected_comp == None:
        fig =px.bar(
        x=data_.groupby("transmission")["price"].mean().index, y=data_.groupby("transmission")["price"].mean().values)
        return fig
    else:
        fig =px.bar(
            x=data_filtered.groupby(selected_comp)["price"].mean().index, y=data_filtered.groupby(selected_comp)["price"].mean().values)
        return fig


#----> Callback for Pie plot 

# Making pie plot for displaying the features and the mean price
@app.callback(Output(component_id="pieplot_graph", component_property="figure"),
              [Input(component_id="dropdown_make", component_property="value"),
               Input(component_id="dropdown_comp", component_property="value"),
               Input(component_id="select_year_dropdown", component_property="value")]
)
def make_pie(selected_make,selected_comp, selected_year):
    
    # Making a filtered dataset
    data_filtered = data_[(data_["make_name"] == selected_make) & (data_["year"] == selected_year)]
    selected = []   # This would be our name for the pieplot
    price_val = []  # This would be the value for the pieplot
    
    data_n = data_filtered.groupby(selected_comp)["price"].mean()
    data_val = data_n.to_dict()
    for fea,price in zip(data_val.keys(),data_val.values()):
        selected.append(fea)
        price_val.append(price)
        
    # Making new dataframe from the list
    data_l = {
        "make": selected,
        "Price": price_val
    }
    df = pd.DataFrame(data_l)
        
    fig = px.pie(data_frame=df, names="make",values="Price")    
    return fig


#---> Callback for updating barplot with year and features

@app.callback(Output(component_id="barplot_graph",component_property="figure"),
              [Input(component_id="dropdown_make",component_property="value"),
               Input(component_id="dropdown_comp",component_property="value")]
              )
def update_barplot_model(selected_make,selected_val):
    selected = []
    year = []
    price = []
    # Making a filtered dataframe
    data_filtered = data_[data_["make_name"] == selected_make]    
    grouped_d = data_filtered.groupby(["year",selected_val])["price"].mean().to_dict()
    for key_p,val_p in zip(grouped_d.keys(),grouped_d.values()):
        year.append(key_p[0])
        selected.append(key_p[1])
        price.append(val_p)
    
    # Plotting the graph
    fig =px.bar(
            x=year,y=price, color=selected, title=f"{selected_make}")
    return fig




#----> Callaback for updating satelite
# @app.callback(Output(component_id="satelite_view",component_property="figure"),
#               Input(component_id="dropdown_make",component_property="value"))
# def update_satelite(selected_make):
    
#     data_filtered = data_[data_['Vehicle Make'] == selected_make]
#     traces = []
#     # Creating access token for mapbox
#     mapbox_access_token = "sk.eyJ1IjoicHNhbGlzaG9sIiwiYSI6ImNrdTZydGhjMjFxbXEycXFrdmd0OWxnMmYifQ.KKXofcYq04f1MiPOIcitQQ"
#     # Layout for the Map
#     layout = dict(
#         autosize=True,
#         automargin=True,
#         margin=dict(
#             l=30,
#             r=30,
#             b=20,
#             t=40
#         ),
#         hovermode="closest",
#         plot_bgcolor="#F9F9F9",
#         paper_bgcolor="#F9F9F9",
#         legend=dict(font=dict(size=10), orientation='h'),
#         title='Satellite Overview',
#         mapbox=dict(
#             accesstoken=mapbox_access_token,
#             style="dark",
#             center=dict(
#                 lon=-78.05,
#                 lat=42.54
#             ),
#             zoom=7,
#         )
#     )
#     trace = dict(
#             type='scattermapbox',
#             lon=data_filtered['Longitude'],
#             lat=data_filtered['Latitude'],
#             marker=dict(
#                 size=4,
#                 opacity=0.6,
#             )
#         )
    
#     figure = dict(data=trace, layout=layout)
    
#     return figure
        
    

    
#----> Callback for updating Barplot with Make as x

@app.callback(Output(
    component_id="make_price",component_property="figure"),
              Input(
                  component_id="dropdown_comp",component_property="value"
              ))
def update_model(selected_co):
    V_price = []
    v_make = []
    color = []
    # Making a copy of the dataset
    new_d = data_.copy()
    mk_grouped = new_d.groupby(["make_name",selected_co])["price"].mean()
    dict_val = mk_grouped.to_dict()
    for make,price in zip(dict_val.keys(),dict_val.values()):
        v_make.append(make[0])
        color.append(make[1])
        V_price.append(price)
    #Plotting the bar plot for showing the make and price 
    fig = px.bar(x=v_make, y=V_price,color=color, title='Vehicle Make with the price')
    
    return fig

if __name__ == '__main__':
    
    FILEPATH = r"C:\Users\PSALISHOL\Documents\My Projects\Car Prediction\Data\Dashboard data"
    # data_ = concat_data(FILEPATH)
    # app.run_server(debug=True)
    os.listdir(FILEPATH)