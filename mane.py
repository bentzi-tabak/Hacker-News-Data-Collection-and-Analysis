import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
import concurrent.futures
import time
from collections import Counter
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Number of top stories to fetch (default is 20)
NUM_OF_STORIES = 20

# Download necessary NLTK data
nltk.download('vader_lexicon', quiet=True)

def fetch_story_details(story_id):
    """
    Fetch details of a story from Hacker News.

    Args:
        story_id (int): The ID of the story to fetch details for.

    Returns:
        dict: A dictionary containing story details.
    """
    story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
    response = requests.get(story_url).json()
    return response

def fetch_comment_details(comment_id):
    """
    Fetch details of a comment from Hacker News.

    Args:
        comment_id (int): The ID of the comment to fetch details for.

    Returns:
        dict: A dictionary containing comment details.
    """
    comment_url = f'https://hacker-news.firebaseio.com/v0/item/{comment_id}.json'
    response = requests.get(comment_url).json()
    return response

def Retrieving_data_about_articles(array, num_stories):
    """
    Retrieve details for a specified number of top stories.

    Args:
        array (list): List of story IDs.
        num_stories (int): Number of top stories to retrieve.

    Returns:
        list: A list of dictionaries containing details of each story.
    """
    stories_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        story_details_list = list(executor.map(fetch_story_details, array[:num_stories]))
    for story_details in story_details_list:
        if story_details:
            stories_data.append({
                'id': story_details.get('id'),
                'title': story_details.get('title'),
                'url': story_details.get('url'),
                'score': story_details.get('score'),
                'author': story_details.get('by'),
                'time': story_details.get('time'),
                'comments_count': len(story_details.get('kids', [])),
                'type': story_details.get('type'),
                'descendants': story_details.get('descendants', 0)
            })
    return stories_data

