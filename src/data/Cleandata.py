# ---Libraries for the cleaning.
from os import path
import time
import pandas as pd
import numpy as np
# data cleaning and transformation


class Cleandata:

    def __init__(self, new_data):
        self.new_data = new_data

    def extract_vinfo(self, drop=True, verbose=False):
        """
        Extracts each vehicle features, and makes them a new variable, Replacing datapoint with the feature with 'Yes' and Otherwise 'NO'

        all_vfea (list): Contains all the vehicle features as list

        Args:
            drop (bool, optional): [description]. Defaults to True.
            verbose (bool, optional): Defaults to True. Prints the cleaning process and the time taken for each

        Returns:
            [type]: Dataframe with Each vehicle feature as variable
        """
        
        start = time.time()
        # Collecting all the car features and making a new faeture out of them
        all_vfea = []
        for i in range(0, len(self.new_data["vehicle_features"])):
            d_point = self.new_data["vehicle_features"][i]
            for feature in d_point:
                if feature not in all_vfea:
                    all_vfea.append(feature)

        # making the new feature
        for feature in all_vfea:
            # Creating an empty column with each vehiclefeature as Variable
            self.new_data[feature] = np.nan
            for i in range(0, len(self.new_data["vehicle_features"])):
                if feature in self.new_data["vehicle_features"][i]:
                    self.new_data.loc[i, feature] = "Yes"
                else:
                    self.new_data.loc[i, feature] = "No"
        end = time.time()  # ---> time the function
        if verbose is True:
            print(
                "[CL]---> Extracted Vehicle Info          || Time taken {}sec".format(str(end-start)))
        # Dropping Vehicle features
        if drop is True:
            self.new_data = self.new_data.drop(
                ["vehicle_features", "files"], axis=1)

        return self.new_data

    def _clean_mpg(self, drop=True, verbose=False):
        """Cleans the mpg by averaging the values

        Args:
            drop (bool, optional): . Defaults to True.
            verbose (bool, optional): Defaults to True. Prints the cleaning process and the time taken for each

        Returns:
            [Dataframe]: Dataframe with Clean mpg
        """
        # Making a new variable for Avg mpg
        start = time.time()
        self.new_data["Avg mpg"] = np.nan
        for i in range(len(self.new_data["mpg"])):
            if self.new_data["mpg"][i] is not None and len(self.new_data["mpg"][i].split("–")) == 1:
                self.new_data.loc[i, "Avg mpg"] = int(
                    self.new_data["mpg"][i].split("–")[0])
            else:
                try:
                    self.new_data.loc[i, "Avg mpg"] = (int(self.new_data["mpg"][i].split("–")[
                                                       0])+int(self.new_data["mpg"][i].split("–")[1]))/2
                except Exception:
                    self.new_data.loc[i, "Avg mpg"] = np.nan
        end = time.time()
        if verbose is True:
            print(
                "[CL]---> Cleaned Mpg          || Time taken {}sec".format(str(end-start)))
        if drop is True:
            self.new_data = self.new_data.drop("mpg", axis="columns")

        return self.new_data

    def _extract_loc(self, drop=True, verbose=False):
        """Extracting Seller State,city, and zip from seller info

        Args:
            drop (bool, optional): . Defaults to True.
            verbose (bool, optional): Defaults to True. Prints the cleaning process and the time taken for each

        Returns:
            [Dataframe]: Dataframe with Zip, City and State as new variable
        """

        # Extracting seller State
        start = time.time()
        i = 0
        self.new_data["State"] = np.nan
        for feature in self.new_data["seller_info"]:
            if len(feature.split(",")[-1].strip().split(" ")) == 2:
                self.new_data.loc[i, "State"] = feature.split(
                    ",")[-1].strip().split(" ")[0]
            else:
                self.new_data.loc[i, "State"] = np.nan

            i += 1

        # Extracting seller Zip
        i = 0
        self.new_data["Zip"] = np.nan
        for feature in self.new_data["seller_info"]:
            if len(feature.split(",")[-1].strip().split(" ")) == 2:
                self.new_data.loc[i, "Zip"] = feature.split(
                    ",")[1].strip().split(" ")[-1]
            else:
                self.new_data.loc[i, "Zip"] = np.nan
            i += 1

        #----> Extracting Seller city <----#

        # Making a list of last words of cities with two words
        w_two = ["City", "Park", "Estates", "Estate", "Louis",
                 "Pines", "Arlington", "Grove", "Beach", "Highland",
                 "Worth", "Nyack", "Angeles", "Jose", "Vegas", "Canaan", "Drum", "Segundo",
                 "Springs", "Wales", "Neck", "Paso", "Rancho", "Augustine", "Island", "Gardens",
                 "Hampton", "Rochelle", "Woods", "Coral", "Vista", "Barbara", "Kisco", "May", "Falls", "Dora",
                 "Barrington", "Miami", "Petersburg", "Paul", "Cleveland", "Monica", "Diego"]

        i = 0
        self.new_data["City"] = np.nan
        for feature in self.new_data["seller_info"]:
            if len(feature.split(",")) == 3:
                self.new_data.loc[i, "City"] = feature.split(
                    ",")[1].strip().split(" ")[-1]

            elif feature.title().split(",")[0].split(' ')[-1] in w_two:
                self.new_data.loc[i, "City"] = " ".join(
                    feature.split(",")[0].split(' ')[-2::])
            else:
                self.new_data.loc[i, "City"] = feature.split(",")[
                    0].split(' ')[-1]
            i += 1
        end = time.time()
        if verbose is True:
            print(
                "[CL]---> Extracted Seller Location         || Time taken {}sec".format(str(end-start)))
        if drop is True:
            self.new_data = self.new_data.drop("seller_info", axis=1)

        return self.new_data

    def _extract_eng_size(self, drop=True, verbose=False):
        """Extracting engine size from engine info.

        Operation performed include;
            - Extracting Engine size
            - Replacing inextractable datapoint with nan

        Args:
            drop (bool, optional): Defaults to True.
            verbose (bool, optional): Defaults to True. Prints the cleaning process and the time taken for each

        Returns:
            [Dataframe]: Dataframe with Enginesize as feature
        """
        start = time.time()
        i = 0
        self.new_data["Engine size"] = np.nan
        for feature in self.new_data["engine_type"]:
            try:
                self.new_data.loc[i, "Engine size"] = float(
                    feature.split(" ")[0].translate({ord(s): None for s in ["L"]}))
            except Exception:
                self.new_data.loc[i, "Engine size"] = np.nan
            i += 1
        end = time.time()
        #---Verbose
        if verbose is True:
            print(
                "[CL]---> Extracted Engine size          || Time taken {}sec".format(str(end-start)))
        # Dropping the engine_type
        if drop is True:
            self.new_data = self.new_data.drop("engine_type", axis="columns")
        return self.new_data

    def clean_fuel(self, verbose=False):
        """
            Cleaning the fueltype
        """
        start = time.time()
        i = 0
        for inf in self.new_data["fueltype"]:
            if inf.title() not in ["Gasoline", "Electric", "Diesel", "Hybrid", "Ethanol", "Biodiesel", "Propane", "CNG"]:
                self.new_data.loc[i, "fueltype"] = np.nan
            else:
                self.new_data.loc[i, "fueltype"] = inf
            i += 1
        end = time.time()
        if verbose is True:
            print(
                "[CL]---> Cleaned FuelType          || Time taken{}sec".format(str(end-start)))
        return self.new_data

    def clean_drivetrain(self, drop=True, verbose=False):
        """Cleaning the drivetrain feature 

        Transformation done include
            - 'All-wheel Drive','AWD' ---> AWD
            - 'Front-wheel Drive','FWD' ---> FWD
            - 'Rear-wheel Drive','RWD' ---> RWD
            - 'Four-wheel Drive','4WD' ---> 4WD
            - '-' ---> np.nan

        Args:
            drop (bool, optional): Defaults to True.
            verbose (bool, optional): Defaults to True. Prints the cleaning process and the time taken for each

        Returns:
            [Dataframe]: Dataframe with clean drivetrain
        """
        start = time.time()
        self.new_data["Drivetrain"] = self.new_data["drivetrain_type"].apply(lambda info: info.replace("All-wheel Drive", "AWD").replace(
            "Front-wheel Drive", "FWD").replace("Four-wheel Drive", "4WD").replace("Rear-wheel Drive", "RWD").replace("All Wheel Drive", "AWD").replace("–", ""))

        i = 0
        # Replacing "-" with nan
        for feature in self.new_data["Drivetrain"]:
            if feature is None:
                pass
            elif feature == "–":
                self.new_data.loc[i, "Drivetrain"] = np.nan
            elif feature == "AWD":
                self.new_data.loc[i,"Drivetrain"] = "All Wheel Drive"
            elif feature == "FWD":
                self.new_data.loc[i,"Drivetrain"] = "Front Wheel Drive"
            elif feature == "4WD":
                self.new_data.loc[i,"Drivetrain"] = "Four Wheel Drive"
            elif feature == "RWD":
                self.new_data.loc[i,"Drivetrain"] = "Rear Wheel Drive"
            i += 1
        end = time.time()

        #--Verbose
        if verbose is True:
            print(
                "[CL]---> Cleaned Drivetrain          || Time taken {}sec".format(str(end-start)))
        # Dropping the columns
        if drop is True:
            self.new_data = self.new_data.drop(
                "drivetrain_type", axis="columns")

        return self.new_data

    def extract_model(self, drop=False, verbose=False):
        """Extracting the car model from vehicle made
            - Replacing vehicle with make which aren't acura make with Null value

        Args:
            drop (bool, optional): Defaults to False.
            verbose (bool, optional): Defaults to True. Prints the cleaning process and the time taken for each

        Returns:
            [Dataframe]: Dataframe with Vehicle model and make as feature
        """
        start = time.time()
        i = 0
        # Making a new feature for Car make
        self.new_data["Model"] = np.nan
        self.new_data["Vehicle Make"] = np.nan
        for feature in self.new_data["vehicle_made"]:
            self.new_data.loc[i, "Vehicle Make"] = feature.split(" ")[
                0].strip()
            self.new_data.loc[i, "Model"] = feature.split(" ")[1].strip()
            i += 1

        end = time.time()

        #--Verbose
        if verbose is True:
            print(
                "[CL]---> Extracted Vehicle Model and Make          || Time taken {}sec".format(str(end-start)))

        # Dropping the column
        if drop is True:
            self.new_data = self.new_data.drop("vehicle_made", axis="columns")

        
        return self.new_data

    def clean_transmission(self, drop=True, verbose=True):
        """
        Cleans transmission

        Operation performed include
        turning:
            - feature with other 'name'+'Automatic' ---> automatic
            - feature with other 'name'+'Manual' ---> manual
            - feature with other 'name'+'Continous Variable' or 'name'+'CVT' ---> Continous Variable
            - feature with other 'name'+'Dual Clutch' ---> Dual Clutch

        Args:
            drop (bool, optional): Defaults to True.
            verbose (bool, optional): Defaults to True. Prints the cleaning process and the time taken for each

        Returns:
            [Dataframe]: Dataframe with clean Transmission type
        """
        start = time.time()
        # using the same thing for the above and all in the same accord
        self.new_data["Transmission"] = np.nan
        for i in range(len(self.new_data["transmission"])):
            if self.new_data["transmission"][i] in ["10-Speed Automatic", "10-SPEED A/T", "10 Cylinder", "9-Speed Automatic", "9-Speed Automatic with Auto-Shift",
                                                    "8-Speed Automatic with Auto-Shift", "8-Speed Automatic", "8-SPEED A/T", "7-Speed Automatic with Auto-Shift", "7-Speed Automatic", "7-SPEED A/T",
                                                    "automatic", "6-Speed Automatic", "5-Speed Automatic", "Automatic", "4-Speed Automatic", "5-SPEED A/T", "6-SPEED A/T", "Automatic 5-Speed", "AUTOMATIC",
                                                    "A", "Auto, 9-Spd w/SprtShft", "Auto, 5-Spd w/SportShift", "6-Speed Shiftable Automatic", "5-Speed Automatic with Overdrive"]:

                self.new_data.loc[i, "Transmission"] = "Automatic"

            elif self.new_data["transmission"][i] in ["6-Speed Manual", "5-Speed Manual", "Manual", "8-Speed Auto-Shift Manual w/OD"]:
                self.new_data.loc[i, "Transmission"] = "Manual"

            elif self.new_data["transmission"][i] in ["Automatic CVT"]:
                self.new_data.loc[i, "Transmission"] = "Continous Variable"

            elif self.new_data["transmission"][i] in ["8-Speed Dual-Clutch", "8-Speed Double Clutch", ""]:
                self.new_data.loc[i, "Transmission"] = "Double Clutch"

        end = time.time()
        #--Verbose
        if verbose is True:
            print(
                "[CL]---> Cleaned Transmission          || Time taken {}sec".format(str(end-start)))

        # Dropping the column
        if drop is True:
            self.new_data = self.new_data.drop("transmission", axis=1)
        return self.new_data


    def mk_pd_type(self, drop=True, verbose=False):
        """Replaces the certified model with "Certified".
        Example include turning "Acura Certified", "Mercedes Certified" to "Certified"


        Args:
            drop (bool, optional): [description]. Defaults to True.

        Returns:
            for
            [Dataframe]: Dataframe with clean product type
        """
        #---> using the test for the above in the sample:
        #---> it gives the main feature for the prediction and the model buidling

        start = time.time()
        i = 0
        self.new_data["Type"] = np.nan
        for feature in self.new_data["product_type"]:
            if feature in ["Used", "New"]:
                self.new_data.loc[i, "Type"] = feature
            else:
                self.new_data.loc[i, "Type"] = "Certified"
            i += 1

        end = time.time()

        #--Verbose
        if verbose is True:
            print(
                "[CL]---> Cleaned Product Type          || Time taken {}sec".format(str(end-start)))

        # Dropping the column
        if drop is True:
            self.new_data = self.new_data.drop("product_type", axis=1)
        return self.new_data


