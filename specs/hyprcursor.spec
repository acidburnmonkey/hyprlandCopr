Name:           hyprcursor
Version:        0.1.13
Release:        %autorelease
Summary:        Cursor library for the Hyprland ecosystem

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprcursor
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz


BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(hyprlang) >= 0.4.2
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(tomlplusplus)

%description
Hyprcursor provides a cursor-related library used by Hyprland components and
other Hyprland ecosystem applications.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and other development files for %{name}.

%prep
%autosetup -p1

%build
%cmake -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

install -Dpm0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

LC_ALL=C find %{buildroot} \( -type f -o -type l \) -print \
  | sed "s|^%{buildroot}||" \
  | sort -u > %{_builddir}/allfiles.list

# devel.files: headers + cmake/pkgconfig metadata + unversioned .so symlink + static libs (if any)
: > %{_builddir}/devel.files
grep -E "^%{_includedir}/" %{_builddir}/allfiles.list >> %{_builddir}/devel.files || :
grep -E "^%{_libdir}/pkgconfig/" %{_builddir}/allfiles.list >> %{_builddir}/devel.files || :
grep -E "^%{_libdir}/cmake/" %{_builddir}/allfiles.list >> %{_builddir}/devel.files || :
grep -E "^%{_libdir}/.*\\.so$" %{_builddir}/allfiles.list >> %{_builddir}/devel.files || :
grep -E "^%{_libdir}/.*\\.a$" %{_builddir}/allfiles.list >> %{_builddir}/devel.files || :
sort -u -o %{_builddir}/devel.files %{_builddir}/devel.files

comm -23 %{_builddir}/allfiles.list %{_builddir}/devel.files > %{_builddir}/runtime.files
grep -v -x "%{_datadir}/licenses/%{name}/LICENSE" %{_builddir}/runtime.files > %{_builddir}/runtime.files.tmp
mv %{_builddir}/runtime.files.tmp %{_builddir}/runtime.files

%files -f %{_builddir}/runtime.files
%license %{_datadir}/licenses/%{name}/LICENSE

%files devel -f %{_builddir}/devel.files

%changelog
* Mon Dec 15 2025 mal0 <mal0@localhost> - 0.1.13-1
- Initial package
