# Platforms and Operations

Use this guide to choose or troubleshoot a deployment model. These are design/preflight recipes,
not pre-approved manifests. Discover the existing platform contract before proposing infrastructure,
and obtain explicit approval for shared writes, production changes, migrations or access changes.

## Choose an Operating Model

| Context | Conservative starting point | Boundary |
| --- | --- | --- |
| Individual local work | Explicit SQLite backend, local artefacts, loopback UI/server if needed | Not a shared high-concurrency service |
| Shared self-hosted tracking | Supported SQL database and durable object storage | Authentication, permissions, operations and upgrades owned by project/platform team |
| OpenShift 4 | Existing supported platform service or restricted container deployment | Arbitrary UID, persistent state, Route/TLS and cluster policy |
| AWS self-hosted | Approved compute, SQL service and S3 with role-based access | You operate MLflow and its runtime |
| SageMaker-managed MLflow | Supported tracking-server version, AWS plugin and IAM | Managed version/feature contract, not arbitrary latest OSS behaviour |

Do not treat a tracking URI, registry URI, database URI, artefact URI and model URI as interchangeable.
Database connection strings can contain secrets and must not be printed in diagnostics or committed.

## Local Windows and WSL

The [Python examples](../examples/README.md) explicitly create local SQLite and artefact paths without
starting a service. This avoids dependence on whichever store MLflow would otherwise infer from the
working directory. Check existing stores before changing default backend behaviour during upgrades.

For a local HTTP client or R smoke test, use a new disposable working directory and an already
prepared, compatible MLflow environment. A loopback-only server pattern is:

```text
mlflow server --host 127.0.0.1 --port 5001 --backend-store-uri sqlite:///mlflow.db --artifacts-destination ./artifacts
```

This creates local state and keeps running until stopped. Choose a free port; do not terminate
another user's service. Recent MLflow versions serve/proxy artefacts by default; verify this in
`mlflow server --help` for the chosen version. Do not expose this development server remotely.

Windows and WSL have separate interpreters, virtual environments, paths and certificate stores.
Create the environment in the OS that executes the code. Use `pathlib`/URI-aware APIs for paths;
do not concatenate drive letters into a Unix file URI. Keep active SQLite databases on an appropriate
local filesystem, not a shared/network-synchronised directory or a cross-OS mount used concurrently.
For teams, use a supported shared database service instead.

Check proxy and corporate CA settings without displaying secrets. Use approved trust roots, including
`MLFLOW_TRACKING_SERVER_CERT_PATH` when appropriate; never solve TLS errors by disabling verification.
Port access from Windows to WSL/containers depends on the actual networking configuration and must
be tested separately from a successful loopback check inside that environment.

## Artefact Access Modes

| Mode | Server configuration pattern | Who needs storage access? |
| --- | --- | --- |
| Proxied | `--artifacts-destination` points to approved object storage, artefact serving enabled | Server identity; clients use authorised tracking access |
| Direct | `--no-serve-artifacts --default-artifact-root` points to approved object storage | Each uploading/downloading client needs storage identity and network access |

Do not combine these options accidentally or assume a config edit migrates old data. Experiments
retain their configured artefact location; existing runs/models may still require the old route.
Test upload and download using the intended training and inference identities. A successful metadata
write proves neither object-store access nor model readability.

Proxy users may reach objects through the server's stronger identity. Enforce tenant isolation and
least privilege at all relevant layers. Evaluate version-specific presigned/direct-transfer features
separately; do not assume they exist in older clients or managed services.

## Shared Service Controls

- Use a supported SQL database for shared metadata/registry operations, with TLS, backups, capacity,
  connection limits and an owner. Do not put a multi-replica service on a shared SQLite file.
- Configure documented authentication/authorisation for the actual server version and platform.
  MLflow capabilities evolve; neither 'no RBAC exists' nor 'RBAC is enabled by default' is a safe
  assumption. Confirm the authenticated identity and least-privilege effective permissions.
- Restrict ingress and egress. Configure trusted host/CORS settings where supported; host validation
  and CORS are not authentication. Keep production TLS and approved identity handling at the intended
  service/ingress boundary, and verify forwarded host/scheme behaviour.
- Pin and scan the runtime image and dependencies. Inject secrets through the platform's approved
  mechanism; never bake them into images, model artefacts or example configuration.
- Provide resource limits, readiness/liveness/startup checks, log redaction, retention and monitoring.
  Readiness should reflect ability to serve; aggressive liveness checks must not amplify a database outage.
