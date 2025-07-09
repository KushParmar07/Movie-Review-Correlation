import pandas as pd
import openpyxl
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import yaml
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

issues = {}

def get_movies():
    movies = []
    with open("review_urls.csv", "r") as f:
        for line in f:
            movies.append(line.strip())
    return movies

def get_ratings(movie):
    ratings = []
    try:
        with sync_playwright() as pw:

            browser = pw.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()


            page.goto(movie)
            page.locator("button.ipc-see-more__button:has-text('All')").click()
            page.wait_for_timeout(60000)

            pageHtml = page.content()
            soup = BeautifulSoup(pageHtml, 'html.parser')
    except:
        issues[movie] = "Playwright Error"
        print(f"Playwright Error for {movie}")
        return "Error", pd.DataFrame()

    try:
        reviews = soup.find_all(class_="sc-a77dbebd-1 iJQoqi user-review-item")
    except:
        issues[movie] = "Finding Reviews Error"
        print(f"Finding Reviews Error for {movie}")
        return "Error", pd.DataFrame()

    for review in reviews:
        try:
            rating_element = review.find(class_="ipc-html-content-inner-div")
            if rating_element:
                rating = rating_element.text.strip()
                rating = ILLEGAL_CHARACTERS_RE.sub(r"", rating)
                ratings.append(rating)
        except:
            pass

    try:
        title = soup.find(class_="sc-405d3be6-10 dXTyJs").text
        for char in ":-[]/?*":
            title = title.replace(char, "")
        if len(title) >= 31:
            title = title[:30]

    except AttributeError:
        issues[movie] = "Finding Title Error"
        print(f"Finding Title Error for {movie}")
        title = "Error"

    column_names = ["Reviews"]
    df = pd.DataFrame(ratings, columns=column_names)

    return title, df


if __name__ == "__main__":
    iteration = 0
    movies = get_movies()
    with pd.ExcelWriter("Movie_Reviews.xlsx", engine="openpyxl") as writer:
        for movie in movies:
            iteration += 1
            print(f"Processing {movie}... {iteration} of {len(movies)}")
            title, this_df = get_ratings(movie)
            this_df.to_excel(sheet_name=title, index=False, excel_writer=writer)

    with open("issues.yaml", 'w') as f:
        yaml.dump(issues, f)