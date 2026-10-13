---
id: on-premise-air-gapped-deployment
title: "On-Premise Air-Gapped Deployment"
category: features
status: limited
confidence: 0.85
generated: 2026-10-03
source: https://wonderful.ai/
generator: Vicaura
language: en
caveats: []
---

# On-Premise Air-Gapped Deployment

[Wonderful](../README.md) / [Funcionalidades](README.md) · `limited` · confiança 0.85 · gerado 2026-10-03

<!-- início do conteúdo original gerado pela Vicaura (inglês, sem edição) -->

## Purpose
Enable high-security organizations to run the product completely isolated from the public internet with zero external dependencies, ensuring absolute data privacy and compliance with strict government, defense, or enterprise security mandates.

## Users and Jobs
- **System Administrators / DevOps Engineers**: Need to deploy, monitor, and maintain the software stack inside an isolated, air-gapped data center without outbound network calls.
- **Security Officers**: Need to audit deployment packages, verify zero outbound telemetry or dependency fetching, and ensure cryptographic integrity of all internal components.

## Functional Requirements
- **Offline Packaging**: All container images, binaries, static assets, database dependencies, and documentation must be bundled into a single self-contained transport artifact (e.g., OCI-compliant tarball or Helm chart with bundled charts).
- **Zero External Telemetry**: The application runtime must have all telemetry, crash reporting, license verification checks, and automatic update checkers completely disabled or routed to an internal stub/sink.
- **Local Certificate and Key Management**: Support custom internal Certificate Authorities (CAs) and self-signed certificates without falling back to public Public Key Infrastructure (PKI) issuers.
- **Local Dependency Resolution**: All third-party libraries, runtime modules, and packaged services must reside locally within the deployment boundaries (e.g., embedded databases, local caching layers).

## Flows
1. **Transfer Phase**: Admin downloads the deployment artifact via an authorized out-of-band physical media transfer (e.g., encrypted USB drive, data diode) into the air-gapped network.
2. **Validation Phase**: Admin runs a verification script provided with the package to check cryptographic checksums and digital signatures against a trusted root key.
3. **Deployment Phase**: Admin executes the installation script or applies the local Kubernetes manifests / Helm charts to the isolated cluster.
4. **Verification Phase**: Runtime performs self-checks to ensure zero sockets are opened to external IP addresses and local storage/database connections are healthy.

## States
- `UNINITIALIZED`: Artifact transferred, but not yet unpacked or validated.
- `VALIDATING`: Cryptographic verification and dependency check in progress.
- `DEPLOYING`: Infrastructure resources, databases, and application containers initializing locally.
- `RUNNING_AIR_GAPPED`: Normal operational state with explicit network isolation enforcement.
- `DEGRADED_ISOLATION`: Detected an unexpected attempt to make an external network connection or missing local dependency.

## Edge Cases
- **Time Synchronization**: Air-gapped environments lacking public NTP sources; must support local NTP servers or operate without strict public time sync while handling token/certificate expiration gracefully.
- **License Renewal**: Manual license key generation and upload mechanism via admin UI or CLI, as automatic cloud-based license re-validation is impossible.
- **Log and Backup Export**: Log shipping and backup mechanisms must support local file rotation or secure manual extraction via physical export rather than cloud buckets (S3/GCS).

## Data Considerations
- All application state, user data, audit logs, and search indexes must persist strictly within local storage volumes provided by the host infrastructure.
- Zero persistent data leakage or caching to external cloud providers.

## Security and Privacy
- Enforce strict network egress blocking at the container/orchestrator level (e.g., Kubernetes NetworkPolicies denying all external traffic).
- Mandatory SHA-256 or better cryptographic signing for all container images and update packages.
- Secrets management must rely on local vaults (e.g., HashiCorp Vault, Kubernetes Secrets) rather than cloud-managed key services (AWS KMS, GCP KMS).

## Accessibility
- Admin CLI tools must provide clear, high-contrast, screen-reader-compatible terminal outputs.
- Admin UI web panels must meet WCAG 2.1 AA standards for operators managing the deployment locally.

## Acceptance Criteria
- Complete successful installation on a test cluster with zero network routes to the public internet.
- Zero external network requests initiated by the application during a standard 24-hour operation cycle (verified via packet capture / eBPF monitoring).
- Successful execution of manual offline license updates.
- Cryptographic verification script successfully rejects tampered or unsigned deployment artifacts.

## Non-Goals
- Automatic over-the-air updates or patch management.
- Cloud-assisted diagnostics or remote support tunneling without manual customer intervention.

<!-- fim do conteúdo original -->
