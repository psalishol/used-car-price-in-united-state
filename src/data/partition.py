import pandas as pd
import hashlib
import os
import shutil
import time

# Partitioning the data
# The dataset contain more than 3million records, 
# we will partition these records into partition of 50 buckets 
# making about 60,000 records per bucket


# PARTITIONING PARAMETER

N_PARTITION = 50    # Number of buckets
base_partitions_dir = r"..\data\external\Partition"
output_dir = r"../data/external/output"

# hashing the listing id to allow even partitioning across the dataset
def hash_(listing_id):
    """Creates an hashed column using the listing id for the vehicle"""
    return int(hashlib.md5(str(listing_id).encode("utf-8")).hexdigest(), 16)

def create_partition():
    """Creates an empty partition directory for the buckets"""
    print("Checking if the directory exists")
    if os.path.exists(base_partitions_dir):
        shutil.rmtree(base_partitions_dir)
        print("removed the directory")
    else:
        print("No Such Directory found.")
        
    # Delaying before creating the directories
    time.sleep(0.5) 
    
    print("Creating empty folder list for partition")
    if not os.path.exists(base_partitions_dir):
        # Making a new directory for the partitions
        for i in range(N_PARTITION):
            partition_path = os.path.join(base_partitions_dir, "Vehicle_used_data_{}".format(i))
            # Printing the path
            print(partition_path)
            if not os.path.exists(partition_path):
                os.mkdir(partition_path)

# Making a blank partition
def create_blank_partition():
    """Creating a blank partition with the number of bucket"""
    for i in range(N_PARTITION):
        
        dir_base = os.path.join(base_partitions_dir,"Vehicle_used_data_{}.csv".format(str(i)))
        # Making directory for the file location
        file_path = r"..\data\external\used_cars_data.csv"  
        
        # Opening the file and writing it to the partition created
        with open(file_path, "r") as data, open(dir_base, "w") as f:
            f.write(",".join(list(data.columns)))
        print(dir)
        return dir



# Partitioing and hashing the dataset
def partition_by_hashing(df, name , progress= None):
    # hashing the listing_id column into the number of partitions
    df["hashed"] = df["listing_id"].apply(hash_) % N_PARTITION
    for partitions, data in df.groupby("partition"):
        # Wrting the data to the partition
        path_dir = os.path.join(base_partitions_dir,"Vehicle_used_data_{}.csv".format(str(partitions)))
        # Writing the data to the path
        with open(path_dir, "w") as f:
            f.write(path_dir, data)
        
dir = create_blank_partition()
os.listdir(dir)

