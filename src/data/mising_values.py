import pandas as pd
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