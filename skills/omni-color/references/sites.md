# Sites de paleta (escolha pela tarefa)

Abra o site e traga o resultado de volta como hex para os seeds do `palette.json`. As URLs vêm de conhecimento/busca na web; verifique antes de depender delas.

| # | Site | Melhor para | Quando NÃO usar |
|---|---|---|---|
| 1 | https://oklch.com | Ver luminosidade/croma/matiz em OKLCH e os limites de gama; ajustar uma cor | Ideação de paleta inteira |
| 2 | https://huetone.ardov.me | Montar rampas com o contraste de cada degrau (WCAG/APCA) | Exploração de humor |
| 3 | https://leonardocolor.io | Rampas guiadas por contraste (Adobe Leonardo); defina a razão e receba as cores | Inspiração rápida |
| 4 | https://coolors.co | Gerar paletas rápido, travar/embaralhar, exportar | Acessibilidade rigorosa |
| 5 | https://color.adobe.com | Regras de harmonia (análoga, tríade…) e extração de imagem | Saída em tokens |
| 6 | https://huemint.com | Paletas por IA com prévia em mockups reais de marca/site | Pixel art |
| 7 | https://colorhunt.co | Conjuntos curados de 4 cores em alta, para achar o humor rápido | Escalas sistemáticas |
| 8 | https://www.realtimecolors.com | Prévia da paleta em um layout real, claro/escuro, ao vivo | Gerar cores |
| 9 | https://uicolors.app | Hex da marca → escala 50-950 do Tailwind | Matemática exata fora do Tailwind |
| 10 | https://m3.material.io/theme-builder | Sistema completo de papéis claro/escuro a partir de uma semente (Material 3) | Visuais fora do Material |
| 11 | https://www.radix-ui.com/colors | Escalas funcionais de 12 degraus comprovadas (fundos → texto) | Matizes de marca personalizados |
| 12 | https://contrast-ratio.com ou https://webaim.org/resources/contrastchecker | Aprovado/reprovado WCAG de um par | Escolher cores |
| 13 | https://colorbrewer2.org | Paletas de dataviz (sequencial/divergente/qualitativa, seguras para daltonismo) | Chrome da UI |
| 14 | https://colorable.jxnblk.com | Matriz de contraste para um conjunto de cores | – |
| 15 | https://lospec.com/palette-list | Paletas limitadas para pixel art / retrô (escolhidas à mão) | Escalas de UI web |
| 16 | https://colorkit.co ou https://www.happyhues.co | Exemplos de paleta aplicados a layouts | – |

## Atalhos de decisão
- Sabe o hex da marca → #9 ou o `build` desta skill, depois #2 para ajustar e #12 para provar.
- Sabe só o humor → #7/#4/#6, depois converta a vencedora com `init --brand`.
- Tem foto/logo → #5 para extrair, fique com 1 primária + 1 acento, descarte o resto.
- Checar modo escuro → #8 e #10.
- Gráficos → só #13.
- Pixel art/retrô → #15, depois entregue o `.hex` à skill `omni-sprite`.
