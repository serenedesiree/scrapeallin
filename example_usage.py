# Example usage of the All In Podcast Scraper

from all_in_scraper import AllInScraper

# Instantiate the scraper
scraper = AllInScraper()

# Scrape the latest episodes
latest_episodes = scraper.scrape_latest_episodes()

# Print the titles and links of the latest episodes
for episode in latest_episodes:
    print(f'Title: {episode.title}, Link: {episode.link}')
