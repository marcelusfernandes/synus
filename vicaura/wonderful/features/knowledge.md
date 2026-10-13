---
id: knowledge
title: "Knowledge"
category: features
status: limited
confidence: 0.7
generated: 2026-10-03
source: https://wonderful.ai/
generator: Vicaura
language: en
caveats:
  - kind: evidence
    title: "Evidência fraca"
    text: "Esta é uma das 9 funcionalidades de plataforma com evidência limitada. O texto lê como template genérico de spec; trate a maioria das afirmações como inferência."
  - kind: inferred
    title: "Ponto extrapolado"
    text: "A filtragem de PII durante a ingestão foi marcada pela Vicaura como extrapolada."
---

# Knowledge

[Wonderful](../README.md) / [Funcionalidades](README.md) · `limited` · confiança 0.70 · gerado 2026-10-03 · 1 ressalva

> [!WARNING]
> **Evidência · Evidência fraca.** Esta é uma das 9 funcionalidades de plataforma com evidência limitada. O texto lê como template genérico de spec; trate a maioria das afirmações como inferência.

> [!NOTE]
> **Inferido · Ponto extrapolado.** A filtragem de PII durante a ingestão foi marcada pela Vicaura como extrapolada.

<!-- início do conteúdo original gerado pela Vicaura (inglês, sem edição) -->

## Purpose
The Knowledge feature connects and manages enterprise data sources to power context-aware AI agents and workflows within the Wonderful platform.

## Users and Jobs
- **AI Engineer / Developer**: Connects enterprise databases, document repositories, and APIs to provide context to AI agents.
- **Enterprise Administrator**: Manages data source permissions, sync schedules, and compliance policies.
- **AI Agent / Workflow**: Queries the knowledge base to retrieve accurate, context-aware information at runtime.

## Functional Requirements
- **Data Source Connectors**: Support connecting various enterprise data sources (e.g., databases, file stores, APIs, SaaS tools).
- **Ingestion and Synchronization**: Provide manual and scheduled syncing of enterprise data.
- **Embedding and Indexing**: Transform ingested documents/data into vector embeddings for semantic search and retrieval.
- **Access Control**: Enforce workspace and role-based permissions on connected data sources.

## Flows
1. **Connection Flow**: Administrator selects a data source type, inputs credentials/auth tokens, and tests the connection.
2. **Sync Flow**: System triggers ingestion, processes/chunks texts, generates embeddings, and indexes them in the vector database.
3. **Query Flow**: AI agent or workflow requests context; system performs vector/hybrid search over the index and returns relevant snippets.

## States
- `Disconnected`: Data source is configured but inactive.
- `Syncing`: Data is actively being ingested, chunked, and embedded.
- `Connected / Active`: Data source is synced, indexed, and available for agent queries.
- `Error`: Sync or authentication failed; requires administrator intervention.

## Edge Cases
- Large file uploads or massive database tables timing out during initial ingestion.
- Credential revocation or expiration leading to authentication failures during sync.
- Handling unstructured data with mixed formats and encodings.

## Data Considerations
- Data must be encrypted at rest and in transit.
- Chunking strategies must respect token limits of target LLMs.
- PII filtering and masking capabilities should be supported during ingestion (extrapolated).

## Security and Privacy
- Role-Based Access Control (RBAC) restricting who can connect new data sources or view indexed contents.
- Secure token storage using encrypted secrets management.

## Accessibility
- Standard web accessibility compliance (WCAG 2.1 AA) for the Knowledge management dashboard.

## Acceptance Criteria
- Admins can successfully add, test, and remove a standard data source connector.
- System successfully syncs data, generates embeddings, and exposes them to configured AI agents.
- Clear error messages are displayed when data source authentication fails.

## Non-Goals
- Building a native general-purpose cloud storage drive.
- Providing custom ETL pipeline development tools outside of standard agentic knowledge connectors.

<!-- fim do conteúdo original -->
