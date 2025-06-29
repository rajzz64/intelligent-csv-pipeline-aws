import json
import boto3

def lambda_handler(event, context):
    print("Lambda triggered")
    s3 = boto3.client('s3')
    glue = boto3.client('glue')
    sns = boto3.client('sns')

    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Bucket: {bucket}")
        print(f"Key: {key}")

        if not key.endswith('.csv'):
            print("Not a CSV file.")
            sns.publish(
                TopicArn='arn:aws:sns:eu-north-1:183631301568:csv-processing-topic',
                Message=f"File '{key}' is not a CSV. Skipping.",
                Subject='CSV Processing Failed'
            )
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid file type')
            }

        print("Starting Glue job...")
        response = glue.start_job_run(JobName='csv-processing-job')
        job_id = response['JobRunId']
        print("Glue job started:", job_id)

        sns.publish(
            TopicArn='arn:aws:sns:eu-north-1:183631301568:csv-processing-topic',
            Message=f"Glue job started for file: {key}",
            Subject='CSV Processing Started'
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Glue job started')
        }

    except Exception as e:
        print("Error:", str(e))
        sns.publish(
            TopicArn='arn:aws:sns:eu-north-1:183631301568:csv-processing-topic',
            Message=f"Error processing file {key}: {str(e)}",
            Subject='CSV Processing Failed'
        )
        return {
            'statusCode': 500,
            'body': json.dumps('Glue job failed')
        }
