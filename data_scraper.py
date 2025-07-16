# Script for scraping movie data from OMDB API and encoding it for analysis
import pandas as pd
import requests


# Function to fetch movie data from OMDB API and store it in a dataframe
def get_data(df: pd.DataFrame, api_key: str, save_raw: bool = False, raw_save_title: str = 'Movie_Dataset_Raw.xlsx'):
    # Read movie titles from text file
    with open('titles.txt', 'r') as f:
        titles = f.read().splitlines()

    index = 0
    for title in titles:
        # Format title for API request
        api_title = title.replace(" ", "+")
        try:
            # Get movie data from OMDB API
            data = requests.get(f'https://www.omdbapi.com/?apikey={api_key}&t={api_title}').json()
            # Store movie details in dataframe
            df.at[index, 'TITLES'] = title
            df.at[index, 'YEAR'] = float(data['Year'])
            df.at[index, 'RATED'] = data['Rated']
            df.at[index, 'RUNTIME'] = data['Runtime']
            df.at[index, 'GENRE'] = data['Genre'].split(",")[0].strip()
            df.at[index, 'RATINGS'] = data['imdbRating']
            df.at[index, 'REVENUE'] = data['BoxOffice']
            df.at[index, 'IMDB_ID'] = data['imdbID']
            index += 1
        except Exception as e:
            with open('errors.txt', 'a') as f:
                f.write(f"{title}: {e}\n")

    if save_raw:
        df.to_excel(raw_save_title, index=False)

    return df


# Function to encode categorical data into numerical format for model processing
def encode_data(df: pd.DataFrame):
    # Convert genre categories to binary columns
    df_encoded = pd.get_dummies(df, columns=['GENRE'], dtype=float)
    # Define rating order and convert to numerical values
    rating_order = ['G', 'PG', 'Approved', 'PG-13', 'TV-MA', 'R', 'Not Rated']
    df_encoded['RATED'] = df_encoded['RATED'].map({rating: i for i, rating in enumerate(rating_order)})
    return df_encoded        
