# Verification (09)

Plan checks before implementation and execute them against the exact candidate. Trace requirements and invariants/risks to IDs, commands/manual procedures, environment/tool versions, UTC time, exit outcome, retained output/digest and subject revision.

Test pure rules, real boundary enforcement and relevant I/O/contracts; include denied/invalid, interrupted/repeated, partial failure/recovery and representative critical journeys. Use performance/query/resource budgets and manual accessibility checks when relevant. No universal coverage percentage is imposed.

Record passed, failed, blocked and not run distinctly. Mocks do not prove integration, syntax does not prove interaction, and the checker does not establish truth. Missing dependencies/access block affected claims. Rerun affected checks after candidate changes. See [tool limits](../tools/README.md) and [tested examples](../examples/reference/README.md).
