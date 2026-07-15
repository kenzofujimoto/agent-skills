# Agent Skills

Skills reutilizáveis para Codex, Claude Code e agentes de programação compatíveis. O repositório oferece pacotes versionados e auditáveis, além de ferramentas multiplataforma para instalação, criação, sincronização, validação e releases.

Português (Brasil) · [English](README.md)

## Skills disponíveis

| Skill | Versão | Categoria | Status | Descrição | Fonte |
| --- | --- | --- | --- | --- | --- |
| `motion-site-builder` | 1.3.0 | frontend / motion / design | stable | Planeja e implementa sites animados premium e experiências WebGL. | [`skills/motion-site-builder`](skills/motion-site-builder) |

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

## Integrações opcionais

A skill pode coordenar [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) e [scroll-world](https://github.com/oso95/scroll-world). Esses projetos não estão incluídos e não são mantidos neste repositório.

## Segurança, licenças e roadmap

Nunca publique tokens, perfis de navegador, cookies, `.env` ou assets privados. Consulte [SECURITY.md](SECURITY.md). Código e documentação originais usam MIT; terceiros mantêm suas próprias licenças, conforme [THIRD_PARTY.md](THIRD_PARTY.md).

O roadmap inclui novas skills focadas, metadados verificáveis e testes dos instaladores em mais plataformas.

## Contribuição

Leia [CONTRIBUTING.md](CONTRIBUTING.md), [o formato das skills](docs/skill-format.md) e [o processo de release](docs/release-process.md). Envie pull requests focados, validados e sem assets de terceiros.
