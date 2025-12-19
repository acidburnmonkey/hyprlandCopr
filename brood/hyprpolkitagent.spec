Name:           hyprpolkitagent
Version:        0.1.3
Release:        %autorelease
Summary:        Simple polkit authentication agent for Hyprland (Qt/QML)

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpolkitagent
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Provides:       PolicyKit-authentication-agent

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig

BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtquickcontrols2-devel
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(polkit-qt6-1)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  systemd-rpm-macros

%description
hyprpolkitagent is a simple polkit authentication agent for Hyprland, written in Qt/QML.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBEXECDIR=%{_libexecdir}
%cmake_build

%install
%cmake_install

install -d %{buildroot}%{_datadir}/%{name}
[ -d qml ] && cp -a qml %{buildroot}%{_datadir}/%{name}/
[ -d assets ] && cp -a assets %{buildroot}%{_datadir}/%{name}/

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun %{name}.service

%files
%license LICENSE
%doc README.md
%{_libexecdir}/hyprpolkitagent
%{_userunitdir}/%{name}.service
%{_datadir}/dbus-1/services/org.hyprland.hyprpolkitagent.service
%{_datadir}/%{name}/

%changelog
%autochangelog
