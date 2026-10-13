# Formato dos arquivos

## Anatomia de um documento

```markdown
---                                   ┐
id: icp                               │
title: "ICP"                          │
category: customers                   │
status: sufficient                    │  FRONTMATTER: você escreve
confidence: 0.92                      │
generated: 2026-10-13                 │
source: https://acme.io/              │
generator: wonderlust                 │
language: en                          │
sources:                              │
  - https://acme.io/customers         │
caveats: []                           │
---                                   ┘

# ICP                                 ┐
                                      │  CABEÇALHO: gerado pelo build
[Acme](../README.md) / [Clientes]…    │  (título, navegação, status, alertas)
                                      │
> [!CAUTION] …                        ┘

<!-- início do conteúdo original gerado por wonderlust (inglês) -->

## Executive Summary                  ┐
…                                     │  CORPO: você escreve
## Boundaries and Disqualifiers       │
…                                     ┘

<!-- fim do conteúdo original -->
```

- Os dois marcadores de comentário delimitam o corpo. Não os remova nem os duplique.
- Tudo entre o `---` de fechamento e o marcador de início é reescrito pelo `build`.

## Campos do frontmatter

| Campo | Obrigatório | Regra |
|---|---|---|
| `id` | sim | Igual ao nome do arquivo sem `.md`, em kebab-case. Único na biblioteca. |
| `title` | sim | Título exibido. Fixo para documentos da taxonomia; para funcionalidades, o nome que a empresa usa. |
| `category` | sim | Igual ao nome da pasta. |
| `status` | sim | `sufficient` ou `limited`. |
| `confidence` | sim | Número de 0.01 a 0.95 (ver `evidence-and-caveats.md`). O stub vem com 0.0 e o `check` recusa. |
| `generated` | sim | `AAAA-MM-DD` (UTC). |
| `source` | sim | URL principal recebida do usuário. |
| `generator` | sim | `wonderlust` (ou `Vicaura` em material legado). |
| `language` | sim | `en` (idioma do corpo). |
| `sources` | recomendado | Lista das URLs efetivamente usadas no documento. |
| `caveats` | sim | Lista de ressalvas (`kind`, `title`, `text`, `link` opcional), ou `[]`. |

Use o formato que o `build` escreve: chaves simples, strings entre aspas duplas quando tiverem `: ` ou caracteres especiais, listas com `  - `. O `build` normaliza a formatação.

## manifest.json

O `init` cria e o `build` reescreve. Campos que **você** pode editar (o `build` os preserva):

| Campo | Para quê |
|---|---|
| `product` | Nome do produto como a empresa escreve. |
| `lede` | Uma frase em português que descreve o produto. Abre o README. O `check` exige. |
| `caveats` | Ressalvas globais, exibidas primeiro no README. |
| `categories[].label`, `.blurb`, `.note` | Rótulo, descrição curta e nota de atenção da categoria. |
| `pending` | Categorias ainda não geradas (aparecem como placeholder). |
| `origin_artifact` | Opcional: link do artifact de origem, citado no rodapé. |

`categories[].docs`, `categories[].path` e `docs` são recalculados a partir dos arquivos a cada `build`.

Para gerar uma categoria pendente depois: mova o objeto dela de `pending` para `categories` (na posição desejada, sem a lista `docs` antiga) e rode `init <url> --root <raiz> --slug <slug>`. Os stubs que faltam são criados e nada existente é sobrescrito.

## Contagens

Nos READMEs, "N ressalvas" conta as ressalvas que não são do tipo `evidence`, como na referência. A tabela do README principal conta documentos por status.

## Ordem dos documentos

- Categorias fixas: a ordem da taxonomia (alfabética por id).
- `features`: maior confiança primeiro, depois título em ordem alfabética, como na referência.

## Mensagens do `check` e como corrigir

| Mensagem (início) | Correção |
|---|---|
| `ainda há TODO no corpo` | Preencha a seção e apague o comentário `<!-- TODO -->`. |
| `confidence não definido` | Defina `confidence` conforme a tabela de `evidence-and-caveats.md`. |
| `seções ausentes: … (estão como ###: promova para ##)` | Suba os títulos para `##` e remova o `##` de título acima deles. |
| `seções ausentes` / `fora de ordem` | Use exatamente as seções do arquétipo, na ordem. |
| `termina sem pontuação final, parece truncado` | Complete o documento; a última linha precisa ser uma frase completa. |
| `desatualizado …: rode build` | Rode `build` (alguém editou o frontmatter ou o corpo depois). |
| `link quebrado` | Corrija o link relativo ou o `link` da ressalva. |
| `ressalva aponta para id inexistente` | Use o `id` do documento (ex.: `market-worldview`), não o caminho. |
| `documento obrigatório ausente` | Rode `init` de novo para recriar o stub e preencha. |
| `lede vazio` | Escreva `lede` no `manifest.json` e rode `build`. |
| `AVISO … título de seção 'x' deveria ser 'X'` | Ajuste a caixa do título. |
| `AVISO … palavras (faixa esperada …)` | Aprofunde com evidência ou corte repetição. |
| `AVISO … limited sem nenhuma marcação (Extrapolated)` | Marque as afirmações inferidas, ou reavalie o status. |
| `AVISO … conflito … sem ressalva conflict no outro documento` | Adicione uma ressalva `conflict` no documento apontado (ver o padrão "central" para 3+ documentos). |
| `AVISO … subseções ausentes` | Crie as subseções `###` pedidas pelo arquétipo. |
