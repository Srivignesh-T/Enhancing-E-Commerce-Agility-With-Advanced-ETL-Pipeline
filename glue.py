# Importing required modules
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

# # properties of the RDS table to connect
# import sys
# import boto3
# from awsglue.transforms import *
# from awsglue.utils import getResolvedOptions
# from awsglue.context import GlueContext
# from pyspark.context import SparkContext

# Creating a spark session
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# properties of the RDS table to connect
jdbc_url = "jdbc:mysql://<RDS_database_url>:3306/<Database_name>"

db_properties = {
    "user": "username",
    "password": "user_password",
    "driver": "com.mysql.jdbc.Driver"
}

def clean_headers(df):
    # Ensure DataFrame is not empty before accessing columns
    if df.count() == 0:
        raise ValueError("DataFrame is empty.")

    # Rename columns and replace spaces with underscores
    headers = list(zip(df.columns, df.first()))
    for old_name, new_name in headers:
        df = df.withColumnRenamed(old_name, new_name)
    
    # Drop rows where the first column is the same as the header
    df = df.filter(df[0] != df.columns[0])

    for col in df.columns:
        df = df.withColumnRenamed(col, col.replace(" ", "_"))

    return df

# Loading the data from Glue Catalog
orders_df = glueContext.create_dynamic_frame.from_catalog(
    database = "ecom_db", 
    table_name = "ecom_orders"
)

returns_df = glueContext.create_dynamic_frame.from_catalog(
    database = "ecom_db", 
    table_name = "ecom_returns"
)

# Converting the data into pyspark dataframe for further manipulations
orders_df = orders_df.toDF()
returns_df = returns_df.toDF()

# Clean headers and join DataFrames
orders_df = clean_headers(orders_df)
returns_df = clean_headers(returns_df)

# Joining the data based on the Order_ID column
joined_df = orders_df.join(
    returns_df,
    orders_df.Order_ID == returns_df.Order_ID,
    'left'
    ).drop(returns_df.Order_ID)

# Insert the joined Dataframe into the RDS table

joined_df.write.jdbc(
    url=jdbc_url,
    table="final_table",
    mode="overwrite",
    properties=db_properties
)
