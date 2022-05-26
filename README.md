# Redis Keda

This project is a proof of concept for event-driven architecture on Kubernetes utilising Keda + Redis.

Inspired by [KEDA: Event Driven and Serverless Containers in Kubernetes - Jeff Hollan, Microsoft](https://www.youtube.com/watch?v=ZK2SS_GXF-g&t=1631s)

## Project Structure

### Redis/

[Redis](https://redis.io/) is a light weight in-memory data structure store that can be used as a database or messaging
queue. This project leverages Redis lists as a message queue and scaling metric for our consumer pods.

### Publisher/

The publisher/ directory contains a simple Python script that periodically appends batches of events to a list in Redis.
The format of the events being published are as follows:

```json5
{
  "wait": 17
} // random between 10 and 20
```

This script is packaged into a dockerfile that is published
to [scottzach1/redis-publisher](https://hub.docker.com/repository/docker/scottzach1/redis-publisher).

### Consumer/

The consumer directory contains a simple Python script that reads the first event in a Redis list. The script will then
parse the event and sleep for `wait` number of seconds before terminating.

Although extremely primitive, this provides a simple variable "IO blocking" workload that we can attempt to scale.

This script is packaged into a dockerfile that is published
to [scottzach1/redis-consumer](https://hub.docker.com/repository/docker/scottzach1/redis-consumer).

### Keda/ (In Progress)

**THIS PART OF THE DEMO IS NOT COMPLETED**

[Keda]](https://keda.sh/) (Kubernetes Event-driven Autoscaling) is an event based autoscaler that can be leveraged to
drive scaling in Kubernetes in useful ways based off a number of strategies.

This project utilises the `Redis Lists` trigger to scale the number of consumer pods based on the number of respective
events in the Redis list. Although Kubernetes provides native scaling strategies with
HPA [Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), this is
typically limited to resource metrics such as memory or CPU usage.

Unfortunately, this isn't always ideal in scenarios such as highly IO bound workloads. In such case, Kubernetes HPA
could retire a node before it had finished a lengthily IO bound job. Instead, by using keda you can enforce various
workflows such as a 1 pod per 1 event lifecycle that is scaled automagically via a
Keda [ScaledObject](https://keda.sh/docs/1.4/concepts/scaling-deployments/#scaledobject-spec).

## Setup Commands

First we will create a namespace for our project. 

```bash
kubectl create namespace redis-demo
```

### Redis

```bash
kubectl -n redis-demo apply -f redis/redis-config.yaml
kubectl -n redis-demo apply -f redis/redis-pod.yaml

kubectl -n redis-demo get all
#----------------------------
NAME                         READY   STATUS    RESTARTS   AGE
pod/redis-8476db56bf-mnzpg   1/1     Running   0          57s

NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/redis   ClusterIP   10.98.200.15   <none>        6379/TCP   57s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/redis   1/1     1            1           57s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/redis-8476db56bf   1         1         1       57s
```

### Publisher

```bash
kubectl -n redis-demo apply -f publisher/publisher-deployment.yaml

# To see created resources:
kubectl -n redis-demo get all
#----------------------------
NAME                                   READY   STATUS    RESTARTS   AGE
pod/redis-8476db56bf-mnzpg             1/1     Running   0          2m38s
pod/redis-publisher-6c45f5c474-g9gtq   1/1     Running   0          6s

NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/redis   ClusterIP   10.98.200.15   <none>        6379/TCP   2m38s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/redis             1/1     1            1           2m38s
deployment.apps/redis-publisher   1/1     1            1           6s

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/redis-8476db56bf             1         1         1       2m38s
replicaset.apps/redis-publisher-6c45f5c474   1         1         1       6s
```

We can then inspect the container output:

```bash
kubectl -n redis-demo logs redis-publisher-6c45f5c474-g9gtq
publishing events:
- {'wait': 15}
- {'wait': 17}
- {'wait': 15}
- {'wait': 13}
- {'wait': 10}
- {'wait': 17}
- {'wait': 20}
- {'wait': 11}
- {'wait': 10}
- {'wait': 14}

sleeping for 10s
```

As well as inspect the redis list:

```bash
kubectl -n redis-demo exec -it redis-8476db56bf-mnzpg -- redis-cli LLEN events
#----------------------------
(integer) 10  # this will increase w/ time
```

### Consumer

```bash
kubectl -n redis-demo apply -f consumer/consumer-deployment.yaml

# To see created resources:
kubectl -n redis-demo get all
#----------------------------
NAME                                   READY   STATUS    RESTARTS   AGE
pod/redis-8476db56bf-mnzpg             1/1     Running   0          7m29s
pod/redis-consumer-546577f78b-4rcr6    1/1     Running   0          16s
pod/redis-consumer-546577f78b-5lhx5    1/1     Running   0          16s
pod/redis-consumer-546577f78b-7xnt8    1/1     Running   0          16s
pod/redis-consumer-546577f78b-pzd6x    1/1     Running   0          16s
pod/redis-consumer-546577f78b-tjktc    1/1     Running   0          16s
pod/redis-publisher-6c45f5c474-g9gtq   1/1     Running   0          4m57s

NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/redis   ClusterIP   10.98.200.15   <none>        6379/TCP   7m29s

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/redis             1/1     1            1           7m29s
deployment.apps/redis-consumer    5/5     5            5           16s
deployment.apps/redis-publisher   1/1     1            1           4m57s

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/redis-8476db56bf             1         1         1       7m29s
replicaset.apps/redis-consumer-546577f78b    5         5         5       16s
replicaset.apps/redis-publisher-6c45f5c474   1         1         1       4m57s
```

We can also interrogate the output of a consumer pod:

```bash
kubectl -n redis-demo logs redis-consumer-546577f78b-5lhx5
#----------------------------
sleeping 19s
(done)
```

### Keda

COMING SOON<sup>tm</sup>
