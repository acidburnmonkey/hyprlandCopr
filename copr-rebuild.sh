#!/bin/bash

# Wave 1 (roots, parallel):  hyprutils, hyprwayland-scanner, hyprland-protocols,
#                             hyprgraphics, hyprlang
# Wave 2 (parallel):         aquamarine, hyprcursor, hyprwire
# Wave 3:                    hyprland
#
set -euo pipefail

PROJECT="acidburnmonkey/hyprland"

ROOT="$(cd "$(dirname "$0")" && pwd)"
SPECS="$ROOT/specs"

# ── helpers ──────────────────────────────────────────────────────────────────

submit() {
    # submit <label> <spec-path>
    local label="$1" spec="$2" today
    today=$(date +%Y-%m-%d)
    if grep -q '^# Rebuilt:' "$spec"; then
        sed -i "s/^# Rebuilt:.*/# Rebuilt: $today/" "$spec"
    else
        sed -i "/^Release:/a # Rebuilt: $today" "$spec"
    fi
    git -C "$ROOT" add "$spec" >&2
    git -C "$ROOT" commit -m "chore: rebuild $label" >&2
    local out id
    out=$(copr-cli build "$PROJECT" "$spec" --nowait 2>&1)
    id=$(echo "$out" | grep -oP '(?<=Created builds: )\d+')
    if [[ -z "$id" ]]; then
        echo "[ERROR] Could not parse build ID for $label. copr-cli output:" >&2
        echo "$out" >&2
        exit 1
    fi
    echo "$id"
}

wait_all() {
    # wait_all <label:id> [<label:id> ...]
    # Watches all given builds; exits 1 if any fail.
    local failed=0
    for entry in "$@"; do
        local label="${entry%%:*}" id="${entry##*:}"
        echo "  Watching $label (build $id)..."
        if ! copr-cli watch-build "$id"; then
            echo "[FAIL] $label (build $id) failed." >&2
            failed=1
        else
            echo "  [OK] $label"
        fi
    done
    [[ $failed -eq 0 ]]
}

# ── Wave 1: roots ─────────────────────────────────────────────────────────────

echo "=== Wave 1: roots (submitting in parallel) ==="
id_utils=$(submit      hyprutils           "$SPECS/hyprutils.spec")
id_scanner=$(submit    hyprwayland-scanner "$SPECS/hyprwayland-scanner.spec")
id_protocols=$(submit  hyprland-protocols  "$SPECS/hyprland-protocols.spec")
id_graphics=$(submit   hyprgraphics        "$SPECS/hyprgraphics.spec")
id_lang=$(submit       hyprlang            "$SPECS/hyprlang.spec")

echo "  hyprutils=$id_utils  hyprwayland-scanner=$id_scanner  hyprland-protocols=$id_protocols  hyprgraphics=$id_graphics  hyprlang=$id_lang"

wait_all \
    "hyprutils:$id_utils" \
    "hyprwayland-scanner:$id_scanner" \
    "hyprland-protocols:$id_protocols" \
    "hyprgraphics:$id_graphics" \
    "hyprlang:$id_lang"

# ── Wave 2: aquamarine, hyprcursor, hyprwire ──────────────────────────────────

echo ""
echo "=== Wave 2: aquamarine / hyprcursor / hyprwire ==="
id_aquamarine=$(submit  aquamarine  "$SPECS/aquamarine.spec")
id_cursor=$(submit      hyprcursor  "$SPECS/hyprcursor.spec")
id_wire=$(submit        hyprwire    "$SPECS/hyprwire.spec")

echo "  aquamarine=$id_aquamarine  hyprcursor=$id_cursor  hyprwire=$id_wire"

wait_all \
    "aquamarine:$id_aquamarine" \
    "hyprcursor:$id_cursor" \
    "hyprwire:$id_wire"

# ── Wave 3: hyprland ──────────────────────────────────────────────────────────

echo ""
echo "=== Wave 3: hyprland ==="
id_hyprland=$(submit hyprland "$SPECS/hyprland.spec")
echo "  hyprland=$id_hyprland"

wait_all "hyprland:$id_hyprland"


# ── Wave 4a: brood roots (hyprtoolkit must rebuild before hyprpaper/guiutils) ──
# hyprpaper and hyprland-guiutils depend on hyprtoolkit-devel; after a hyprutils
# soname bump the stale hyprtoolkit in the repo breaks their dep resolution.
# hyprpicker only needs hyprutils+hyprwayland-scanner so it runs here too.

echo ""
echo "=== Wave 4a: brood roots ==="
id_toolkit=$(submit    hyprtoolkit                "$ROOT/brood/hyprtoolkit.spec")
id_polkit=$(submit     hyprpolkitagent            "$ROOT/brood/hyprpolkitagent.spec")
id_xdgportal=$(submit  xdg-desktop-portal-hyprland "$ROOT/brood/xdg-desktop-portal-hyprland.spec")
id_idle=$(submit       hypridle                   "$ROOT/brood/hypridle.spec")
id_lock=$(submit       hyprlock                   "$ROOT/brood/hyprlock.spec")
id_picker=$(submit     hyprpicker                 "$ROOT/brood/hyprpicker.spec")

echo "  hyprtoolkit=$id_toolkit  hyprpolkitagent=$id_polkit  xdg-desktop-portal-hyprland=$id_xdgportal  hypridle=$id_idle  hyprlock=$id_lock  hyprpicker=$id_picker"

wait_all \
    "hyprtoolkit:$id_toolkit" \
    "hyprpolkitagent:$id_polkit" \
    "xdg-desktop-portal-hyprland:$id_xdgportal" \
    "hypridle:$id_idle" \
    "hyprlock:$id_lock" \
    "hyprpicker:$id_picker"

# ── Wave 4b: hyprtoolkit dependents ───────────────────────────────────────────

echo ""
echo "=== Wave 4b: hyprtoolkit dependents ==="
id_paper=$(submit      hyprpaper         "$ROOT/brood/hyprpaper.spec")
id_guiutils=$(submit   hyprland-guiutils "$ROOT/brood/hyprland-guiutils.spec")

echo "  hyprpaper=$id_paper  hyprland-guiutils=$id_guiutils"

wait_all \
    "hyprpaper:$id_paper" \
    "hyprland-guiutils:$id_guiutils"

echo ""
echo "=== All builds completed successfully ==="
