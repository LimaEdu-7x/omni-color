# Entrevista de paleta (rode com a skill `grill-me`: rodadas de perguntas independentes, cada uma com resposta recomendada)

Rodada 1 = perguntas 1–3 (não dependem entre si). Rodada 2 = 4–7, depois de definidos superfície/modo/âncora. Rodada 3 = 8–10. Pule o que já for conhecido pelo projeto. Após cada rodada, reafirme as decisões em uma linha. Pare quando conseguir preencher todos os campos do **Registro de decisões** abaixo e espere a confirmação do usuário.

1. **Superfície** – É um site novo ou existente? (Se existente: caminho do código → rode `scan` primeiro.)
2. **Modo** – Só claro, só escuro ou ambos? *Recomendação: ambos, claro como padrão.*
3. **Âncora de marca** – Existe hex/logo fixo? (Cores fixadas nunca são alteradas; só muda o papel delas.)
4. **Humor** – Escolha dois: calmo / enérgico / premium / divertido / técnico / quente / austero / futurista. *Recomendação: um humor principal e um contra-humor.*
5. **Público e contexto** – Quem usa, onde (escritório, celular ao ar livre, à noite)? Alguma necessidade de acessibilidade (baixa visão, daltonismo)? *Padrão: WCAG AA, texto a 4,5:1, UI a 3:1.*
6. **Estratégia de cor** – Monocromática + neutra, análoga, acento complementar ou tríade? *Recomendação: uma primária + um acento + neutras com tom (máx. 3–4 matizes).*
7. **Densidade de cor** – Majoritariamente neutro com cor só nas ações, ou superfícies ricas em cor? *Recomendação: dominância neutra, 60/30/10.*
8. **Dados/gráficos?** – Precisa de escalas categóricas ou sequenciais? (use conjuntos seguros do tipo ColorBrewer)
9. **Referências** – Algum site, produto, imagem ou paleta que você gosta/não gosta? (extraia com os sites de `sites.md`)
10. **Restrições** – Framework (Tailwind v4 / CSS puro / SCSS / CSS-in-JS), tokens de design existentes, guia de marca a respeitar?

## Registro de decisões (escreva nos comentários do palette.json ou na descrição do PR)
`modo · semente primária · semente de acento (ou auto) · origem do tom das neutras · estratégia · meta de contraste · saídas (css/tailwind/hex) · cores fixadas`

## Comandos para entregar ao usuário (copiar e colar)
```
python scripts/omni_color.py init --brand "#RRGGBB"
python scripts/omni_color.py check --fix
python scripts/omni_color.py build --css src/theme.css [--tailwind src/tailwind-colors.css] [--hex palette.hex]
python scripts/omni_color.py scan ./src
python scripts/omni_color.py adopt ./src            # simulação
python scripts/omni_color.py adopt ./src --apply    # grava, com backups
```
