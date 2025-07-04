import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
glue = boto3.client('glue')
sns = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:eu-north-1:183631301568:csv-processing-topic'
GLUE_JOB_NAME = 'csv-processing-job'

def lambda_handler(event, context):
    print("Lambda triggered")

    try:
        # Extract bucket and key from event
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        print(f"Bucket: {bucket}")
        print(f"Key: {key}")

        # Validate file type
        if not key.endswith('.csv'):
            print("Not a CSV file.")
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"File '{key}' is not a CSV. Skipping.",
                Subject='CSV Processing Skipped'
            )
            return {'statusCode': 400, 'body': 'Not a CSV file'}

        # Construct full S3 path
        input_path = f's3://{bucket}/{key}'
        print("Input path for Glue job:", input_path)

        # Start Glue job with input path argument
        response = glue.start_job_run(
            JobName=GLUE_JOB_NAME,
            Arguments={
                '--input_path': input_path
            }
        )

        job_id = response['JobRunId']
        print("Glue job started:", job_id)

        # Notify via SNS
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Glue job started for file: {key}\nJob ID: {job_id}",
            Subject='CSV Processing Started'
        )

        return {'statusCode': 200, 'body': f'Glue job started: {job_id}'}

    except Exception as e:
        print("Error:", str(e))
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Error processing file {key}: {str(e)}",
            Subject='CSV Processing Failed'
        )
        return {'statusCode': 500, 'body': 'Glue job failed'}
