import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# Load the sentiment data
df = pd.read_csv('sentiment_feedback_data.csv')

# Ensure 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Data Validation: Check for missing values and handle them
if df.isnull().sum().any():
    print("Warning: Missing values detected. Filling missing values in 'Comment' with a default string.")
    df['Comment'].fillna("No comment provided", inplace=True)

# Sentiment Score Calculation with type checking and imputation
def calculate_sentiment_score(comment):
    if isinstance(comment, str):  # Check if comment is a string
        analysis = TextBlob(comment)
        return analysis.sentiment.polarity  # Returns a float in the range [-1.0, 1.0]
    else:
        return 0.0  # Return a neutral score for non-string comments

# Adding sentiment score to the DataFrame
df['Sentiment_Score'] = df['Comment'].apply(calculate_sentiment_score)

# 1. Analyze sentiment trends over time
# Group by date and calculate sentiment counts
sentiment_trends = df.groupby(df['Date'].dt.date)['Sentiment'].value_counts().unstack(fill_value=0)

# Plotting the sentiment trends over time
plt.figure(figsize=(12, 6))
sentiment_trends.plot(kind='line', marker='o')
plt.title('Sentiment Trends Over Time', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Comments', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='Sentiment', fontsize=12)
plt.tight_layout()
plt.savefig('sentiment_trends.png')
plt.show()

# 2. Determine which feedback channels generate the most negative or positive comments
channel_sentiment = df.groupby(['Feedback Channel', 'Sentiment']).size().unstack(fill_value=0)

# Plotting sentiment by feedback channel
plt.figure(figsize=(12, 6))
channel_sentiment.plot(kind='bar', stacked=True, color=sns.color_palette("Set2"))
plt.title('Sentiment by Feedback Channel', fontsize=16)
plt.xlabel('Feedback Channel', fontsize=14)
plt.ylabel('Number of Comments', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='Sentiment', fontsize=12)
plt.tight_layout()
plt.savefig('sentiment_by_channel.png')
plt.show()

# 3. Calculate average ratings per channel and identify areas for improvement
average_ratings = df.groupby('Feedback Channel')['Rating'].mean()

# Display average ratings per channel
print("Average Ratings per Feedback Channel:")
print(average_ratings)

# Plotting average ratings per channel
plt.figure(figsize=(12, 6))
average_ratings.plot(kind='bar', color='skyblue')
plt.title('Average Ratings per Feedback Channel', fontsize=16)
plt.xlabel('Feedback Channel', fontsize=14)
plt.ylabel('Average Rating', fontsize=14)
plt.xticks(rotation=45)
plt.axhline(y=average_ratings.mean(), color='red', linestyle='--', label='Overall Average Rating')
plt.legend()
plt.tight_layout()
plt.savefig('average_ratings_per_channel.png')
plt.show()

# 4. Total comments count by feedback channel
comments_count = df['Feedback Channel'].value_counts()

# Print total comments count for context
print("Total Comments Count by Feedback Channel:")
print(comments_count)

# 5. Statistical analysis (example: t-test for ratings comparison)
from scipy import stats

# Example between two channels (make sure to adjust as per your data)
channel1_ratings = df[df['Feedback Channel'] == 'Email']['Rating']
channel2_ratings = df[df['Feedback Channel'] == 'Survey']['Rating']

t_stat, p_value = stats.ttest_ind(channel1_ratings, channel2_ratings, nan_policy='omit')
print(f"T-test between Email and Survey Channels: T-statistic = {t_stat}, P-value = {p_value}")

