Summary:	VISL CG-3 constraint grammar system
Summary(pl.UTF-8):	VISL CG-3 - system ograniczonej gramatyki
Name:		vislcg3
Version:	0.9.7.7823
Release:	1
License:	GPL v3+
Group:		Applications/Text
Source0:	http://beta.visl.sdu.dk/download/vislcg3/%{name}-%{version}.tar.gz
# Source0-md5:	a74e87f4b19dc39172674b37ce27aa5a
URL:		http://beta.visl.sdu.dk/cg3.html
BuildRequires:	cmake >= 2.6.4
BuildRequires:	boost-devel >= 1.36.0
BuildRequires:	libicu-devel >= 3.6
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.603
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VISL CG-3 constraint grammar system.

%description -l pl.UTF-8
VISL CG-3 - system ograniczonej gramatyki.

%prep
%setup -q

sed -i -e 's#DESTINATION lib#DESTINATION %{_lib}#g' \
	-e 's#GOOGLE_TCMALLOC_LIB tcmalloc#GOOGLE_TCMALLOC_LIB tcmalloc_disabled#' \
	src/CMakeLists.txt

%build
%cmake .

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# "improved" cmake scripts don't install it
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install src/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# API not installed
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcg3.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc APERTIUM_FORMAT AUTHORS README TODO
%attr(755,root,root) %{_bindir}/cg-comp
%attr(755,root,root) %{_bindir}/cg-conv
%attr(755,root,root) %{_bindir}/cg-proc
%attr(755,root,root) %{_bindir}/cg3-autobin.pl
%attr(755,root,root) %{_bindir}/vislcg3
%attr(755,root,root) %{_libdir}/libcg3.so
%{_mandir}/man1/cg-comp.1*
%{_mandir}/man1/cg-proc.1*
%{_mandir}/man1/vislcg3.1*
