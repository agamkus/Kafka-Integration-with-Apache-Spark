# Kafka-Integration-with-Apache-Spark

## Objective
Kafka is a potential messaging and integration platform for Spark Streaming. It acts as the central hub for real-time streams of data, which are processed in Spark Streaming using complex algorithms. Once the data is processed, Spark Streaming either publishes the results into another Kafka topic or stores them in HDFS, databases or dashboards.

Kafka is a **state-of-the-art messaging system**. It is **highly scalable** as well; hence, it is popular in the industry. It follows the **publisher-subscriber** or **pub-sub model**. In this model, a publisher can give their inputs to a topic, and multiple subscribers can access that topic. A **topic** can be thought of as **equivalent** to a **table** in a **database system**. This integrates well with Spark Streaming for further processing of the data streams.

![image](https://user-images.githubusercontent.com/56078504/154792323-0f9aa268-5598-4741-accf-70be5e77b6fd.png)

The flow for the exercise is as follows:
- Set up Kafka
- Create a Topic
- Publish into the Kafka Topic
- Set up a Spark Job to read from the Kafka Topic
- Execute

Our objective is to setup Kafka and perform below 2 operations on Kafka:
1. Read from Kafka
2. Write to Kafka

## Segment 1: Read from Kafka
1. Login to AWS console and launch EC2 instance.

![image](https://user-images.githubusercontent.com/56078504/154792376-8e12e2e7-eed6-42ac-a1d8-eb5bfb37d17d.png)

2. Create a folder where you want to download the Kafka. Let’s create with name ‘**kafka**’.

   ````
    mkdir kafka
    cd kafka
   ````
   
   ![image](https://user-images.githubusercontent.com/56078504/154792451-f6edc414-7744-4df5-bc19-b3b768d554f7.png)

   
 3. Download the Kafka binaries using below command:
 
    ````
    wget https://archive.apache.org/dist/kafka/2.3.0/kafka_2.12-2.3.0.tgz
    ````
    
4. Unzip the Kafka **tgz** file. Below is the command:
   
   ````
   tar -xzf kafka_2.12-2.3.0.tgz
   ````
   
   ![image](https://user-images.githubusercontent.com/56078504/154792499-f3865b72-0692-41b6-b948-2e290304d205.png)

5. Change the directory to the unzipped folder:

   ![image](https://user-images.githubusercontent.com/56078504/154792510-afd09cc4-bb54-447c-afd4-536c6a3ef695.png)

6. ZooKeeper is primarily used for service synchronization to track the status of nodes in the Kafka cluster and maintain a list of Kafka topics and messages. Open a **new terminal** and first start the Zookeeper server.

    ````
    bin/zookeeper-server-start.sh config/zookeeper.properties
    ````
    ![image](https://user-images.githubusercontent.com/56078504/154792542-cabb8aaa-7d07-4c07-8d51-3cd0b4a3cc62.png)
    
    
7. Start the **Kafka server** and keep this terminal up and running Below is the command:
   
   ````
   bin/kafka-server-start.sh config/server.properties
   ````
   
   ![image](https://user-images.githubusercontent.com/56078504/154792654-0f8e5681-f705-46eb-a488-fcae049db443.png)

8. Open another session and let’s create a topic named **kafka-new-topic** with a **single partition** and **replication factor 1**.
   
   ````
   bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic kafka-new-topic
   ````
   
   ![image](https://user-images.githubusercontent.com/56078504/154792671-8a997be8-3133-4dc5-8385-d5cf64ba6863.png)

9. Create a file **read_from_kafka.py** using below command:
   
   ````
   vi read_from_kafka.py
   ````
   ![image](https://user-images.githubusercontent.com/56078504/154792707-ca3efbdc-9d9f-46c4-8f4a-88a01821e398.png)


10. Below is the complete code. Hit the ‘**I**’ key to turn the console into edit mode and paste the codes to the file. Press ‘**Esc**’ key and enter **:wq!** to save the file. Here, we are subscribing to the Kafka topic “**new-kafka-topic**” and set the output mode as **append** and will print the output on **console**. Also, we are creating a Datafarme which casts key and value of kafka topic messages into string.

    ````
     from pyspark.sql import SparkSession
     from pyspark.sql.functions import *
     from pyspark.sql.types import *
   
     spark = SparkSession \ 
            .builder \ 
            .appName("StructuredSocketRead") \ 
            .getOrCreate()
     spark.sparkContext.setLogLevel('ERROR') 

     lines = spark \ 
            .readStream \ 
            .format("kafka") \ 
            .option("kafka.bootstrap.servers","ec2-54-237-150-57.compute-1.amazonaws.com:9092") \ 
            .option("subscribe","kafka-new-topic") \ 
            .load()

     kafkaDF = lines.selectExpr("cast(key as string)","cast(value as string)")

     query = kafkaDF \ 
            .writeStream \ 
            .outputMode("append") \ 
            .format("console") \ 
            .start()

     query.awaitTermination()
     ````

11. Start a **Kafka Producer** and connect to the newly created topic to publish something here.
    
    ````
    bin/kafka-console-producer.sh --broker-list localhost:9092 --topic kafka-new-topic
    ````
    ![image](https://user-images.githubusercontent.com/56078504/154793000-95d05d2a-6f13-4530-9d62-3d94d9974bc6.png)

12. As spark doesn't come with Kafka, we need to tell spark to run the jar as dependency. Download the **spark-sql-kafka-0-10_2.11-2.3.0.jar** file using below command:
    
    ````
    wget https://ds-spark-sql-kafka-jar.s3.amazonaws.com/spark-sql-kafka-0-10_2.11-2.3.0.jar
    ````
    ![image](https://user-images.githubusercontent.com/56078504/154793018-e3d111b9-19ea-4868-9077-092413e3c60b.png)

13. Run the application program using below command which inlcudes the jar file as well:
    
    ````
    spark2-submit –jars spark-sql-kafka-0-10_2.11-2.3.0.jar read_from_kafka.py
    ````
    
    ![image](https://user-images.githubusercontent.com/56078504/154793124-af6e649f-d387-45c5-9d66-ff04174f0e49.png)

14. Let’s write something on Kafka host and check the output on primary console. Below is the screenshot:
    
    ![image](https://user-images.githubusercontent.com/56078504/154793141-afdb7688-b4e9-4c33-b3d7-78aa491a936a.png)

    As we see from the above results that we have given 3 inputs “**New Kafka message**”, “**Another message**” and “**One more**” on the Kafka host and the out is printed on the console in 3 separate batches.
    
## Segment 2: Write to Kafka
As Kafka setup is already done, so we are skipping this step. Let’s follow below steps to write something to Kafka. Here, we are reading data from HDFS and will write it to the Kafka host.

1. Create a file **write_to_kafka.py** by using below command:
   
   ````
   vi write_to_kafka.py
   ````   
   
   ![image](https://user-images.githubusercontent.com/56078504/154793351-2659cb3c-4787-4599-8a61-becce7b13748.png)
   
2. Below is the complete code. Hit the ‘**I**’ key to turn the console into edit mode and paste the codes to the file. Press ‘**Esc**’ key and enter **:wq!** to save the file. Here, we are reading the stream from **HDFS** using Spark and will publish it to the Kafka topic “**kafka-new-topic**”. The output will be printed on **Kafka Host Consume Console**. We are creating a Datafarme which casts key and value of kafka topic messages into string. Also, we are creating a checkpoint location **checkpoint_dir**.
   
   ````
   from pyspark.sql import SparkSession
   from pyspark.sql.functions import *
   from pyspark.sql.types import StructType
   
   spark = SparkSession \
           .builder \ 
           .appName("StructuredSocketRead") \ 
           .getOrCreate()
   spark.sparkContext.setLogLevel('WARN')
   
   mySchema = StructType().add("name", "string").add("age","integer")
   
   lines = spark \ 
           .readStream \ 
           .option("delimiter",";") \ 
           .format("csv") \ 
           .schema(mySchema) \ 
           .load("testdir/")
           
   kafkaDF = lines.selectExpr("name as key","cast(age as string) as value")
   
   query = kafkaDF \ .writeStream \ 
           .outputMode("append") \ 
           .format("kafka") \ 
           .option("kafka.bootstrap.servers","ec2-3-236-151-70.compute-1.amazonaws.com:9092") \ 
           .option("topic","kafka-new-topic") \ .option("checkpointLocation","checkpoint_dir") \ 
           .start() query.awaitTermination()
           
    ````
    
3. Let’s create a directory **checkpoint_dir** which is used to maintain intermediate states on HDFS compativle file systems to recover from failures.
   
   ![image](https://user-images.githubusercontent.com/56078504/154793480-5d1ff621-5f06-4a85-9138-7ec7531d27cd.png)

4. There is a file in our directory called **players.csv**. We’ll send this file to HDFS so that Spark can read the streams from this file and write to the Kafka. Let’s see the contents of the file using below command:
   
   ````
   cat players.csv
   ````
   ![image](https://user-images.githubusercontent.com/56078504/154793573-99e37378-7908-4a42-b45e-875cfda8c7bb.png)

5. Start the **Kafka Consumer** to receive the messages from the topic.
   
   ````
   bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic kafka-new-topic
   ````
   
   ![image](https://user-images.githubusercontent.com/56078504/154793588-7c0e29cf-c5f4-4d7b-a4d1-7a682a0accf8.png)

6. Now, run the Spark program using below command:
   
   ````
   spark2-submit –jars spark-sql-kafka-0-10_2.11-2.3.0.jar write_to_kafka.py
   ````
   ![image](https://user-images.githubusercontent.com/56078504/154793621-b8425be7-9659-4ae7-99d5-78b9fc334136.png)

7. Launch a new session and let’s move the players.csv file to testdir on HDFS. Below is the command
   
   ````
   hadoop fs -put players.csv testdir/players.csv
   ````   
   ![image](https://user-images.githubusercontent.com/56078504/154793651-7e0e9524-c137-49cc-92f0-6a0d8a0cdf45.png)
   
8. We see that the age of the players is printed on the consumer console. Below is the screenshot:
   
   ![image](https://user-images.githubusercontent.com/56078504/154793674-37d61beb-1570-4f6f-8ea6-63984ba2e2fd.png)

## Conclusion

Today, Kafka is used by thousands of companies including top ones. Kafka allows organizations to modernize their data strategies with event streaming architecture. Below are the few points which we grabbed from the above case study:

- Downloaded Kafka binaries and setup it on AWS EC2 instance.
- Used Kafka for 2 operations – Read from Kafka and Write to Kafka.
- Created a topic called **new-kafka-topic** and published the messages there
- Integrated Kafka to read from a consumer and applying various transformations.
- Passed data to **HDFS** as reading source and written the output into Kafka.

 
   

    
    

    
    



  
