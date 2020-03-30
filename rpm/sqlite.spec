Name:       sqlite
Summary:    Library that implements an embeddable SQL database engine
Version:    3.30.0
Release:    1
License:    Public Domain
URL:        http://www.sqlite.org/download.html
Source0:    %{name}-%{version}.tar.gz
Patch0:     sqlite-3.12.2-no-malloc-usable-size.patch
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(zlib)
# See bug 15004 Add ICU support to sqlite.
BuildRequires:  pkgconfig(icu-i18n)
# Need to have tcl since sqlite generates files like sqlite3.h and
# shell.c with the tclsh script.
BuildRequires:  tcl
Requires:   %{name}-libs = %{version}-%{release}

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1

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
Requires:  %{name} = %{version}-%{release}

%description doc
Man page for %{name}.

%package libs
Summary:    SQlite shared library
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
# We need to ensure rpm is updated before sqlite-libs as this can break
# the rpm during installation. Newer rpm's do not depend on this anymore.
Conflicts:  rpm < 4.14.1+git8
Requires(pre): rpm >= 4.14.1+git8
Obsoletes:  %{name} < 3.13.0+git1

%description libs
This package contains the shared library for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
export CFLAGS="$RPM_OPT_FLAGS \
	-DSQLITE_ENABLE_COLUMN_METADATA=1 \
	-DSQLITE_DISABLE_DIRSYNC=1 \
	-DYYSTACKDEPTH=500 \
	-DSQLITE_SECURE_DELETE=1 \
	-DSQLITE_ENABLE_FTS3_PARENTHESIS \
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

%configure  --disable-tcl \
	    --disable-static \
	    --enable-json1 \
	    --enable-fts3 \
	    --enable-fts4 \
	    --enable-fts5 \
	    --enable-rtree \
	    --enable-threadsafe \
	    --enable-readline

# rpath removal fix
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

# Disable test for now since, tests are using tcl. 
#make test || echo Tests failed

%install
rm -rf %{buildroot}
%make_install

install -D -m0644 ../sqlite/sqlite3.1 $RPM_BUILD_ROOT/%{_mandir}/man1/sqlite3.1

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
%exclude %{_libdir}/*.la

%files doc
%defattr(-,root,root,-)
%{_mandir}/man1/%{name}3.*

%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*
