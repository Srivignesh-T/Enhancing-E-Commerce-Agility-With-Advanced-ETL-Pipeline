import boto3
import streamlit as st
import os
from dotenv import load_dotenv
from io import BytesIO
from datetime import datetime
import time

# Load environment variables from .env file
load_dotenv()

access_key_id = os.getenv('ACCESS_KEY_ID')
secret_key_id = os.getenv('SECRET_ACCESS_KEY')
region = "us-east-1"
orders_bucket = os.getenv('ORDERS_BUCKET')
returns_bucket = os.getenv('RETURNS_BUCKET')
step_arn = os.getenv('STEP_ARN')

# Creating an S3 client 
s3_client = boto3.client(
        service_name='s3',
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_key_id
    )

# Creating a step function client:
step_client = boto3.client(
        service_name='stepfunctions',
        region_name=region,
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_key_id
    )

# function to upload file to S3 bucket
def s3_upload_file(file, bucket, s3_file_name):
    try:
        s3_client.upload_fileobj(file, bucket, s3_file_name)

    except Exception as e:
        st.error(e)

# function to convert the received file into file-like object and call the s3 file upload function
def file_uploader(file, bucket):
    file_data = BytesIO(file.getvalue())
    tstamp = str(datetime.now())
    tstamp = tstamp.replace(" ", "_")
    file_name = f"{tstamp}.csv"
    s3_upload_file(file_data, bucket, file_name)

# Creating the file_uploader widgets to get files from user
with st.form("File uploader", clear_on_submit=True):
    st.title("Orders file uploader : ")
    orders_file = st.file_uploader("Upload your orders csv file : ", type = "csv", key = "Orders")
    st.title("Returns file uploader : ")
    returns_file = st.file_uploader("Upload your returns csv file : ", type = "csv", key = "Returns")
    submitted = st.form_submit_button("Upload")

    # Uploading the received files into S3 bucket and waiting for the ETL job to complete
    if submitted and (orders_file is not None and returns_file is not None):
        upload_time = str(datetime.now())
        file_uploader(orders_file, orders_bucket)
        file_uploader(returns_file, returns_bucket)
        success = st.success("Files uploaded successfully")
        time.sleep(5)
        success.empty()
        result = st.warning("ETL job is in progress")
        complete = False
        while complete != True:
            response = step_client.list_executions(stateMachineArn = step_arn)
            latest_run = sorted(response["executions"], key = lambda x:x["startDate"], reverse = True)[0]
            start_time = latest_run['startDate'].strftime('%Y-%m-%d %H:%M:%S.%f')
            if latest_run["status"] == "SUCCEEDED" and start_time > upload_time:
                result.empty()
                result = st.success(f"ETL job succeeded. For further details check the step function execution {latest_run['name']}")
                complete = True
            elif latest_run["status"] == "FAILED" and start_time > upload_time:
                result.empty()
                result = st.error(f"ETL job failed. For further details check the step function execution {latest_run['name']}")
                complete = True
            else:
                time.sleep(10)
    elif submitted and (orders_file is None or returns_file is None):
        st.warning("Please submit both the orders and the returns file to upload")
    else:
        st.write("Please upload the orders and the returns files")