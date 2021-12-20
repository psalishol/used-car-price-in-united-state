import pandas as pd
import numpy as np
from partition import *

def clean_data(data):
    """Removing some irrelevant columns in the dataframe"""

    # Defining some columns to remove
    cols = ["vin", 'description', "exterior_color", "wheel_system", "vehicle_damage_category", "trimId",
            "theft_title", "sp_id", "main_picture_url", "longitude", "listing_id", "listing_color", "latitude",
                "interior_color", "cabin", "major_options", "back_legroom", "bed", "bed_height", "bed_length", "is_certified",
                    "is_cpo", "is_oemcpo", "salvage", "wheelbase", "width","combine_fuel_economy","daysonmarket","dealer_zip","engine_cylinders",
                    "franchise_dealer","front_legroom","fuel_tank_volume","height","length","franchise_make","savings_amount","transmission_display","trim_name"
                      ]   
    # Dropping the columns
    data = data.drop(columns=cols)
    # data = data.drop(cols, axis=1)
    
    # listed date to pandas datetime
    data["listed_date"] = pd.to_datetime(data["listed_date"])
    
    # For transforming power and torque
    def torque(feature):
        if feature == None:
            pass
        else:
            int(feature.split("@")[0].strip().split(" ")[0])
    def transmission(feature):
        if feature == None:
            pass
        else:
            feature.replace("A","Automatic").replace("M","Manual")
    def max_seating(feature):
        if feature == None:
            pass
        else:
            int(feature.strip().split(" ")[0])
            
    # Transforming
    data["transmission"] = data["transmission"].apply(transmission)
    data["power"] = data["power"].apply(torque)
    data["torque"] = data["torque"].apply(torque)
    data["maximum_seating"] = data["maximum_seating"].apply(max_seating)
    data["Listing_year"] = data["listed_date"].apply(lambda inf: inf.year)
    data["engine_displacement"] = data["engine_displacement"].apply(lambda inf: inf/1000)
    
    
    # Renaming some columns
    data = data.rename(columns={"wheel_system_display":"Drivetrain",
                                "transmission":"Transmission",
                                "body_type":"body_style",
                                "city_fuel_economy":"city_MPG",
                                "engine_displacement":"engine_size",
                                "highway_fuel_economy":"highway_MPG"})
    
    return data
    
    
if __name__ == '__main__':
    DATAPATH = r"file path here"
    data = pd.read_csv(DATAPATH)
    # Cleaning the data
    cleanData = clean_data(data)