def Saving_data_in_a_csv_file(array_of_dictionaries, path='', name='top_stories'):
    """
    Save the stories data to a CSV file.

    Args:
        array_of_dictionaries (list): List of dictionaries containing story details.
        path (str): Path where the CSV file will be saved.
        name (str): Name of the CSV file.
    """
    with open(path + name + '.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'url', 'score', 'author', 'time', 'comments_count', 'type', 'descendants']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for story in array_of_dictionaries:
            writer.writerow(story)

def Fetching_responses_to_top_stories(stories_data):
    """
    Fetch comments for the top stories.

    Args:
        stories_data (list): List of dictionaries containing story details.

    Returns:
        list: A list of dictionaries containing comment details.
    """
    comments_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for story in stories_data:
            story_id = story['id']
            story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            story_details = requests.get(story_url).json()
            if story_details and 'kids' in story_details:
                comment_ids = story_details['kids']
                comment_details_list = list(executor.map(fetch_comment_details, comment_ids))
                for comment_details in comment_details_list:
                    if comment_details:
                        comments_data.append({
                            'author': comment_details.get('by'),
                            'text': comment_details.get('text'),
                            'time': comment_details.get('time'),
                            'parent_story': story_id
                        })
    return comments_data

def Saving_comments_data_in_a_csv_file(comments_data):
    """
    Save the comments data to a CSV file.

    Args:
        comments_data (list): List of dictionaries containing comment details.
    """
    with open('comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['author', 'text', 'time', 'parent_story']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments_data:
            writer.writerow(comment)
    print("Comments saved to CSV.")

def Data_analysis_and_statistics(stories_df, comments_df):
    """
    Perform data analysis and generate statistics for stories and comments.

    Args:
        stories_df (DataFrame): DataFrame containing stories data.
        comments_df (DataFrame): DataFrame containing comments data.
    """
    # Dictionary to store all statistical results
    stats_results = {}

    # Summary statistics for top stories
    avg_score = stories_df['score'].mean()
    avg_comments_count = stories_df['comments_count'].mean()
    stats_results['average_score'] = avg_score
    stats_results['average_comments_count'] = avg_comments_count

    # Sort stories by score and comments_count
    stories_df_sorted_by_score = stories_df.sort_values(by='score')
    stories_df_sorted_by_comments = stories_df.sort_values(by='comments_count')

    # Time-based analysis
    current_time = time.time()
    stories_df['time_since_posted'] = (current_time - stories_df['time']) / 3600  # in hours

    # Plotting scores
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 2, 1)
    plt.bar(stories_df_sorted_by_score['title'], stories_df_sorted_by_score['score'], color='blue')
    plt.axhline(y=avg_score, color='red', linestyle='--')
    plt.text(len(stories_df_sorted_by_score) - 1, avg_score, f'Avg Score: {avg_score:.2f}', color='red', va='center')
    plt.title('Scores of Top Stories')
    plt.xlabel('Stories')
    plt.ylabel('Score')
    plt.xticks(rotation=90)
    
    plt.subplot(2, 2, 2)
    plt.bar(stories_df_sorted_by_comments['title'], stories_df_sorted_by_comments['comments_count'], color='green')
    plt.axhline(y=avg_comments_count, color='red', linestyle='--')
    plt.text(len(stories_df_sorted_by_comments) - 1, avg_comments_count, f'Avg Comments: {avg_comments_count:.2f}', color='red', va='center')
    plt.title('Comments Count of Top Stories')
    plt.xlabel('Stories')
    plt.ylabel('Comments Count')
    plt.xticks(rotation=90)

    plt.subplot(2, 2, 3)
    plt.scatter(stories_df['time_since_posted'], stories_df['score'], color='blue')
    plt.axhline(y=avg_score, color='red', linestyle='--')
    plt.title('Score vs. Time Since Posted')
    plt.xlabel('Time Since Posted (hours)')
    plt.ylabel('Score')

    plt.subplot(2, 2, 4)
    plt.scatter(stories_df['time_since_posted'], stories_df['comments_count'], color='green')
    plt.axhline(y=avg_comments_count, color='red', linestyle='--')
    plt.title('Comments Count vs. Time Since Posted')
    plt.xlabel('Time Since Posted (hours)')
    plt.ylabel('Comments Count')

    plt.tight_layout()
    plt.savefig('data_analysis_plots.png')
    plt.close()

    # New analyses
    
    # 1. Distribution of story topics (based on title keywords)
    def extract_keywords(title):
        return [word.lower() for word in title.split() if len(word) > 3]
    
    all_keywords = [keyword for title in stories_df['title'] for keyword in extract_keywords(title)]
    keyword_freq = Counter(all_keywords).most_common(10)
    stats_results['top_10_keywords'] = dict(keyword_freq)
    
    plt.figure(figsize=(10, 5))
    plt.bar([kw[0] for kw in keyword_freq], [kw[1] for kw in keyword_freq])
    plt.title('Top 10 Keywords in Story Titles')
    plt.xlabel('Keyword')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('keyword_distribution.png')
    plt.close()

    # 2. Average time between story posting and reaching front page
    avg_time_to_frontpage = stories_df['time_since_posted'].mean()
    stats_results['average_time_to_frontpage'] = avg_time_to_frontpage
    print(f"Average time to reach front page: {avg_time_to_frontpage:.2f} hours")

    # 3. Percentage of stories with external links vs. self posts
    external_links = stories_df['url'].notna().sum()
    self_posts = len(stories_df) - external_links
    stats_results['external_links_percentage'] = (external_links / len(stories_df)) * 100
    stats_results['self_posts_percentage'] = (self_posts / len(stories_df)) * 100
    plt.figure(figsize=(8, 8))
    plt.pie([external_links, self_posts], labels=['External Links', 'Self Posts'], autopct='%1.1f%%')
    plt.title('Distribution of External Links vs. Self Posts')
    plt.savefig('link_distribution.png')
    plt.close()

    # Distribution of story posting times
    stories_df['hour_posted'] = pd.to_datetime(stories_df['time'], unit='s').dt.hour
    hour_counts = stories_df['hour_posted'].value_counts().sort_index()
    stats_results['posting_time_distribution'] = hour_counts.to_dict()
    plt.figure(figsize=(12, 6))
    plt.bar(hour_counts.index, hour_counts.values)
    plt.title('Distribution of Story Posting Times')
    plt.xlabel('Hour of Day (UTC)')
    plt.ylabel('Number of Stories')
    plt.xticks(range(0, 24))
    plt.savefig('posting_time_distribution.png')
    plt.close()

    # Comment analysis
    if not comments_df.empty:
        # Convert 'text' column to string and replace NaN with empty string
        comments_df['text'] = comments_df['text'].astype(str).fillna('')
        
        # Average and median comment lengths
        comments_df['comment_length'] = comments_df['text'].str.len()
        avg_comment_length = comments_df['comment_length'].mean()
        median_comment_length = comments_df['comment_length'].median()
        stats_results['average_comment_length'] = avg_comment_length
        stats_results['median_comment_length'] = median_comment_length
        print(f"Average comment length: {avg_comment_length:.2f} characters")
        print(f"Median comment length: {median_comment_length:.2f} characters")

        # Percentage of comments with links
        comments_with_links = comments_df['text'].str.contains('http').sum()
        total_comments = len(comments_df)
        link_percentage = (comments_with_links / total_comments) * 100
        stats_results['comments_with_links_percentage'] = link_percentage
        print(f"Percentage of comments with links: {link_percentage:.2f}%")

        # Basic sentiment analysis
        sia = SentimentIntensityAnalyzer()
        comments_df['sentiment'] = comments_df['text'].apply(lambda x: sia.polarity_scores(x)['compound'] if x else 0)
        sentiment_distribution = comments_df['sentiment'].apply(lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')).value_counts()
        stats_results['sentiment_distribution'] = sentiment_distribution.to_dict()
        plt.figure(figsize=(8, 8))
        plt.pie(sentiment_distribution.values, labels=sentiment_distribution.index, autopct='%1.1f%%')
        plt.title('Comment Sentiment Distribution')
        plt.savefig('sentiment_distribution.png')
        plt.close()

    # Correlation between story score and number of comments
    correlation = stories_df['score'].corr(stories_df['comments_count'])
    stats_results['score_comments_correlation'] = correlation
    plt.figure(figsize=(10, 6))
    plt.scatter(stories_df['score'], stories_df['comments_count'])
    plt.title(f'Story Score vs Number of Comments (Correlation: {correlation:.2f})')
    plt.xlabel('Story Score')
    plt.ylabel('Number of Comments')
    plt.savefig('score_comments_correlation.png')
    plt.close()

    # Save all statistical results to CSV
    with open('statistical_analysis.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Metric', 'Value'])
        for key, value in stats_results.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    writer.writerow([f"{key} - {sub_key}", sub_value])
            else:
                writer.writerow([key, value])

def Data_collection_and_analysis_from_Hacker_News(num_of_stories):
    """
    Collect and analyze data from Hacker News.

    Args:
        num_of_stories (int): The number of top stories to retrieve and analyze.
    """
    # Fetch top stories IDs
    top_stories_ids_array = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()
    
    # Retrieve detailed information about the top stories
    articles_data = Retrieving_data_about_articles(top_stories_ids_array, num_of_stories)
    
    # Save the articles data to a CSV file
    Saving_data_in_a_csv_file(articles_data)
    
    # Fetch comments for the top stories
    comments_data = Fetching_responses_to_top_stories(articles_data)
    
    # Save the comments data to a CSV file if available
    if comments_data:
        Saving_comments_data_in_a_csv_file(comments_data)
    else:
        print("No comments data to save")

    # Load the stories and comments data into DataFrames
    stories_df = pd.read_csv('top_stories.csv')
    comments_df = pd.read_csv('comments.csv')
    
    # Perform data analysis and generate statistics
    Data_analysis_and_statistics(stories_df, comments_df)

# Run the data collection and analysis process for the specified number of top stories
Data_collection_and_analysis_from_Hacker_News(NUM_OF_STORIES)

    
    
    
    
    
    
    
    
    

