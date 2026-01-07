Name:           hyprlang
Version:        0.6.8
Release:        %autorelease
Summary:        The official implementation library for the Hypr config language

License:        LGPL-3.0-only
URL:            https://github.com/hyprwm/hyprlang
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(hyprutils) >= 0.7.1

%description
hyprlang is the official implementation library for the Hypr configuration language.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files, pkg-config file, and linker symlink for developing against %{name}.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -G Ninja -DCMAKE_BUILD_TYPE=Release
%cmake_build --target hyprlang

%install
%cmake_install

if [ ! -e %{buildroot}%{_libdir}/libhyprlang.so ]; then
  ln -s libhyprlang.so.2 %{buildroot}%{_libdir}/libhyprlang.so
fi

%files
%license LICENSE
%doc README.md
%{_libdir}/libhyprlang.so.2*
%{_libdir}/libhyprlang.so.%{version}

%files devel
%{_includedir}/hyprlang.hpp
%{_libdir}/libhyprlang.so
%{_libdir}/pkgconfig/hyprlang.pc

%changelog
%autochangelog
