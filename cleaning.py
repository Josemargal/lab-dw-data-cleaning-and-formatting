# cleaning.py

import pandas as pd

def load_data(url):
    df = pd.read_csv(url)
    return df

def standardize_column_names(df):
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    return df

def clean_gender(df):
    df['gender'] = df['gender'].replace({
        'female': 'F', 'femal': 'F', 'f': 'F',
        'male': 'M', 'm': 'M'
    })
    return df

def map_states(df):
    state_mapping = {
        'az': 'Arizona', 'cali': 'California', 'wa': 'Washington'
    }
    df['st'] = df['st'].str.lower().replace(state_mapping)
    return df

def standardize_education(df):
    df['education'] = df['education'].replace({
        'bachelors': 'Bachelor'
    })
    return df

def clean_customer_lifetime_value(df):
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '')
    df['customer_lifetime_value'] = df['customer_lifetime_value'].astype(float)
    return df

def clean_vehicle_class(df):
    vehicle_class_mapping = {
        'sports_car': 'Luxury',
        'luxury_suv': 'Luxury',
        'luxury_car': 'Luxury'
    }
    df['vehicle_class'] = df['vehicle_class'].replace(vehicle_class_mapping)
    return df

def clean_number_of_open_complaints(df):
    df['number_of_open_complaints'] = df['number_of_open_complaints'].str.split('/').str[1].fillna(0).astype(int)
    return df

def handle_null_values(df):
    # Rellenar numéricos con la media
    numerical_columns = df.select_dtypes(include=['float64', 'int']).columns
    for column in numerical_columns:
        df[column] = df[column].fillna(df[column].mean())

    # Rellenar categóricos con la moda
    categorical_columns = df.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        df[column] = df[column].fillna(df[column].mode()[0])
    
    return df

def handle_duplicates(df):
    df = df.drop_duplicates(keep='first')
    df.reset_index(drop=True, inplace=True)
    return df

def main(url):
    df = load_data(url)
    df = standardize_column_names(df)
    df = clean_gender(df)
    df = map_states(df)
    df = standardize_education(df)
    df = clean_customer_lifetime_value(df)
    df = clean_vehicle_class(df)
    df = clean_number_of_open_complaints(df)
    df = handle_null_values(df)
    df = handle_duplicates(df)

    # Convertir todas las variables numéricas a enteros
    numerical_columns = df.select_dtypes(include=['float64']).columns
    df[numerical_columns] = df[numerical_columns].astype(int)

    return df

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/data-bootcamp-v4/data/main/file1.csv"
    cleaned_df = main(url)
    cleaned_df.to_csv('cleaned_data.csv', index=False)
    print("Limpieza completada y datos guardados en 'cleaned_data.csv'")