import pandas as pd

df = pd.read_excel('Movie_Dataset_Encoded.xlsx')
# df_encoded = pd.get_dummies(df, columns=['GENRE'], dtype=float)

rating_order = ['G', 'PG', 'Approved', 'PG-13', 'TV-MA', 'R', 'Not Rated']
rating_map = {rating: i for i, rating in enumerate(rating_order)}
df['RATED'] = df['RATED'].map(rating_map)
df.to_excel('Movie_Dataset_Encoded.xlsx')