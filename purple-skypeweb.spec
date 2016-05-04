%global plugin_name skypeweb

%global commit0 f23913d1287ab212aa2c3cd32eda64555a49281b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20160420

Name: purple-%{plugin_name}
Version: 1.1
Release: 4.%{date}git%{shortcommit0}%{?dist}
Summary: Adds support for Skype to Pidgin

License: GPLv3
URL: https://github.com/EionRobb/skype4pidgin
Source0: https://github.com/EionRobb/skype4pidgin/archive/%{commit0}.tar.gz#/skype4pidgin-%{shortcommit0}.tar.gz

%if 0%{?fedora}
Patch0: https://github.com/xvitaly/purple-skypeweb/raw/master/fix_build_under_patched_fedora.patch
%endif

BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(purple)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(zlib)
BuildRequires: gcc

%description
Adds support for Skype to Pidgin, Adium, Finch and other libpurple 
based messengers.

%package -n pidgin-%{plugin_name}
Summary: Adds pixmaps, icons and smileys for Skype protocol
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: pidgin

%description -n pidgin-%{plugin_name}
Adds pixmaps, icons and smileys for Skype protocol inplemented by libskypeweb.

%prep
%autosetup -n skype4pidgin-%{commit0} -p1
cd %{plugin_name}

# fix W: wrong-file-end-of-line-encoding
perl -i -pe 's/\r\n/\n/gs' README.md

# generating empty configure script
echo '#!/bin/bash' > configure
chmod +x configure

%build
cd %{plugin_name}
%configure
%make_build

%install
cd %{plugin_name}
%make_install
chmod 755 %{buildroot}%{_libdir}/purple-2/lib%{plugin_name}.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/purple-2/lib%{plugin_name}.so
%doc %{plugin_name}/README.md CHANGELOG.txt
%license COPYING.txt

%files -n pidgin-%{plugin_name}
%{_datadir}/pixmaps/pidgin/protocols/*/skype*.png
%{_datadir}/pixmaps/pidgin/emotes/skype/theme

%changelog
* Mon May 02 2016 V1TSK <vitaly@easycoding.org> - 1.1-4.20160420gitf23913d
- Updated to latest Git version.

* Fri Mar 04 2016 V1TSK <vitaly@easycoding.org> - 1.1-3.20160226git80368db
- Updated to latest Git version.

* Tue Feb 16 2016 V1TSK <vitaly@easycoding.org> - 1.1-2.20160214git04312d8
- Updated to latest Git version. Added EPEL7 support.

* Thu Jan 07 2016 V1TSK <vitaly@easycoding.org> - 1.1-1.20160107git9764e31
- Updated to version 1.1: added support of file transfers, fixed Live logins, fixed other crashes.

* Sat Jan 02 2016 V1TSK <vitaly@easycoding.org> - 1.0-4.20160101git68cb5f3
- Updated to latest version: added support for receiving server-backed files. Added patch.

* Fri Dec 25 2015 V1TSK <vitaly@easycoding.org> - 1.0-3.20151225gita173efa
- Updated to latest version: fixed plugin crash.

* Thu Nov 26 2015 V1TSK <vitaly@easycoding.org> - 1.0-2
- Applyed Maxim Orlov's fixes.

* Sun Nov 08 2015 V1TSK <vitaly@easycoding.org> - 1.0-1
- Updated to version 1.0.

* Mon Aug 24 2015 jparvela <jparvela@gmail.com> - 0.1-4
- Added missing files to spec file list.

* Mon Aug 03 2015 BOPOHA <vorona.tolik@gmail.com> - 0.1-3
- Fixed build with OBS. RPMS can be built from main tarball.

* Sat May 09 2015 V1TSK <vitaly@easycoding.org> - 0.1-2
- Separated packages. Now can be used with other libpurple-based clients without Pidgin being installed.

* Mon Mar 16 2015 V1TSK <vitaly@easycoding.org> - 0.1-1
- Created first RPM spec for Fedora/openSUSE.
