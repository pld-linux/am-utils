Summary:	Automount utilities including an updated version of Amd
Summary(es):	Utilitarios del automount - incluye el servidor automount NFS
Summary(pl):	Narzêdzia do automatycznego montowania systemów plików
Summary(pt_BR):	Utilitários do automount - inclui o servidor automount NFS
Name:		am-utils
Version:	6.0.7
Release:	3
Epoch:		5
License:	BSD
Group:		Daemons
Source0:	ftp://shekel.mcl.cs.columbia.edu/pub/am-utils/%{name}-%{version}.tar.gz
# Source0-md5:	76a95778c5ad1e41699e15f1d668e89e
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.sysconf
Patch0:		%{name}-6.0a16-linux.patch
Patch1:		%{name}-6.0a16-alpha.patch
URL:		http://www.am-utils.org/
BuildRequires:	autoconf
Prereq:		/sbin/chkconfig
Requires:	portmap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	amd

%description
Am-utils includes an updated version of Amd, the popular BSD
automounter. An automounter is a program which maintains a cache of
mounted filesystems. Filesystems are mounted when they are first
referenced by the user and unmounted after a certain period of
inactivity. Amd supports a variety of filesystems, including NFS, UFS,
CD-ROMS and local drives.

You should install am-utils if you need a program for automatically
mounting and unmounting filesystems.

%description -l es
Am-utils es la "próxima generación" del popular automounter BSD Amd.
Incluye muchas adiciones: actualizaciones, portes, programas,
características, correcciones de problemas, etc. AMD es el servidor
automount de Berkeley. Tiene la capacidad de automáticamente montar
sistemas de archivos de todos los tipos, incluyendo sistemas de
archivos NFS, CD-ROMs y accionadores locales y de desmontarlos cuando
no estén en uso. La configuración por defecto permite que se haga un
'cd /net/[máquina]' para obtener una lista de los directorios
exportados por aquella máquina

%description -l pl
Pakiet am-utils zawiera uaktualnion± wersjê amd, popularnego
automountera z BSD. Automounter to program zarz±dzaj±cy montowaniem
systemów plików. Systemy plików s± montowane przy pierwszym u¿yciu
przez u¿ytkownika, a odmontowywane po pewnym czasie nieu¿ywania. amd
obs³uguje wiele systemów plików, w tym NFS, UFS, CD-ROM oraz lokalne
urz±dzenia.

%description -l pt_BR
O am-utils é a "próxima geração" do popular automounter BSD amd.
Inclui muitas adições: atualizações, portes, programas,
características, correções de problemas, etc.

O AMD é o servidor automount de Berkeley. Tem a capacidade de
automaticamente montar sistemas de arquivos de todos os tipos,
incluindo sistemas de arquivos NFS, CD-ROMs e acionadores locais e de
desmontá-los quando não estiverem mais sendo usados.

A configuração default permite que seja feito um 'cd /net/[máquina]'
para obter uma lista dos diretórios exportados por aquela máquina

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
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d} \
	$RPM_BUILD_ROOT/.automount

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/amd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/amd.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/amd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/chkconfig --add amd
if [ -f /var/lock/subsys/drbd ]; then
	/etc/rc.d/init.d/amd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/amd start\" to start amd service." >&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/amd ]; then
		/etc/rc.d/init.d/amd stop
	fi
	/sbin/chkconfig --del amd
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*.ps AUTHORS BUGS NEWS README* ChangeLog ldap-id.txt
%dir /.automount
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/amd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/amd
%attr(754,root,root) /etc/rc.d/init.d/amd
%attr(755,root,root) %{_bindir}/pawd
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/*
%{_mandir}/man[158]/*
%{_infodir}/am-utils.info*
