import pandas as pd
import requests
from dotenv import load_dotenv
import os

def get_data(df: pd.DataFrame):
    with open('titles.txt', 'r') as f:
        titles = f.read().splitlines()

    index = 0
    for title in titles:
        api_title = title.replace(" ", "+")
        try:
            data = requests.get(f'https://www.omdbapi.com/?apikey={api_key}&t={api_title}').json()
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

    return df


def encode_data(df: pd.DataFrame):
    df_encoded = pd.get_dummies(df, columns=['GENRE'], dtype=float)
    rating_order = ['G', 'PG', 'Approved', 'PG-13', 'TV-MA', 'R', 'Not Rated']
    df_encoded['RATED'] = df_encoded['RATED'].map({rating: i for i, rating in enumerate(rating_order)})
    return df_encoded


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("API_KEY")
    df = pd.DataFrame(columns=['TITLES', 'YEAR', 'RATED', 'RUNTIME', 'GENRE', 'RATINGS', 'REVENUE', 'IMDB_ID', 'REVIEW_SCORE'])
    raw_data = get_data(df)
    raw_data.to_excel('Movie_Dataset_Test.xlsx', index=False)
    encode_data(raw_data).to_excel('Movie_Dataset_Encoded_Test.xlsx', index=False)
    
        
        
