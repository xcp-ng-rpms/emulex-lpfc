%define vendor_name Emulex
%define vendor_label emulex
%define driver_name lpfc

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 12.0.0.10
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-emulex-lpfc/archive?at=12.0.0.10&format=tgz&prefix=driver-emulex-lpfc-12.0.0.10#/emulex-lpfc-12.0.0.10.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-emulex-lpfc/archive?at=12.0.0.10&format=tgz&prefix=driver-emulex-lpfc-12.0.0.10#/emulex-lpfc-12.0.0.10.tar.gz) = fe7e1b1a21a85e6bdd91e125ef124ccf56efc85c


BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{__install} -d %{buildroot}%{_sysconfdir}/modprobe.d
%{__install} %{driver_name}.conf %{buildroot}%{_sysconfdir}/modprobe.d
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
%config(noreplace) %{_sysconfdir}/modprobe.d/*.conf
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Tue Jan 15 2019 Deli Zhang <deli.zhang@citrix.com> - 12.0.0.10-1
- CP-30421: Upgrade lpfc driver to version 12.0.0.10

* Thu Nov 29 2018 Deli Zhang <deli.zhang@citrix.com> - 12.0.0.8-1
- CP-29709: Upgrade lpfc driver to version 12.0.0.8
