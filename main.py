from scrape_data import LinkedInScraper

if __name__ == "__main__":
    search_term = "google"

    linkedin_scraper = LinkedInScraper()
    linkedin_scraper.run_scraper(search_term)