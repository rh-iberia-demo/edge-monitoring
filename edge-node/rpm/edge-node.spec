#### NOTE: if building locally you may need to do the following:
####
#### yum install rpmdevtools -y
#### spectool -g -R edge-node.spec
####
#### At this point you can use rpmbuild -ba edge-node.spec
#### (this is because Source0 is a remote Github location

Name:       edge-node
Version:    {{{git_dir_version}}}
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
mkdir -p %{buildroot}%{_sysconfdir}/prometheus

cp edge-node/node-exporter/container-node-exporter.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql-exporter.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/pod-postgresql-pod.service %{buildroot}%{_unitdir}
cp edge-node/prometheus/container-prometheus.service %{buildroot}%{_unitdir}

echo "enable container-node-exporter.service" > %{buildroot}%{_presetdir}/container-node-exporter.preset
echo "enable container-postgresql-exporter.service" > %{buildroot}%{_presetdir}/container-postgresql-exporter.preset
echo "enable container-postgresql.service" > %{buildroot}%{_presetdir}/container-postgresql.preset
echo "enable pod-postgresql-pod.service" > %{buildroot}%{_presetdir}/pod-postgresql-pod.preset
echo "enable container-prometheus.service" > %{buildroot}%{_presetdir}/container-prometheus.preset

cp edge-node/prometheus/prometheus.yml %{buildroot}%{_sysconfdir}/prometheus

%files
%{_unitdir}/container-node-exporter.service
%{_unitdir}/container-postgresql-exporter.service
%{_unitdir}/container-postgresql.service
%{_unitdir}/pod-postgresql-pod.service
%{_unitdir}/container-prometheus.service

%{_presetdir}/container-node-exporter.preset
%{_presetdir}/container-postgresql-exporter.preset
%{_presetdir}/container-postgresql.preset
%{_presetdir}/pod-postgresql-pod.preset
%{_presetdir}/container-prometheus.preset

%{_sysconfdir}/prometheus/prometheus.yml

%post
%systemd_post container-node-exporter.service
%systemd_post container-postgresql-exporter.service
%systemd_post container-postgresql.service
%systemd_post pod-postgresql-pod.service
%systemd_post container-prometheus.service

%preun
%systemd_preun container-node-exporter.service
%systemd_preun container-postgresql-exporter.service
%systemd_preun container-postgresql.service
%systemd_preun pod-postgresql-pod.service
%systemd_preun container-prometheus.service

%postun
%systemd_postun_with_restart container-node-exporter.service
%systemd_postun_with_restart container-postgresql-exporter.service
%systemd_postun_with_restart container-postgresql.service
%systemd_postun_with_restart pod-postgresql-pod.service
%systemd_postun_with_restart container-prometheus.service
