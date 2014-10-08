Summary:	VISL CG-3 constraint grammar system
Summary(pl.UTF-8):	VISL CG-3 - system ograniczonej gramatyki
Name:		vislcg3
Version:	0.9.8.9708
Release:	2
License:	GPL v3+
Group:		Applications/Text
Source0:	http://beta.visl.sdu.dk/download/vislcg3/%{name}-%{version}.tar.gz
# Source0-md5:	573ffaa88a6850930cbeb7341d66df2e
URL:		http://beta.visl.sdu.dk/cg3.html
BuildRequires:	cmake >= 2.8.0
BuildRequires:	boost-devel >= 1.40.0
BuildRequires:	libicu-devel >= 4.2
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.603
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VISL CG-3 constraint grammar system.

%description -l pl.UTF-8
VISL CG-3 - system ograniczonej gramatyki.

%package devel
Summary:	Header file for VISL CG-3 library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki VISL CG-3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for VISL CG-3 library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki VISL CG-3.

%package static
Summary:	Static VISL CG-3 library
Summary(pl.UTF-8):	Statyczna biblioteka VISL CG-3
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static VISL CG-3 library.

%description static -l pl.UTF-8
Statyczna biblioteka VISL CG-3.

%prep
%setup -q

%{__sed} -i -e 's#DESTINATION lib/pkgconfig#DESTINATION %{_lib}/pkgconfig#g' CMakeLists.txt
%{__sed} -i -e 's#DESTINATION lib#DESTINATION %{_lib}#g' src/CMakeLists.txt

%build
# it expectls only relative CMAKE_INSTALL_LIBDIR
%cmake . \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DOPT_TCMALLOC=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# "improved" cmake scripts don't install it
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install src/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/cg-comp
%attr(755,root,root) %{_bindir}/cg-conv
%attr(755,root,root) %{_bindir}/cg-proc
%attr(755,root,root) %{_bindir}/cg3-autobin.pl
%attr(755,root,root) %{_bindir}/vislcg3
%attr(755,root,root) %{_libdir}/libcg3.so
%{_mandir}/man1/cg-comp.1*
%{_mandir}/man1/cg-proc.1*
%{_mandir}/man1/vislcg3.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/cg3.h
%{_pkgconfigdir}/cg3.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcg3.a
