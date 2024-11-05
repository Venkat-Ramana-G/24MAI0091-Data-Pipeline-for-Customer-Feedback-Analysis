import pandas as pd
from textblob import TextBlob

# Load cleaned data
df = pd.read_csv('cleaned_feedback_data.csv')

# Sentiment Analysis Function
def get_sentiment(comment):
    # Check if the comment is a valid string, if not return 'unknown'
    if not isinstance(comment, str):
        return 'unknown'  # or 'neutral', depending on your preference
    analysis = TextBlob(comment)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Apply sentiment analysis
df['Sentiment'] = df['Comment'].apply(get_sentiment)

# Save sentiment data
df.to_csv('sentiment_feedback_data.csv', index=False)
print("Sentiment analysis completed and saved to 'sentiment_feedback_data.csv'.")
