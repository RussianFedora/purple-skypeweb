%global plugin_name skypeweb

%global commit0 68cb5f35b70e8279b97cc0da91449fae78d32b20
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20160102

Name: purple-%{plugin_name}
Version: 1.0
Release: 4.%{date}git%{shortcommit0}%{?dist}
Summary: Adds support for Skype to Pidgin

License: GPLv3
URL: https://github.com/EionRobb/skype4pidgin
Source0: https://github.com/EionRobb/skype4pidgin/archive/%{commit0}.tar.gz#/skype4pidgin-%{shortcommit0}.tar.gz
Patch0: https://github.com/xvitaly/purple-skypeweb/raw/master/fix_build_under_patched_fedora.patch

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
%setup -qn skype4pidgin-%{commit0}
cd %{plugin_name}

# applying patches
%patch0 -p1

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
* Sat Jan 02 2016 V1TSK <vitaly@easycoding.org> - 1.0-4.20160102git68cb5f3
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
