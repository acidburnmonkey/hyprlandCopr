Name:           hyprland-protocols
Version:        0.7.0
Release:        %autorelease
Summary:        Wayland protocol files for Hyprland
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-protocols
Source0:        https://github.com/hyprwm/hyprland-protocols/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config

%description
Protocol XML files used by Hyprland and related projects.

%prep
%autosetup -n %{name}-%{version}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_datadir}/hyprland-protocols/protocols/*.xml
%{_datadir}/pkgconfig/hyprland-protocols.pc

%changelog
%autochangelog
