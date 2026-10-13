# Wonderful

> Arquivos de referência da Vicaura sobre a Wonderful ([wonderful.ai](https://wonderful.ai/)), organizados por categoria.

Um sistema operacional de IA enterprise unificado, com capacidades de plataforma e times de deployment para transformar operações de negócio.

| Fonte | Gerado | Documentos | Limited |
|---|---|---|---|
| [wonderful.ai](https://wonderful.ai/) | 2026-10-03 UTC | 43 | 13 |

> [!IMPORTANT]
> **Produto de referência.** Estes arquivos descrevem a Wonderful, não o nosso produto. Use como exemplo, benchmark ou evidência de mercado.

## Categorias

| Categoria | Descrição | Docs | Sufficient | Limited |
|---|---|---|---|---|
| [Estratégia de produto](product-strategy/README.md) | Tese, princípios, gosto de produto, casos de uso centrais e lógica de expansão. | 5 | 5 | 0 |
| [Clientes](customers/README.md) | ICP, persona compradora e persona usuária. | 3 | 3 | 0 |
| [Problemas e demanda](problems-and-demand/README.md) | Modelo de problema, JTBD, resultados desejados, gatilhos de compra e troca, alternativas atuais. | 6 | 6 | 0 |
| [Mercado e posicionamento](market-and-positioning/README.md) | Categoria, posicionamento, promessa de valor, diferenciação e visão de mercado. | 5 | 5 | 0 |
| [Competição](competition-and-market-dynamics/README.md) | Pilha de vantagens competitivas e estratégia de troca. | 2 | 2 | 0 |
| [Preço e monetização](pricing-and-monetization/README.md) | Modelo de preço, métrica de valor, empacotamento e filosofia de monetização. | 4 | 3 | 1 |
| [Mensagem e marca](messaging-and-brand/README.md) | Hierarquia de mensagens, narrativa, voz, léxico e linguagem do cliente. | 5 | 4 | 1 |
| [Funcionalidades](features/README.md) | Plataforma (Orchestrator, Skills, Knowledge, Guardrails…) e modelos de deployment. | 13 | 2 | 11 |
| [Vendas e GTM](sales-and-gtm/README.md) | Ainda não gerado (Sales Motion). | 0 | — | — |

## Como ler a confiabilidade

- **`sufficient`**: a Vicaura encontrou evidência suficiente para sustentar o arquivo.
- **`limited`**: menos evidência. Afirmações não marcadas podem ser inferidas, não observadas.
- **Marcações**: pontos às vezes aparecem como *Extrapolated* ou *structural inference*, mas sem consistência: um ponto sem marca não está necessariamente verificado.

Cada documento traz `status` e `confidence` (0 a 1) no frontmatter.

## Ressalvas conhecidas

Cada uma também aparece no topo do documento correspondente.

- **Evidência · Funcionalidades de plataforma com evidência fraca.** As 9 funcionalidades de plataforma (Orchestrator até CLI) têm evidência fraca (limited, 0.60 a 0.80). Leem mais como templates genéricos de spec do que como comportamento documentado da Wonderful. Trate a maior parte como inferência.
- **Conflito · Inconsistência.** ([Buyer Persona](customers/buyer-persona.md)) Usa “OTC”; o ICP chama o mesmo cliente de “OTE”. Ver também: [ICP](customers/icp.md).
- **Estranheza · Dado estranho.** ([ICP](customers/icp.md)) Menciona “a $550M Series C in late 2026”, mantido como a Vicaura retornou.
- **Conflito · Inconsistência.** ([ICP](customers/icp.md)) Cita “OTE” como cliente; Buyer Persona usa “OTC” para o mesmo cliente. Ver também: [Buyer Persona](customers/buyer-persona.md).
- **Truncado · Arquivo truncado.** ([Jobs to Be Done](problems-and-demand/jobs-to-be-done.md)) Para no meio de uma frase em Causal Structure, com 3 das 6 seções habituais. A Vicaura gerou assim e ainda o reporta como completo.
- **Conflito · Dado conflitante.** ([Differentiation](market-and-positioning/differentiation.md)) Banco Caja Social aparece como “zero to production in 19 days” em Differentiation, mas como “collections across 2.5 million clients in 19 days” em Market Worldview. Ver também: [Market Worldview](market-and-positioning/market-worldview.md).
- **Truncado · Arquivo truncado.** ([Positioning](market-and-positioning/positioning.md)) Para no meio de uma frase na última seção, Strategic Implications. A Vicaura gerou assim e o reporta como completo.
- **Estranheza · Número provavelmente corrompido.** ([Switching Strategy](competition-and-market-dynamics/switching-strategy.md)) Diz “19 to 3 weeks” até produção. Outros arquivos falam em 19 dias (Banco Caja Social) e 3 a 5 semanas (utilities e telecom). Ver também: [Desired Outcomes](problems-and-demand/desired-outcomes.md).
- **Truncado · Arquivo truncado.** ([Pricing Model](pricing-and-monetization/pricing-model.md)) Para no meio de uma frase em Expansion Mechanics, com 5 das 6 seções habituais.
- **Estranheza · Termo provavelmente corrompido.** ([Value Metric](pricing-and-monetization/value-metric.md)) “bring-your-spec” provavelmente quer dizer bring-your-own-cloud. Ver também: [Bring Your Own Cloud](features/bring-your-own-cloud.md).
- **Inferido · Métricas inferidas.** ([Value Metric](pricing-and-monetization/value-metric.md)) As estruturas de métrica de valor (agentes ativos, throughput, tiers de deployment) são candidatas inferidas, não preço público.
- **Estranheza · Termo truncado.** ([Multi-Tenant Deployment](features/multi-tenant-deployment.md)) “Resource Contubation” em Edge Cases provavelmente significa “Resource Contention”.
- **Inferido · Ponto extrapolado.** ([Bring Your Own Cloud](features/bring-your-own-cloud.md)) A nota sobre bundle offline foi marcada como extrapolada.
- **Inferido · Inferência estrutural.** ([Alerts](features/alerts.md)) O edge case de alertas intermitentes (flapping) foi marcado como “structural inference”.
- **Inferido · Ponto extrapolado.** ([Knowledge](features/knowledge.md)) A filtragem de PII durante a ingestão foi marcada pela Vicaura como extrapolada.
- **Inferido · Pontos extrapolados.** ([Skills](features/skills.md)) O padrão de validação de schema e o data store foram marcados como extrapolados.

> [!NOTE]
> **Ainda não gerado:** Sales & GTM (Sales Motion).

## Estrutura

```text
wonderful/
├── README.md              # esta visão geral
├── manifest.json          # metadados de categorias, documentos e ressalvas
├── product-strategy/                     # 5 docs + README.md
├── customers/                            # 3 docs + README.md
├── problems-and-demand/                  # 6 docs + README.md
├── market-and-positioning/               # 5 docs + README.md
├── competition-and-market-dynamics/      # 2 docs + README.md
├── pricing-and-monetization/             # 4 docs + README.md
├── messaging-and-brand/                  # 5 docs + README.md
├── features/                             # 13 docs + README.md
└── sales-and-gtm/                        # placeholder
```

Cada documento segue o mesmo formato:

1. **Frontmatter YAML**: `id`, `title`, `category`, `status`, `confidence`, `generated`, `source`, `generator`, `language` e `caveats` (lista de `kind`, `title`, `text` e, quando houver, `link` para o `id` de outro documento).
2. **Cabeçalho**: título, navegação e as ressalvas como alertas (`CAUTION` para conflito/truncado, `WARNING` para evidência fraca, `NOTE` para inferência/estranheza).
3. **Conteúdo original** entre os comentários `<!-- início do conteúdo original ... -->` e `<!-- fim do conteúdo original -->`, mantido em inglês e sem edição, inclusive nos arquivos truncados.

Tipos de ressalva (`kind`): `evidence` (evidência fraca), `inferred` (inferido), `oddity` (estranheza), `conflict` (conflito entre arquivos), `truncated` (arquivo truncado).

---

Arquivos gerados pela Vicaura em 2026-10-03 (UTC). Conteúdo dos documentos mantido no original em inglês. Migrado do artifact [Wonderful Reference](https://claude.ai/artifact/QUz56NJ19SM67REajzvYEC).
