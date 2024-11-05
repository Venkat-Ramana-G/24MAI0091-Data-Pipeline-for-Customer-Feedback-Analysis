import pandas as pd
import re
from spellchecker import SpellChecker

# Text Cleaning Function
def clean_text(text):
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()  # Convert to lowercase
    return text

# Spell Correction Function
def correct_spelling(text):
    spell = SpellChecker()
    words = text.split()
    corrected = []
    
    for word in words:
        if word in spell.unknown([word]):  # If the word is unknown, suggest correction
            candidates = spell.candidates(word)
            corrected_word = list(candidates)[0] if candidates else word  # Choose the first candidate if found
        else:
            corrected_word = word
        corrected.append(corrected_word)
    
    return ' '.join(corrected)

# Load your dataset and limit to 200 rows
df = pd.read_csv('feedback_data.csv').head(100)

# Clean the comments column
df['Comment'] = df['Comment'].fillna('No comment')  # Handle missing values
df['Comment'] = df['Comment'].apply(clean_text)     # Clean text
df['Comment'] = df['Comment'].apply(correct_spelling)  # Correct spelling

# Save the cleaned dataset
df.to_csv('cleaned_feedback_data.csv', index=False)
print("Data cleaning completed and saved for 100 rows.")


# import pandas as pd
# import re
# from spellchecker import SpellChecker
# from confluent_kafka import Consumer, KafkaError

# # Kafka Consumer Configuration
# consumer_config = {
#     'bootstrap.servers': 'localhost:9092',  # Adjust as needed
#     'group.id': 'feedback_group',
#     'auto.offset.reset': 'earliest'
# }

# consumer = Consumer(consumer_config)
# consumer.subscribe(['feedback'])

# # Prepare to collect messages
# messages = []
# MAX_MESSAGES = 20  # Limit to 20 messages

# try:
#     while len(messages) < MAX_MESSAGES:
#         msg = consumer.poll(1.0)  # Timeout after 1 second
#         if msg is None:
#             continue
#         if msg.error():
#             if msg.error().code() == KafkaError._PARTITION_EOF:
#                 continue
#             else:
#                 print(f"Error: {msg.error()}")
#                 break
#         messages.append(msg.value().decode('utf-8'))
# except KeyboardInterrupt:
#     pass
# finally:
#     consumer.close()

# # Convert messages to DataFrame
# data = [line.split(',') for line in messages]
# df = pd.DataFrame(data, columns=['Customer ID', 'Feedback Channel', 'Rating', 'Date', 'Comment'])

# # Initialize the spell checker outside the loop for efficiency
# spell = SpellChecker()

# # Data Cleaning Function
# def clean_comment(comment):
#     # Check for missing values and handle them
#     if pd.isnull(comment) or comment.strip() == "":
#         return "No comment"  # Placeholder for missing comments
    
#     # Remove special characters
#     comment = re.sub(r'[^a-zA-Z\s]', '', comment)

#     # Split comment into words and get a list of unique misspelled words
#     words = comment.split()
#     misspelled = spell.unknown(words)  # Faster with unknown() method

#     # Correct misspelled words if found
#     corrected_words = [
#         spell.correction(word) if word in misspelled else word for word in words
#     ]

#     # Join cleaned words into a single string
#     cleaned_comment = ' '.join(corrected_words).strip()
#     return cleaned_comment

# # Apply cleaning to the 'Comment' column on the limited dataset
# df['Cleaned_Comment'] = df['Comment'].apply(clean_comment)

# # Save cleaned data
# df.to_csv('cleaned_feedback_data.csv', index=False)
# print("Data cleaning completed and saved to 'cleaned_feedback_data.csv'.")

