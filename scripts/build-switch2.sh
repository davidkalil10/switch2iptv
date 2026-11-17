#!/usr/bin/env bash
set -euo pipefail

export DEVKITPRO="${DEVKITPRO:-/opt/devkitpro}"
export DEVKITA64="${DEVKITA64:-$DEVKITPRO/devkitA64}"
export PATH="$DEVKITPRO/tools/bin:$DEVKITA64/bin:$DEVKITPRO/portlibs/switch2/bin:$DEVKITPRO/portlibs/switch/bin:$PATH"
export PKG_CONFIG_PATH="$DEVKITPRO/portlibs/switch2/lib/pkgconfig:$DEVKITPRO/portlibs/switch/lib/pkgconfig"

cd "$(dirname "$0")/.."
ROOT_DIR="$(pwd)"

if [[ ! -f "$DEVKITPRO/libounce/cmake/Switch2.cmake" ]]; then
  echo "ERROR: Switch2.cmake not found at $DEVKITPRO/libounce/cmake/Switch2.cmake" >&2
  exit 1
fi

apply_patch_if_needed() {
  local patch_file="$1"
  if git -C "$ROOT_DIR/library/borealis" apply --reverse --check "$patch_file" >/dev/null 2>&1; then
    echo "Patch already applied: $(basename "$patch_file")"
  else
    git -C "$ROOT_DIR/library/borealis" apply "$patch_file"
    echo "Applied patch: $(basename "$patch_file")"
  fi
}

echo "==> Applying Borealis patches..."
apply_patch_if_needed "$ROOT_DIR/patches/borealis-iptv.patch"
apply_patch_if_needed "$ROOT_DIR/patches/borealis-switch2.patch"

BUILD_DIR="$ROOT_DIR/build/switch2"
JOBS="${SWITCH2IPTV_BUILD_JOBS:-$(nproc)}"

echo "==> Configuring IptvPlayerSwitch for Nintendo Switch 2..."
cmake -B "$BUILD_DIR" -G Ninja \
  -DCMAKE_TOOLCHAIN_FILE="$DEVKITPRO/libounce/cmake/Switch2.cmake" \
  -DCMAKE_BUILD_TYPE=Release \
  -DPLATFORM_SWITCH=ON \
  -DNINTENDO_SWITCH2=ON

echo "==> Building IptvPlayerSwitch-switch2.nro..."
cmake --build "$BUILD_DIR" --target IptvPlayerSwitch.nro -j"$JOBS"

python3 "$ROOT_DIR/tools/verify_switch2_package.py" \
  "$BUILD_DIR/IptvPlayerSwitch-switch2.nro" \
  --link-map "$BUILD_DIR/IptvPlayerSwitch-switch2.map"

printf '\nBuilt: %s\n' "$BUILD_DIR/IptvPlayerSwitch-switch2.nro"
