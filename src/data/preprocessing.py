import pandas as pd
import numpy as np
from partition import *

import pandas as pd
import hashlib
import os
import shutil
import time

# Partitioning the data
# The dataset contain more than 3million records, 
# we will partition these records into partition of 50 buckets 
# making about 60,000 records per bucket

# LOADING PARAMETER
chunksize= 1e5
df_dir = r"\Data\external\used_cars_data.csv"


# PARTITIONING PARAMETER
N_PARTITION = 50    # Number of buckets
base_partitions_dir = r"..\data\external\Partition"
output_dir = r"../data/external/output"

# loading chunk of the data for the column list
def col_list(data_path, chunksize):
    for df_iter, chunk in enumerate(pd.read_csv(data_path, chunksize=chunksize, iterator=False)):
        pass
    col_list = list(chunk.columns)
    return col_list

# hashing the listing id to allow even partitioning across the dataset
def hash_(listing_id):
    """Creates an hashed column using the listing id for the vehicle"""
    return int(hashlib.md5(str(listing_id).encode("utf-8")).hexdigest(), 16)


# For creating directory for the partition
def create_partition():
    """Creates an empty partition directory for the buckets"""
    start = time.time()
    print("Checking if the directory exists...")
    time.sleep(0.9)
    if os.path.exists(base_partitions_dir):
        print("Directory found")
        time.sleep(0.4)
        print("Removing directory")
        time.sleep(1)
        shutil.rmtree(base_partitions_dir)
        print("Removed the directory")
    else:
        print("No Such Directory found.")

    # Delaying before creating the directories
    time.sleep(2.5)

    print("Creating empty folder list for partition")
    time.sleep(0.9)
    if not os.path.exists(base_partitions_dir):
        # Creating partition directory
        os.mkdir(base_partitions_dir)
        # Making a new directory for the partitions
        for i in range(N_PARTITION):
            partition_path = os.path.join(
                base_partitions_dir, "p{}".format(i)).replace("\\", "/")
            # Printing the path
            print('| {} | Partition left {} |'.format(partition_path,N_PARTITION-i))
            if not os.path.exists(partition_path):
                os.mkdir(partition_path)
            else:
                print("Path Already exist")
            time.sleep(0.6)
    end = time.time()
    print("| Completed | Time Taken ------------------------- {}sec |".format(str(end-start)))


# Making a new directory for the partitioning
# Making a blank partition
def create_blank_partition():
    """Creating a blank partition with the number of bucket"""
    start = time.time()
    data_list = col_list(df_dir, chunksize)
    for i in range(N_PARTITION):
        file_base_dir = os.path.join(base_partitions_dir,"p{}".format(str(i)),"").replace("\\","/")
        print(file_base_dir)
        # Opening the file and writing it to the partition created
        with open(file_base_dir+"vehicle_used_data.csv", "w") as f:
            f.write(",".join(data_list))
    end = time.time()
    print("Time taken ------------------- | {}sec".format(str(end-start)))
    return file_base_dir

# Partitioing and hashing the 
def partition_by_hashing(df):
    # hashing the listing_id column into the number of partitions
    df["hashed"] = df["listing_id"].apply(hash_) % N_PARTITION
    for partitions, data in df.groupby("hashed"):
        # dropping the hashed column
        data = data.drop("hashed", axis=1)
        path_dir = os.path.join(base_partitions_dir,"Vehicle_used_data_{}.csv".format(str(partitions)))
        # Writing the data to the path
        with open(path_dir, "a") as f:
            data.to_csv(f, header=False, index=False)
        
dir = create_blank_partition()
os.listdir(dir)

if __name__ == 'main':
    # Making the directory for partitions
    chunksize = 1e5
    df_dir = r"..\Data\external\used_cars_data.csv"
    for df_iter, data in enumerate(pd.read_csv(r"..\Data\external\used_cars_data.csv", iterator=True, chunksize=chunksize, encoding="latin1"),1):
        print(df_iter)
        partition = partition_by_hashing(df=data)
        # data = partition_by_hashing(df, name="listing_id", progress=None)

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

def impute_missing_values(data, verbose: int, estimator):
    """Imputation of missing values using the IterativeImputer method.
    All categorical features would be encoded using the label encoding and then imputed using Iterative imputer with the estimator chosen

    Args:
        new_data (Dataframe): Data to be inputed 
        verbose (int): Either ```0``` or ```1``` for printing during imputation

    Raises:
        TypeError: if verbose is any value apart from ```0``` or ```1```

    Returns:
        [Dataframe]: Dataframe with no missing values
    """
    # Performing input validation
    if (verbose not in [0, 1]):
        raise ValueError("Code ran into an Exception \
                                verbose can only be 0 or 1")
    from sklearn.experimental import enable_iterative_imputer
    from sklearn.impute import IterativeImputer
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import LabelEncoder
    from sklearn.neighbors import KNeighborsRegressor
    cat_fea = [
        feature for feature in data.columns if data[feature].dtype == object]
    num_missing_fea = [feature for feature in data.columns if data[feature].isnull(
    ).sum() > 0 and data[feature].dtype != object]
    not_null_fea = [
        feature for feature in data.columns if data[feature].isnull().sum() == 0]

    # Label encoding the categorical feature
    le = LabelEncoder()
    print("Encoding the categorical feature")
    for feature in cat_fea:
        data[feature] = le.fit_transform(data[feature])
        
    # imputing the missing features
    estimator = RandomForestRegressor(random_state=42)
    estimator_neighbour = KNeighborsRegressor(n_neighbors=5)
    print("Imputing the missing values")
    imputer = IterativeImputer(
        estimator=estimator, max_iter=7, verbose=verbose, random_state=42
    )
    imputer.fit(data)
    transformed = imputer.transform(data)
    transformed_data = pd.DataFrame(transformed, columns=data.columns)
    
    # Reverting the encoded cat features
    print("Reverting encoded feature to original")
    for feature in cat_fea:
        transformed_data[feature] = le.inverse_transform(
            transformed_data[feature])

    return transformed_data
    
    
if __name__ == "__main__":
    pass