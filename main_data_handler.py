import pandas as pd
from dotenv import load_dotenv
import os
import data_scraper
import review_handler


if __name__ == "__main__":
    #Basic setup
    load_dotenv()
    api_key = os.getenv("API_KEY")
    df = pd.DataFrame(
        columns=['TITLES', 'YEAR', 'RATED', 'RUNTIME', 'GENRE', 'RATINGS', 'REVENUE', 'IMDB_ID', 'REVIEW_SCORE'])

    #Fetching data from OMDB api and encoding to prepare for model fitting
    raw_data = data_scraper.get_data(df, api_key)
    encoded_data = data_scraper.encode_data(raw_data)
    encoded_data.to_excel('Movie_Dataset_Encoded_Test.xlsx', index=False) #Saving prior to scraping to ensure data is stored incase of error

    #Scraping reviews and performing sentiment analysis
    movie_ids = encoded_data['IMDB_ID'].tolist()
    for movie_id in movie_ids:
        if pd.isna(encoded_data.loc[encoded_data['IMDB_ID'] == movie_id, 'REVIEW_SCORE'].values[0]):
            reviews = review_handler.get_ratings(movie_id)
            if reviews:
                sentiment = review_handler.sentiment_analyzer(reviews)
                encoded_data.loc[encoded_data['IMDB_ID'] == movie_id, 'REVIEW_SCORE'] = sentiment

    #Final save after review sentiment data is added to dataframe
    encoded_data.to_excel('Movie_Dataset_Encoded_Test.xlsx', index=False)

