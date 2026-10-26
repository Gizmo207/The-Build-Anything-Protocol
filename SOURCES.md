# Primary public guidance

Peter's SOP uses these practices; it does not reproduce unpublished company procedures, promise defect-free software, or certify compliance. Sources checked 2026-10-26.

| Source | Used for |
| --- | --- |
| [NIST SSDF v1.1, SP 800-218 (2022)](https://csrc.nist.gov/pubs/sp/800/218/final) | Security requirements, verification criteria, release integrity and response |
| [OWASP Authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | Default deny, least privilege, permission checks, authorization tests |
| [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | Secret lifecycle and exposure reduction |
| [OWASP SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | Outbound target validation where integrations fetch user-supplied locations |
| [Google SRE Workbook: Canarying Releases](https://sre.google/workbook/canarying-releases/) | Limited staged exposure and rollout evaluation when justified |
| [W3C accessibility evaluation](https://www.w3.org/WAI/test-evaluate/) and [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Selecting criteria and evaluating user-facing interfaces |

The pin defines this protocol's requirements; citations are a rationale, not claims that every small artifact needs enterprise infrastructure.