- Coordinate schema migrations as a controlled step with backup/restore rehearsal and a compatibility
  plan. Do not let every replica race to perform an upgrade during startup.
- For multi-replica deployments, inspect job queues and periodic/background task coordination in
  the deployed MLflow version. HTTP load balancing alone does not prove correct shared background work.

## OpenShift 4 Preflight

Discover the cluster minor version, namespace, SCC/pod-security requirements, platform-supported
MLflow option, image registry, service identity, ingress, storage classes and database/object-store
services. OpenShift 4 is not one fixed runtime or security configuration.

| Concern | Required design/check |
| --- | --- |
| Arbitrary UID | Image starts under the namespace-assigned non-root UID; no fixed-user assumption |
| Writable paths | Only required cache/temp/runtime paths are writable; image permissions support the cluster's user/group model |
| Privilege | Unprivileged port, restricted capabilities, no broad `anyuid`/privileged exception as a workaround |
| Filesystem | Read-only root where supported, bounded temporary volumes, durable state outside ephemeral pod storage |
| Identity | Dedicated service account and narrowly scoped DB/object-store credentials or federation |
| Networking | Service/Route, TLS mode, DNS, allowed hosts, authorised ingress and necessary egress |
| State | External supported SQL database and approved durable artefacts; tested restores |
| Resources | CPU/memory requests and limits, concurrency budget, startup/readiness/liveness probes |
| Lifecycle | Immutable image, controlled migrations, graceful shutdown, rollout/rollback and monitoring |

Red Hat documents root-group permissions for required writable image directories under arbitrary
UID execution. Apply that pattern only to intended runtime directories, not sensitive system files,
and validate it under the actual cluster policy. Do not relax SCCs just to accommodate an unsuitable
image. Avoid downloading Python dependencies on pod startup; build the approved environment into
the image and provide writable cache/temp locations only where required.

Acceptance: synthetic run plus artefact round trip through the Route using a normal project identity,
unauthorised access denied, pod replacement preserves evidence, replicas behave correctly, and backup
restore/rollback are exercised in a non-production environment. YAML syntax alone is not acceptance.

## AWS: Self-Hosted Versus Managed

For self-hosting, identify the chosen compute service, region, SQL backend, S3 bucket/prefix, KMS key,
network endpoints and IAM roles. Use workload roles/federation and credential refresh rather than
long-lived keys. Separate server storage authority from experiment-writer, model-reader and operator
authority. Scope S3/KMS permissions to the required operations and objects; test both API and artefact
access, including encryption permissions and private-network routing.

For SageMaker-managed MLflow, first read the actual tracking server's version and current AWS
compatibility guidance. AWS documents the `sagemaker-mlflow` plugin, tracking-server ARN as the tracking
URI, and SigV4-authenticated requests. The client needs relevant IAM MLflow actions; S3 access and
runtime/network permissions remain separate concerns. Do not substitute an ordinary HTTP URL or
assume the same authentication configuration as self-hosted OSS MLflow.

The reference examples exercised with MLflow 3.16 are not a SageMaker compatibility guarantee. The AWS integration
page inspected for this skill documents specific client/server pairings, including 2.13.x, 2.16.x
and 3.0.x. Consult current service support in the intended region before choosing versions or APIs;
adapt and revalidate examples within the approved managed stack.

Check managed registry integration, supported flavours, tracking limits, stopped/started lifecycle,
network mode, cost and recovery constraints explicitly. A registered MLflow model is not automatically
a deployed SageMaker endpoint. Provisioning tracking servers/endpoints, changing IAM/KMS policies or
starting billable resources requires the project's approval process.

## Upgrade and Incident Checklist

1. Capture a redacted inventory of client/server/plugin/runtime versions and storage mode.
2. Reproduce with one synthetic run and one small artefact, under the failing identity.
3. Separate DNS/TLS/authentication, metadata, artefact and model-runtime failures.
4. Preserve evidence and perform upgrades/migrations in staging with validated backups first.
5. Run old-model load, old-experiment access, new-run/model write and permission regression checks.
6. Record rollback limits: a previous application image may not work against an upgraded schema.
7. Obtain approval before production rollout or irreversible cleanup.

Sources: [MLflow tracking server](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/),
[AWS integration](https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-track-experiments.html),
[AWS tracking servers](https://docs.aws.amazon.com/sagemaker/latest/dg/mlflow-create-tracking-server.html),
[OpenShift image guidance](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/images/creating-images).
The Red Hat source is version 4.18 guidance; verify the target cluster's corresponding documentation.
