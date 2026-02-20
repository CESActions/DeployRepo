# DeployRepo (Reusable Apigee CI/CD Workflows)

Reusable GitHub Actions for **Apigee** CI/CD with:
- **apigeelint** gate
- **Python** import+deploy via Apigee Management API
- **Google Secret Manager** (OIDC/WIF)
- **Maven** `apigee-config-maven-plugin`
- **Slack & Microsoft Teams notifications** (always run at job end)

## Required secrets/vars
- `WIF_PROVIDER`, `WIF_SA` (OIDC/WIF to GCP)
- `SLACK_BOT_TOKEN` (xoxb- token), `SLACK_CHANNEL_ID` (e.g. C12345)
- `MS_TEAMS_WEBHOOK_URL` (Teams Incoming Webhook or Teams Workflow Webhook)
- Repo variable: `APIGEE_ORG`
