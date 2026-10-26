# Profile selector

Apply [the core](../CORE.md) every time. Select all relevant profiles and risk modules in the record, each as applicable or not applicable with a reason. Unknown needs investigation. These additions share the core's version and cannot relax protections.

| Platform/workload | Select when |
| --- | --- |
| [web](web.md) | Browser interface/interactive content |
| [mobile](mobile.md) | Installed mobile app/device integration |
| [backend](backend.md) | APIs, persistence, services, workers |
| [automation](automation.md) | CLI, scripts, jobs, infrastructure/configuration |
| [artifact](artifact.md) | Documents, libraries, static sites, games, simulations, other local output |

| Risk module | Select when |
| --- | --- |
| [identity](risk-modules.md#identity-and-authorization) | Authentication, authorization, ownership/tenant boundaries |
| [data](risk-modules.md#data-and-privacy) | Durable/sensitive data or consequential mutation |
| [payments](risk-modules.md#payments-and-value) | Payments, billing, credits, valuable transfers |
| [integration](risk-modules.md#external-integrations) | External dependencies, network calls, third-party side effects |
| [operations](risk-modules.md#operations) | Deployed/shared service or automated production operation |

Combine as needed; artifact is not a fallback that excludes backend risks. Document novel domain risks in the project record; add a new profile only when it offers distinct reusable value. Regulated or physical-safety work also needs qualified domain review and applicable requirements; this generic SOP is insufficient alone.
