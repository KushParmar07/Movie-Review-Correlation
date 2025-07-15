import pandas as pd
import requests
from dotenv import load_dotenv
import os
load_dotenv()

df = pd.read_excel("Movie_Dataset.xlsx")
api_key = os.getenv("API_KEY")

for index, row in df.iterrows():
    title = row['TITLES'].replace(" ", "+")
    try:
        data = requests.get(f'https://www.omdbapi.com/?apikey={api_key}&t={title}').json()
        df.at[index, 'YEAR'] = float(data['Year'])
        df.at[index, 'RATED'] = data['Rated']
        df.at[index, 'RUNTIME'] = data['Runtime']
        df.at[index, 'GENRE'] = data['Genre'].split(",")[0].strip()
        df.at[index, 'RATINGS'] = data['imdbRating']
        df.at[index, 'REVENUE'] = data['BoxOffice']


    except Exception as e:
        with open("errors.txt", "a") as f:
            f.write(f"{title}: {e}\n")

df.to_excel("Movie_Dataset.xlsx", index=False)



