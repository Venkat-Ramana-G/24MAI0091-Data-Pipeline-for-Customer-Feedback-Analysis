from confluent_kafka import Consumer, KafkaError

# Initialize the Kafka consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',  # Adjust if your broker is different
    'group.id': 'feedback_group',  # Group ID for the consumer group
    'auto.offset.reset': 'earliest'  # Start reading from the earliest message
})

# Subscribe to the feedback topic
consumer.subscribe(['feedback'])

# Consume messages
try:
    while True:
        message = consumer.poll(1.0)  # Timeout set to 1 second
        if message is None:
            continue
        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached')
            else:
                print(f"Error: {message.error()}")
        else:
            print(f"Received message: {message.value().decode('utf-8')}")  # Decode the byte message to string
except KeyboardInterrupt:
    pass
finally:
    # Close the consumer to commit final offsets and leave the group
    consumer.close()
