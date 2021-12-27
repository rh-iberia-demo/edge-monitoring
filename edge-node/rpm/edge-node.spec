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

cp edge-node/node-exporter/container-node-exporter.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql-db-exporter.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql-db.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/pod-postgresql.service %{buildroot}%{_unitdir}
cp edge-node/prometheus/container-prometheus.service %{buildroot}%{_unitdir}

echo "enable container-node-exporter.service" > %{buildroot}%{_presetdir}/80-container-node-exporter.preset
echo "enable container-postgresql-db-exporter.service" > %{buildroot}%{_presetdir}/80-container-postgresql-db-exporter.preset
echo "enable container-postgresql-db.service" > %{buildroot}%{_presetdir}/80-container-postgresql-db.preset
echo "enable pod-postgresql.service" > %{buildroot}%{_presetdir}/80-pod-postgresql.preset
echo "enable container-prometheus.service" > %{buildroot}%{_presetdir}/80-container-prometheus.preset

cp edge-node/prometheus/prometheus.yml %{buildroot}%{_sysconfdir}/prometheus
cp edge-node/postgresql/prometheus/targets.d/postgresql-exporter.yml %{buildroot}%{_sysconfdir}/prometheus/targets.d

%files
%{_unitdir}/container-node-exporter.service
%{_unitdir}/container-postgresql-db-exporter.service
%{_unitdir}/container-postgresql-db.service
%{_unitdir}/pod-postgresql.service
%{_unitdir}/container-prometheus.service

%{_presetdir}/80-container-node-exporter.preset
%{_presetdir}/80-container-postgresql-db-exporter.preset
%{_presetdir}/80-container-postgresql-db.preset
%{_presetdir}/80-pod-postgresql.preset
%{_presetdir}/80-container-prometheus.preset

%{_sysconfdir}/prometheus/prometheus.yml
%{_sysconfdir}/prometheus/targets.d/postgresql-exporter.yml

%post
%systemd_post container-node-exporter.service
%systemd_post container-postgresql-db-exporter.service
%systemd_post container-postgresql-db.service
%systemd_post pod-postgresql.service
%systemd_post container-prometheus.service

%preun
%systemd_preun container-node-exporter.service
%systemd_preun container-postgresql-db-exporter.service
%systemd_preun container-postgresql-db.service
%systemd_preun pod-postgresql.service
%systemd_preun container-prometheus.service

%postun
%systemd_postun_with_restart container-node-exporter.service
%systemd_postun_with_restart container-postgresql-db-exporter.service
%systemd_postun_with_restart container-postgresql-db.service
%systemd_postun_with_restart pod-postgresql.service
%systemd_postun_with_restart container-prometheus.service
