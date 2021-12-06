# Car Price Prediction in the United State
![LOGO](https://images.ctfassets.net/ro7z507xvlp4/6jEGoVcKW1X26UrzoYvpT0/ff2c16451be3c22fcb9d8ddf6bcc600d/fullwidth_banner_1__2x.jpg?q=80&fm=jpg&w=800)
#### Project Status: In progress


## Introduction to the Project
This project aim to build a model that predicts the average price one can sell or buy different models of Cars in the United State.

Suppose a car owner wants to sell his car but then he wants to know the estimated price the car can be sold without  having to go to a dealership shop. he can use the model built to check the price which will return the average price of the car with the inputed features. 

To make user have the feel of the project, a website will be built and deployed with heroku, the website will have webpage for the prediction, and also another webpage for dashboard, where user can check vehicle data for a specific make and also compare the features of the Make with price.


Project Folder Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Contains the Intermediate data that has been transformed/Cleaned.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original/just extracted, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Contains all the Jupyter notebooks. 
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis in PDF.
    │   └── figures        <- Generated graphics and figures used for reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt` or `pip install -r requirements`
    │
    ├── setup.py           <- makes project pip installable so the src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   |── Datacollection
    |   |       └──Datacollection
    |   |          └──Spider <- Contains Scripts for Data crawling and extraction
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------


## Data Collection
The crucial part of this project is the data collection. To collect the data for this project, we scraped vehicle info from different website that buys and sells cars. The data was extracted to a json file. different car model were extracted seperately.

**Library used: Scrapy. Check [Documentation](https://docs.scrapy.org/en/latest/)**
```bash
  pip install Scrapy
```
```bash
  conda install -c conda-forge scrapy
```
**Info collected:** model_name/year, mpg, mileage, transmission_type, enginesize, seller_info/location, fueltype, drivetraintype, features, and price.

Check link to script [here](https://github.com/psalishol/Car-price-in-United-state/tree/main/data_collection)


