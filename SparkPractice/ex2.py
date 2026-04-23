from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat, count, desc, lit

def main():
    spark = (
        SparkSession.builder
        .appName("Solution 2.") 
        .getOrCreate()
    )
    db_url = "jdbc:postgresql://pgdb:5432/pagila"

    inventory_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "inventory") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    rental_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "rental") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    films_rented_df = (
            inventory_df
            .join(rental_df, on="inventory_id")
            .groupBy("film_id")
            .agg(count("*").alias("cnt"))
            .orderBy(desc("cnt"))
            )

    film_and_actor_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "film_actor") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    actors_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "actor") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    actors_in_movies_df = (
        actors_df
        .join(film_and_actor_df, on="actor_id")
        .withColumn("actor", concat(
            col("first_name"), 
            lit(" "),
            col("last_name"))
        )
    )

    res = (
            actors_in_movies_df
            .join(films_rented_df, on="film_id")
            .select(["actor", "cnt"])
            .orderBy("cnt", ascending=False)
            )

    res.show()

if __name__ == "__main__":
    main()
