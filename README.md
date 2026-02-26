# All In Podcast Scraper Bot

## Installation

To install the All In Podcast Scraper Bot, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/serenedesiree/scrapeallin.git
cd scrapeallin
pip install -r requirements.txt
```

## Usage

Run the scraper using the following command:

```bash
python scraper.py
```

## Examples

Here are some examples of how to use the scraper:

```bash
python scraper.py --episode 123
```

This command will scrape data for episode 123 of the All In podcast.

## Output Files

The scraper generates the following output files:

- `episodes.json`: Contains metadata for each scraped episode.
- `transcripts`: A directory with transcript files named by episode number.

## Customization

You can customize the scraper by modifying the following parameters in the `config.py` file:

- `BASE_URL`: The base URL for the All In podcast.
- `OUTPUT_DIRECTORY`: The directory to save output files.

## Troubleshooting

If you encounter any issues, consider the following solutions:

- Ensure you have the required Python version (3.6 or higher).
- Check your internet connection.
- Review the logs for any specific error messages.

## Features

- Scrapes episode metadata and transcripts.
- Customizable output formats.
- Error handling for network issues.
