#!/usr/bin/env bash
# Sincroniza um repo local com o upstream: fast-forward se der, senão merge assinado.
# Uso: sync.sh <dir> <upstream_url> <upstream_branch>
# Não faz push. Em conflito, para e deixa o merge aberto para resolução manual.
set -euo pipefail
dir="$1"; url="$2"; ub="$3"
cd "$dir"
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "$url"
git remote set-url upstream "$url"
git config remote.upstream.promisor true
git config remote.upstream.partialclonefilter blob:none
git fetch -q upstream "$ub"
lb=$(git symbolic-ref --short HEAD)
git pull -q --ff-only origin "$lb"
if git merge-base --is-ancestor "upstream/$ub" HEAD; then echo "$dir: já contém upstream/$ub"; exit 0; fi
if git merge -q --ff-only "upstream/$ub" 2>/dev/null; then echo "$dir: fast-forward para upstream/$ub"; exit 0; fi
git merge -S --no-edit -m "Merge upstream $url ($ub) into $lb" "upstream/$ub" && echo "$dir: merge ok" || { echo "$dir: CONFLITO"; git diff --name-only --diff-filter=U | head -30; exit 2; }
