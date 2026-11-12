# Integrações e ideias aproveitadas

## Skills analisadas (a revisão crítica informou o design)
| Skill | Origem | Aproveitado | Deliberadamente evitado |
|---|---|---|---|
| artistic-color-palettes | github.com/youssef4laa/artistic-color-palettes | Perguntar primeiro, escolher 3–5 candidatas, o usuário decide; rampas OKLCH; portão WCAG; correção só de luminosidade; cor de marca fixada nunca escurecida; modo escuro como novo fundo; gravar só dentro de regiões marcadas | Dependência de script em todas as etapas; dados de paleta só históricos |
| color-palette-extractor | github.com/OneWave-AI/claude-skills | Extrair de imagem/site; ignorar quase-branco/quase-preto; ideia de simulação de daltonismo; exportação multiformato | Sem fonte única da verdade; agrupamento vago |
| skill.color-expert | github.com/meodai/skill.color-expert | Reduzir croma (não L/H) para caber na gama; camadas referência → semântico → componente; derivar estados por regra; ferramentas (Huetone, oklch.com, Leonardo) | Carregar enormes conjuntos de referência no contexto |
| color-palette | github.com/jezweb/claude-skills | Tokens semânticos com par bg/fg; `@theme` do Tailwind v4 + `.dark`; reduzir saturação na ponta clara | Rampas em HSL; contraste "no limite" aceito |
| color-palette | github.com/NickCrew/Claude-Cortex | Nomes de token por papel; neutras com tom; máx. 3–4 matizes; teste em escala de cinza | Dois sistemas de escala concorrentes |
| algorithmic-color-palette | github.com/dembrandt/dembrandt-skills | Tokens funcionais (foco, seleção, overlay, deltas de hover/active); faixas de matiz semânticas | Matemática HSL sem verificação de contraste |

(As revisões são resumos de uma passada crítica independente; abra cada repositório para ver o código de verdade.)

## Skills companheiras (opcionais; use se estiverem instaladas)
| Skill | Papel na omni-color |
|---|---|
| **impeccable** (skill de design/polimento/auditoria de UI, ex.: `impeccable-craft`) | Depois de construir a paleta: rode a crítica/auditoria/polimento nas páginas que consomem os tokens; use para tipografia, hierarquia, estados, casos vazios/extremos e para escrever o `DESIGN.md` que documenta os tokens |
| **grill-me** (instalada junto, de Matt Pocock, MIT) | Conduz a entrevista de `questions.md`: rodadas de perguntas independentes, cada uma com resposta recomendada, até esgotar a árvore de decisões |
| frontend-design / skills de estilo "taste" | Escolher a direção estética *antes* da paleta (humor, densidade) |
| accessibility-review / web-design-guidelines | Auditoria final de contraste, anel de foco e significado só por cor |
| design-system / design-handoff | Exportar tokens para um documento de design system ou passar para desenvolvedores |
| dataviz | Gráficos precisam das próprias paletas categóricas/sequenciais validadas |
| **`/sprite`** (omni-sprite) | `build --hex palette.hex` → importar no Aseprite para pixel art combinando com o site |
| skills de tokens/ui-craft (ex.: extratores de design tokens) | Semear o `palette.json` com os estilos computados de um site ao vivo |

Se uma companheira não existir, faça a etapa dela você mesmo com o checklist do `SKILL.md`; nunca trave por causa disso.
