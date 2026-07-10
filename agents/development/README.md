# Development Agents

Custom `.agent.md` definitions for code review, refactoring, testing, and DevOps.

## Agents

| Agent | Description |
| --- | --- |
| [C++ Expert](cpp/expert-cpp-software-engineer.agent.md) | Provide expert C++ software engineering guidance using modern C++ and industry best practices. |
| [aws-cloud-expert](devops/aws-cloud-expert.agent.md) | AWS Cloud Expert provides deep, hands-on guidance for designing, building, and operating AWS workloads. |
| [DevOps Expert](devops/devops-expert.agent.md) | DevOps specialist following the infinity loop principle (Plan → Code → Build → Test → Release → Deploy → Operate → Monitor) with focus on automation, collaboration, and continuous improvement |
| [Dynatrace Expert](devops/dynatrace-expert.agent.md) | Dynatrace observability and security specialist for incident response, deployment validation, performance regression analysis, vulnerability triage, and DQL-assisted investigation. |
| [elasticsearch-agent](devops/elasticsearch-observability.agent.md) | Our expert AI assistant for debugging code (O11y), optimising vector search (RAG), and remediating security threats using live Elastic data. |
| [GitHub Actions Expert](devops/github-actions-expert.agent.md) | GitHub Actions specialist focused on secure CI/CD workflows, action pinning, OIDC authentication, permissions least privilege, and supply-chain security |
| [SE: DevOps/CI](devops/se-gitops-ci-specialist.agent.md) | DevOps specialist for CI/CD pipelines, deployment debugging, and GitOps workflows focused on making deployments boring and reliable |
| [Terraform IaC Reviewer](devops/terraform-iac-reviewer.agent.md) | Terraform-focused agent that reviews and creates safer IaC changes with emphasis on state safety, least privilege, module patterns, drift detection, and plan/apply discipline |
| [Terraform Agent](devops/terraform.agent.md) | Terraform infrastructure specialist with automated HCP Terraform workflows. Leverages Terraform MCP server for registry integration, workspace management, and run orchestration. |
| [Terratest Module Testing](devops/terratest-module-testing.agent.md) | Generate and refactor Go Terratest suites for Terraform modules, including CI-safe patterns, staged tests, and negative-path validation. |
| [C#/.NET Janitor](dotnet/csharp-dotnet-janitor.agent.md) | Perform janitorial tasks on C#/.NET code including cleanup, modernisation, and tech debt remediation. |
| [C# Expert](dotnet/csharp-expert.agent.md) | An agent designed to assist with software development tasks for .NET projects. |
| [.NET Upgrade](dotnet/dotnet-upgrade.agent.md) | Perform janitorial tasks on C#/.NET code including cleanup, modernisation, and tech debt remediation. |
| [Expert .NET software engineer mode instructions](dotnet/expert-dotnet-software-engineer.agent.md) | Provide expert .NET software engineering guidance using modern software design patterns. |
| [Ember](frontend/ember.agent.md) | An AI partner, not an assistant. Ember carries fire from person to person — helping humans discover that AI partnership isn't something you learn, it's something you find. |
| [Expert React Frontend Engineer](frontend/expert-react-frontend-engineer.agent.md) | Expert React 19.2 frontend engineer specialising in modern hooks, Server Components, Actions, TypeScript, and performance optimisation |
| [Frontend Performance Investigator](frontend/frontend-performance-investigator.agent.md) | Runtime web-performance specialist for diagnosing Core Web Vitals, Lighthouse regressions, layout shifts, long tasks, and slow network paths with Chrome DevTools MCP. |
| [SE: UX Designer](frontend/se-ux-ui-designer.agent.md) | Jobs-to-be-Done analysis, user journey mapping, and UX research artefacts for Figma and design workflows |
| [Expert Vue.js Frontend Engineer](frontend/vuejs-expert.agent.md) | Expert Vue.js frontend engineer specialising in Vue 3 Composition API, reactivity, state management, testing, and performance with TypeScript |
| [modernise-java](java/modernize-java.agent.md) | Upgrades Java projects to target versions (e.g., Java 21, Spring Boot 3.2) via incremental planning and execution. |
| [Power BI Data Modelling Expert Mode](power-platform/power-bi-data-modeling-expert.agent.md) | Expert Power BI data modelling guidance using star schema principles, relationship design, and Microsoft best practices for optimal model performance and usability. |
| [Power BI DAX Expert Mode](power-platform/power-bi-dax-expert.agent.md) | Expert Power BI DAX guidance using Microsoft best practices for performance, readability, and maintainability of DAX formulas and calculations. |
| [Power BI Performance Expert Mode](power-platform/power-bi-performance-expert.agent.md) | Expert Power BI performance optimisation guidance for troubleshooting, monitoring, and improving the performance of Power BI models, reports, and queries. |
| [Power BI Visualisation Expert Mode](power-platform/power-bi-visualization-expert.agent.md) | Expert Power BI report design and visualisation guidance using Microsoft best practices for creating effective, performant, and user-friendly reports and dashboards. |
| [Power Platform Expert](power-platform/power-platform-expert.agent.md) | Power Platform expert providing guidance on Code Apps, canvas apps, Dataverse, connectors, and Power Platform best practices |
| [Python Notebook Sample Builder](python/python-notebook-sample-builder.agent.md) | Custom agent for building Python Notebooks in VS Code that demonstrate Azure and AI features |
| [Arcanum Autonomous Executor](tooling/arcanum-autonomous-executor.agent.md) | Autonomous end-to-end execution agent for multi-step coding tasks, debugging, refactoring, validation, resume work, and practical implementation with concise progress updates. |
| [neo4j-docker-client-generator](tooling/neo4j-docker-client-generator.agent.md) | AI agent that generates simple, high-quality Python Neo4j client libraries from GitHub issues with proper best practices |
| [PySpark Expert Agent](tooling/spark-performance.agent.md) | Diagnose PySpark performance bottlenecks, distributed execution pitfalls, and suggest Spark-native rewrites and safer distributed patterns (incl. |
| [terminal-helper](tooling/terminal-helper.agent.md) | Fast terminal syntax and command helper for PowerShell and Bash |

## Deploy

Copy an `.agent.md` file into `.github/agents/` (project) or a personal agents directory (`~/.claude/agents/`, `~/.copilot/agents/`, `~/.agents/`).
