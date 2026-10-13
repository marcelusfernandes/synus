# Evidência, confiança e ressalvas

## Status e confiança

Cada documento declara no frontmatter `status` (`sufficient` ou `limited`) e `confidence` (0 a 1, duas casas, teto 0.95). Os valores refletem **quanto do documento foi observado em fontes** e quanto foi deduzido.

| confidence | status | Quando usar |
|---|---|---|
| 0.95 | sufficient | Quase tudo sustentado por várias páginas próprias da empresa; pouca síntese. |
| 0.88 – 0.92 | sufficient | Sustentado por fontes, com síntese ou interpretação relevante em uma ou duas seções. |
| 0.80 – 0.85 | limited | Partes centrais inferidas: preço não publicado, persona deduzida de poucos sinais, funcionalidade com página mas sem docs. |
| 0.60 – 0.75 | limited | O documento lê como especificação genérica: a funcionalidade é só citada, a evidência é indireta. |
| < 0.60 | — | Não escreva como se fosse real. Prefira deixar a categoria pendente (`--skip`) ou fale com o usuário. |

O `check` avisa quando `sufficient` vem com menos de 0.86 ou `limited` com mais de 0.85.

## Marcação `(Extrapolated)`

Toda frase ou item que **não vem diretamente de uma fonte** termina com `(Extrapolated)`, em qualquer documento, seja `sufficient` ou `limited`. Variante permitida: `(Extrapolated: motivo curto)`.

```markdown
- **Skill Registration**: Provide an API to register new skills with input schemas (Extrapolated: JSON Schema or similar).
- Enterprise buyers demand predictable budgeting, requiring usage tiers or caps. (Extrapolated)
```

Por quê: na biblioteca da Wonderful a marcação aparece "sem consistência", então um ponto sem marca não dava garantia de nada. A regra aqui é simples: **sem marca = tem fonte no ledger**. O `check` avisa quando um documento `limited` não tem nenhuma marca e quando um `sufficient` tem mais de 6 (provavelmente devia ser `limited`).

Não marque como inferida a síntese óbvia de fatos citados no próprio parágrafo. Marque conclusões, números, comportamentos e intenções que não estão na fonte.

## Ressalvas (`caveats`)

Ressalvas ficam no frontmatter, escritas **em português**. O `build` as transforma em alertas no topo do documento e as lista no README principal (exceto as do tipo `evidence`, que aparecem só no documento).

```yaml
caveats:
  - kind: conflict
    title: "Dado conflitante"
    text: "Banco Caja Social aparece como “zero to production in 19 days” em Differentiation, mas como “collections across 2.5 million clients in 19 days” em Market Worldview."
    link: market-worldview
```

| kind | Alerta | Use quando | Títulos usados na referência |
|---|---|---|---|
| `evidence` | WARNING | O documento como um todo tem evidência fraca ou de um tipo limitado (ex.: linguagem do cliente tirada do texto da própria empresa). | "Evidência fraca", "Fonte da linguagem" |
| `inferred` | NOTE | Um ponto específico e importante foi inferido e o leitor precisa saber, além da marca `(Extrapolated)`. | "Ponto extrapolado", "Pontos extrapolados", "Métricas inferidas", "Inferência estrutural" |
| `oddity` | NOTE | A fonte traz algo estranho (data no futuro, número implausível, termo que parece corrompido) e você o manteve como encontrado. | "Dado estranho", "Número provavelmente corrompido", "Termo provavelmente corrompido" |
| `conflict` | CAUTION | Duas fontes ou dois documentos discordam sobre o mesmo fato. | "Inconsistência", "Dado conflitante" |
| `truncated` | CAUTION | Só para material legado importado truncado. Documento gerado pela skill nunca fica truncado. | "Arquivo truncado" |

Regras:

- **`link`** recebe o `id` (não o caminho) de outro documento da biblioteca. O `build` transforma em "Ver também: [Título](caminho)".
- **Conflitos são recíprocos**: registre a ressalva nos dois documentos, cada uma com `link` para o outro. O `check` avisa quando falta a recíproca.
- **Não esconda conflitos.** Se as fontes discordam, mostre as duas versões, cada uma com a sua fonte. Escolher uma em silêncio cria o mesmo defeito da referência (OTE/OTC).
- `text` é uma ou duas frases objetivas: o que é, onde está e, se souber, a provável explicação.

## Ressalvas no nível da categoria e da biblioteca

- **`categories[].note`** (no `manifest.json`) vale para lacunas que afetam a categoria inteira. Aparece como aviso no README da categoria. Exemplos da referência: competição sem concorrentes nomeados nas fontes; preço sem nenhum valor público; funcionalidades com evidência fraca.
- **`caveats`** (no topo do `manifest.json`) vale para ressalvas transversais que devem abrir a lista do README principal. Use o mesmo formato `kind`/`title`/`text`.

Depois de editar o manifest, rode o `build`.
