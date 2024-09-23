import pandas as pd
import os

def get_dataset(path=None):
    """
    Load the dataset from the given path
    
    Parameters:
    path : str
        The path to the dataset file
        
    Returns:
    pd.DataFrame
        The dataset loaded as a pandas DataFrame
    """
    if path is None:
        path = os.path.join('src', 'data', 'datatran2024.csv')
    # Construir o caminho do arquivo de forma independente do sistema operacional
    full_path = os.path.join(os.getcwd(), path)
    return pd.read_csv(full_path, sep=';', encoding='latin1')

def general_statistics(df):
    """
    Returns general statistics about the traffic accidents dataset.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    dict: Dictionary containing general statistics.
    """
    
    
    datatran_dataset = df
    
    # Drop duplicates and remove any rows with missing values
    datatran_dataset = datatran_dataset.drop_duplicates()
    datatran_dataset = datatran_dataset.dropna()
    datatran_dataset = datatran_dataset.dropna(axis=1)
    
    
    statistics = {}

    # Total number of unique accidents
    total_accidents = datatran_dataset['id'].nunique()
    
    # Time range covered by the dataset (minimum and maximum dates)
    time_period = (datatran_dataset['data_inversa'].min(), df['data_inversa'].max())
    
    # Total number of deaths (sum of the 'mortos' column)
    total_deaths = datatran_dataset['mortos'].sum()
    
    # Total number of minor injuries (sum of the 'feridos_leves' column)
    total_minor_injuries = datatran_dataset['feridos_leves'].sum()

    # Fatality rate: percentage of accidents with at least 1 death
    fatality_rate = (datatran_dataset['mortos'] > 0).mean() * 100

    # Filling the dictionary with the computed statistics
    statistics['Total Accidents'] = total_accidents
    statistics['Dataset Time Period'] = f"{time_period[0]} to {time_period[1]}"
    statistics['Total Deaths'] = total_deaths
    statistics['Total Minor Injuries'] = total_minor_injuries
    statistics['Fatality Rate (%)'] = round(fatality_rate, 2)
    
    return statistics

def accident_severity(df):
    """
    Analyzes the severity of traffic accidents based on the dataset.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    pd.DataFrame: A DataFrame summarizing the severity of accidents.
    """
    # Define severity categories based on deaths and injuries
    severity_levels = {
        'No Injury': (0, 0),
        'Minor Injury': (0, 1),  # At least one minor injury
        'Serious Injury': (1, 0),  # At least one death
        'Multiple Deaths': (1, 1)  # At least one death and at least one minor injury
    }
    
    # Initialize a dictionary to count occurrences of each severity level
    severity_counts = {level: 0 for level in severity_levels}

    # Iterate through each accident and categorize its severity
    for _, row in df.iterrows():
        deaths = row['mortos']
        minor_injuries = row['feridos_leves']
        
        if deaths > 0:
            if minor_injuries > 0:
                severity_counts['Multiple Deaths'] += 1
            else:
                severity_counts['Serious Injury'] += 1
        elif minor_injuries > 0:
            severity_counts['Minor Injury'] += 1
        else:
            severity_counts['No Injury'] += 1
    
    # Convert the counts into a DataFrame for plotting
    severity_df = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
    
    return severity_df

def main_causes(df):
    """
    Analyzes the main causes of traffic accidents.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    pd.DataFrame: A DataFrame summarizing the frequency of each cause.
    """
    cause_counts = df['causa_acidente'].value_counts()
    cause_df = cause_counts.reset_index()
    cause_df.columns = ['Cause', 'Frequency']
    
    return cause_df

def common_accident_types(df):
    """
    Analyzes the most common types of traffic accidents.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    pd.DataFrame: A DataFrame summarizing the frequency of each type of accident.
    """
    type_counts = df['tipo_acidente'].value_counts()
    type_df = type_counts.reset_index()
    type_df.columns = ['Accident Type', 'Frequency']
    
    return type_df

def accident_classification(df):
    """
    Analyzes the classification of traffic accidents.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    pd.DataFrame: A DataFrame summarizing the frequency of each classification.
    """
    classification_counts = df['classificacao_acidente'].value_counts()
    classification_df = classification_counts.reset_index()
    classification_df.columns = ['Classification', 'Frequency']
    
    return classification_df

def weather_conditions(df):
    """
    Analyzes the distribution of weather conditions during traffic accidents.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    pd.DataFrame: A DataFrame summarizing the frequency of each weather condition.
    """
    weather_counts = df['condicao_metereologica'].value_counts()
    weather_df = weather_counts.reset_index()
    weather_df.columns = ['Weather Condition', 'Frequency']
    
    return weather_df

def road_direction(df):
    """
    Analyzes the distribution of accidents based on road direction.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    pd.DataFrame: A DataFrame summarizing the frequency of each road direction.
    """
    direction_counts = df['sentido_via'].value_counts()
    direction_df = direction_counts.reset_index()
    direction_df.columns = ['Road Direction', 'Frequency']
    
    return direction_df

def road_type(df):
    """
    Analyzes the frequency of accidents in different types of roads.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the traffic accidents data.

    Returns:
    pd.DataFrame: A DataFrame summarizing the frequency of each road type.
    """
    type_counts = df['tipo_pista'].value_counts()
    type_df = type_counts.reset_index()
    type_df.columns = ['Road Type', 'Frequency']
    
    return type_df