def clean_data(Transformer, to_csv=False, filename=None, verbose=False):
    """Cleanse the data and return a new clean dataframe

    Raises:
        ValueError: if to_csv is True and filename is None

    Returns:
        [Dataframe]: A clean Dataframe

    """
    transformer = Transformer
    if verbose is True:
        start = time.time()
        data = transformer.clean_fuel(verbose=True)
        data = transformer.clean_drivetrain(drop=True, verbose=True)
        data = transformer.clean_transmission(drop=True, verbose=True)
        data = transformer._extract_loc(drop=True, verbose=True)
        data = transformer._extract_eng_size(drop=True, verbose=True)
        data = transformer._clean_mpg(drop=True, verbose=True)
        data = transformer.extract_model(drop=True, verbose=True)
        data = transformer.extract_vinfo(drop=True, verbose=True)
        data = transformer.mk_pd_type(drop=True, verbose=True)
        end = time.time()
        print(
            "[CL]---> Successfully Cleaned {}.      || Total Time Taken {}min".format(" ".join(filename.title().split("_"))), str(np.round((end-start)/60,2)))

    else:
        start = time.time()
        data = transformer.clean_fuel(verbose=True)
        data = transformer.clean_drivetrain(drop=True, verbose=False)
        data = transformer.clean_transmission(drop=True, verbose=False)
        data = transformer._extract_loc(drop=True, verbose=False)
        data = transformer._extract_eng_size(drop=True, verbose=False)
        data = transformer._clean_mpg(drop=True, verbose=False)
        data = transformer.extract_model(drop=True, verbose=False)
        data = transformer.extract_vinfo(drop=True, verbose=False)
        data = transformer.mk_pd_type(drop=True, verbose=False)
        end = time.time()
        print(
            "[CL]---> Successfully Cleaned {}.      || Total Time Taken {}min".format(" ".join(filename.title().split("_"))), str(np.round((end-start)/60,2)))
        

    if to_csv is True and filename is None:
        raise ValueError(
            "To save the data to a csv, you must give it a name with the extension csv"

            "Example: to_csv=True, filename=Acura.csv"
        )

    #--- Dumping the clean data to Interim folder
    if to_csv is True:
        file = path.join(
            r"C:\Users\PSALISHOL\Documents\My Projects\Car Prediction\data\interim", filename+"_cl.csv")
        data.to_csv(file)
    return data


if __name__ == '__main__':
    # Making a list of the raw data names
    data_s = ["Acura_model","Audi", "BMW", "Buick", "cardillac", "Chevrolet",
              "Chrysler", "Dodge", "Ford", "GMC","honda", "hyundai", "jaguar", "toyota","volvo"]
    for data_name in data_s:
        filepath = path.join(
            r"C:\Users\PSALISHOL\Documents\My Projects\Car Prediction\data\raw", data_name+".json")
        new_d = pd.read_json(filepath)

        print("[Data name]:---> {}".format(" ".join(data_name.title().split("_"))))
        # Cleaning the data and dumping the cleaned data in Interim filepath.
        transformed_data = clean_data(Transformer=Cleandata(
            new_d), to_csv=True, filename=data_name, verbose=True)
