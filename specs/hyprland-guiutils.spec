Name:           hyprland-guiutils
Version:        0.2.0
Release:        %autorelease
Summary:        GUI utilities for the Hyprland compositor

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-guiutils
Source0:        https://github.com/hyprwm/hyprland-guiutils/releases/download/v%{version}/source-v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(hyprlang) >= 0.6.0
BuildRequires:  pkgconfig(hyprtoolkit) >= 0.4.0
BuildRequires:  pkgconfig(hyprutils) >= 0.10.2
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       hyprlang >= 0.6.0
Requires:       hyprtoolkit >= 0.4.0
Requires:       hyprutils >= 0.10.2

%description
Hyprland GUI helper programs used for onboarding, update dialogs, and other compositor-provided UX.

%prep
%setup -q -T -c %{name}-%{version}
tar -xaf %{SOURCE0} --strip-components=1

%build
%cmake -G Ninja -D CMAKE_BUILD_TYPE=RelWithDebInfo
%cmake_build

%install
%cmake_install
find %{buildroot} -type f -o -type l \
  | sed -e "s|^%{buildroot}||" \
  | sort -u > %{_builddir}/%{name}-%{version}-filelist.txt

%files -f %{_builddir}/%{name}-%{version}-filelist.txt
%license LICENSE*
%doc README*

%changelog
%autochangelog
