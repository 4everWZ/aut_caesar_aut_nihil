#!/usr/bin/env bash
set -euo pipefail
root=$(git rev-parse --show-toplevel)
destination=${1:?Specify a font build directory outside the checkout}
mkdir -p "$destination/inputs"
cd "$destination/inputs"
curl -fsSL --retry 2 -o cjk.deb 'https://deb.debian.org/debian/pool/main/f/fonts-noto-cjk/fonts-noto-cjk_20240730+repack1-1_all.deb'
curl -fsSL --retry 2 -o latin.deb 'https://deb.debian.org/debian/pool/main/f/fonts-noto/fonts-noto-core_20201225-2_all.deb'
printf '%s\n' \
  'f5dc28a754e17327d99f0a612134d92c8dd6187314ae967cb77f25df60860139  cjk.deb' \
  '97978d09b68445fcf85342b106cd2e812d7813e3d5626f9884a5f344c3a55973  latin.deb' | sha256sum --check
dpkg-deb -x cjk.deb extracted
dpkg-deb -x latin.deb extracted
printf '%s\n' \
  'b76b0433203017ca80401b2ee0dd69350349871c4b19d504c34dbdd80541690a  extracted/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc' \
  '89c3c497f618fdaa0b2d1e98fef93582f28c71debd2c4a8cdf41f190ced2909d  extracted/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf' | sha256sum --check
python3 -B "$root/tools/localization/build_font_candidate.py" \
  --root "$root" --cjk-font "$PWD/extracted/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" \
  --latin-font "$PWD/extracted/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf" \
  --license-file "$root/tools/localization/font_candidate/OFL.txt" --out "$destination"
