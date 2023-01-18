# Disable test for now by default since tests are using tcl
%bcond_with check

Name:       sqlite
Summary:    Library that implements an embeddable SQL database engine
Version:    3.40.1
Release:    1
License:    Public Domain
URL:        https://www.sqlite.org
Source0:    %{name}-%{version}.tar.bz2
Patch0:     sqlite-3.12.2-no-malloc-usable-size.patch
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(zlib)
# See bug 15004 Add ICU support to sqlite.
BuildRequires:  pkgconfig(icu-i18n)
%if %{with check}
BuildRequires:  tcl-devel
%else
# Need to have tcl since sqlite generates files like sqlite3.h and
# shell.c with the tclsh script.
BuildRequires:  tcl
%endif
Requires:   %{name}-libs = %{version}-%{release}

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server.  Version 2 and version 3 binaries
are named to permit each to be installed on a single host

%package devel
Summary:    Development tools for the sqlite3 embeddable SQL database engine
Requires:   %{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%package doc
Summary:   Documentation for %{name}
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}

%description doc
Man page for %{name}.

%package libs
Summary: Shared library for the sqlite3 embeddable SQL database engine
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# We need to ensure rpm is updated before sqlite-libs.
# 4.3.0 release had already 4.16.1.3 version of the rpm.
Requires(pre): rpm >= 4.14.1+git8

%description libs
This package contains the shared library for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS \
	-DSQLITE_ENABLE_COLUMN_METADATA=1 \
	-DSQLITE_DISABLE_DIRSYNC=1 \
	-DSQLITE_SECURE_DELETE=1 \
	-DSQLITE_ENABLE_UNLOCK_NOTIFY=1 \
	-DSQLITE_ENABLE_DBSTAT_VTAB=1 \
	-DSQLITE_ENABLE_FTS3_PARENTHESIS \
	-DSQLITE_SOUNDEX=1 \
	-DSQLITE_ENABLE_ICU \
	-DSQLITE_DEFAULT_CACHE_SIZE=500 \
	-DSQLITE_DEFAULT_TEMP_CACHE_SIZE=125 \
	-Wall \
	-fno-strict-aliasing"

export LDFLAGS="-lm `icu-config --ldflags-libsonly`"

%reconfigure \
    --disable-static \
    --disable-debug \
    --disable-tcl \
    --enable-json1 \
    --enable-fts3 \
    --enable-fts4 \
    --enable-fts5 \
    --enable-rtree \
    --enable-threadsafe \
    --enable-readline

%make_build

%install
%make_install

install -D -m0644 sqlite3.1 %{buildroot}/%{_mandir}/man1/sqlite3.1

%if %{with check}
%check
# XXX shell tests are broken due to loading system libsqlite3, work around...
export LD_LIBRARY_PATH=`pwd`/.libs
export MALLOC_CHECK_=3

# csv01 hangs on all non-intel archs i've tried
%ifarch x86_64 %{ix86}
%else
rm test/csv01.test
%endif

make test
%endif

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/sqlite3

%files libs
%defattr(-,root,root,-)
%license LICENSE.md
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%doc README.md
%{_mandir}/man1/%{name}3.*
