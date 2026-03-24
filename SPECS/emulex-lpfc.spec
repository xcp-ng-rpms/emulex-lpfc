%global package_speccommit 738ff9c8460ba54dc474f8555fb65bc08006860f
%global usver 14.4.393.31
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 14.4.393.31
%define vendor_name Emulex
%define vendor_label emulex
%define driver_name lpfc

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 14.4.393.31
Release: %{?xsrel}%{?dist}
License: GPL
Source0: emulex-lpfc-14.4.393.31.tar.gz

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%{?_cov_results_package}

%changelog
* Fri May 02 2025 Ross Lagerwall <ross.lagerwall@citrix.com> - 14.4.393.31-1
- CA-410184: Update to 14.4.393.31

* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 12.0.0.10-3
- CP-38416: Enable static analysis

* Tue Dec 01 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 12.0.0.10-2
- CP-35517: Silence an RPM warning and fix the build

* Tue Jan 15 2019 Deli Zhang <deli.zhang@citrix.com> - 12.0.0.10-1
- CP-30421: Upgrade lpfc driver to version 12.0.0.10

* Thu Nov 29 2018 Deli Zhang <deli.zhang@citrix.com> - 12.0.0.8-1
- CP-29709: Upgrade lpfc driver to version 12.0.0.8
