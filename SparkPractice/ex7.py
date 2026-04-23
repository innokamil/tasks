from pyspark.sql import SparkSession, Window
import pyspark.sql.functions as sf 

def main():
    spark = (SparkSession.builder
             .appName("Solution 7.") 
             .getOrCreate())
    db_url = "jdbc:postgresql://pgdb:5432/pagila"

    city_df = (spark.read
               .format("jdbc")
               .option("url", db_url)
               .option("dbtable", "city")
               .option("user", "postgres")
               .option("password", "123456")
               .load())

    address_df = (spark.read
                  .format("jdbc")
                  .option("url", db_url)
                  .option("dbtable", "address")
                  .option("user", "postgres")
                  .option("password", "123456")
                  .load())

    customer_df = (spark.read
                   .format("jdbc")
                   .option("url", db_url)
                   .option("dbtable", "customer")
                   .option("user", "postgres")
                   .option("password", "123456")
                   .load())

    rental_df = (spark.read
                 .format("jdbc")
                 .option("url", db_url)
                 .option("dbtable", "rental")
                 .option("user", "postgres")
                 .option("password", "123456")
                 .load())

    inventory_df = (spark.read
                    .format("jdbc")
                    .option("url", db_url)
                    .option("dbtable", "inventory")
                    .option("user", "postgres")

                    .option("password", "123456")
                    .load())

    film_category_df = (spark.read
                        .format("jdbc")
                        .option("url", db_url)
                        .option("dbtable", "film_category")
                        .option("user", "postgres")
                        .option("password", "123456")
                        .load())

    category_df = (spark.read
                   .format("jdbc")
                   .option("url", db_url)
                   .option("dbtable", "category")
                   .option("user", "postgres")
                   .option("password", "123456")
                   .load())



    res = (city_df
           .join(address_df, on="city_id")
           .join(customer_df, on="address_id")
           .join(rental_df, on="customer_id")
           .join(inventory_df, on="inventory_id")
           .join(film_category_df, on="film_id")
           .join(category_df.alias("cat"), on="category_id")
           .where(sf.col("city").ilike("a%") | 
                  sf.col("city").like("%-%"))
           .select(sf.when(sf.col("city").ilike("a%"), "A*")
                   .when(sf.col("city").ilike("%-%"), "*-*")
                   .alias("city_group"),
                   sf.col("cat.name").alias("category_name"),
                   ((sf.col("return_date").cast("long") -
                    sf.col("rental_date").cast("long")) / 3600).alias("hours"))
           .groupBy("city_group", "category_name")
           .agg(sf.sum("hours")).alias("total_hours")
           .withColumn("rank",
                       sf.rank().over(Window.partitionBy("city_group").orderBy(sf.desc("sum(hours)"))))
           .filter(sf.col("rank") == 1)
           .drop("rank"))



    res.show()

if __name__ == "__main__":
    main()
