# Java GitHub Actions Demo

A deliberately vulnerable Java Spring application, used to demonstrate
NightVision scans from CI. It contains real security flaws on purpose.
Run it only on your own machine or in a throwaway CI runner, and never
expose it to the internet.

## Run it locally

You need Docker with Compose.

```shell
docker compose up -d
```

The application listens on https://localhost:9000 with a self-signed
certificate. Sign in with the username `user` and the password
`password`. Stop it with `docker compose down`.

## Scan it with NightVision

Start with the [quickstart](https://docs.nightviz.ai/get-started/quickstart/)
to install the CLI and log in. Then pick the CI system you use. Each guide
walks through creating the application in NightVision, recording the login,
adding an API token as a secret, and running the scan.

| CI system | Pipeline file in this repository | Guide |
| --- | --- | --- |
| GitHub Actions | `.github/workflows/nightvision.yml` | [GitHub Actions](https://docs.nightviz.ai/integrations/github-actions/) |
| GitLab CI/CD | `.gitlab-ci.yml` | [GitLab](https://docs.nightviz.ai/integrations/gitlab/) |
| Azure Pipelines | `azure-pipelines.yml` | [Azure DevOps](https://docs.nightviz.ai/integrations/azure-devops/) |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` | [Bitbucket](https://docs.nightviz.ai/integrations/bitbucket/) |
| Jenkins | `Jenkinsfile` | [Jenkins](https://docs.nightviz.ai/integrations/jenkins/) |

Every pipeline file here is the one its guide shows. Before the first
run, replace `my-project` with the name of your NightVision project and
add your API token as the `NIGHTVISION_TOKEN` secret (a credential named
`nightvision-token` in Jenkins).

To try the CLI by hand against the running application:

```shell
nightvision login
nightvision target create javaspringvulny-api https://localhost:9000 --type API
nightvision auth playwright create javaspringvulny-api https://localhost:9000
nightvision openapi extract . --target javaspringvulny-api --lang java
nightvision scan javaspringvulny-api --auth javaspringvulny-api
```
