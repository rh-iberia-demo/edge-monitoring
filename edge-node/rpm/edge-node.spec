#### NOTE: if building locally you may need to do the following:
####
#### yum install rpmdevtools -y
#### spectool -g -R edge-node.spec
####
#### At this point you can use rpmbuild -ba edge-node.spec
#### (this is because Source0 is a remote Github location

Name:       edge-node
Version:    {{{ git_dir_version name="edge-node" }}}
Release:    1%{?dist}
Summary:    This is a side project created to understand the application of usual monitoring technologies in the container space (prometheus, thanos, grafana, etc) on usual RHEL scenarios.
License:    Apache-2.0
URL:        https://github.com/rh-iberia-demo/edge-monitoring
Source0:    https://github.com/rh-iberia-demo/edge-monitoring/archive/refs/heads/main.zip
Requires:           podman
Requires:           systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
BuildRequires:      systemd
BuildRequires:      systemd-rpm-macros

%description
This is a side project created to understand the application of usual monitoring technologies in the container space (prometheus, thanos, grafana, etc) on usual RHEL scenarios.

%prep
%autosetup -n edge-monitoring-main

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_presetdir}
mkdir -p %{buildroot}%{_sysconfdir}/prometheus
mkdir -p %{buildroot}%{_sysconfdir}/prometheus/targets.d
mkdir -p %{buildroot}%{_sysconfdir}/promtail

cp edge-node/prometheus/container-prometheus.service %{buildroot}%{_unitdir}
cp edge-node/node-exporter/container-node-exporter.service %{buildroot}%{_unitdir}
cp edge-node/promtail/container-promtail.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql-exporter.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql-db.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/pod-postgresql.service %{buildroot}%{_unitdir}
cp edge-node/quarkus/container-cart-item-app.service %{buildroot}%{_unitdir}

echo "enable container-prometheus.service" > %{buildroot}%{_presetdir}/80-container-prometheus.preset
echo "enable container-node-exporter.service" > %{buildroot}%{_presetdir}/80-container-node-exporter.preset
echo "enable container-promtail.service" > %{buildroot}%{_presetdir}/80-container-promtail.preset
echo "enable container-postgresql-exporter.service" > %{buildroot}%{_presetdir}/80-container-postgresql-exporter.preset
echo "enable container-postgresql-db.service" > %{buildroot}%{_presetdir}/80-container-postgresql-db.preset
echo "enable pod-postgresql.service" > %{buildroot}%{_presetdir}/80-pod-postgresql.preset
echo "enable container-cart-item-app.service" > %{buildroot}%{_presetdir}/80-container-cart-item-app.preset

cp edge-node/prometheus/prometheus.yml %{buildroot}%{_sysconfdir}/prometheus
cp edge-node/promtail/config.yml %{buildroot}%{_sysconfdir}/promtail
cp edge-node/promtail/prometheus/targets.d/promtail.yml %{buildroot}%{_sysconfdir}/prometheus/targets.d
cp edge-node/postgresql/prometheus/targets.d/postgresql-exporter.yml %{buildroot}%{_sysconfdir}/prometheus/targets.d
cp edge-node/quarkus/prometheus/targets.d/quarkus.yml %{buildroot}%{_sysconfdir}/prometheus/targets.d

%files
%{_unitdir}/container-prometheus.service
%{_unitdir}/container-node-exporter.service
%{_unitdir}/container-promtail.service
%{_unitdir}/container-postgresql-exporter.service
%{_unitdir}/container-postgresql-db.service
%{_unitdir}/pod-postgresql.service
%{_unitdir}/container-cart-item-app.service

%{_presetdir}/80-container-prometheus.preset
%{_presetdir}/80-container-node-exporter.preset
%{_presetdir}/80-container-promtail.preset
%{_presetdir}/80-container-postgresql-exporter.preset
%{_presetdir}/80-container-postgresql-db.preset
%{_presetdir}/80-pod-postgresql.preset
%{_presetdir}/80-container-cart-item-app.preset

%{_sysconfdir}/prometheus/prometheus.yml
%{_sysconfdir}/prometheus/targets.d/promtail.yml
%{_sysconfdir}/prometheus/targets.d/postgresql-exporter.yml
%{_sysconfdir}/prometheus/targets.d/quarkus.yml
%{_sysconfdir}/prometail/config.yml

%post
%systemd_post container-prometheus.service
%systemd_post container-node-exporter.service
%systemd_post container-promtail.service
%systemd_post container-postgresql-exporter.service
%systemd_post container-postgresql-db.service
%systemd_post pod-postgresql.service
%systemd_post container-cart-item-app.service

%preun
%systemd_preun container-prometheus.service
%systemd_preun container-node-exporter.service
%systemd_preun container-promtail.service
%systemd_preun container-postgresql-exporter.service
%systemd_preun container-postgresql-db.service
%systemd_preun pod-postgresql.service
%systemd_preun container-cart-item-app.service

%postun
%systemd_postun_with_restart container-prometheus.service
%systemd_postun_with_restart container-node-exporter.service
%systemd_postun_with_restart container-promtail.service
%systemd_postun_with_restart container-postgresql-exporter.service
%systemd_postun_with_restart container-postgresql-db.service
%systemd_postun_with_restart pod-postgresql.service
%systemd_postun_with_restart container-cart-item-app.service
