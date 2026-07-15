# Agent Skills

Skills reutilizáveis para Codex, Claude Code e agentes de programação compatíveis. O repositório oferece pacotes versionados e auditáveis, além de ferramentas multiplataforma para instalação, criação, sincronização, validação e releases.

Português (Brasil) · [English](README.md)

## Skills disponíveis

| Skill | Versão | Categoria | Status | Descrição | Fonte |
| --- | --- | --- | --- | --- | --- |
| `motion-site-builder` | 1.3.0 | frontend / motion / design | stable | Planeja e implementa sites animados premium e experiências WebGL. | [`skills/motion-site-builder`](skills/motion-site-builder) |
| `scroll-world-browser` | 1.0.0 | frontend / motion / automação de navegador | stable | Cria jornadas cinematográficas com scrub por scroll e geração de mídia via navegador. | [`skills/scroll-world-browser`](skills/scroll-world-browser) |
| `ui-ux-pro-max` | 2.11.0 | UI/UX / design systems | stable | Pesquisa inteligência de design estruturada e produz design systems orientados à implementação. | [`skills/ui-ux-pro-max`](skills/ui-ux-pro-max) |

## Compatibilidade

- Codex em `~/.codex/skills`;
- aplicativo ChatGPT/Codex;
- Claude Code em `~/.claude/skills`;
- agentes compatíveis com o diretório genérico `~/.agents/skills`.

## Instalação rápida

### Windows

```powershell
.\scripts\install-skill.ps1 -Name motion-site-builder -Targets agents,codex,claude
```

### macOS/Linux

```bash
./scripts/install-skill.sh motion-site-builder agents,codex,claude
```

## Invocação

```text
$motion-site-builder
```

Depois, descreva o site, público, restrições e linguagem de movimento desejada.

## Atualização e sincronização

Após `git pull`, execute novamente o instalador. Mantenedores podem importar a instalação local mais completa:

```powershell
.\scripts\sync-skill.ps1 -Name motion-site-builder -Source auto
```

## Criar uma skill

```powershell
.\scripts\new-skill.ps1 -Name my-new-skill
```

```bash
./scripts/new-skill.sh my-new-skill
```

O comando cria a versão `0.1.0` e registra uma entrada inicial em `skills.json`. Consulte [Como adicionar uma skill](docs/adding-a-skill.md).

## Empacotar uma release

```powershell
.\scripts\package-skill.ps1 -Name motion-site-builder
```

```bash
./scripts/package-skill.sh motion-site-builder
```

O pacote e seu SHA-256 são criados em `dist/`, que não é versionado.

## Skills complementares incluídas

A `motion-site-builder` pode coordenar [`ui-ux-pro-max`](skills/ui-ux-pro-max) para pesquisa de design systems e [`scroll-world-browser`](skills/scroll-world-browser) para fluxos cinematográficos assistidos por navegador. Ambas são distribuídas neste repositório com licença e proveniência preservadas. A primeira está fixada na release upstream `v2.11.0`; a segunda é uma adaptação derivada de [oso95/scroll-world](https://github.com/oso95/scroll-world).

## Segurança, licenças e roadmap

Nunca publique tokens, perfis de navegador, cookies, `.env` ou assets privados. Consulte [SECURITY.md](SECURITY.md). Código e documentação originais usam MIT; terceiros mantêm suas próprias licenças, conforme [THIRD_PARTY.md](THIRD_PARTY.md).

O roadmap inclui novas skills focadas, metadados verificáveis e testes dos instaladores em mais plataformas.

## Contribuição

Leia [CONTRIBUTING.md](CONTRIBUTING.md), [o formato das skills](docs/skill-format.md) e [o processo de release](docs/release-process.md). Envie pull requests focados, validados e sem assets de terceiros.
