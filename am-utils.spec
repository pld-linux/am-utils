Summary: Automount utilities including an updated version of Amd.
Name: am-utils
Version: 6.0
Serial: 1
Release: 4
Copyright: BSD
Group: System Environment/Daemons
Source: ftp://shekel.mcl.cs.columbia.edu/pub/am-utils/am-utils-%{version}.tar.gz
Source1: am-utils.init
Source2: am-utils.conf
Source3: am-utils.sysconf
Patch0: am-utils-6.0a16-linux.patch
Patch1: am-utils-6.0a16-alpha.patch
Patch2: am-utils-6.0a16-glibc21.patch
Requires: portmap
BuildRoot: /var/tmp/am-utils-root
Prereq: /sbin/chkconfig
Prereq:         /usr/sbin/fix-info-dir
Obsoletes: amd

%description
Am-utils includes an updated version of Amd, the popular BSD
automounter.  An automounter is a program which maintains a cache of
mounted filesystems.  Filesystems are mounted when they are first
referenced by the user and unmounted after a certain period of inactivity.
Amd supports a variety of filesystems, including NFS, UFS, CD-ROMS and
local drives.  

You should install am-utils if you need a program for automatically
mounting and unmounting filesystems.

%prep
%setup -q
%patch2 -p1 -b .glibc21
%patch0 -p1 -b .lnx
%ifnarch i386
%patch1 -p1 -b .noauto
%endif

%build
cd aux ; autoconf ; mv -f configure .. ; cd ..
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr \
	--enable-shared --sysconfdir=/etc --enable-libs=-lnsl
# fun with autoconf
touch `find -name Makefile.in`
make

%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT/usr sysconfdir=`pwd`/etc
mkdir -p $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}
install -m 600 $RPM_SOURCE_DIR/am-utils.conf $RPM_BUILD_ROOT/etc/amd.conf
install -m 755 $RPM_SOURCE_DIR/am-utils.sysconf $RPM_BUILD_ROOT/etc/sysconfig/amd
install -m 755 $RPM_SOURCE_DIR/am-utils.init $RPM_BUILD_ROOT/etc/rc.d/init.d/amd
strip $RPM_BUILD_ROOT/usr/sbin/* $RPM_BUILD_ROOT/usr/bin/* || :
gzip -q9f $RPM_BUILD_ROOT/usr/info/*info*
mkdir -p $RPM_BUILD_ROOT/.automount
# get rid of some lame scripts
file $RPM_BUILD_ROOT/usr/sbin/* | \
	grep -v ELF | grep -v am-eject | \
	cut -f 1 -d':' | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add amd
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
/usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/ldconfig
if [ $1 = 0 ]; then
    /sbin/chkconfig --del amd
fi

%files
%defattr(-,root,root)
%doc doc/*.ps AUTHORS BUGS ChangeLog NEWS README* TODO
%dir /.automount
/usr/bin/pawd
/usr/sbin/*
/usr/man/man[58]/*
/usr/man/man1/pawd.1
%config /etc/amd.conf
%config /etc/sysconfig/amd
%config /etc/rc.d/init.d/amd
/usr/info/*info*.gz
/usr/lib/libamu.so
/usr/lib/libamu.so.*
