from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StructType


spark = SparkSession  \
	.builder  \
	.appName("StructuredSocketRead")  \
	.getOrCreate()
spark.sparkContext.setLogLevel('WARN')	
	
	
mySchema = StructType().add("name", "string").add("age","integer")	
	
lines = spark  \
	.readStream  \
	.option("delimiter",";")  \
	.format("csv")  \
	.schema(mySchema)  \
	.load("testdir/")

kafkaDF = lines.selectExpr("name as key","cast(age as string) as value")

query = kafkaDF  \
	.writeStream  \
	.outputMode("append")  \
	.format("kafka")  \
	.option("kafka.bootstrap.servers","ec2-3-218-67-108.compute-1.amazonaws.com:9092")  \
	.option("topic","kafka-new-topic")  \
	.option("checkpointLocation","checkpoint_dir")  \
	.start()
	
query.awaitTermination()
