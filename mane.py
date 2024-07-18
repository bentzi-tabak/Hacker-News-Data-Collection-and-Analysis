import requests
import csv

NUM_OF_STORIES = 10
TOP_STORY_IDS_ARRAY = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()

def Data_collection_and_analysis_from_Hacker_News(NUM_OF_STORIES):
    top_stories_ids_array = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json').json()
    Retrieving_data_about_articles(top_stories_ids_array, NUM_OF_STORIES)
    Saving_data_in_a_csv_file(array)
    
    
    
    
    
    
    

