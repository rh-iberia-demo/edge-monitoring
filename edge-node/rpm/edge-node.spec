Name:       edge-node
Version:    0.0.1
Release:    1%{?dist}
Summary:    This is a side project created to understand the application of usual monitoring technologies in the contariner space (prometheus, thanos, grafana, etc) on usual RHEL scenarios.
License:    Apache-2.0
URL:        https://github.com/rh-iberia-demo/edge-monitoring
Source0:    https://github.com/rh-iberia-demo/edge-monitoring/archive/refs/heads/main.zip
Requires:   podman
BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
This is a side project created to understand the application of usual monitoring technologies in the contariner space (prometheus, thanos, grafana, etc) on usual RHEL scenarios.

%prep
%autosetup -n edge-monitoring-main

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/edge

cp edge-node/node-exporter/container-node-exporter.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql-exporter.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/container-postgresql.service %{buildroot}%{_unitdir}
cp edge-node/postgresql/pod-postgresql-pod.service %{buildroot}%{_sysconfdir}
cp edge-node/prometheus/container-prometheus.service %{buildroot}%{_sysconfdir}

cp edge-node/prometheus/prometheus.yml %{buildroot}%{_sysconfdir}/edge

%files
%{_unitdir}/systemd/system/container-node-exporter.service
%{_unitdir}/systemd/system/container-postgresql-exporter.service
%{_unitdir}/systemd/system/container-postgresql.service
%{_unitdir}/systemd/system/pod-postgresql-pod.service
%{_unitdir}/systemd/system/container-prometheus.service
%{_sysconfdir}/edge/prometheus.yml

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
