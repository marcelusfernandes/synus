---
id: evals
title: "Evals"
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
---

# Evals

[Wonderful](../README.md) / [Funcionalidades](README.md) · `limited` · confiança 0.70 · gerado 2026-10-03

> [!WARNING]
> **Evidência · Evidência fraca.** Esta é uma das 9 funcionalidades de plataforma com evidência limitada. O texto lê como template genérico de spec; trate a maioria das afirmações como inferência.

<!-- início do conteúdo original gerado pela Vicaura (inglês, sem edição) -->

## Purpose
The Evals feature provides continuous evaluation of AI model outputs and performance in production to ensure accuracy, reliability, and governance compliance (particularly targeting regulated domains like banking).

## Users and Jobs
- **AI Engineer / Developer**: Wants to automatically test and grade model outputs against reference datasets or programmatic assertions to catch regressions before or during production deployment.
- **Risk / Compliance Officer**: Wants continuous assurance and audit trails proving that model outputs remain accurate, safe, and aligned with governance policies.

## Functional Requirements
- **Evaluation Pipeline Execution**: Support scheduled and event-driven execution of evaluations against recorded or live AI model outputs.
- **Scoring and Assertions**: Allow definition of custom evaluation metrics (e.g., accuracy, toxicity, hallucination detection, format compliance) returning standardized scores.
- **Dashboard & Reporting**: Expose historical trends, aggregate score metrics, and drill-down views into individual evaluation runs and payload traces.
- **Alerting Integration**: Trigger notifications (e.g., webhook, email, PagerDuty) when evaluation metrics fall below configured thresholds.

## Flows
1. **Setup Evaluation**: User defines a test dataset, selects target model endpoints, and associates evaluation metrics/graders.
2. **Run Execution**: The system executes evaluations asynchronously, processing traces or batch inputs against the specified metrics.
3. **Review & Triage**: User views results on the Evals dashboard, filters by failing scores, and inspects underlying inputs and outputs.

## States
- **Idle**: No active evaluation runs scheduled.
- **Running**: Evaluation suite is actively processing records.
- **Completed**: All metrics successfully computed and logged.
- **Failed**: Execution error encountered during data retrieval or metric computation.

## Edge Cases
- **Rate Limiting / Timeout**: Upstream model providers throttling evaluation calls; implement backoff and retry logic with graceful degradation.
- **Empty Dataset**: Handling runs triggered with zero records without crashing the runner.

## Data Considerations
- Store evaluation definitions, metric configurations, time-series run results, and individual trace scores.
- Retain historical evaluation data in accordance with configurable retention policies for auditability.

## Security and Privacy
- Encrypt evaluation payloads and prompts both at rest and in transit.
- Ensure role-based access control (RBAC) restricts viewing and modifying evaluation pipelines to authorized personnel.

## Accessibility
- Ensure dashboard tables, filter controls, and configuration modals adhere to WCAG 2.1 AA contrast and keyboard navigation standards.

## Acceptance Criteria
- Users can create, configure, and manually trigger an evaluation suite.
- Evaluation runs produce visible aggregate scores and detailed log traces.
- Alerts fire successfully when metric scores drop below a user-defined threshold.

## Non-Goals
- Providing out-of-the-box domain-specific financial models (this feature evaluates models, it does not host them).
- Manual human-in-the-loop annotation labeling workflows (focus is automated continuous evaluation, though extensible interface may support it in future iterations).

<!-- fim do conteúdo original -->
