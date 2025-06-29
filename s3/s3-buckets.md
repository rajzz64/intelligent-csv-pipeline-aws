# S3 Bucket Configuration

## 1. Input Bucket
- **Name**: `csv-input-bucket-raj`
- **Purpose**: Receives uploaded raw CSV files
- **Triggers**: Lambda function `validate_and_trigger`
- **Settings**:
  - Public access: **Disabled**
  - Object Ownership: **ACLs disabled (recommended)**
  - Versioning: **Enabled**
  - Default Encryption: **SSE-S3 (Amazon S3 managed keys)**

## 2. Output Bucket
- **Name**: `csv-output-bucket-raj`
- **Purpose**: Stores processed and cleaned CSV files
- **Settings**:
  - Public access: **Disabled**
  - Object Ownership: **ACLs disabled (recommended)**
  - Versioning: **Enabled**
  - Default Encryption: **SSE-S3 (Amazon S3 managed keys)**
