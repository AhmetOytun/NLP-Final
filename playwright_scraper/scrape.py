import json
from playwright.sync_api import sync_playwright

def scrape_letterboxd_reviews(review_pages, output_file="reviews.json"):
    """
    Scrape reviews from the IMDB page of a movie and write each review to a JSON file.
    """
    all_reviews = []
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir="playwright_data",
            headless=False,
            channel="chrome",
            no_viewport=True,
            java_script_enabled=True,
        )
        
        page = browser.new_page()
        for review_page in review_pages:
            page.goto(review_page)
            page.locator('xpath=//html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]/div[3]/div/span[2]/button').click()
            page.wait_for_timeout(10000)
            section = page.locator('xpath=//html/body/div[2]/main/div/section/div/section/div/div[1]/section[1]')
            articles = section.locator("article")
            count = articles.count()
            print(f"Number of reviews: {count}")
            for i in range(min(count, 100)):
                article = articles.nth(i)
                title = article.locator('xpath=./div[1]/div[1]/div[2]')
                review_title = title.inner_text() if title.count() > 0 else ""

                review = article.locator('xpath=./div[1]/div[1]/div[3]')
                review_text = review.inner_text() if review.count() > 0 else ""

                stars = article.locator('xpath=./div[1]/div[1]/div[1]/span[1]/span[1]')
                review_stars = stars.inner_text() if stars.count() > 0 else ""

                review_data = review_title + review_text

                all_reviews.append(review_data)

        browser.close()
        
    return all_reviews 

positive_review_pages = [
    "https://www.imdb.com/title/tt4154796/reviews/?ref_=tt_ururv_sm&rating=9&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt4154756/reviews/?ref_=tt_ururv_sm&rating=10&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt0111161/reviews/?ref_=tt_ururv_sm&rating=9&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt7286456/reviews/?ref_=tt_ururv_sm&rating=10&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt6751668/reviews/?ref_=tt_ururv_sm&rating=9&spoilers=EXCLUDE",
]
negative_review_pages = [
    "https://www.imdb.com/title/tt4154796/reviews/?ref_=tt_ururv_sm&rating=2&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt4154756/reviews/?ref_=tt_ururv_sm&rating=1&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt0111161/reviews/?ref_=tt_ururv_sm&rating=1&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt7286456/reviews/?ref_=tt_ururv_sm&rating=1&spoilers=EXCLUDE",
    "https://www.imdb.com/title/tt6751668/reviews/?ref_=tt_ururv_sm&rating=2&spoilers=EXCLUDE",
]

positive_reviews = scrape_letterboxd_reviews(positive_review_pages)
negative_reviews = scrape_letterboxd_reviews(negative_review_pages)

# write positive reviews to file
with open("positive_reviews.json", "w") as f:
    json.dump(positive_reviews, f)

# write negative reviews to file
with open("negative_reviews.json", "w") as f:
    json.dump(negative_reviews, f)