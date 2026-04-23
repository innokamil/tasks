from pyspark.sql import SparkSession
from pyspark.sql.functions import count, desc

def main():
    spark = (
        SparkSession.builder
        .appName("Solution 1.") 
        .getOrCreate()
    )
    db_url = "jdbc:postgresql://pgdb:5432/pagila"

    film_category_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "film_category") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    category_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "category") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    res = (
        film_category_df
        .join(other=category_df, on="category_id")
        .groupBy("name")
        .agg(count("*").alias("cnt"))
        .orderBy(desc("cnt"))
    )

    res.show()

if __name__ == "__main__":
    main()
