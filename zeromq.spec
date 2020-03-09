%global build_test 0 

Name:           zeromq
Version:        4.1.7
Release:        2
Summary:        An open-source universal messaging library
License:        LGPLv3+
URL:            http://www.zeromq.org
Source0:        https://github.com/zeromq/zeromq4-1/releases/download/v%{version}/zeromq-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/zeromq/cppzmq/master/zmq.hpp
Source2:        https://raw.githubusercontent.com/zeromq/cppzmq/master/LICENSE
#Fix https://github.com/zeromq/libzmq/issues/1129
Patch0001:      lt-test_many_sockets-and-lt-test_filter_ipc-fail-in-Docker-container-environment.patch
#Fix https://github.com/zeromq/libzmq/issues/1412
Patch0002:      HPUX-build-and-gmake-check-issues-solve.patch
BuildRequires:  autoconf automake libtool libsodium-devel gcc-c++
BuildRequires:  glib2-devel libuuid-devel openpgm-devel krb5-devel

%description
ZeroMQ (also spelled ØMQ, 0MQ or ZMQ) is a high-performance asynchronous messaging library,
aimed at use in distributed or concurrent applications. It provides a message queue,
but unlike message-oriented middleware, a ZeroMQ system can run without a dedicated message broker.
The library's API is designed to resemble Berkeley sockets.

%package devel
Summary:        Development files for zeromq
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains Development files for zeromq.

%package -n cppzmq-devel
Summary:        Development files for cppzmq
License:        MIT
Requires:       %{name}-devel = %{version}-%{release}

%description -n cppzmq-devel
This package contains Development files for zeromq.

%package     help
Summary:     Help documentation for zeromq

%description help
Help documentation for zeromq.

%prep
%autosetup -n %{name}-%{version} -p1
cp -a %{SOURCE2} .
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" configure.ac

%build
autoreconf -fi
%configure  --with-pgm --with-libgssapi_krb5 --disable-static
%make_build

%install
%make_install
install -pm644 %{SOURCE1} %{buildroot}%{_includedir}/
%delete_la

%check
%if %{build_test}
make check V=1 || ( cat test-suite.log && exit 1 )
%endif
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS
%license COPYING COPYING.LESSER
%{_bindir}/curve_keygen
%{_libdir}/libzmq.so.5*

%files devel
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*.h

%files -n cppzmq-devel
%license LICENSE
%{_includedir}/zmq.hpp

%files help
%doc ChangeLog MAINTAINERS NEWS
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*

%changelog
* Fri Mar 6 2020 shijian <shijian16@huawei.com> - 4.1.7-2
- Package init
