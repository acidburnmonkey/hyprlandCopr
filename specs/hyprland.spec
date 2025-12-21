Name:           hyprland
Version:        0.52.2
Release:        %autorelease
Summary:        Dynamic tiling Wayland compositor
License:        BSD-3-Clause
URL:            https://github.com/hyprwm/Hyprland
Source0:        https://github.com/hyprwm/Hyprland/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  meson
BuildRequires:  pkgconf-pkg-config
BuildRequires:  patchelf

# COPR-built Hypr deps (system-installed)
BuildRequires:  hyprwayland-scanner-devel
BuildRequires:  hyprutils-devel
BuildRequires:  hyprlang-devel
BuildRequires:  hyprcursor-devel
BuildRequires:  hyprgraphics-devel
BuildRequires:  aquamarine-devel
BuildRequires:  hyprwire-devel
BuildRequires:  hyprland-protocols
BuildRequires:  glaze-devel

# System libs/tools (matches known-good Fedora 43 build set)
BuildRequires:  cairo-devel
BuildRequires:  glm-devel
BuildRequires:  glslang-devel
BuildRequires:  hwdata
BuildRequires:  libdisplay-info-devel
BuildRequires:  libdrm-devel
BuildRequires:  libepoxy-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libinput-devel
BuildRequires:  libjxl-devel
BuildRequires:  libliftoff-devel
BuildRequires:  libspng-devel
BuildRequires:  libwebp-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libxcvt-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pango-devel
BuildRequires:  pixman-devel
BuildRequires:  pugixml-devel
BuildRequires:  re2-devel
BuildRequires:  scdoc
BuildRequires:  libseat-devel
BuildRequires:  systemd-devel
BuildRequires:  tomlplusplus-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libzip-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  file-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-errors-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xorg-x11-server-Xwayland
BuildRequires:  libXfont2-devel
BuildRequires:  xkeyboard-config
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
BuildRequires:  uuid-c++-devel
BuildRequires:  uuid-devel
BuildRequires:  udis86-devel

# If linking against system udis86:
Requires:       xorg-x11-server-Xwayland%{?_isa}

%description
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice on its looks.

%package devel
Summary:        Header and protocol files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and pkg-config file for Hyprland.

%prep
%autosetup -n Hyprland-%{version}


%build
#udis err
# GCC 15 + generated protocol code can error on zero-length arrays
export CXXFLAGS="%{optflags} -Wno-zero-length-array"
export CFLAGS="%{optflags} -Wno-zero-length-array"

# Fedora udis86-devel ships headers/libs but NO udis86.pc.
# Hyprland checks pkg-config for "udis86>=1.7.2", so provide a local .pc:
cat > udis86.pc <<'EOF'
prefix=/usr
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: udis86
Description: udis86 disassembler library
Version: 1.7.2
Libs: -L${libdir} -ludis86
Cflags: -I${includedir}
EOF
export PKG_CONFIG_PATH="$PWD:${PKG_CONFIG_PATH:-}"

%cmake -GNinja \
  -DCMAKE_BUILD_TYPE=Release \
  -DNO_TESTS=TRUE \
  -DBUILD_TESTING=FALSE
%cmake_build

%install
%cmake_install

# provide legacy name if upstream installs lowercase
if [ -f %{buildroot}%{_bindir}/hyprland ] && [ ! -e %{buildroot}%{_bindir}/Hyprland ]; then
  ln -s hyprland %{buildroot}%{_bindir}/Hyprland
fi

# NOT want to package these:
rm -f %{buildroot}%{_bindir}/hyprtester
rm -f %{buildroot}%{_libdir}/hyprtestplugin.so
rm -f %{buildroot}/usr/lib/hyprtestplugin.so

%files
%license LICENSE
%doc README.md

%{_bindir}/hyprland
%{_bindir}/Hyprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm

%{_datadir}/hypr/
%{_datadir}/wayland-sessions/*.desktop
%{_datadir}/xdg-desktop-portal/*.conf

%{_mandir}/man1/Hyprland.1*
%{_mandir}/man1/hyprctl.1*

%{bash_completions_dir}/hypr*
%{fish_completions_dir}/hypr*.fish
%{zsh_completions_dir}/_hypr*

%files devel
%{_includedir}/hyprland/
%{_datadir}/pkgconfig/hyprland.pc

%changelog
%autochangelog
