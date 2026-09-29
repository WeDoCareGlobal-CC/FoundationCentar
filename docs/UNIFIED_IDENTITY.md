# Unified Identity

Google is the primary AppDeploy account identity. GitHub, ORCID and Zenodo are external OAuth connections linked to the same AppDeploy user ID.

Required backend secrets: APP_ENCRYPTION_KEY, GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, ORCID_CLIENT_ID, ORCID_CLIENT_SECRET, ZENODO_CLIENT_ID, ZENODO_CLIENT_SECRET. Optional: ZENODO_BASE_URL for sandbox and PUBLIC_APP_URL for a custom hostname.

Register these callback URLs with the corresponding provider:
https://we-do-care-global-agentic-operations-os-jn4cg7.v2.appdeploy.ai/api/oauth/github/callback
https://we-do-care-global-agentic-operations-os-jn4cg7.v2.appdeploy.ai/api/oauth/orcid/callback
https://we-do-care-global-agentic-operations-os-jn4cg7.v2.appdeploy.ai/api/oauth/zenodo/callback

OAuth access tokens are encrypted server-side before persistence. The browser receives only connection status and display metadata.
