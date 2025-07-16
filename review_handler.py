import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


def get_ratings(movie_id: str, show_logs: bool = False):
    reviews = []
    if show_logs:
        print(f"Processing {movie_id}...")
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
    
            page.goto(f"https://www.imdb.com/title/{movie_id}/reviews/?ref_=tt_ov_ururv")
            if page.locator("button.ipc-see-more__button:has-text('All')"):
                page.locator("button.ipc-see-more__button:has-text('All')").click()
            page.wait_for_timeout(60000)

            pageHtml = page.content()
            soup = BeautifulSoup(pageHtml, 'html.parser')

        for review in soup.find_all(class_="sc-a77dbebd-1 iJQoqi user-review-item"):
            rating_element = review.find(class_="ipc-html-content-inner-div")
            if rating_element:
                rating = rating_element.text.strip()
                rating = ILLEGAL_CHARACTERS_RE.sub(r"", rating)
                reviews.append(rating)        
        
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(f"{movie_id}: {e}\n")
    
    return reviews

def sentiment_analyzer(reviews: list):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []
    for rating in reviews:
        sentiment = analyzer.polarity_scores(rating)
        sentiment_scores.append(sentiment['compound'])
    
    return sum(sentiment_scores) / len(sentiment_scores)


if __name__ == "__main__":
    movies = pd.read_excel('Movie_Dataset_Encoded_Test.xlsx')
    movie_ids = movies['IMDB_ID'].tolist()

    for movie_id in movie_ids:
        if pd.isna(movies.loc[movies['IMDB_ID'] == movie_id, 'REVIEW_SCORE'].values[0]):
            print(f"Processing {movie_id}...")
            reviews = get_ratings(movie_id)
            if reviews:
                sentiment = sentiment_analyzer(reviews)
                movies.loc[movies['IMDB_ID'] == movie_id, 'REVIEW_SCORE'] = sentiment

    movies.to_excel('Movie_Dataset_Encoded_Test.xlsx', index=False)

