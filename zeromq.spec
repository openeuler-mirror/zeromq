Name:           zeromq
Version:        4.3.4
Release:        1
Summary:        Software library for fast, message-based applications

License:        LGPLv3+
URL:            https://zeromq.org
Source0:        https://github.com/%{name}/libzmq/archive/v%{version}/libzmq-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  asciidoc
BuildRequires:  xmlto
BuildRequires:  libsodium-devel
BuildRequires:  libunwind-devel
BuildRequires:  openpgm-devel
BuildRequires:  krb5-devel

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package help
Summary:        Help documents for zeromq

%description help
Help documents for zeromq.


%prep
%autosetup -p1 -n libzmq-%{version}
rm -rf external/wepoll
chmod -x src/xsub.hpp


%build
autoreconf -fi
%configure \
            --with-pgm \
            --with-libgssapi_krb5 \
            --with-libsodium \
            --enable-libunwind \
            --disable-Werror \
            --disable-static
%make_build


%install
%make_install
rm %{buildroot}%{_libdir}/libzmq.la


%check
make check V=1 || ( cat test-suite.log && exit 1 )
%ldconfig_scriptlets


%files
%doc AUTHORS
%{_bindir}/curve_keygen
%{_libdir}/libzmq.so.5*

%files devel
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*.h

%files help
%doc README.md NEWS
%license COPYING COPYING.LESSER
%{_mandir}/man3/zmq_*
%{_mandir}/man7/zmq_*
%{_mandir}/man7/zmq.*

%changelog
* Fri Jun 4 2021 wutao <wutao61@huawei.com> - 4.3.4-3
- upgrade to 4.3.4 to fix CVE-2021-20236

* Fri Mar 6 2020 shijian <shijian16@huawei.com> - 4.1.7-2
- Package init
