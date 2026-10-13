---
id: cli
title: "CLI"
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

# CLI

[Wonderful](../README.md) / [Funcionalidades](README.md) · `limited` · confiança 0.70 · gerado 2026-10-03

> [!WARNING]
> **Evidência · Evidência fraca.** Esta é uma das 9 funcionalidades de plataforma com evidência limitada. O texto lê como template genérico de spec; trate a maioria das afirmações como inferência.

<!-- início do conteúdo original gerado pela Vicaura (inglês, sem edição) -->

## Purpose
Provide an implementation-ready specification for the Wonderful platform Command Line Interface (CLI), enabling users to interact with and manage platform configurations directly from their terminal.

## Users and Jobs
- **Platform Developers / Engineers**: Need to script configuration changes, automate deployments, and manage project resources without relying solely on the web dashboard.
- **DevOps / SysAdmins**: Need to integrate platform configuration checks and updates into CI/CD pipelines.

## Functional Requirements
- **Authentication & Authorization**: The CLI must support secure authentication against the Wonderful platform (e.g., via personal access tokens, OAuth device flow, or stored configuration profiles).
- **Configuration Management**: Provide subcommands to view, update, export, and import platform configurations.
- **Output Formatting**: Support multiple output formats (JSON, YAML, plain text/table) via standard flags (e.g., `--output json`).
- **Error Handling & Logging**: Return standard exit codes (0 for success, non-zero for errors) with descriptive error messages written to stderr.

## Flows
1. **Installation**: User installs the CLI binary via package manager or direct download script.
2. **Authentication**: User runs `wonderful auth login` and completes the browser or token-based authentication flow.
3. **Execution**: User executes configuration commands (e.g., `wonderful config get`, `wonderful config set`).

## States
- **Unauthenticated**: No valid token present in local config store; requires login.
- **Authenticated**: Valid session or token loaded; API requests succeed.
- **Rate Limited / Offline**: Network failures or API limits reached; CLI displays a clear warning and retries if safe.

## Edge Cases
- Expired or revoked auth tokens during a long-running command.
- Malformed configuration input files passed via flags or stdin.
- Network timeouts during large configuration payloads.

## Data Considerations
- Local configuration and credentials must be stored securely with restricted file system permissions (e.g., `~/.config/wonderful/` with 0600 permissions).
- Sensitive values (secrets, tokens) must never be printed to stdout or logs.

## Security and Privacy
- Secure transport (HTTPS/TLS) required for all communication with the Wonderful platform API.
- Clear validation of local inputs to prevent injection attacks.

## Accessibility
- Ensure high-contrast terminal output compatibility and readable typography in standard terminal emulators.

## Acceptance Criteria
- CLI successfully authenticates with the platform.
- Core CRUD operations for platform configurations are executable via terminal commands.
- Exit codes and error messages conform to standard UNIX CLI conventions.

## Non-Goals
- Replacing the primary web-based dashboard for complex visual debugging.
- Providing a graphical user interface (GUI) inside the terminal.

<!-- fim do conteúdo original -->
