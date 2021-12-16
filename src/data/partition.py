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

columns_list = col_list(df_dir, chunksize)

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
    for i in range(N_PARTITION):
        
        dir_base = os.path.join(base_partitions_dir,"Vehicle_used_data_{}.csv".format(str(i)))
        # Making directory for the file location
        file_path = r"..\data\external\used_cars_data.csv"  
        
        # Opening the file and writing it to the partition created
        with open(file_path, "r") as data, open(dir_base, "w") as f:
            f.write(",".join(list(data.columns)))
        print(dir)
        return dir



# Partitioing and hashing the 
def partition_by_hashing(df, name , progress= None):
    # hashing the listing_id column into the number of partitions
    df["hashed"] = df["listing_id"].apply(hash_) % N_PARTITION
    for partitions, data in df.groupby("hashed"):
        # Wrting the data to the partition
        path_dir = os.path.join(base_partitions_dir,"Vehicle_used_data_{}.csv".format(str(partitions)))
        # Writing the data to the path
        with open(path_dir, "a") as f:
            f.write("\n")
            data.to_csv(f, header=False, index=False)
        
dir = create_blank_partition()
os.listdir(dir)

if __name__ == 'main':
    # Making the directory for partitions
    dir = create_partition()
    # # Reading the data in chunk
    # chunksize = 1e6
    # df = pd.read_csv("C:\Users\PSALISHOL\Documents\My Projects\Car Prediction\Data\used_vehicle_data.csv", chunksize=chunksize)
    # partition = partition_by_hashing(df, name="read", progress=10)
    # print(partition)