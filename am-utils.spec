Summary:	Automount utilities including an updated version of Amd.
Name:		am-utils
Version:	6.0
Release:	5
Copyright:	BSD
Group:		Daemons
Group(pl):	Serwery
Source:		ftp://shekel.mcl.cs.columbia.edu/pub/am-utils/%{name}-%{version}.tar.gz
Source1:	am-utils.init
Source2:	am-utils.conf
Source3:	am-utils.sysconf
Patch0:		am-utils-6.0a16-linux.patch
Patch1:		am-utils-6.0a16-alpha.patch
Patch2:		am-utils-6.0a16-glibc21.patch
Requires:	portmap
Prereq:		/sbin/chkconfig
Prereq:	        /usr/sbin/fix-info-dir
Obsoletes:	amd
BuildRoot:	/tmp/%{name}-%{version}-root

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
CFLAGS="$RPM_OPT_FLAGS" ./configure \
	--prefix=%{_prefix} \
	--enable-shared \
	--sysconfdir=/etc \
	--enable-libs=-lnsl
	
# fun with autoconf
touch `find -name Makefile.in`
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

make install prefix=$RPM_BUILD_ROOT%{_prefix} sysconfdir=`pwd`/etc
install $RPM_SOURCE_DIR/am-utils.conf $RPM_BUILD_ROOT/etc/amd.conf
install $RPM_SOURCE_DIR/am-utils.sysconf $RPM_BUILD_ROOT/etc/sysconfig/amd
install $RPM_SOURCE_DIR/am-utils.init $RPM_BUILD_ROOT/etc/rc.d/init.d/amd

strip $RPM_BUILD_ROOT%{_sbindir}/* $RPM_BUILD_ROOT%{_bindir}/*

gzip -9nf AUTHORS TODO BUGS NEWS README* ChangeLog \
	$RPM_BUILD_ROOT%{_mandir}/*
	$RPM_BUILD_ROOT%{_infodir}/*

install -d $RPM_BUILD_ROOT/.automount

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
%defattr(644,root,root,755)
%doc doc/*.ps {AUTHORS,BUGS,ChangeLog,NEWS,README*,TODO}.gz
%dir /.automount
%config /etc/amd.conf
%config /etc/sysconfig/amd
%attr(754,root,root) /etc/rc.d/init.d/amd
%attr(755,root,root) %{_bindir}/pawd
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man[158]/*
%{_infodir}/*
