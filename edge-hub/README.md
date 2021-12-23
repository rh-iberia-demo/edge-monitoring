# Cental Hub

[![Edge Hub COPR Package](https://copr.fedorainfracloud.org/coprs/drhelius/edge-monitoring/package/edge-hub/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/drhelius/edge-monitoring/package/edge-hub/)


## Deploying on minikube

First, create a minikube instance. With 2 CPUs and 8 Gb RAM should be enough if you have a previous s3 storge. As we will also deploy an s3 with rook and ceph, we will add 2 extra CPUs, and we will add an extra disk for the Ceph OSD. We use kvm to virtualize the minikube node, but you can do it with other alternatives if you prefer.

```bash
minikube start --cpus=4 --memory=8192Mb --driver=kvm2 --addons dashboard,ingress,metrics-server -p central-node
```

To add a second disk for deploying ceph (not needed if you already have s3), refer to your virtualization choice on how to do it. If you use kvm, either you can use `virsh` or instal virt-manager as visual tooling.

## S3

You can skip this section if you already have a s3 object storage provider.

TO-DO

## Thanos Receiver

TO-DO

## Thanos Storage Proxy

TO-DO

## Thanos Querier

TO-DO

## Grafana

TO-DO

### Dashboards

TO-DO

## References

[Thanos and the Prometheus Operator](https://prometheus-operator.dev/docs/operator/thanos/)
[Community-Driven Thanos Helm Charts](https://github.com/thanos-community/helm-charts)
