import pandas as pd
from confluent_kafka import Producer

# Load the dataset
df = pd.read_csv('feedback_data.csv')  # Replace with the actual path to your dataset

# Initialize the Kafka producer
producer = Producer({'bootstrap.servers': 'localhost:9092'})  # Adjust if your broker is different

# Delivery report callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Produce messages to the Kafka topic
for index, row in df.iterrows():
    feedback_message = str(row['Comment']) if pd.notna(row['Comment']) else 'No comment'  # Handle NaN values
    producer.produce('feedback', value=feedback_message.encode('utf-8'), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery reports to be received
producer.flush()
