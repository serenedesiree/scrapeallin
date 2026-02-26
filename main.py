import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import re

# List of keywords to track
keywords = [
    "Data Center", "$13 Vol.", "62%", "0123456789", "%",
    "Buy Yes", "78¢", "Buy No", "55¢", "Audit",
    "$0 Vol.", "43%", "Sanders", "Trump", "Biden",
    "Kamala", "Elon/Musk", "Gavin/Newsom", "Epstein",
    "Tesla", "SpaceX", "Nvidia", "DeepSeek", "Microsoft",
    "Google", "Gemini", "California", "New York", "China",
    "Iran", "Israel", "Nuclear", "Tariff", "Supreme Court",
    "Bitcoin/Crypto"
]

# Function to scrape YouTube for podcast episodes
def scrape_youtube(channel_url):
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract episode links (this will vary based on actual YouTube page structure)
    episodes = []
    for link in soup.find_all('a', href=True):
        if '/watch?v=' in link['href']:
            episodes.append(link['href'])
    return episodes

# Function to extract transcripts (assuming transcripts are available on a specific page)
def extract_transcript(video_url):
    transcript_api_url = f"{video_url};transcript"  # Update with actual API call
    response = requests.get(transcript_api_url)
    if response.status_code == 200:
        # Assuming a JSON response; this will vary
        transcript_data = response.json()
        return ' '.join([line['text'] for line in transcript_data['transcripts']])
    return ""

# Function to analyze keywords in transcripts
def analyze_transcripts(episodes):
    keyword_dates = {keyword: [] for keyword in keywords}
    
    for episode in episodes:
        transcript = extract_transcript(episode)
        date = re.search(r'\d{4}-\d{2}-\d{2}', episode)  # Example date regexp
        if date:
            for keyword in keywords:
                if keyword in transcript:
                    keyword_dates[keyword].append(date.group(0))
    
    return keyword_dates

# Function to plot keywords over time
def plot_keywords(keyword_dates):
    for keyword, dates in keyword_dates.items():
        series = pd.Series(pd.to_datetime(dates))
        series.value_counts().sort_index().plot(label=keyword)

    plt.title('Keyword Mentions Over Time')
    plt.xlabel('Date')
    plt.ylabel('Mentions')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    channel_url = "https://www.youtube.com/c/AllInPodcast"  # Example channel
    episodes = scrape_youtube(channel_url)
    keyword_dates = analyze_transcripts(episodes)
    plot_keywords(keyword_dates)