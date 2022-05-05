from sys import api_version
from tokenize import group
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SimpleQueueServiceSqs
from diagrams.aws.network import APIGateway
from diagrams.custom import Custom
from urllib.request import urlretrieve

graph_attr = {
    "splines":"spline"
}

clus_attr = {
    "style": "invis"
}

with Diagram("AWS Serverless Event-Driven Architecture", show=False, graph_attr=graph_attr):
    csv_icon_url = "https://cdn-icons-png.flaticon.com/512/28/28842.png"
    csv_icon = "assets/csv_icon.png"
    urlretrieve(csv_icon_url, csv_icon)
    csv = Custom("CSV files", csv_icon)
    
    app_icon_url = "https://cdn-icons-png.flaticon.com/512/5/5069.png"
    app_icon = "assets/app_icon.png"
    urlretrieve(app_icon_url, app_icon)
    app = Custom("Application", app_icon)
    
    with Cluster("AWS Cloud"):
        s3 = S3("S3 Bucket")
        lambda_s3_sqs = Lambda("Lambda\n\(S3 to SQS\)")
        with Cluster("", graph_attr=clus_attr):
            sqs_queue = SimpleQueueServiceSqs("SQS Queue")
            sqs_dlq = SimpleQueueServiceSqs("SQS DLQ")
        lambda_sqs_dynamo = Lambda("Lambda\n\(SQS to DynamoDB\)")
        dynamo = Dynamodb("DynamoDB Table")
        apigtw = APIGateway("API Gateway\nEdge Optimized API")
        lambda_get = Lambda("", width="0.80")
        lambda_post = Lambda("", width="0.80")
        lambda_delete = Lambda("", width="0.80")
        blankA = Node("", shape="plaintext", width="0", height="0")
        blankB = Node("", shape="plaintext", width="0", height="0")
                
    csv >> s3 
    s3 >> Edge(label="S3 Event Trigger") >> lambda_s3_sqs
    s3 >> Edge(label="Retrieve File Contents") >> lambda_s3_sqs 
    lambda_s3_sqs >> Edge(label="Produce Messages") >> sqs_queue
    sqs_queue >> Edge(style="dashed",constraint="False") >> sqs_dlq
    sqs_queue >> Edge(label="SQS Event Trigger") >> lambda_sqs_dynamo
    sqs_queue << Edge(label="Consume Messages") << lambda_sqs_dynamo
    lambda_sqs_dynamo >> Edge(label="get\nscan\nput\nupdate\ndelete") >> dynamo
    app - blankA - blankB >> Edge(label="HTTP(S)\nREST") >> apigtw
    apigtw >> Edge(label="GET", style="dashed") >> lambda_get >> Edge(label="get", style="dashed") >> dynamo
    apigtw >> Edge(label="POST") >> lambda_post >> Edge(label="put") >> dynamo
    apigtw >> Edge(label="DELETE", style="dashed") >> lambda_delete >> Edge(label="delete", style="dashed") >> dynamo