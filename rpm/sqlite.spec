Name:       sqlite
Summary:    Library that implements an embeddable SQL database engine
Version:    3.13.0
Release:    1
Group:      Applications/Databases
License:    Public Domain
URL:        http://www.sqlite.org/download.html
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(icu-i18n)
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
Group:      Development/Libraries
Requires:   %{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
Man page for %{name}.

%package libs
Summary:    SQlite shared library
Group:      Applications/Databases
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Obsoletes:  %{name} < 3.13.0+git1
%description libs
This package contains the shared library for %{name}.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
export CFLAGS="$RPM_OPT_FLAGS \
	-DSQLITE_ENABLE_COLUMN_METADATA=1 \
	-DSQLITE_DISABLE_DIRSYNC=1 \
	-DYYSTACKDEPTH=500 \
	-DSQLITE_SECURE_DELETE=1 \
	-DSQLITE_ENABLE_FTS4 \
	-DSQLITE_ENABLE_FTS5 \
	-DSQLITE_ENABLE_FTS3_PARENTHESIS \
	-DSQLITE_ENABLE_JSON1 \
	-DSQLITE_ENABLE_RTREE \
	-DSQLITE_SOUNDEX=1 \
	-DNDEBUG \
	-D_XOPEN_SOURCE=500 \
	-DSQLITE_ENABLE_DBSTAT_VTAB=1 \
	-DUSE_PREAD \
	-DSQLITE_ENABLE_UNLOCK_NOTIFY=1 \
	-DSQLITE_ENABLE_ICU \
	-DSQLITE_DEFAULT_CACHE_SIZE=500 \
	-DSQLITE_DEFAULT_TEMP_CACHE_SIZE=125 \
	-Wall \
	-fno-strict-aliasing"
	
export LDFLAGS="-lm `icu-config --ldflags-libsonly`"

%reconfigure --disable-static \
    --without-tcl \
    --disable-tcl \
    --enable-threadsafe \
    --enable-threads-override-locks \
    --enable-readline

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/%{name}3.*

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*
