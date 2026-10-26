# Capabilities

Capabilities are what the product must be able to do. They are extracted from user stories and journeys.

## Identity and access
- Identity verification (establish who is making a request)
- Authorization (decide what actions are allowed)
- Default-deny when identity or permissions are unclear

## Connections and safety
- Register a data source connection
- Store connection details securely
- Validate connection usability before it can be used

## Data exposure policy
- Require explicit selection of what data is exposed
- Ensure unselected data is not exposed
- Make exposure decisions reviewable over time

## API definition and lifecycle
- Define endpoints tied to data sources
- Define accepted inputs and returned outputs
- Test endpoints prior to publishing
- Publish and evolve APIs without unexpected breakage

## Observability and governance
- Record access attempts and outcomes
- Provide operational controls that prevent abuse
- Make failure modes visible and recoverable

Reference: `prd/03_capabilities.md` and `architecture/01_domain_map.md`.
