# SYNC

Existing deployment:
https://we-do-care-global-agentic-operations-os-jn4cg7.v2.appdeploy.ai/

This version retains the existing repository and public release metadata configuration. It verifies public GitHub/Zenodo/ORCID metadata and stores sync-run records.

The existing public UI does not expose an authoritative state API for agents, budgets, workflows or learning history. Therefore no destructive two-way merge is claimed. For full migration, export JSON/CSV from the source system and import it through a dedicated authenticated migration endpoint, preserving source IDs and creating an audit record.

Do not scrape and invent private state from the public UI.
