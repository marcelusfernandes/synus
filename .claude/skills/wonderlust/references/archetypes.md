# Arquétipos de documento

Cada categoria tem **um** arquétipo: a mesma sequência de seções `##` em todos os documentos da categoria. A lista exata, as subseções obrigatórias e a faixa de palavras estão em `assets/taxonomy.json`, e os stubs do `init` já trazem os títulos certos. Este arquivo explica **o que vai em cada seção** e a forma especial de alguns documentos. Os trechos de exemplo vêm de `vicaura/wonderful/`.

Sumário: [Estilo comum](#estilo-comum) · [strategy](#strategy--product-strategy) · [customer](#customer--customers) · [demand](#demand--problems-and-demand) · [positioning](#positioning--market-and-positioning) · [competition](#competition--competition-and-market-dynamics) · [commercial](#commercial--pricing-and-monetization) · [gtm](#gtm--sales-and-gtm) · [messaging](#messaging--messaging-and-brand) · [feature](#feature--features)

## Estilo comum

- **Língua**: corpo em inglês; títulos de seção em inglês e em Title Case, exatamente como no stub.
- **Hierarquia**: `##` para as seções do arquétipo, `###` para subseções. Sem `#` no corpo (o título vem do frontmatter) e sem um `##` de título antes das seções. Três documentos da Wonderful fizeram isso (`core-use-cases`, `pricing-model`, `brand-voice`) e o `check` acusa erro.
- **Voz**: analítica, em terceira pessoa e no presente. O Executive Summary abre com o produto como sujeito e a tese do documento: *"Wonderful provides an applied AI platform and operating system (AI OS) designed to take complex enterprise workflows into regulator-ready production."*
- **Listas**: itens com rótulo em negrito, `- **Label:** explanation.`; listas numeradas para sequências, cadeias causais, fases e flywheels. Tabela só onde o arquétipo pede (pilha de vantagens).
- **Prova concreta**: clientes, métricas, datas e valores com a grafia exata do ledger. Prefira "*91.5% containment (Telefónica)*" a "*high containment rates*".
- **Sem hype**: adjetivos de marketing só dentro de citações literais.
- **Inferência marcada**: `(Extrapolated)` no fim de cada frase ou item que não vem de uma fonte.
- **Sem seção de fontes no corpo**: as URLs vão para `sources` no frontmatter.
- **Final completo**: a última linha é uma frase terminada em pontuação.
- **Tamanho**: Executive Summary com 1 a 2 parágrafos (90 a 180 palavras). O documento inteiro fica dentro da faixa do arquétipo (o `check` avisa fora dela).

---

## strategy — product-strategy

Seções: **Executive Summary · Strategic Thesis · Core Principles · Product Expression · Tradeoffs and Boundaries · Implementation Implications**

- **Strategic Thesis**: a aposta de fundo. Ou uma frase "If …, then … must …, producing …" seguida de 2 a 3 pilares numerados, ou 3 afirmações numeradas em negrito.
- **Core Principles**: 3 a 5 itens `- **Principle Name:** explanation`.
- **Product Expression**: onde a tese aparece de verdade, com superfícies, funcionalidades, opções de deployment e clientes nomeados.
- **Tradeoffs and Boundaries**: o que o produto deliberadamente não faz e para quem não serve.
- **Implementation Implications**: consequências práticas, de preferência agrupadas por público (`**For Product Architecture:**`, `**For Deployment Teams:**`).

Formas especiais:
- `product-principles`: Core Principles em subseções `### 1. Prefer X over Y`, cada uma com dois itens:
  ```markdown
  ### 1. Prefer Operational Reliability over Feature Abundance
  * **Operational Rule:** Prefer building deterministic guardrails ... over shipping raw ... feature breadth.
  * **Context:** Enterprise environments cannot tolerate unpredictable model outputs ...
  ```
- `product-thesis`: a Strategic Thesis começa com a frase "If …, then …".
- `product-taste`: Product Expression cobre *Interface Density & Layout*, *Interaction Style*, *Copywriting & Terminology* e *Onboarding & Guidance*. Tradeoffs and Boundaries cobre *Opinionated vs. Configurable*, *Speed vs. Ceremony* e *Expert vs. Novice*.
- `core-use-cases`: Product Expression agrupa casos por indústria ou função, cada um com cliente e resultado.
- `expansion-logic`: Product Expression numera os vetores de expansão (entry wedge → amplitude horizontal → replicação por linha de negócio → superfícies → handover).

## customer — customers

Seções: **Executive Summary · Primary Profile · Evidence-Backed Attributes · Needs and Constraints (### Needs, ### Constraints) · Decision Implications · Boundaries and Disqualifiers**

- **Primary Profile**: itens com rótulo. No `icp`: *Company Type & Industry*, *Company Size*, *Team & Function* e *Operating Maturity*. Nas personas: *Role & Title*, *Reporting Line*, *Responsibilities*, *Success Metrics* e *Tools & Environment*.
- **Evidence-Backed Attributes**: cada atributo com o sinal concreto que o sustenta, como as faixas do formulário de contato, os clientes dos estudos de caso ou os requisitos de vagas: *"Contact form qualification tiers explicitly start at 0-100 and scale through 100-1,000, 1,000-10,000, to 10,000+ employees"*.
- **Needs and Constraints**: sempre com as duas subseções, 3 a 4 itens cada.
- **Boundaries and Disqualifiers**: quem não é cliente e por quê (porte, maturidade, tipo de necessidade).

## demand — problems-and-demand

Seções: **Executive Summary · Core Model · Causal Structure · Triggers and Context · Customer Consequences · Product Implications**

- **Core Model**: a tensão central em 1 parágrafo, mais o modelo no formato do documento (abaixo).
- **Causal Structure**: a cadeia de causas, com itens rotulados ou numerados.
- **Triggers and Context**: condições em que o problema ou a demanda aparece.
- **Product Implications**: como a arquitetura do produto responde. Cite funcionalidades reais, com os nomes da categoria features.

Formas especiais do Core Model:
- `problem-model`: pilha causal numerada, *1. Surface Symptom → 2. Underlying Operational Mechanism → 3. Business Consequence → 4. Emotional and Strategic Consequence*.
- `jobs-to-be-done`: 3 a 5 declarações `- **When** …, **I want to** …, **so I can** …`, mais os jobs funcionais, emocionais e sociais.
- `buying-triggers` e `switching-triggers`: Triggers and Context com subseções `### 1. Trigger Name`.
- `current-alternatives`: Core Model lista as alternativas (DIY ou interno, incumbentes, consultorias, status quo) e onde cada uma falha.
- `desired-outcomes`: resultados mensuráveis, com as métricas que a própria empresa usa.

## positioning — market-and-positioning

Seções: **Executive Summary · Strategic Definition · Audience and Frame of Reference (### Target Audience, ### Frame of Reference) · Value and Differentiation · Supporting Proof · Strategic Implications**

- **Frame of Reference**: as alternativas genéricas que o comprador considera. Cite concorrentes pelo nome **só** se as fontes o fizerem; senão descreva as classes de alternativa (como a Wonderful: wrappers de LLM, SaaS self-serve, soluções internas) e registre isso na nota da categoria competição.
- **Supporting Proof**: só fatos do ledger (clientes, métricas, rodadas, parcerias), com a grafia exata.

Formas especiais:
- `category`: Strategic Definition com três camadas numeradas, **Declared Category**, **Evaluation Category** e **Emergent/Owned Category**.
- `positioning`: Value and Differentiation com subseções `### 1. …`, uma por diferenciador.
- `market-worldview`: o "jeito antigo vs. jeito novo" e o porquê de agora.
- `value-promise`: a promessa em uma frase e como ela é cumprida.

## competition — competition-and-market-dynamics

Seções: **Executive Summary · Strategic Model · Advantage or Switching Stack · Buyer Consequences · Reinforcing Mechanisms · Risks and Limits**

- `competitive-advantage-stack`: Advantage or Switching Stack **em tabela**:
  ```markdown
  | Advantage Dimension | Description | Buyer Consequence | Uniqueness | Evidence | Score / Strength |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | **Product: Unified AI OS & Custom Apps** | ... | ... | High | Direct product pages ... | Strong |
  ```
  Dimensões típicas: Product, Service, Trust & Architecture, Distribution, Data & R&D. A coluna Evidence descreve a fonte; a coluna Score / Strength usa Exceptional, Strong, Moderate ou Weak.
- `switching-strategy`: Advantage or Switching Stack como lista numerada de neutralizadores de custo de troca.
- **Reinforcing Mechanisms**: o flywheel numerado, em que cada item alimenta o próximo.

## commercial — pricing-and-monetization

Seções: **Executive Summary · Commercial Architecture · Value and Scaling Logic · Packaging and Boundaries · Expansion Mechanics · Risks and Tradeoffs**

- O Executive Summary diz **explicitamente** se há preço público. Sem preço público, a frase é algo como "*X does not publish pricing; engagements are …*", sustentada por uma lacuna registrada no ledger.
- Preços públicos vão exatamente como publicados (moeda, período, unidade, plano).
- `value-metric`: liste as métricas candidatas e avalie cada uma. Candidatas inferidas levam `(Extrapolated)` e uma ressalva `inferred`.
- Quando a categoria inteira depende de inferência (sem preço público) ou de fontes que se contradizem (preços diferentes entre páginas), escreva `categories[].note` no manifest. Exemplo da Wonderful: *"Nenhum arquivo traz preço. A Wonderful não publica preços … As métricas de valor … são candidatas inferidas, não preço público."*

## gtm — sales-and-gtm

Seções: **Executive Summary · Motion Model · Buyer Journey and Stages · Roles and Channels · Proof and Enablement · Risks and Tradeoffs**

A Vicaura nunca gerou esta categoria (na Wonderful ela ficou pendente), então o arquétipo foi desenhado aqui no mesmo padrão dos outros.
- **Motion Model**: sales-led, product-led ou híbrido; porta de entrada (self-serve, demo, contato); sinais de tamanho de contrato.
- **Buyer Journey and Stages**: etapas numeradas e observáveis, do primeiro contato à expansão (formulário, demo, piloto, fases de deployment).
- **Roles and Channels**: papéis comerciais e de deployment (vagas são ótima evidência), parceiros, presença regional, marketplaces e eventos.
- **Proof and Enablement**: estudos de caso, alegações de ROI, trials e pilotos, certificações.

## messaging — messaging-and-brand

Seções: **Executive Summary · Core System · Patterns and Hierarchy · Representative Evidence · Usage Rules · Application Guidance**

- **Representative Evidence**: só **citações literais** entre aspas, tiradas do ledger. Nunca parafraseie aqui.
- **Usage Rules**: regras do tipo faça e não faça, com rótulo em negrito.

Formas especiais:
- `messaging-hierarchy`: Core System com seis subseções, `### 1. Category and Context`, `### 2. Primary Promise`, `### 3. Supporting Benefits`, `### 4. Differentiation`, `### 5. Proof` e `### 6. Capabilities`. Cada uma traz itens rotulados com a frase literal (*Primary Anchor*, *Core Statement*…).
- `vocabulary-lexicon`: Core System com sete grupos, `### Category Terms`, `### Owned and Branded Terms`, `### Customer Nouns`, `### Problem Terms`, `### Action Verbs`, `### Outcome Terms` e `### Avoided and Rejected Terms`, cada um com itens `- **Term:** definition`.
- `brand-narrative`: Patterns and Hierarchy com `### Narrative Pillars` (numerados) e `### Voice and Tone`.
- `customer-language`: prefira citações atribuídas a clientes. Se a linguagem vier sobretudo do texto da própria empresa, registre uma ressalva `evidence` dizendo isso. Exemplo da Wonderful: *"Construído principalmente a partir do copy de posicionamento da própria Wonderful, não de citações de clientes."*

## feature — features

Seções: **Purpose · Users and Jobs · Functional Requirements · Flows · States · Edge Cases · Data Considerations · Security and Privacy · Accessibility · Acceptance Criteria · Non-Goals**

É uma especificação de produto (PRD curto), não marketing. Escreva o que a fonte documenta e marque o resto.
- **Purpose**: 1 a 2 frases. Esse parágrafo vira o resumo no README da categoria.
- **Users and Jobs**: `- **Role**: job`.
- **Functional Requirements**: `- **FR1: Name**: description`.
- **Flows**: fluxos numerados (criação, execução, monitoramento), com `->` para sequências.
- **States**: `` - `State`: meaning ``.
- **Acceptance Criteria**: `AC-1: …`, testáveis.

A Wonderful mostra o risco desta categoria: 9 das 13 funcionalidades "leem como template genérico de spec". Quando a fonte só **menciona** a funcionalidade, a maior parte do documento é inferência. Nesse caso: confiança até 0.70, status `limited`, `(Extrapolated)` em cada requisito, estado ou caso de borda inferido, e uma ressalva `evidence`. Se isso valer para várias funcionalidades, escreva também a nota da categoria.
