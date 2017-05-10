%define oname Uranium
%define lname %(echo %oname | tr [:upper:] [:lower:])

Summary:	A Python framework for building 3D printing related applications
Name:		%{oname}
Version:	2.5.0	
Release:	1
License:	AGPLv3+
Group:		Development/Python
URL:		https://github.com/Ultimaker/%{name}
Source0:	https://github.com/Ultimaker/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		%{oname}-2.5.0-CMakeLists.patch
Patch1:		%{oname}-2.5.0-plugins.patch
BuildArch:	noarch

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(python)
# tests
BuildRequires:	python-arcus = %{version}
BuildRequires:	python-numpy
BuildRequires:  python-pytest
BuildRequires:	python-qt5-core
BuildRequires:	python-qt5-gui
BuildRequires:	python-qt5-opengl
BuildRequires:	python-qt5-qml
BuildRequires:	python-qt5-widgets
BuildRequires:	python-qt5-qml
BuildRequires:	python-qt5-quick
BuildRequires:	python-qt5-quickwidgets
BuildRequires:	python-qt5-svg
BuildRequires:	python-scipy

Requires:	python
Requires:	python-arcus = %{version}
Requires:	python-numpy
#Requires:	python-qt5
Requires:	python-qt5-core
Requires:	python-qt5-gui
Requires:	python-qt5-opengl
Requires:	python-qt5-qml
Requires:	python-qt5-widgets
Requires:	python-qt5-qml
Requires:	python-qt5-quick
Requires:	python-qt5-quickwidgets
Requires:	python-qt5-svg
Requires:	python-scipy
Requires:	qt5-qtdeclarative
Requires:	qt5-qtquickcontrols

%description
Uranium is a Python framework for building 3D printing related applications.


#----------------------------------------------------------------------------

%package -n python-%{lname}
Summary:	A Python framework for building 3D printing related applications
Provides:	%{lname} = %{version}-%{release}
Provides:	%{oname} = %{version}-%{release}
Provides:	python-%{lname} = %{version}-%{release}

%description -n python-%{lname}
Uranium is a Python framework for building 3D printing related applications.

%files -n python-%{lname} -f %{name}.lang
%{_datadir}/%{lname}/
%{_datadir}/cmake/Modules/%{oname}*cmake
%{py_puresitedir}/UM/
#%{py_puresitedir}/%{lname}/
%doc docs/
%doc html/
%doc README.md
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q -n %{oname}-%{version}

# Apply all patches
%patch0 -p1 -b .orig
%patch1 -p1 #-b .plugins

# remove UpdateChecker plugin
rm -fr plugins/UpdateChecker

%build
%cmake \
	-DPYTHON_INSTALL_DIR=%{py_puresitedir} \
	%{nil}
%make

# documentation
%make doc

%install
%makeinstall_std -C build

# Fix locales files path
mv %{buildroot}%{_datadir}/%{lname}/resources/i18n %{buildroot}%{_datadir}/locale
ln -s ../../locale %{buildroot}%{_datadir}/%{lname}/resources/i18n

# Only .mo files are used
find %{buildroot}%{_datadir}/locale -name \*po -or -name \*pot -delete

# locales
%find_lang %{name} --all-name

%check
#%{__python3} -m pytest -v

