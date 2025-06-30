import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Get job name
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize contexts and job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from the input bucket
input_dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://csv-input-bucket-raj/sample1.csv"]},
    format="csv",
    format_options={"withHeader": True}
)

# (Optional) Add any transformation here if needed

# Write to the output bucket
glueContext.write_dynamic_frame.from_options(
    frame=input_dynamic_frame,
    connection_type="s3",
    connection_options={"path": "s3://csv-output-bucket-raj/", "partitionKeys": []},
    format="csv"
)

# Commit job
job.commit()
