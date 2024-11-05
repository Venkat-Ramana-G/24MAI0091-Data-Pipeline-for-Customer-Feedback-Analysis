24MAI0091
Venkat Ramana G

Data Ingestion Starts by installing Apacke Kafka from : 
https://kafka.apache.org/downloads --> Binary Downloads --> and Set the Paths accordingly in Zookeeper file and Server Properties File

Then Run the Following Command's in Different Command Prompts :
1) C:\Kafka\kafka_2.12-3.8.1 > .\bin\windows\kafka-server-start.bat .\config\server.properties --> for starting the server.
   
2) C:\Kafka\kafka_2.12-3.8.1>.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties --> For starting the Zookeeper.
   
3) \bin\windows\kafka-topics.bat --create --topic feedback --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 --> To Create an Topic For Sending and Retrieving Messages.

After Doing the Above Steps then start execution from Step 1 ( S1 ) in Repository
