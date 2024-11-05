import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the sentiment data
df = pd.read_csv('sentiment_feedback_data.csv')

# Ensure 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Set seaborn style for better aesthetics
sns.set(style="whitegrid")

# 1. Analyze sentiment distribution with a pie chart (donut chart)
sentiment_counts = df['Sentiment'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Distribution of Sentiments')
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is a circle.
plt.tight_layout()
plt.savefig('sentiment_distribution.png')
plt.show()

# 2. Calculate average ratings by feedback channel
average_ratings = df.groupby(['Feedback Channel'])['Rating'].mean().reset_index()

# Display average ratings DataFrame for clarity
print("Average Ratings by Feedback Channel:")
print(average_ratings)

# Create a heatmap for average ratings
plt.figure(figsize=(12, 6))
sns.heatmap(average_ratings.set_index('Feedback Channel').T, annot=True, cmap='coolwarm', fmt='.1f')
plt.title('Average Ratings by Feedback Channel')
plt.xlabel('Feedback Channel')
plt.ylabel('Average Rating')
plt.tight_layout()
plt.savefig('average_ratings_heatmap.png')
plt.show()

# 3. Time series plot for sentiment trends over time
sentiment_trends = df.groupby(df['Date'].dt.date)['Sentiment'].value_counts().unstack(fill_value=0)

# Check the columns of the sentiment_trends DataFrame
print("Sentiment Trends Columns:")
print(sentiment_trends.columns)

# Plot sentiment trends
plt.figure(figsize=(12, 6))
for sentiment in sentiment_trends.columns:
    sentiment_trends[sentiment].rolling(window=7).mean().plot(label=f'{sentiment} (7-day MA)', marker='o')

plt.title('Sentiment Trends Over Time with 7-Day Moving Average')
plt.xlabel('Date')
plt.ylabel('Number of Comments')
plt.xticks(rotation=45)
plt.legend(title='Sentiment')
plt.tight_layout()
plt.savefig('sentiment_trends_moving_average.png')
plt.show()
