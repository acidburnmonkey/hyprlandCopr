Name:           hyprland-guiutils
Version:        0.2.0
Release:        1%{?dist}
Summary:        Hyprland GUI utilities (successor to hyprland-qtutils)

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-guiutils
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  git
BuildRequires:  hyprwayland-scanner-devel

# From upstream CMake pkg_check_modules(...)
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprutils) >= 0.10.2
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(cairo)

Obsoletes:      hyprland-qtutils < 0.2.0

%description
Hyprland GUI utilities: a set of small helper applications (dialogs, update/donate
screens, welcome app, and run helper) used by Hyprland. It replaces hyprland-qtutils.
%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_bindir}/hyprland-dialog
%{_bindir}/hyprland-donate-screen
%{_bindir}/hyprland-run
%{_bindir}/hyprland-update-screen
%{_bindir}/hyprland-welcome

%changelog
%autochangelog
