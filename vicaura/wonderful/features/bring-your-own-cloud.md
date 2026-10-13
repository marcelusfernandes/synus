---
id: bring-your-own-cloud
title: "Bring Your Own Cloud"
category: features
status: limited
confidence: 0.8
generated: 2026-10-03
source: https://wonderful.ai/
generator: Vicaura
language: en
caveats:
  - kind: inferred
    title: "Ponto extrapolado"
    text: "A nota sobre bundle offline foi marcada como extrapolada."
---

# Bring Your Own Cloud

[Wonderful](../README.md) / [Funcionalidades](README.md) · `limited` · confiança 0.80 · gerado 2026-10-03 · 1 ressalva

> [!NOTE]
> **Inferido · Ponto extrapolado.** A nota sobre bundle offline foi marcada como extrapolada.

<!-- início do conteúdo original gerado pela Vicaura (inglês, sem edição) -->

## Purpose
The Bring Your Own Cloud (BYOC) feature allows organizations to host and run AI implementations directly within their own cloud infrastructure. This ensures data remains strictly inside the organization's perimeter, providing full authority over security controls, governance policies, and upgrade timing.

## Users and Jobs
- **Cloud / Security Architects:** Need to enforce data residency, network boundaries, and access control policies while deploying managed AI pipelines.
- **Platform Engineers:** Need to provision, monitor, and maintain cluster resources and underlying cloud primitives.
- **IT / Compliance Officers:** Need verifiable proof that data does not leave corporate perimeters and that updates can be deferred or scheduled based on audit requirements.

## Functional Requirements
- **FR1:** The system shall provide infrastructure-as-code (IaC) modules or deployment scripts (e.g., Terraform, Helm charts) to orchestrate components within the customer's cloud account (AWS, GCP, or Azure).
- **FR2:** The system shall establish secure, outbound-only telemetry and control plane connections back to the management plane without exposing inbound ports to external entities.
- **FR3:** The system shall allow administrators to review, approve, and defer software version updates and patches to match internal change management windows.
- **FR4:** The system shall enforce data locality constraints, ensuring all inference payloads, vector stores, and cached logs reside exclusively within the customer-provisioned storage buckets and databases.

## Flows
1. **Provisioning Flow:**
   - Administrator generates a deployment token and cloud permissions manifest from the central management console.
   - Administrator runs the provided IaC templates within their private cloud environment.
   - Cloud resources initialize, establish an outbound heartbeat, and register the private cluster with the management plane.
2. **Upgrade Management Flow:**
   - Management plane flags an available update and surfaces release notes.
   - Administrator selects a target cluster, inspects pre-flight checks, and triggers an update manually or sets a maintenance window.

## States
- **Disconnected / Unhealthy:** The private cloud instance has lost its outbound heartbeat or telemetry channel.
- **Provisioning:** Resources are being created and initialized within the customer cloud account.
- **Active / Healthy:** All services are operational, data stays local, and the control plane is synchronized.
- **Update Pending:** A new software version is available but held pending administrator authorization.

## Edge Cases
- **Outbound Proxy / Firewall Blocks:** If corporate firewalls drop the outbound control plane socket, the local AI runtime must continue serving traffic locally while logging connection errors.
- **Partial Cloud Outage:** If a dependent cloud service (e.g., KMS or IAM) fails, the cluster must fail safe without leaking unencrypted data or credentials.

## Data Considerations
- **Data Residency:** All customer data, user inputs, outputs, and embeddings must be stored in customer-owned cloud storage buckets and databases.
- **Encryption:** Data at rest must be encrypted using customer-managed keys (CMK via KMS). Data in transit must use TLS 1.3.

## Security and Privacy
- Zero inbound public access requirements; all control channels must be initiated outbound.
- Strict separation between the vendor control plane (metadata/telemetry only) and the customer data plane (payloads and model execution).

## Accessibility
- The management dashboard used to monitor BYOC instances must comply with WCAG 2.1 AA standards for keyboard navigation, color contrast, and screen reader compatibility.

## Acceptance Criteria
- AC1: Deployment templates successfully spin up isolated clusters in a clean cloud account without requiring inbound firewall rules.
- AC2: Verification testing confirms zero data egress to external endpoints during normal inference operations.
- AC3: Administrators can successfully defer an available software upgrade past its release date without service disruption.

## Non-Goals
- Managing native cloud provider IAM users or billing relationships directly on behalf of the customer.
- Providing fully air-gapped (completely offline) updates without any internet connectivity unless bundled via a designated offline bundle mechanism (extrapolated requirement for future iterations).

<!-- fim do conteúdo original -->
