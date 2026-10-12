#!/usr/bin/env bash
# Aplica/atualiza o cabeçalho OSA no README de um repo. Idempotente.
# Uso: apply-header.sh <repo>   (rodar a partir de g-open-software-alliance/)
set -euo pipefail
repo="$1"
root="$(cd "$(dirname "$0")/.." && pwd)"
line=$(awk -F'\t' -v r="$repo" '$1==r' "$root/.osa/repos.tsv")
[ -n "$line" ] || { echo "repo $repo fora do manifesto" >&2; exit 1; }
IFS=$'\t' read -r _ product tagline alt upname upurl license <<<"$line"
readme="$root/$repo/README.md"
[ -f "$readme" ] || touch "$readme"
body=$(awk '/<!-- osa:header:start -->/{s=1} !s{print} /<!-- osa:header:end -->/{s=0}' "$readme")
alt_line=""
[ "$alt" != "-" ] && alt_line="Open alternative to **$alt**, part of the [Open Software Alliance](https://github.com/OpenSoftwareAlliance) suite."
[ "$alt" = "-" ] && alt_line="Part of the [Open Software Alliance](https://github.com/OpenSoftwareAlliance) suite."
{
cat <<H
<!-- osa:header:start -->
# $product

$tagline $alt_line

| | |
|---|---|
| Upstream | [$upname]($upurl), kept in sync with this repository |
| License | $license |

Credit for the original work goes to the $upname authors. Everything below this header is the upstream README.

---
<!-- osa:header:end -->
H
printf '%s\n' "$body" | sed '/./,$!d'
} > "$readme.tmp" && mv "$readme.tmp" "$readme"
echo "header ok: $repo"
