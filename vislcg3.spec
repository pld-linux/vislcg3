#
# Conditional build:
%bcond_without	python		# Python(3) binding
%bcond_without	static_libs	# static library

Summary:	VISL CG-3 constraint grammar system
Summary(pl.UTF-8):	VISL CG-3 - system ograniczonej gramatyki
Name:		vislcg3
Version:	1.3.2
Release:	5
License:	GPL v3+
Group:		Applications/Text
#Source0Download: https://github.com/TinoDidriksen/cg3/releases
Source0:	https://github.com/TinoDidriksen/cg3/archive/v%{version}/cg3-%{version}.tar.gz
# Source0-md5:	495ed8b59968c071a44fc7e525d779a7
Patch0:		%{name}-static.patch
URL:		http://beta.visl.sdu.dk/cg3.html
BuildRequires:	cmake >= 3.0
BuildRequires:	boost-devel >= 1.63.0-4
BuildRequires:	libicu-devel >= 50.0
# -std=c++14
BuildRequires:	libstdc++-devel >= 6:5.0
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	swig-python >= 3.0
%endif
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

%package -n python3-constraint_grammar
Summary:	Python 3 bindings for CG-3 library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki CG-3
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.5

%description -n python3-constraint_grammar
Python 3 bindings for CG-3 library.

%description -n python3-constraint_grammar -l pl.UTF-8
Wiązania Pythona 3 do biblioteki CG-3.

%package -n emacs-cg-mode
Summary:	CG-3 mode for Emacs
Summary(pl.UTF-8):	Tryb CG-3 dla Emacsa
Group:		Applications/Editors/Emacs
Requires:	emacs-common
BuildArch:	noarch

%description -n emacs-cg-mode
CG-3 mode for Emacs.

%description -n emacs-cg-mode -l pl.UTF-8
Tryb CG-3 dla Emacsa.

%prep
%setup -q -n cg3-%{version}
%patch0 -p1

# not executable
%{__sed} -i -e '1s,.*/usr/bin/env perl,,' scripts/CG3_External.pm
# invoke directly
%{__sed} -i -e '1s,/usr/bin/env perl,%{__perl},' scripts/{cg-sort,cg-strictify,cg-untrace,cg3-autobin.pl.in}

%build
# it expectls only relative CMAKE_INSTALL_LIBDIR and CMAKE_INSTALL_INCLUDEDIR (see cg.pc)
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DUSE_TCMALLOC=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_python:-DENABLE_PYTHON_BINDINGS=ON} \
	-DPYTHON_INSTALL_PARAMS="--prefix=%{_prefix} --root=$RPM_BUILD_ROOT --optimize=2" \
	-DUSE_TCMALLOC=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static/src install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md TODO
%attr(755,root,root) %{_bindir}/cg-comp
%attr(755,root,root) %{_bindir}/cg-conv
%attr(755,root,root) %{_bindir}/cg-mwesplit
%attr(755,root,root) %{_bindir}/cg-proc
%attr(755,root,root) %{_bindir}/cg-relabel
%attr(755,root,root) %{_bindir}/cg-sort
%attr(755,root,root) %{_bindir}/cg-strictify
%attr(755,root,root) %{_bindir}/cg-untrace
%attr(755,root,root) %{_bindir}/cg3-autobin.pl
%attr(755,root,root) %{_bindir}/vislcg3
%attr(755,root,root) %{_libdir}/libcg3.so.1
%{_mandir}/man1/cg-comp.1*
%{_mandir}/man1/cg-conv.1*
%{_mandir}/man1/cg-proc.1*
%{_mandir}/man1/cg3-autobin.pl.1*
%{_mandir}/man1/vislcg3.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcg3.so
%{_includedir}/cg3.h
%{_pkgconfigdir}/cg3.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcg3.a
%endif

%if %{with python}
%files -n python3-constraint_grammar
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_constraint_grammar.cpython-*.so
%{py3_sitedir}/cg3.py
%{py3_sitedir}/constraint_grammar.py
%{py3_sitedir}/__pycache__/cg3.cpython-*.py[co]
%{py3_sitedir}/__pycache__/constraint_grammar.cpython-*.py[co]
%{py3_sitedir}/constraint_grammar-%{version}.*-py*.egg-info
%endif

%files -n emacs-cg-mode
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/cg.el
