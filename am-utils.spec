Summary:	Automount utilities including an updated version of Amd
Summary(pl):	Narzêdzia do automatycznego montowania systemów plików
Name:		am-utils
Version:	6.0.7
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
URL:		http://www.am-utils.org/
BuildRequires:	autoconf
Prereq:		/sbin/chkconfig
Requires:	portmap
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

%description -l pl
Pakiet am-utils zawiera uaktualnion± wersjê amd, popularnego
automountera z BSD. Automounter to program zarz±dzaj±cy montowaniem
systemów plików. Systemy plików s± montowane przy pierwszym u¿yciu
przez u¿ytkownika, a odmontowywane po pewnym czasie nieu¿ywania. amd
obs³uguje wiele systemów plików, w tym NFS, UFS, CD-ROM oraz lokalne
urz±dzenia.

%prep
%setup -q
%patch0 -p1
%ifnarch i386
%patch1 -p1
%endif

%build
CFLAGS="%{rpmcflags}" 
%configure2_13 \
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

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/amd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/amd.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/amd

install -d $RPM_BUILD_ROOT/.automount

gzip -9nf AUTHORS BUGS NEWS README* ChangeLog ldap-id.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add amd
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/ldconfig
if [ "$1" = "0" ]; then
    /sbin/chkconfig --del amd
fi

%files
%defattr(644,root,root,755)
%doc doc/*.ps *.gz
%dir /.automount
%config %{_sysconfdir}/amd.conf
%config /etc/sysconfig/amd
%attr(754,root,root) /etc/rc.d/init.d/amd
%attr(755,root,root) %{_bindir}/pawd
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man[158]/*
%{_infodir}/*
