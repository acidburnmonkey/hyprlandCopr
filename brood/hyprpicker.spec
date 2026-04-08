Name:           hyprpicker
Version:        0.4.6
Release:        %autorelease
Summary:        A wlroots-compatible Wayland color picker that does not suck

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprpicker
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(xkbcommon)

# Hypr ecosystem deps listed by upstream
BuildRequires:  pkgconfig(hyprutils) >= 0.2.0
BuildRequires:  pkgconfig(hyprwayland-scanner) >= 0.4.0

%description
A wlroots-compatible Wayland color picker that does not suck.
Supports hex, RGB, and other output formats.

%prep
%autosetup -p1
# GCC 16 no longer pulls in <mutex> transitively; add the missing include.
# https://github.com/hyprwm/hyprpicker/issues (upstream bug in 0.4.6)
sed -i '1a #include <mutex>' src/hyprpicker.hpp

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
