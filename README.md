# Open Software Alliance

Clones da org [OpenSoftwareAlliance](https://github.com/OpenSoftwareAlliance): hard forks branded "OSA <Nome>", mantidos em sync com o upstream, para formar uma alternativa aberta ao Google Workspace.

| Repo | Produto | Concorre com | Upstream |
|---|---|---|---|
| [`pad`](pad/) | OSA Pad | Google Docs | [Etherpad](https://github.com/ether/etherpad) |
| [`sheet`](sheet/) | OSA Sheet | Google Sheets | [Luckysheet](https://github.com/dream-num/Luckysheet) |
| [`cal`](cal/) | OSA Cal | Google Calendar (appointment schedules) | [Cal.diy](https://github.com/calcom/cal.diy) |
| [`mail`](mail/) | OSA Mail | Gmail | [Forward Email](https://github.com/forwardemail/forwardemail.net) |
| [`meet`](meet/) | OSA Meet | Google Meet | [Briefing](https://github.com/holtwick/briefing) |
| [`draw`](draw/) | OSA Draw | Google Drawings / Jamboard | [tldraw](https://github.com/tldraw/tldraw) |
| [`drop`](drop/) | OSA Drop | Quick Share | [Snapdrop](https://github.com/SnapDrop/snapdrop) |
| [`share`](share/) | OSA Share | Google Drive (file links) | [Uguu](https://github.com/nokonoko/Uguu) |
| [`share-admin`](share-admin/) | OSA Share Admin | Google Drive admin | [Moe Panel](https://github.com/pomf/MoePanel) |
| [`bin`](bin/) | OSA Bin | Google Keep (secure notes) | [PrivateBin](https://github.com/PrivateBin/PrivateBin) |
| [`snip`](snip/) | OSA Snip | Google Keep (snippets) | [Drift](https://github.com/MaxLeiter/Drift) |
| [`short`](short/) | OSA Short | goo.gl | [Kutt](https://github.com/thedevs-network/kutt) |
| [`alias`](alias/) | OSA Alias | Google Domains forwarding | [redirect.name](https://github.com/frolic/redirect.name) |
| [`page`](page/) | OSA Page | Google Sites | [Singlelink](https://github.com/singlelink-co/Singlelink) |
| [`feedback`](feedback/) | OSA Feedback | Google Forms (product feedback) | [LogChimp](https://github.com/logchimp/logchimp) |
| [`jam`](jam/) | OSA Jam | Google Meet (audio) | [Jam](https://github.com/jam-systems/jam) |
| [`micro`](micro/) | OSA Micro | Google Cloud APIs | [M3O](https://github.com/keonjeo/m3o) |
| [`username`](username/) | OSA Username | - | [Instant Username Search](https://github.com/instantusername/instant-username-search) |
| [`status`](status/) | OSA Status | — | [Upptime](https://github.com/upptime/upptime) |

## Ferramentas (`.osa/`)

- `repos.tsv`: manifesto (produto, alternativa, upstream, licença).
- `readme.py [repo...]`: gera o README padronizado OSA (modelo único: features, stack, roadmap, suíte, licença). Rodar de novo depois de cada sync que mexer no README.
- `issues.tsv`: URLs das issues de pesquisa (landscape e migração) de cada repo.
- `apply-header.sh`: obsoleto (modelo antigo de cabeçalho + README do upstream).
- `sync.sh <dir> <upstream_url> <branch>`: fast-forward ou merge assinado com o upstream. Não faz push; em conflito, para.

Para os forks sem divergência, `gh repo sync OpenSoftwareAlliance/<repo>` resolve direto no GitHub.

## Como usar este repo

Este repo é a raiz da área de trabalho: clone-o e depois os repos da org dentro dele.

```bash
gh repo clone OpenSoftwareAlliance/osa-tooling ~/Dev/4-projetos/g-open-software-alliance
cd ~/Dev/4-projetos/g-open-software-alliance
for r in $(cut -f1 .osa/repos.tsv | grep -v '^#') status; do gh repo clone OpenSoftwareAlliance/$r $r -- --filter=blob:none; done
gh repo clone OpenSoftwareAlliance/vorssaint-utils vorssaint-utils   # OSA Desktop (será renomeado para osa-desktop)
gh repo clone OpenSoftwareAlliance/boring.notch boring.notch
```

Os diretórios clonados são ignorados (`.gitignore`); só `.osa/` e este README são versionados.
