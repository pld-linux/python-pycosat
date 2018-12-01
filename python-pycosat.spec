#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		pycosat
%define		egg_name	pycosat
%define		pypi_name	pycosat
Summary:	Python bindings to picosat (a SAT solver)
Name:		python-%{pypi_name}
Version:	0.6.3
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://github.com/ContinuumIO/pycosat/archive/%{version}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	08e378db1c15dc1668bc62897bd325a5
URL:		https://github.com/ContinuumIO/pycosat
BuildRequires:	picosat-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-pytest
BuildRequires:	python3-setuptools
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PicoSAT is a popular SAT solver written by Armin Biere in pure C. This
package provides efficient Python bindings to picosat on the C level,
i.e. when importing pycosat, the picosat solver becomes part of the
Python process itself.

%package -n python3-%{pypi_name}
Summary:	Python bindings to picosat (a SAT solver)
Group:		Libraries/Python

%description -n python3-%{pypi_name}
PicoSAT is a popular SAT solver written by Armin Biere in pure C. This
package provides efficient Python bindings to picosat on the C level,
i.e. when importing pycosat, the picosat solver becomes part of the
Python process itself.

%prep
%setup -q -n %{pypi_name}-%{version}
sed -i -e s/distutils.core/setuptools/ setup.py
rm picosat.*

%build
%if %{with python2}
CFLAGS="%{rpmcflags}" %{__python} setup.py build_ext --inplace
%if %{with tests}
py.test-2 -vv
%endif
%endif

%if %{with python3}
CFLAGS="%{rpmcflags}" %{__python3} setup.py build_ext --inplace
%if %{with tests}
py.test-3 -vv
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%{__python} setup.py \
	install --skip-build \
	--prefix=%{_prefix} \
	--install-purelib=%{py_sitescriptdir} \
	--install-platlib=%{py_sitedir} \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_postclean

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/test_pycosat.py*
%endif

%if %{with python3}
%{__python3} setup.py \
	install --skip-build \
	--prefix=%{_prefix} \
	--install-purelib=%{py3_sitescriptdir} \
	--install-platlib=%{py3_sitedir} \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README.rst LICENSE
%attr(755,root,root) %{py_sitedir}/pycosat.so
%{py_sitedir}/%{egg_name}-%{version}-py*.egg-info

%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGELOG README.rst LICENSE
%attr(755,root,root) %{py3_sitedir}/%{module}.cpython-*.so
%{py3_sitedir}/%{egg_name}-%{version}-py*.egg-info
