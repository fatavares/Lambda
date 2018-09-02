"""
Lambda Function build to create a Health Check of a Service on a specific server.
If you want to create a Failover DNS Record for a private service you can use the CloudWatch metric to create a
Route 53 health check from the metric ALARM
The Route 53 Endpoint Health Check needs the subnet to be public.
This Lambda Function requires a IAM Role with permission AWSLambdaENIManagementAccess and CloudWatchFullAccess, the
Lambda Function must be configured on a VPC, inside a private subnet that have a NAT Gateway
"""

from socket import socket
import boto3

# Open a socket on a specified TCP port
def tcp_test(server, port):
    try:
        sock = socket()
        sock.connect((server, port))
        sock.close()
        return True
    except:
        return False

# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch')


# Put the result in a custom Cloudwatch metric
def put_data(ip, port):
    if tcp_test(ip, port) is True:
        # Put custom metrics
        cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'Server_XXXXX_Service_Availability',
                    'Dimensions': [
                        {
                            'Name': 'Availability',
                            'Value': 'Status'
                        },
                    ],
                    'Unit': 'None',
                    'Value': 1.0
                },
            ],
            Namespace='LambdaHealthCheck'
        )
    else:
        cloudwatch.put_metric_data(
            MetricData=[
                {
                    'MetricName': 'Server_XXXXX_Service_Availability',
                    'Dimensions': [
                        {
                            'Name': 'Availability',
                            'Value': 'Status'
                        },
                    ],
                    'Unit': 'None',
                    'Value': 0.0
                },
            ],
            Namespace='LambdaHealthCheck'
        )


def lambda_handler(event, context):
    put_data('192.168.0.1', 80)
