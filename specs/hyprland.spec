-%global hyprland_commit ff50dc36e912b6ad764802d51be838bc7f6ed323
-%global hyprland_shortcommit %(c=%{hyprland_commit}; echo ${c:0:7})
-%global bumpver 58
-%global commits_count 6545
-%global commit_date Wed Oct 29 00:53:42 2025
-
-%global protocols_commit 3a5c2bda1c1a4e55cc1330c782547695a93f05b2
-%global protocols_shortcommit %(c=%{protocols_commit}; echo ${c:0:7})
-
-%global udis86_commit 5336633af70f3917760a6d441ff02d93477b0c86
-%global udis86_shortcommit %(c=%{udis86_commit}; echo ${c:0:7})
-
 %global libxkbcommon_version 1.11.0
 
-Name:           hyprland-git
-Version:        0.51.1%{?bumpver:^%{bumpver}.git%{hyprland_shortcommit}}
+Name:           hyprland
+Version:        0.51.1
 Release:        %autorelease
 Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks
 
@@
 URL:            https://github.com/hyprwm/Hyprland
-%if 0%{?bumpver}
-Source0:        %{url}/archive/%{hyprland_commit}/%{name}-%{hyprland_shortcommit}.tar.gz
-Source2:        https://github.com/hyprwm/hyprland-protocols/.../%{protocols_commit}/protocols-%{protocols_shortcommit}.tar.gz
-Source3:        https://github.com/canihavesomecoffee/udis86/archive/%{udis86_commit}/udis86-%{udis86_shortcommit}.tar.gz
-%else
 Source0:        %{url}/releases/download/v%{version}/source-v%{version}.tar.gz
-%endif
 Source4:        macros.hyprland
 Source5:        https://github.com/xkbcommon/libxkbcommon/.../%{libxkbcommon_version}/libxkbcommon-%{libxkbcommon_version}.tar.gz
 
@@
 %prep
-%autosetup -n %{?bumpver:Hyprland-%{hyprland_commit}} %{!?bumpver:hyprland-source} -N
+%autosetup -n hyprland-source -N
@@
-%if 0%{?bumpver}
-tar -xf %{SOURCE2} -C subprojects/hyprland-protocols --strip=1
-tar -xf %{SOURCE3} -C subprojects/udis86 --strip=1
-sed -e '/GIT_COMMIT_HASH/s/unknown/%{hyprland_commit}/' \
-    -e '/GIT_BRANCH/s/unknown/main/' \
-    -e '/GIT_COMMIT_DATE/s/unknown/%{commit_date}/' \
-    -e '/GIT_TAG/s/unknown/%{lua:print((macros.version:gsub('[%^~].*', '')))}/' \
-    -e '/GIT_DIRTY/s/unknown/clean/' \
-    -e '/GIT_COMMITS/s/0/%{commits_count}/' \
-    -i CMakeLists.txt
-%endif