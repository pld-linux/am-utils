Summary:	Automount utilities including an updated version of Amd
Summary(pl):	Narzêdzia do automatycznego montowania systemów plików
Name:		am-utils
Version:	6.0.3
Release:	1
License:	BSD
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	ftp://shekel.mcl.cs.columbia.edu/pub/am-utils/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.sysconf
Patch0:		%{name}-6.0a16-linux.patch
Patch1:		%{name}-6.0a16-alpha.patch
Patch2:		%{name}-6.0a16-glibc21.patch
Requires:	portmap
Prereq:		/sbin/chkconfig
Obsoletes:	amd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Am-utils includes an updated version of Amd, the popular BSD
automounter. An automounter is a program which maintains a cache of
mounted filesystems. Filesystems are mounted when they are first
referenced by the user and unmounted after a certain period of
inactivity. Amd supports a variety of filesystems, including NFS, UFS,
CD-ROMS and local drives.

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
CFLAGS="%{rpmcflags}" ./configure \
	--prefix=%{_prefix} \
	--enable-shared \
	--sysconfdir=%{_sysconfdir} \
	--enable-libs=-lnsl
	
# fun with autoconf
touch `find -name Makefile.in`
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

%{__make} install prefix=$RPM_BUILD_ROOT%{_prefix} sysconfdir=`pwd`%{_sysconfdir}
install $RPM_SOURCE_DIR/am-utils.conf $RPM_BUILD_ROOT%{_sysconfdir}/amd.conf
install $RPM_SOURCE_DIR/am-utils.sysconf $RPM_BUILD_ROOT/etc/sysconfig/amd
install $RPM_SOURCE_DIR/am-utils.init $RPM_BUILD_ROOT/etc/rc.d/init.d/amd

gzip -9nf AUTHORS TODO BUGS NEWS README* ChangeLog

install -d $RPM_BUILD_ROOT/.automount

# get rid of some lame scripts
file $RPM_BUILD_ROOT%{_sbindir}/* | \
	grep -v ELF | grep -v am-eject | \
	cut -f 1 -d':' | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
NAME=amd; %chkconfig_add
%fix_info_dir

%preun
NAME=amd; %chkconfig_del

%postun
%fix_info_dir
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*.ps {AUTHORS,BUGS,ChangeLog,NEWS,README*,TODO}.gz
%dir /.automount
%config %{_sysconfdir}/amd.conf
%config /etc/sysconfig/amd
%attr(754,root,root) /etc/rc.d/init.d/amd
%attr(755,root,root) %{_bindir}/pawd
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man[158]/*
%{_infodir}/*
