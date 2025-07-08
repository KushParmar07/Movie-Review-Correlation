import csv
from imdb import IMDb

def load_titles_from_csv(filename="titles_2.csv"):
    movie_titles = []
    try:
        with open(filename, mode="r", encoding="latin-1") as infile:
            reader = csv.reader(infile)
            for row in reader:
                if row:
                    movie_titles.append(row[0])
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return movie_titles

def get_review_urls(movie_titles):
    ia = IMDb()
    review_urls = []
    not_found_titles = []

    for title in movie_titles:
        print(f"Searching for '{title}'...")
        try:
            search_results = ia.search_movie(title)

            if not search_results:
                not_found_titles.append(title)
                continue

            best_match = search_results[0]
            movie_id = best_match.movieID
            review_url = f"https://www.imdb.com/title/tt{movie_id}/reviews"
            review_urls.append(review_url)

        except Exception as e:
            not_found_titles.append(title)

    if not_found_titles:
        print("\nCould not find URLs for the following titles:")
        for title in not_found_titles:
            print(f"- {title}")

    return review_urls

def save_review_urls(urls, filename="review_urls_2.csv"):
    with open(filename, "w") as f:
        for url in urls:
            f.write(f"{url}\n")


if __name__ == "__main__":
    csv_input_filename = "titles_2.csv"

    my_movie_list = load_titles_from_csv(csv_input_filename)
    if my_movie_list:
        generated_urls = get_review_urls(my_movie_list)

        if generated_urls:
            save_review_urls(generated_urls)
        else:
            print("\nNo review URLs generated.")

