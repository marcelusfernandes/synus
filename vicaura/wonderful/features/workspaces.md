---
id: workspaces
title: "Workspaces"
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

# Workspaces

[Wonderful](../README.md) / [Funcionalidades](README.md) · `limited` · confiança 0.70 · gerado 2026-10-03

> [!WARNING]
> **Evidência · Evidência fraca.** Esta é uma das 9 funcionalidades de plataforma com evidência limitada. O texto lê como template genérico de spec; trate a maioria das afirmações como inferência.

<!-- início do conteúdo original gerado pela Vicaura (inglês, sem edição) -->

## Purpose
Enable users to organize projects, users, and operational resources into dedicated, isolated boundaries called Workspaces.

## Users and Jobs
- **Workspace Administrators**: Create and configure workspaces, assign users, and manage operational resources.
- **Team Members**: Collaborate within assigned workspaces across shared projects and resources.

## Functional Requirements
- **FR1**: System shall support the creation of isolated workspaces identified by a unique ID and a display name.
- **FR2**: System shall allow administrators to associate projects and operational resources with a specific workspace.
- **FR3**: System shall provide user membership management within each workspace.

## Flows
1. **Creation Flow**: User navigates to platform settings -> clicks 'Create Workspace' -> provides name and configuration -> system provisions the workspace.
2. **Association Flow**: User selects a project or resource -> assigns it to a target workspace.

## States
- **Active**: Workspace is fully provisioned and accessible to members.
- **Archived**: Workspace is read-only, hidden from standard active navigation.

## Edge Cases
- Deleting a workspace containing active projects requires explicit cascading confirmation or re-assignment of assets.

## Data Considerations
- All projects, user memberships, and operational resources must contain a foreign key reference to their parent workspace ID.

## Security and Privacy
- Access control lists (ACLs) must restrict workspace resources to members explicitly assigned to that workspace.

## Accessibility
- Workspace navigation menus and management modals must meet WCAG 2.1 AA standards.

## Acceptance Criteria
- AC1: An authorized user can successfully create a new workspace.
- AC2: Projects and users can be bound to a workspace.
- AC3: Users outside a workspace cannot access its resources.

## Non-Goals
- Cross-workspace resource sharing without explicit federation is out of scope.

<!-- fim do conteúdo original -->
