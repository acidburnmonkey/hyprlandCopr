Name:           hyprwire
Version:        0.2.1
Release:        1%{?dist}
Summary:        Hyprland wire/IPC helper library

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwire
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  pugixml-devel
BuildRequires:  pkgconfig(hyprutils) >= 0.9.0
BuildRequires:  pkgconfig(libffi)

%description
Hyprwire is a helper library used by Hyprland ecosystem components.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       /usr/bin/pkg-config

%description devel
Headers, pkg-config metadata, CMake config files, and the upstream hyprwire-scanner tool.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -G Ninja -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE*
%doc README*
%{_libdir}/libhyprwire.so.*

%files devel
%{_includedir}/hyprwire*
%{_libdir}/libhyprwire.so
%{_libdir}/pkgconfig/hyprwire.pc

# upstream "scanner" tool + its dev metadata, bundled into -devel
%{_bindir}/hyprwire-scanner
%{_libdir}/pkgconfig/hyprwire-scanner.pc
%{_libdir}/cmake/hyprwire-scanner/

%changelog
%autochangelog
