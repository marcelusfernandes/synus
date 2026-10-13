---
id: single-tenant-deployment
title: "Single Tenant Deployment"
category: features
status: sufficient
confidence: 0.9
generated: 2026-10-03
source: https://wonderful.ai/
generator: Vicaura
language: en
caveats: []
---

# Single Tenant Deployment

[Wonderful](../README.md) / [Funcionalidades](README.md) · `sufficient` · confiança 0.90 · gerado 2026-10-03

<!-- início do conteúdo original gerado pela Vicaura (inglês, sem edição) -->

## Purpose
Provide enterprise customers with fully isolated, dedicated infrastructure instances for deploying workloads. This ensures strict data residency, security boundaries, custom configurations, and automated maintenance channels.

## Users and Jobs
- **Enterprise DevOps Engineers**: Provision, monitor, and manage isolated infrastructure instances without sharing compute or storage nodes with other tenants.
- **Security & Compliance Officers**: Verify strict tenant isolation, audit automated update schedules, and enforce custom security configurations.

## Functional Requirements
- **FR1: Dedicated Infrastructure Provisioning**: The system must provision fully isolated compute, memory, and storage resources per tenant upon request.
- **FR2: Custom Configuration Management**: The system must allow tenant-specific parameter overrides (e.g., environment variables, resource limits, network policies).
- **FR3: Automated Updates**: The system must support scheduled or continuous automatic updates for base images and runtime dependencies without manual tenant intervention.
- **FR4: Tenant Isolation**: Network and storage layers must be logically or physically segregated to ensure zero cross-tenant data leakage.

## Flows
1. **Provisioning Flow**:
   - User selects Single Tenant Deployment tier.
   - User inputs custom configuration parameters.
   - System provisions dedicated control plane and worker nodes.
   - System runs health checks and reports deployment readiness.
2. **Update Flow**:
   - System schedules maintenance window or triggers rolling updates.
   - System applies patches/updates to isolated infrastructure.
   - System validates instance health post-update and reports status.

## States
- `Provisioning`: Infrastructure is being allocated and configured.
- `Active`: Tenant workloads are running in a healthy state.
- `Updating`: Automatic updates are being applied to the dedicated infrastructure.
- `Degraded`: Infrastructure is experiencing resource or health issues.
- `Terminated`: Dedicated infrastructure and associated volumes have been wiped.

## Edge Cases
- **Resource Exhaustion**: If cloud provider capacity is unavailable during provisioning, queue the request and alert platform operators.
- **Update Failure**: If an automatic update fails health checks, automatically roll back to the last stable snapshot and notify the tenant.

## Data Considerations
- **Residency**: Data must reside within the specified geographic region matching the tenant's compliance requirements.
- **Encryption**: Data at rest must be encrypted using dedicated tenant encryption keys (BYOK/Customer Managed Keys).
- **Retention**: Upon termination, all tenant persistent volumes must undergo secure zero-fill wipe protocols.

## Security and Privacy
- Complete separation of compute, network (VPC/VNet isolation), and database layers per tenant.
- Access to the single tenant control plane must be protected via role-based access control (RBAC) and mandatory multi-factor authentication (MFA).

## Accessibility
- Administrative dashboard for managing single-tenant deployments must comply with WCAG 2.1 AA standards, ensuring full keyboard navigation and high contrast support.

## Acceptance Criteria
- AC1: Provisioning successfully spins up infrastructure with zero shared compute/storage nodes.
- AC2: Custom configuration parameters are correctly applied and persisted across restarts.
- AC3: Automatic updates apply cleanly during scheduled windows with zero manual intervention.
- AC4: Rollback mechanism activates successfully if a post-update health check fails.

## Non-Goals
- Multi-tenant shared cluster resource pooling is out of scope for this feature.
- Manual customer-driven patching of underlying hypervisors is excluded; updates are fully automated.

<!-- fim do conteúdo original -->
