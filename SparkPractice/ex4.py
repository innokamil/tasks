from pyspark.sql import SparkSession
import pyspark.sql.functions as sf 

def main():
    spark = (
        SparkSession.builder
        .appName("Solution 4.") 
        .getOrCreate()
    )
    db_url = "jdbc:postgresql://pgdb:5432/pagila"

    film_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "film") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    inventory_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "inventory") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )


    df = (
            film_df
            .join(inventory_df, on="film_id", how="left_anti")
            # .where(sf.col("inventory_id").isNull())
            .select(sf.col("title"))
    )
    df.show()

if __name__ == "__main__":
    main()
