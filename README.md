# Enhancing E-Commerce Agility With Advanced ETL Pipeline
As a Data Engineer Your objective is to build an end-to-end automated data processing workflow that handles data uploads from the Order and Returns teams, performs a join operation using Glue & PySpark, stores the joined data in Redshift, and sends notifications about the pipeline's status using SNS.

# Tools used:
* AWS Glue
* pyspark
* Step Funtion
* SNS
* RDS
* S3
* Athena
* Streamlit

# Project files:
* 'data_files' : Contains the csv files with e-commerce data.
* 'glue.py' : Contains the glue script.

# Workflow:
1. Data Ingestion to S3 - New data files (e.g., orders, returns) are uploaded to an S3 bucket and an S3 event triggers a Lambda function upon file upload.
2. Triggering Step Function - The Lambda function initiates the Step Function to automate the ETL process.
3. Data Processing in Glue - The Step Function starts an AWS Glue job that reads data from the Glue Data Catalog and merge it into a single table.
4. Loading Data to RDS - The transformed data is written to a table in Amazon RDS via JDBC
5. Logging and Monitoring - Step Function monitors each stage, logs execution results, and triggers alerts for any failures throw SNS.

# Teams and Data Upload:
*The Order and Returns teams use a Streamlit web application tailored to their needs to upload their respective data files.
* The Order team uploads "order" data files, while the Returns team uploads "returned" data files.
* The Streamlit app ensures secure data transfer and uploads the files to designated S3 buckets for each team.

# Lambda Trigger and Glue ETL:
* The Glue ETL job outputs the joined dataset based on “Order ID”, which includes information from both the "order" and "returned" data files.
* Store the joined table into Redshift data warehouse and finally team should query the final table by Athena.

# AWS Step Functions and Monitoring:
* Develop an AWS Step Function to orchestrate the entire workflow.
* Monitor the progress of each stage to track the execution status and any failures.
* And the team wants to see the success or fails pipeline execution message in streamlit UI

# SNS Notifications:
* Configure two subscription endpoints for email notifications
* After each execution, send an SNS notification indicating whether the pipeline succeeded or failed.

> [!CAUTION]
> * Ensure correct IAM permissions for Lambda, Glue, and Step Functions to access S3, execute workflows, and interact with RDS.

