from socket import socket
import boto3


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


def put_data(ip, port):
    if tcp_test(ip, port) == True:
        # Put custom metrics
        print("OK")
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
        print("FALHA")
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
