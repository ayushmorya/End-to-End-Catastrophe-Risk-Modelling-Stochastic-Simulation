import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
# Added 'lit' to the imports
from pyspark.sql.functions import col, when, lit, create_map, udf
from pyspark.sql.types import IntegerType, DoubleType, StringType

# Initialize Contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init("CatModel_EDM_ETL", {})

# Load Raw Location Data
loc_raw = spark.read.option("header", "true") \
  .csv("s3://cat-mod-project/landing/location_raw/location_raw.csv")

# Load Raw Policy Data
pol_raw = spark.read.option("header", "true") \
  .csv("s3://cat-mod-project/landing/policy_raw/policy_raw.csv")
   
#------------------------------------------------------------------------------------------
# Construction Map: Wood->1, Masonry->2, Steel->4, RCC->6
const_map = create_map(
    lit("Wood"), lit(1),
    lit("Masonry"), lit(2),
    lit("Steel"), lit(4),
    lit("RCC"), lit(6)
)

# Occupancy Map: Residential->301, Commercial->311, Industrial->321
occ_map = create_map(
    lit("Residential"), lit(301),
    lit("Commercial"), lit(311),
    lit("Industrial"), lit(321)
)

# Apply Transformations
loc_transformed = loc_raw.withColumn("const_code", const_map[col("construction_type")]) \
                        .withColumn("occ_code", occ_map[col("occupancy_type")]) \
                        .withColumn("latitude", col("latitude").cast(DoubleType())) \
                        .withColumn("longitude", col("longitude").cast(DoubleType())) \
                        .withColumn("tiv", col("sum_insured").cast(DoubleType())) \
                        .withColumn("year_built", col("year_built").cast(IntegerType()))

# Data Quality Check: Filter invalid TIVs or Coordinates
loc_clean = loc_transformed.filter(
    (col("tiv") > 0) & 
    (col("latitude").between(-90, 90)) & 
    (col("longitude").between(-180, 180))
)

#------------------------------------------------------------------------------------------
# The Financial Join

pol_clean = pol_raw.withColumn("deductible", col("deductible").cast(DoubleType())) \
                  .withColumn("limit", col("policy_limit").cast(DoubleType())) \
                  .withColumn("coinsurance", col("coinsurance").cast(DoubleType()))

# Join Location and Policy Data
edm_df = loc_clean.join(pol_clean, ["account_id", "location_id"], "left")

edm_df.write.mode("overwrite").parquet("s3://cat-mod-project/curated/edm/")