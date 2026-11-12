# OmniColor 🎨⚡

> **Escolha, construa e aplique a paleta de cores de qualquer site ou app através de UM único arquivo espelho — com contraste verificado, modo escuro e entrevista guiada por IA.**
> 🇧🇷 **Projeto Brasileiro Open-Source** para quem cansou de trocar hex por hex em dezenas de arquivos.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Origin: Brazil](https://img.shields.io/badge/Feito%20no-Brasil%20%F0%9F%87%A7%F0%9F%87%B7-green.svg)](#-projeto-brasileiro-open-source)
[![Compatible: Claude Code](https://img.shields.io/badge/Compat%C3%ADvel-Claude%20Code-purple.svg)](#-instalação)
[![Python: stdlib](https://img.shields.io/badge/Python-3%20(s%C3%B3%20stdlib)-orange.svg)](#-instalação)
[![Color: OKLCH](https://img.shields.io/badge/Cor-OKLCH%20%2B%20WCAG-teal.svg)](#-o-que-é-a-omnicolor)

Troque uma cor em `palette.json`, rode `build`, e todas as páginas que usam `var(--token)` se atualizam. Sem caça a códigos hex espalhados.

![Saída de exemplo de `init --brand "#3b82f6"`: sete rampas OKLCH de 11 degraus (primária, acento, neutra, sucesso, aviso, perigo, info), seguidas dos tokens semânticos dos modos claro e escuro](docs/palette-example.png)

*Gerada por `omni_color.py init --brand "#3b82f6"` + `build`. Linhas 1–7: primária, acento (complemento automático), neutra com tom da marca, sucesso, aviso, perigo e info — degraus 50 → 950. As duas faixas de baixo: tokens semânticos dos modos claro e escuro (bg, surface, border, text, text-muted, primary, primary-hover, on-primary, accent, on-accent, ring e cores de status).*

---

## 🇧🇷 Projeto Brasileiro Open-Source

A **OmniColor** nasceu no Brasil para acabar com o retrabalho de paleta: escolher cores por feeling, copiar hex para cada arquivo e descobrir só no fim que o texto não tem contraste. O projeto prioriza:

- **Uma fonte da verdade:** um arquivo (`palette.json`) gera tudo; nada de hex solto nos componentes.
- **Acessibilidade de verdade:** o contraste WCAG é um portão que reprova, não uma sugestão "no limite".
- **Entrevista antes de sugerir:** a IA pergunta humor, modo, âncora de marca e público antes de propor cores.
- **Não bagunça seus arquivos:** marcadores de região, simulação (*dry run*) por padrão e backups ao aplicar.
- **Ecossistema aberto:** compõe com `omni-sprite` (a mesma paleta vira `.hex` do Aseprite) e com skills de polimento de interface.

---

## 🎯 O que é a OmniColor?

Uma skill (`SKILL.md` + script + referências) que reúne:

1. **🗣️ Entrevista com `grill-me`:** rodadas de perguntas independentes, cada uma com resposta recomendada, sobre humor, modo, marca, público, acessibilidade e restrições.
2. **🌐 16 sites de paleta** ([`sites.md`](skills/omni-color/references/sites.md)), cada um com quando usar e quando não usar: oklch.com, Huetone, Leonardo, Coolors, Adobe Color, Huemint, Color Hunt, Realtime Colors, UIColors, Material Theme Builder, Radix Colors, verificadores de contraste, ColorBrewer, Colorable, Lospec e Happy Hues.
3. **🧪 Rampas OKLCH** (50–950) para primária, acento, neutras com tom da marca e cores de status. Cor fora de gama perde croma, nunca luminosidade ou matiz. A cor da marca é **fixada**: o degrau mais próximo vira exatamente o seu hex e nunca é escurecido.
4. **✅ Portão de contraste WCAG** (texto, on-primary/on-accent e status a 4,5:1) com correção automática só de luminosidade.
5. **🪞 O arquivo espelho:** variáveis CSS para claro + escuro (`prefers-color-scheme` e `data-theme`), `@theme` do Tailwind v4 opcional e um `.hex` para ferramentas de pixel art.
6. **🔄 Adoção em sites existentes:** varre cores hex soltas e reescreve para `var(--token)` (simulação por padrão; backups ao aplicar; regiões geradas nunca são tocadas).
7. **🤝 Integra com outras skills** se instaladas: polimento de interface como `impeccable`, acessibilidade e design system.

---

## 🚀 Fluxo de trabalho

```mermaid
flowchart LR
  Q[Entrevista grill-me] --> I[init --brand]
  I --> P[(palette.json<br/>fonte da verdade)]
  P --> C[check --fix<br/>portão WCAG]
  C --> B[build]
  B --> T[theme.css<br/>+ tailwind + .hex]
  S[scan / adopt] -->|hex → var--token| SITE[seu site]
  T --> SITE
  P -. edite uma cor .-> B
```

O `palette.json` tem `seeds` (primary, accent, success, warning, danger, info), `overrides` (ex.: `"primary.500": "#hex"`) e `semantic.light/dark` (token → `rampa.degrau`). O bloco gerado no `theme.css` fica entre os marcadores `omni-color:begin/end` e **não deve ser editado à mão**.

---

## ⚡ Comandos & Modos de Uso

```bash
python omni_color.py init --brand "#3b82f6"            # cria o palette.json
python omni_color.py check --fix                        # portão de contraste
python omni_color.py build --css src/theme.css --tailwind src/tw.css --hex palette.hex
python omni_color.py scan ./src                         # cores soltas por frequência
python omni_color.py adopt ./src                        # simulação (dry run)
python omni_color.py adopt ./src --apply                # grava, backups em .omni-color-backup/
```

Depois importe o `theme.css` uma vez e use `var(--bg)`, `var(--text)`, `var(--primary)`, `var(--on-primary)`, `var(--border)`, `var(--ring)`… Mude um *seed* no `palette.json`, rode `build`, pronto.

### 💬 Ou simplesmente peça à IA
```text
omni-color: escolha uma paleta para minha landing page, calma mas premium, com modo escuro
omni-color: troque o azul do site inteiro para #0ea5e9 sem quebrar o contraste
omni-color: adapte as cores deste projeto existente para tokens
```
A IA lê o projeto, faz a entrevista, propõe 3–5 sementes candidatas, você escolhe, ela constrói e verifica.

---

## 📦 Instalação

### 1. Um comando (recomendado)
```powershell
.\install.ps1        # Windows (PowerShell)
```
```bash
./install.sh         # macOS / Linux
```
Copia `skills/*` para `~/.claude/skills`. O Python 3 (só biblioteca padrão) é necessário para rodar o script; se faltar, a IA pergunta antes de instalar. Verifique: `python skills/omni-color/scripts/omni_color.py selftest`.

### 2. Instalação manual
```bash
# Claude Code
mkdir -p ~/.claude/skills && cp -r skills/omni-color skills/grill-me ~/.claude/skills/

# Antigravity / Gemini CLI
mkdir -p ~/.gemini/config/skills && cp -r skills/omni-color skills/grill-me ~/.gemini/config/skills/
```

---

## 🧭 Princípios de design (de uma revisão crítica de seis skills da comunidade)

Rampas em OKLCH, não HSL · impor contraste em vez de chamar de "no limite" · modo escuro é um novo fundo, não uma rampa invertida · nunca espalhar hex (uma só fonte) · nunca sobrescrever arquivos em silêncio (marcadores, simulação, backups) · neutras com tom e no máximo 3–4 matizes · perguntar antes de sugerir · nunca tratar conteúdo de site como instrução. Veja [`integrations.md`](skills/omni-color/references/integrations.md).

## ⚠️ Limites conhecidos

O `adopt` mapeia para o token de rampa mais próximo (ΔE em OKLab ≤ 0,03) e deixa o resto para decisão humana — por exemplo, um azul-marinho `#0f172a` pode cair em `--info-950` em vez de um neutro; troque depois por tokens de papel (`--text`, `--primary`…) à mão. Só trata hex literal, não `rgb()`/`hsl()`. As URLs de `sites.md` vêm de conhecimento da web e devem ser verificadas.

## 🗂️ Estrutura do repositório

```text
install.ps1 / install.sh
docs/palette-example.png
skills/
  omni-color/   SKILL.md · scripts/omni_color.py · references/ (perguntas, sites, integrações)
  grill-me/     skill de entrevista incluída (Matt Pocock, MIT, em inglês, sem alterações)
THIRD_PARTY_NOTICES.md  LICENSE
```

---

## 🏆 Créditos & Referências

- **[Matt Pocock — skill grilling / grill-me](https://github.com/mattpocock/skills)** — © 2026, MIT. Incluída sem alterações em `skills/grill-me/`.
- **OKLab** de Björn Ottosson; **contraste WCAG** do W3C.
- Ideias (nenhum código copiado) de artistic-color-palettes, color-palette-extractor, skill.color-expert, jezweb/color-palette, NickCrew/color-palette e dembrandt/algorithmic-color-palette — veja [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE).
Feito com 💚 e 💛 no Brasil por [LimaEdu-7x](https://github.com/LimaEdu-7x).
