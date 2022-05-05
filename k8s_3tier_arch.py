from diagrams import Diagram, Cluster
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Pod, StatefulSet
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.storage import PV, PVC, StorageClass
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.client import User

with Diagram("Kubernetes 3-Tier Architecture", show=False):
    user = User("client")
    lb = LoadBalancing("load balancer")
    
    with Cluster("Kubernetes Cluster"):
        with Cluster("namespace: frontend"):
            ingress = Ingress("domain.com")
            frontsvc = Service("frontend svc")
            frontpods = [Pod("frontend pod1"), Pod("frontend pod2"), Pod("frontend pod3")]
            ingress >> frontsvc >> frontpods
        
        with Cluster("namespace: backend"):
            backsvc = Service("backend svc")
            backpods = [Pod("backend pod1"), Pod("backend pod2"), Pod("backend pod3")]
            backsvc >> backpods
        
        with Cluster("namespace: database"):
            dbsvc = Service("database svc")
            dbsts1 = StatefulSet("db sts1")
            dbsts2 = StatefulSet("db sts2")
            dbsts3 = StatefulSet("db sts3")
            dbsts = [dbsts1, dbsts2, dbsts3]
            dbsvc >> dbsts
        
        pvc1 = PVC("")
        pvc2 = PVC("")
        pvc3 = PVC("")
        pvcs = [pvc1, pvc2, pvc3]
        pv = PV("")
        stclass = StorageClass("")
        
        frontpods >> backsvc
        backpods >> dbsvc
        pvcs << pv << stclass
        dbsts1 << pvc1
        dbsts2 << pvc2
        dbsts3 << pvc3
        
        user >> lb >> ingress