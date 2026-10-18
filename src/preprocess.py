from pyspark.sql import SparkSession

def load_data():
    spark = (
        SparkSession.builder
        .appName("Student Performance Analytics")
        .master("local[*]")
        .getOrCreate()
    )

    df = spark.read.csv(
        "data/students.csv",
        header=True,
        inferSchema=True
    )

    return spark, df