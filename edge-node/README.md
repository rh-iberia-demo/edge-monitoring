# Edge Node

[![Edg Node COPR Package](https://copr.fedorainfracloud.org/coprs/drhelius/edge-monitoring/package/edge-node/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/drhelius/edge-monitoring/package/edge-node/)

The edge node has been defined in our case to run light containers. It will provide a simple and easy way to deploy different technologies ([prometheus](https://prometheus.io/), [node-exporter](https://prometheus.io/docs/guides/node-exporter/), database, services, etc), in a portable way, similar to what is expected for a container orchestrator. The difference with this setup is that it has been lightened, eliminating the need of orchestration capabilities, assuming the limitations and the benefits of it.

As a rule of thumb, we will try to store configuration files in /opt folder, to avoid any kind of clash with similar files for the operating system that can be included (sometimes just for showing examples).

We will implement an example app with a local database and a quarkus app.

<p align="center">
  <img src="edge-node.svg" alt="Sublime's custom image"/>
</p>

## Prometheus

We have chosen to use a push approach to send the metrics from the edge nodes to the central hub using remote-write storage configuration. Though, we will use `net=host` param only for debugging purposes.

The [prometheus configuration](prometheus/prometheus.yml) will be stored in `/etc/prometheus/prometheus.yml`.

The configuration will include a job scraper for every target (node-exporter, database, service), and a remote write for thanos receiver, which is explained in the central hub.

The command to run a prometheus container service in RHEL is:

```bash
podman run \
  --detach="true" \
  --volume="/etc/prometheus:/etc/prometheus:z" \
  --net="host" \
  --name="prometheus" \
  quay.io/prometheus/prometheus:latest
```

As we want prometheus to be run as a [systemd unit](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/building_running_and_managing_containers/index#assembly_porting-containers-to-systemd-using-podman_building-running-and-managing-containers), we have used `podman-generate-systemd` to create [the unit](prometheus/container-prometheus.service) using:

```bash
podman systemd create --new --files --name prometheus
```

For installing this systemd unit, we should follow the instructions documented in the previous link:

```bash
cp -Z container-prometheus.service /etc/systemd/system
systemctl daemon-reload
systemctl enable --now container-prometheus.service
```


## Node Exporter 

Similar as we have done with prometheus, we can deploy node-exporter with:

```bash
podman run \
  --detach="true" \
  --volume="/:/host:ro,rslave" \
  --net="host" \
  --pid="host" \
  --name="node-exporter"
  quay.io/prometheus/node-exporter:latest \
  --path.rootfs=/host
```

But we have created a [similar unit](node-exporter/container-node-exporter.service)

## CAdvisor (WIP)


```bash
podman run \
  --detach=true \
  --volume="/:/rootfs:ro" \
  --volume="/var/run:/var/run:rw" \
  --volume="/sys:/sys:ro" \
  --volume="/var/lib/containers/:/var/lib/containers:ro" \
  --volume="/sys/fs/cgroup:/sys/fs/cgroup:ro" \
  --publish=10250:8080 \
  --name=cadvisor \
  gcr.io/cadvisor/cadvisor:v0.43.0
```

## Database (Postgresql)

In this case, as we want to run two containers, the database and the exporter, sharing the same cgroup, we can do it like a kubernetes pod, creating it with `podman-pod-create`, like it is described in [this post](https://developers.redhat.com/blog/2019/01/15/podman-managing-containers-pods). 

```bash
podman pod create --name postgresql
```

Then, we will run the containers in the pod space with `--pod`

```bash
podman run \
  --pod="postgresql" \
  --detach="true" \
  --net="host" \
  --env="POSTGRES_PASSWORD=password" \
  --name="postgresql" \
  docker.io/library/postgres:latest
```

```bash
podman run \
  --pod="postgresql" \
  --detach="true" \
  --net="host" \
  --env="DATA_SOURCE_NAME=postgresql://postgres:password@localhost:5432/postgres?sslmode=disable" \
  --name="postgresql-exporter" \
  quay.io/prometheuscommunity/postgres-exporter:latest
```

Now, we can create the systemd unit with all the containers.

```bash
podman generate systemd --files --name postgresql
```
