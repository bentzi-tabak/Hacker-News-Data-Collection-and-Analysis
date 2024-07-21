
# Hacker News Data Collection and Analysis Project

This project is designed to collect, analyze, and visualize data from Hacker News, a popular social news website focusing on computer science and entrepreneurship. By default, the project fetches data for the top 20 stories, but this can be adjusted in the code.

## Features

1. **Data Collection**: 
    - Fetches the top stories from Hacker News.
    - Retrieves detailed information about each story, including the title, URL, score, author, time of posting, and the number of comments.
    - Collects comments for each story.

2. **Data Storage**:
    - Saves the fetched data to CSV files for easy access and further analysis.

3. **Data Analysis**:
    - Computes summary statistics such as average score and average number of comments.
    - Sorts and visualizes the data based on scores and comments.
    - Performs time-based analysis to understand how scores and comments change over time.
    - Extracts and analyzes keywords from story titles.
    - Analyzes the distribution of story posting times.
    - Evaluates comments, including their length and sentiment.

4. **Visualization**:
    - Generates various plots to visualize scores, comments, keyword distributions, and posting times.
    - Saves the generated plots as image files for reference.

## Usage

To use this project, ensure you have the necessary Python packages installed:
- `requests`
- `csv`
- `pandas`
- `matplotlib`
- `concurrent.futures`
- `nltk`

Run the project by executing the script. By default, it will fetch data for the top 20 stories. To change this, modify the `NUM_OF_STORIES` variable in the code.

```python
NUM_OF_STORIES = 20
The data will be saved to top_stories.csv and comments.csv files. The analysis results, including plots and a CSV file with statistical results, will be saved in the same directory.

This project provides a comprehensive overview of the current top stories on Hacker News, offering valuable insights through data analysis and visualization.
