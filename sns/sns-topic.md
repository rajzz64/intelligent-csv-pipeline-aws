# SNS Topic for Notification

## Topic Details
- **Topic Name**: `csv-processing-topic`
- **Type**: Standard
- **Purpose**: Sends success/failure email alerts during the CSV processing pipeline

## Subscription
- **Protocol**: Email
- **Endpoint**: rajgupt611+csvpipeline@gmail.com
- **Status**:✅ Confirmed

## Use Case
This topic is triggered by the Lambda function to notify:
- ✅ On successful validation and Glue job start
- ❌ On errors (invalid file format, bad schema, etc.)
