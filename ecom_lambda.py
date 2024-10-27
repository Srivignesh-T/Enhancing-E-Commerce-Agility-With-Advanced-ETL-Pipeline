import json
import boto3

# Initialize the Step Functions client
sfn_client = boto3.client('stepfunctions')

# Step Function ARN (replace with your Step Function's ARN)
STEP_FUNCTION_ARN = 'arn:aws:states:us-east-1:123456789012:stateMachine:YourStateMachineName'

def lambda_handler(event, context):
    try:
        # Start the Step Function execution
        response = sfn_client.start_execution(
            stateMachineArn=STEP_FUNCTION_ARN,
            input=json.dumps(event)  # Passing the entire event if needed by Step Function
        )
        
        return {
            'statusCode': 200,
            'body': f"Step Function triggered successfully with execution ARN: {response['executionArn']}"
        }
        
    except Exception as e:
        print(f"Error triggering Step Function: {e}")
        return {
            'statusCode': 500,
            'body': "Failed to trigger Step Function."
        }
