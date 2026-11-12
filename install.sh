#!/usr/bin/env bash
# Instalação em um comando: copia as skills para ~/.claude/skills. O Python 3 só é necessário para rodar o script de paleta.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"; mkdir -p "$DEST"
for s in "$HERE"/skills/*/; do
  n="$(basename "$s")"
  if [ "$n" = "grill-me" ] && [ -d "$DEST/$n" ]; then echo "grill-me já instalada, pulando"; continue; fi
  rm -rf "${DEST:?}/$n"; cp -r "$s" "$DEST/$n"; echo "skill instalada: $n"
done
command -v python3 >/dev/null || command -v python >/dev/null || echo "Python 3 não encontrado. A IA vai oferecer instalá-lo quando precisar."
