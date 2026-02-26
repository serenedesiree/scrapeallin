#!/usr/bin/env python3
"""
All In Podcast Scraper - Analyzes episodes for keyword mentions
Tracks which episodes contain specific keywords and generates visualizations
"""

from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

# Keywords to track
KEYWORDS = [
    "Data Center",
    "$13 Vol.",
    "62%",
    "Buy Yes",
    "78¢",
    "Buy No",
    "55¢",
    "Audit",
    "$0 Vol.",
    "43%",
    "Sanders",
    "Trump",
    "Biden",
    "Kamala",
    "Elon",
    "Musk",
    "Gavin",
    "Newsom",
    "Epstein",
    "Tesla",
    "SpaceX",
    "Nvidia",
    "DeepSeek",
    "Microsoft",
    "Google",
    "Gemini",
    "California",
    "New York",
    "China",
    "Iran",
    "Israel",
    "Nuclear",
    "Tariff",
    "Supreme Court",
    "Bitcoin",
    "Crypto"
]

class AllInScraper:
    """Scrapes and analyzes All In podcast episodes from YouTube"""
    
    def __init__(self):
        self.keyword_data = {keyword: [] for keyword in KEYWORDS}
        self.episodes = []
    
    def extract_transcript(self, video_id):
        """Extract transcript from a YouTube video"""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = " ".join([entry['text'] for entry in transcript])
            return text
        except Exception as e:
            print(f"Error extracting transcript for {video_id}: {e}")
            return None
    
    def analyze_episode(self, video_id, publish_date):
        """Analyze a single episode for keyword mentions"""
        transcript = self.extract_transcript(video_id)
        
        if not transcript:
            return False
        
        # Normalize text for case-insensitive matching
        transcript_lower = transcript.lower()
        
        keywords_found = []
        for keyword in KEYWORDS:
            keyword_lower = keyword.lower()
            if keyword_lower in transcript_lower:
                self.keyword_data[keyword].append(publish_date)
                keywords_found.append(keyword)
        
        if keywords_found:
            self.episodes.append({
                'video_id': video_id,
                'date': publish_date,
                'keywords_found': keywords_found
            })
            print(f"✓ {publish_date}: Found {len(keywords_found)} keywords")
        
        return True
    
    def analyze_batch(self, video_list):
        """
        Analyze a batch of videos
        video_list should be a list of dicts with 'id' and 'date' keys
        Example: [{'id': 'dQw4w9WgXcQ', 'date': '2026-01-15'}, ...]
        """
        print(f"Analyzing {len(video_list)} episodes...")
        
        for i, video_info in enumerate(video_list):
            print(f"\n[{i+1}/{len(video_list)}] Processing: {video_info['date']}")
            self.analyze_episode(video_info['id'], video_info['date'])
    
    def generate_keyword_summary(self):
        """Generate summary of keyword appearances"""
        summary = []
        for keyword, dates in self.keyword_data.items():
            if dates:
                summary.append({
                    'keyword': keyword,
                    'episode_count': len(dates),
                    'first_mention': min(dates),
                    'last_mention': max(dates)
                })
        
        return pd.DataFrame(summary).sort_values('episode_count', ascending=False)
    
    def plot_keyword_timeline(self, output_file='keyword_timeline.png'):
        """Create a timeline chart showing when each keyword appears"""
        # Filter keywords that actually appear
        active_keywords = {k: v for k, v in self.keyword_data.items() if v}
        
        if not active_keywords:
            print("No keywords found in any episodes.")
            return
        
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # Create a scatter plot for each keyword
        colors = plt.cm.tab20c(range(len(active_keywords)))
        
        for idx, (keyword, dates) in enumerate(active_keywords.items()):
            date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
            y_positions = [idx] * len(date_objects)
            ax.scatter(date_objects, y_positions, s=100, alpha=0.6, label=keyword, color=colors[idx])
        
        ax.set_yticks(range(len(active_keywords)))
        ax.set_yticklabels(list(active_keywords.keys()))
        ax.set_xlabel('Episode Date', fontsize=12)
        ax.set_title('All In Podcast - Keyword Mentions Over Time', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\n✓ Timeline chart saved to {output_file}")
        plt.close()
    
    def plot_keyword_frequency(self, output_file='keyword_frequency.png'):
        """Create a bar chart showing keyword frequency"""
        summary = self.generate_keyword_summary()
        
        if summary.empty:
            print("No keywords found in any episodes.")
            return
        
        # Take top 20 keywords
        top_keywords = summary.head(20)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.barh(top_keywords['keyword'], top_keywords['episode_count'], color='steelblue')
        ax.set_xlabel('Number of Episodes', fontsize=12)
        ax.set_title('Top Keywords in All In Podcast', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Frequency chart saved to {output_file}")
        plt.close()
    
    def save_results(self, output_file='analysis_results.json'):
        """Save analysis results to JSON"""
        summary = self.generate_keyword_summary()
        
        results = {
            'total_episodes_analyzed': len(self.episodes),
            'total_keywords_tracked': len(KEYWORDS),
            'keywords_found': len(summary),
            'keyword_summary': summary.to_dict('records'),
            'episode_details': self.episodes
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"✓ Results saved to {output_file}")
        
        # Print summary to console
        print("\n" + "="*60)
        print("KEYWORD ANALYSIS SUMMARY")
        print("="*60)
        print(summary.to_string(index=False))
        print("="*60)
    
    def load_video_list(self, json_file):
        """Load video list from JSON file (from yt-dlp)"""
        try:
            with open(json_file, 'r') as f:
                videos = json.load(f)
            
            # Convert yt-dlp format to our format
            video_list = []
            for video in videos:
                if 'id' in video and 'upload_date' in video:
                    # Convert YYYYMMDD to YYYY-MM-DD
                    date_str = video['upload_date']
                    formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                    video_list.append({
                        'id': video['id'],
                        'date': formatted_date
                    })
            
            return video_list
        except Exception as e:
            print(f"Error loading video list: {e}")
            return []

def main():
    """Main execution"""
    scraper = AllInScraper()
    
    print("=" * 60)
    print("ALL IN PODCAST SCRAPER")
    print("=" * 60)
    
    # Check if videos.json exists (from yt-dlp)
    if os.path.exists('videos.json'):
        print("\nLoading videos from videos.json...")
        video_list = scraper.load_video_list('videos.json')
        
        if video_list:
            print(f"Found {len(video_list)} episodes")
            scraper.analyze_batch(video_list)
            
            # Generate outputs
            scraper.plot_keyword_timeline()
            scraper.plot_keyword_frequency()
            scraper.save_results()
        else:
            print("No valid videos found in videos.json")
    else:
        print("\nNo videos.json file found.")
        print("\nTo use this script:")
        print("1. Install yt-dlp: pip install yt-dlp")
        print("2. Run: yt-dlp -j --flat-playlist 'https://www.youtube.com/@allin' > videos.json")
        print("3. Run this script again")

if __name__ == "__main__":
    main()