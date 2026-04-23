from pyspark.sql import SparkSession
import pyspark.sql.functions as sf 

def main():
    spark = (
        SparkSession.builder
        .appName("Solution 6.") 
        .getOrCreate()
    )
    db_url = "jdbc:postgresql://pgdb:5432/pagila"

    customer_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "customer") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    address_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "address") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    customers_with_address = (
            customer_df
            .join(address_df, on="address_id")
            .select(
                sf.col("city_id"),
                sf.col("customer_id"),
                sf.col("first_name"),
                sf.col("last_name"),
                sf.col("active")
                )
            )
    city_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "city") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )


    res = (
            customers_with_address
            .join(city_df, on="city_id")
            .groupBy("city")
            .agg(
                sf.count("*").alias("customers"),
                sf.count_if(sf.col("active")==1).alias("active_customers"),
                sf.count_if(sf.col("active")==0).alias("inactive_customers"),
                )
            )

    res.show()

if __name__ == "__main__":
    main()
