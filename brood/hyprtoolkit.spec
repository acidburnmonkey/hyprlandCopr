Name:           hyprtoolkit
Version:        0.5.10.5.0
Release:        %autorelease
Summary:        Modern C++ Wayland-native GUI toolkit

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprtoolkit
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  pkgconfig

# Needed by upstream to generate / use Wayland protocols
BuildRequires:  cmake(hyprwayland-scanner)

# Core Wayland / graphics stack
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(pixman-1)

# Text / rendering
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)

# Config parser
BuildRequires:  pkgconfig(iniparser)

BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  mesa-libGLES-devel

%description
Hyprtoolkit is a small, modern C++ Wayland-native GUI toolkit used by parts of the
Hyprland ecosystem.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hyprwayland-scanner
Requires:       hyprutils-devel%{?_isa}
Requires:       hyprlang-devel%{?_isa}
Requires:       hyprgraphics-devel%{?_isa}
Requires:       aquamarine-devel%{?_isa}

%description devel
Headers and development files for building software against %{name}.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprtoolkit.so.*

%files devel
%{_includedir}/hyprtoolkit/
%{_libdir}/libhyprtoolkit.so
%{_libdir}/pkgconfig/hyprtoolkit.pc

%changelog
%autochangelog
