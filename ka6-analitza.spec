#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		analitza
Summary:	Analitza
Name:		ka6-%{kaname}
Version:	25.08.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	aeb7adb1331fef07a0011b29bb8607bf
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Network-devel >= 5.11.1
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Qml-devel
BuildRequires:	Qt6Quick-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	Qt6Xml-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The analitza library will let you add mathematical features to your
program.

%description -l pl.UTF-8
Biblioteka analitza pozwoli Ci dodać matematyczne właściwości do
Twoich programów.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build install

%find_lang %{kaname} --all-name --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libAnalitza.so.9
%attr(755,root,root) %{_libdir}/libAnalitza.so.*.*
%ghost %{_libdir}/libAnalitzaGui.so.9
%attr(755,root,root) %{_libdir}/libAnalitzaGui.so.*.*
%ghost %{_libdir}/libAnalitzaPlot.so.9
%attr(755,root,root) %{_libdir}/libAnalitzaPlot.so.*.*
%ghost %{_libdir}/libAnalitzaWidgets.so.9
%attr(755,root,root) %{_libdir}/libAnalitzaWidgets.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/analitza
%{_libdir}/qt6/qml/org/kde/analitza/Graph2D.qml
%{_libdir}/qt6/qml/org/kde/analitza/Graph3D.qml
%{_libdir}/qt6/qml/org/kde/analitza/analitzadeclarativeplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/analitza/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/analitza/libanalitzadeclarativeplugin.so
%{_libdir}/qt6/qml/org/kde/analitza/qmldir
%{_datadir}/libanalitza

%files devel
%defattr(644,root,root,755)
%{_includedir}/Analitza6
%{_libdir}/cmake/Analitza6
%{_libdir}/libAnalitza.so
%{_libdir}/libAnalitzaGui.so
%{_libdir}/libAnalitzaPlot.so
%{_libdir}/libAnalitzaWidgets.so
