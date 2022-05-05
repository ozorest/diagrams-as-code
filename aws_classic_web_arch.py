from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, EC2AutoScaling
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.network import ELB, Route53, CloudFront, NATGateway
from diagrams.aws.security import WAF, CertificateManager
from diagrams.aws.storage import S3, EFS
from diagrams.onprem.client import User

with Diagram("AWS Classic Web Architecture", show=False):
    user = User("webclient")
    dns = Route53("dns service")
    waf = WAF("waf")
    cf = CloudFront("cdn")
    acm = CertificateManager("cert manager")
    s3 = S3("s3")    
    
    with Cluster("VPC"):        
        weblb = ELB("web lb")
        applb = ELB("app lb")
        efs = EFS("shared storage")
        ecache = Elasticache("caching service")
        with Cluster("Web Subnet"):              
            webaz1 = EC2("web server\nAZ1")
            EC2AutoScaling("web autoscale")
            webaz2 = EC2("web server\nAZ2")
            webservers = [webaz1, webaz2]
    
        with Cluster("App Subnet"):
            appaz1 = EC2("app server\nAZ1")
            EC2AutoScaling("app autoscale")
            appaz2 = EC2("app server\nAZ2")
            appservers = [appaz1, appaz2]
    
        with Cluster("Database Subnet"):
            primary_db = RDS("primary database\nAZ1")
            primary_db - RDS("standby database\nAZ2")            
    
    waf >> cf >> [s3, acm]
    acm << weblb
    user >> dns >> waf >> weblb >> webservers >> applb >> appservers >> primary_db
    appservers >> efs
    appservers >> ecache << primary_db