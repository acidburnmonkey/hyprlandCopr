Name:           glaze
Version:        6.2.0
Release:        %autorelease
Summary:        Extremely fast, in-memory JSON and interface library

License:        MIT
URL:            https://github.com/stephenberry/glaze
Source0:        https://github.com/stephenberry/glaze/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
glaze is a fast, in-memory JSON and interface library. This package provides headers
and build metadata for consumers.

%package devel
Summary:        Development files for glaze
Requires:       %{name} = %{version}-%{release}

%description devel
Headers and build metadata (pkg-config + CMake package config) for glaze.

%prep
%autosetup -n glaze-%{version}

%build
# header-only packaging: no build

%install
# Headers
install -d %{buildroot}%{_includedir}
if [ -d include/glaze ]; then
  cp -a include/glaze %{buildroot}%{_includedir}/
else
  # fallback (some tags may use "glaze/" directly)
  cp -a glaze %{buildroot}%{_includedir}/
fi

# pkg-config file (Hyprland can use pkg_check_modules)
install -d %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/glaze.pc << 'EOF'
prefix=/usr
includedir=${prefix}/include

Name: glaze
Description: header-only JSON/interface library
Version: %{version}
Cflags: -I${includedir}
EOF

# CMake package config (Hyprland can use find_package(glaze CONFIG))
install -d %{buildroot}%{_libdir}/cmake/glaze
cat > %{buildroot}%{_libdir}/cmake/glaze/glazeConfig.cmake << 'EOF'
# Minimal config for consumers: provides glaze::glaze as an INTERFACE target
if(NOT TARGET glaze::glaze)
  add_library(glaze::glaze INTERFACE IMPORTED)
  # glazeConfig.cmake lives at /usr/lib64/cmake/glaze -> ../../../include == /usr/include
  get_filename_component(_glaze_prefix "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)
  set_target_properties(glaze::glaze PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${_glaze_prefix}/include"
  )
endif()
EOF

%files
%license LICENSE*
%doc README*

%files devel
%{_includedir}/glaze
%{_libdir}/pkgconfig/glaze.pc
%{_libdir}/cmake/glaze/glazeConfig.cmake

%changelog
%autochangelog
