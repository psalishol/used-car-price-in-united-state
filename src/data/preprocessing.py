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
                    "franchise_dealer","front_legroom","fuel_tank_volume","height","length","franchise_make","savings_amount","transmission_display","trim_name","sp_name"
                    ]
    
    # Dropping the columns
    data = data.drop(columns=cols)
    # data = data.drop(cols, axis=1)
    
    # listed date to pandas datetime
    data["listed_date"] = pd.to_datetime(data["listed_date"])
    
    # Transforming
    data["transmission"] = data["transmission"].apply(lambda inf: str(inf).replace("A","Automatic").replace("M","Manual"))
    data["power"] = data["power"].apply(lambda inf: str(inf).split("@")[0].strip().split(" ")[0])
    data["torque"] = data["torque"].apply(lambda inf: str(inf).split("@")[0].strip().split(" ")[0])
    data["maximum_seating"] = data["maximum_seating"].apply(lambda inf: str(inf).strip().split(" ")[0])
    data["Listing_year"] = data["listed_date"].apply(lambda inf: inf.year)
    data["engine_displacement"] = data["engine_displacement"].apply(lambda inf: inf/1000)
    
    
    # Renaming some columns
    data = data.rename(columns={"wheel_system_display":"Drivetrain",
                                "transmission":"Transmission",
                                "body_type":"body_style",
                                "city_fuel_economy":"city_MPG",
                                "engine_displacement":"engine_size",
                                "highway_fuel_economy":"highway_MPG",
                                "year": "Vehicle_year"})
    
    return data
    
    
    
if __name__ == '__main__':
    DATAPATH = r"file path here"
    data = pd.read_csv(DATAPATH)
    # Cleaning the data
    cleanData = clean_data(data)