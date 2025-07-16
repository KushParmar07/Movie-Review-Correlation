from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


# Function to scrape reviews from IMDB for a given movie ID
def get_ratings(movie_id: str, show_logs: bool = False):
    reviews = []
    if show_logs:
        print(f"Processing {movie_id}...")
    try:
        # Setup browser for web scraping
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

            # Extract review text from each review element on the page
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


# Function to analyze sentiment of movie reviews
def sentiment_analyzer(reviews: list):
    try:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = []
        # Calculate sentiment score for each review and return average
        for rating in reviews:
            sentiment = analyzer.polarity_scores(rating)
            sentiment_scores.append(sentiment['compound'])

        return sum(sentiment_scores) / len(sentiment_scores)
    except:
        return 0