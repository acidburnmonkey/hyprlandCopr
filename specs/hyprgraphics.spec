Name:           hyprgraphics
Version:        0.5.0
Release:        %autorelease
Summary:        Hyprland graphics / resource utilities

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprgraphics
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig

BuildRequires:  cairo-devel
BuildRequires:  pixman-devel
BuildRequires:  hyprutils-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libwebp-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2-devel
BuildRequires:  file-devel
BuildRequires:  libjxl-devel

%description
Hyprgraphics is a small C++ library with graphics / resource related utilities used
across the hypr* ecosystem. :contentReference[oaicite:1]{index=1}

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config file, and CMake config files for developing against %{name}.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprgraphics.so.*

%files devel
%{_includedir}/hyprgraphics
%{_libdir}/libhyprgraphics.so
%{_libdir}/pkgconfig/hyprgraphics.pc

%changelog
%autochangelog