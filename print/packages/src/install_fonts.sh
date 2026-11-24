#!/usr/bin/env bash
# Installs the fonts the one-sheet needs as user fonts (Linux/macOS).
# "SG Print" = static instances of Schibsted Grotesk (400/500/600/800) renamed so the
# PDF embeds plain TrueType instead of a variable font, which some printers' preflight rejects.
set -e
cd "$(dirname "$0")/../fonts"
if [ "$(uname)" = "Darwin" ]; then DEST="$HOME/Library/Fonts"; else DEST="$HOME/.fonts"; fi
mkdir -p "$DEST"
cp SGPrint-*.ttf IBMPlexMono-*.ttf "$DEST/"
command -v fc-cache >/dev/null && fc-cache -f >/dev/null || true
echo "Installed fonts to $DEST"
