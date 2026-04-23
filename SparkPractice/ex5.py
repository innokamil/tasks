from pyspark.sql import SparkSession, Window
import pyspark.sql.functions as sf 

def main():
    spark = (
        SparkSession.builder
        .appName("Solution 5.") 
        .getOrCreate()
    )
    db_url = "jdbc:postgresql://pgdb:5432/pagila"

    film_actor_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "film_actor") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    film_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "film") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
        )

    film_and_actors_df = (
            film_actor_df
            .join(film_df, on="film_id")
            .select(sf.col("film_id"), 
                    sf.col("actor_id"), 
                    sf.col("title"))
            )

    films_category_df = (
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

    film_and_categories_df = (
            films_category_df
            .join(category_df, on="category_id")
            .select(
                sf.col("category_id"),
                sf.col("film_id"),
                sf.col("name").alias("category_name")
                )
            )

    actor_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "actor") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
        )


    actor_rankings_df = (
            actor_df
            .join(film_and_actors_df, on="actor_id")
            .join(film_and_categories_df, on="film_id")
            .where(sf.col("category_name") == "Children")
            .withColumn("fullname", sf.concat_ws(" ", "first_name", "last_name"))
            .groupBy("fullname")
            .agg(
                sf.count(sf.col("title")).alias("movie_count"),
                )
            .withColumn("ranked", 
                        sf.dense_rank()
                        .over(Window
                              .orderBy(sf.col("movie_count").desc()))
                        )
            .orderBy(sf.col("movie_count").desc())
            )



    res = (
            actor_rankings_df
            .where(sf.col("ranked") <= 3)
            .select(
                sf.col("fullname"),
                sf.col("movie_count")
                )
            )
    res.show()

if __name__ == "__main__":
    main()
