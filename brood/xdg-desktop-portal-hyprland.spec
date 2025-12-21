Name:           xdg-desktop-portal-hyprland
Version:        1.3.11
Release:        %autorelease
Summary:        XDG Desktop Portal backend for Hyprland

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/xdg-desktop-portal-hyprland
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  hyprlang-devel
BuildRequires:  hyprutils-devel
BuildRequires:  hyprwayland-scanner-devel
BuildRequires:  pkgconfig(hyprland-protocols)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  systemd-rpm-macros

Requires:       xdg-desktop-portal
Requires:       qt6-qtwayland

%description
XDG Desktop Portal backend for Hyprland (including the Hyprland share picker).

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBEXECDIR=%{_prefix}/lib
%cmake_build

%install
%cmake_install

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun %{name}.service

%files
%license LICENSE
%doc README.md

%{_bindir}/hyprland-share-picker
/usr/lib/xdg-desktop-portal-hyprland

%{_datadir}/xdg-desktop-portal/portals/hyprland.portal
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.hyprland.service
%{_userunitdir}/%{name}.service


%changelog
%autochangelog
