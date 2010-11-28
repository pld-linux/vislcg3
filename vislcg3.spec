Summary:	VISL CG-3 constraint grammar system
Summary(pl.UTF-8):	VISL CG-3 - system ograniczonej gramatyki
Name:		vislcg3
Version:	0.9.7.6500
Release:	1
License:	GPL v3+
Group:		Applications/Text
Source0:	http://beta.visl.sdu.dk/download/vislcg3/%{name}-%{version}.tar.gz
# Source0-md5:	be274b0690f03f4d5692bb596033883d
Patch0:		%{name}-opt.patch
URL:		http://beta.visl.sdu.dk/cg3.html
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.36.0
BuildRequires:	libicu-devel >= 3.6
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VISL CG-3 constraint grammar system.

%description -l pl.UTF-8
VISL CG-3 - system ograniczonej gramatyki.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc APERTIUM_FORMAT AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/cg-comp
%attr(755,root,root) %{_bindir}/cg-conv
%attr(755,root,root) %{_bindir}/cg-proc
%attr(755,root,root) %{_bindir}/cg3-autobin.pl
%attr(755,root,root) %{_bindir}/vislcg3
%{_mandir}/man1/cg-comp.1*
%{_mandir}/man1/cg-proc.1*
%{_mandir}/man1/vislcg3.1*
