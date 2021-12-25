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
    
    
    # Changing series type to actual datatype
    
    
    # Renaming some columns
    data = data.rename(columns={"wheel_system_display":"Drivetrain",
                                "transmission":"Transmission",
                                "body_type":"body_style",
                                "city_fuel_economy":"city_MPG",
                                "engine_displacement":"engine_size",
                                "highway_fuel_economy":"highway_MPG",
                                "year": "Vehicle_year"})
    
    return data

def impute_missing_values(new_data, verbose: int):
    """Dealing with the missing values by imputation"""
    # Performing input validation
    if (verbose not in [0, 1]):
        raise TypeError("Code ran into an Exception \
                        Because verbose is either a string or not 0 or 1")
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder
    from sklearn.neighbors import KNeighborsRegressor
    cat_fea = [
        feature for feature in new_data.columns if new_data[feature].dtype == object]
    num_missing_fea = [feature for feature in new_data.columns if new_data[feature].isnull(
    ).sum() > 0 and new_data[feature].dtype != object]
    not_null_fea = [
        feature for feature in new_data.columns if new_data[feature].isnull().sum() == 0]

    # Label encoding the categorical feature
    le = LabelEncoder()
    print("Encoding the categorical feature")
    for feature in cat_fea:
        new_data[feature] = le.fit_transform(new_data[feature])
        
    # imputing the missing features
    estimator = RandomForestRegressor(random_state=42)
    estimator_neighbour = KNeighborsRegressor(n_neighbors=5)
    print("Imputing the missing values")
    imputer = IterativeImputer(
        estimator=estimator, max_iter=7, verbose=verbose, random_state=42
    )
    imputer.fit(new_data)
    transformed = imputer.transform(new_data)
    transformed_data = pd.DataFrame(transformed, columns=new_data.columns)
    
    # Reverting the encoded cat features
    print("Reverting encoded feature to original")
    for feature in cat_fea:
        transformed_data[feature] = le.inverse_transform(
            transformed_data[feature])

    return transformed_data
    
    
if __name__ == '__main__':
    DATAPATH = r"file path here"
    data = pd.read_csv(DATAPATH)
    # Cleaning the data
    cleanData = clean_data(data)