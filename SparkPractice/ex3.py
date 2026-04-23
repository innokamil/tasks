from pyspark.sql import SparkSession
import pyspark.sql.functions as sf 

def main():
    spark = (
        SparkSession.builder
        .appName("Solution 3.") 
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

    payment_df = (
        spark.read 
        .format("jdbc") 
        .option("url", db_url) 
        .option("dbtable", "payment") 
        .option("user", "postgres") 
        .option("password", "123456") 
        .load()
    )

    films_rented_with_amount_df = (
            inventory_df
            .join(rental_df, on="inventory_id")
            .join(payment_df, on="rental_id")
            .select("film_id", "amount")
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

    films_and_categories_df = (
            film_df
            .join(film_category_df, on="film_id")
            .join(category_df, on="category_id")
    )

    films_and_categories_df = (films_and_categories_df
                               .select(films_and_categories_df["film_id"],
                                       films_and_categories_df["title"], 
                                       films_and_categories_df["name"].alias("category_name")))

    res = (
            films_and_categories_df
            .join(films_rented_with_amount_df, on="film_id")
            .groupBy("category_name")
            .agg(
                sf.sum("amount").alias("counted")
            )
            .orderBy(sf.desc("counted"))
    )

    res.show()

if __name__ == "__main__":
    main()
