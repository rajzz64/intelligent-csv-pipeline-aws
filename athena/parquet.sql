CREATE EXTERNAL TABLE IF NOT EXISTS clean_students_parquet (
  studentid bigint,
  name string,
  email string,
  score bigint
)
STORED AS PARQUET
LOCATION 's3://csv-output-bucket-raj/processed-data/';
