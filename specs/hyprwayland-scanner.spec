Name:           hyprwayland-scanner
Version:        0.4.5
Release:        2%{?dist}
Summary:        A Hyprland implementation of wayland-scanner, in and for C++

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwayland-scanner
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(pugixml)
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
CMake config and pkg-config files for %{name}.

%prep
%autosetup -p1

%build
%cmake -G Ninja
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
%autochangelog

