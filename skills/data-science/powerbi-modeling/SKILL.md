---
name: powerbi-modelling
description: 'Power BI semantic modelling assistant for building optimised data models. Use when working with Power BI semantic models, creating measures, designing star schemas, configuring relationships, implementing RLS, or optimising model performance. Triggers on queries about DAX calculations, table relationships, dimension/fact table design, naming conventions, model documentation, cardinality, cross-filter direction, calculation groups, and data model best practices. Always connects to the active model first using power-bi-modelling MCP tools to understand the data structure before providing guidance.'
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Power BI Semantic Modelling

Guide users in building optimised, well-documented Power BI semantic models following Microsoft best practices.

## When to Use This Skill

Use this skill when users ask about:
- Creating or optimising Power BI semantic models
- Designing star schemas (dimension/fact tables)
- Writing DAX measures or calculated columns
- Configuring table relationships (cardinality, cross-filter)
- Implementing row-level security (RLS)
- Naming conventions for tables, columns, measures
- Adding descriptions and documentation to models
- Performance tuning and optimisation
- Calculation groups and field parameters
- Model validation and best practice checks

**Trigger phrases:** "create a measure", "add relationship", "star schema", "optimise model", "DAX formula", "RLS", "naming convention", "model documentation", "cardinality", "cross-filter"

## Prerequisites

### Required Tools
- **Power BI Modelling MCP Server**: Required for connecting to and modifying semantic models
  - Enables: connection_operations, table_operations, measure_operations, relationship_operations, etc.
  - Must be configured and running to interact with models

### Optional Dependencies
- **Microsoft Learn MCP Server**: Recommended for researching latest best practices
  - Enables: microsoft_docs_search, microsoft_docs_fetch
  - Use for complex scenarios, new features, and official documentation

## Workflow

### 1. Connect and Analyse First

Before providing any modelling guidance, always examine the current model state:

```
1. List connections: connection_operations(operation: "ListConnections")
2. If no connection, check for local instances: connection_operations(operation: "ListLocalInstances")
3. Connect to the model (Desktop or Fabric)
4. Get model overview: model_operations(operation: "Get")
5. List tables: table_operations(operation: "List")
6. List relationships: relationship_operations(operation: "List")
7. List measures: measure_operations(operation: "List")
```

### 2. Evaluate Model Health

After connecting, assess the model against best practices:

- **Star Schema**: Are tables properly classified as dimension or fact?
- **Relationships**: Correct cardinality? Minimal bidirectional filters?
- **Naming**: Human-readable, consistent naming conventions?
- **Documentation**: Do tables, columns, measures have descriptions?
- **Measures**: Explicit measures for key calculations?
- **Hidden Fields**: Are technical columns hidden from report view?

### 3. Provide Targeted Guidance

Based on analysis, guide improvements using references:
- Star schema design: See [star-schema.md](references/star-schema.md)
- Relationship configuration: See [relationships.md](references/relationships.md)
- DAX measures and naming: See [measures-dax.md](references/measures-dax.md)
- Performance optimisation: See [performance.md](references/performance.md)
- Row-level security: See [rls.md](references/rls.md)

## Quick Reference: Model Quality Checklist

| Area | Best Practice |
|------|--------------|
| Tables | Clear dimension vs fact classification |
| Naming | Human-readable: `Customer Name` not `CUST_NM` |
| Descriptions | All tables, columns, measures documented |
| Measures | Explicit DAX measures for business metrics |
| Relationships | One-to-many from dimension to fact |
| Cross-filter | Single direction unless specifically needed |
| Hidden fields | Hide technical keys, IDs from report view |
| Date table | Dedicated marked date table |

## MCP Tools Reference

Use these Power BI Modelling MCP operations:

| Operation Category | Key Operations |
|-------------------|----------------|
| `connection_operations` | Connect, ListConnections, ListLocalInstances, ConnectFabric |
| `model_operations` | Get, GetStats, ExportTMDL |
| `table_operations` | List, Get, Create, Update, GetSchema |
| `column_operations` | List, Get, Create, Update (descriptions, hidden, format) |
| `measure_operations` | List, Get, Create, Update, Move |
| `relationship_operations` | List, Get, Create, Update, Activate, Deactivate |
| `dax_query_operations` | Execute, Validate |
| `calculation_group_operations` | List, Create, Update |
| `security_role_operations` | List, Create, Update, GetEffectivePermissions |

## Common Tasks

### Add Measure with Description
```
measure_operations(
  operation: "Create",
  definitions: [{
    name: "Total Sales",
    tableName: "Sales",
    expression: "SUM(Sales[Amount])",
    formatString: "$#,##0",
    description: "Sum of all sales amounts"
  }]
)
```

### Update Column Description
```
column_operations(
  operation: "Update",
  definitions: [{
    tableName: "Customer",
    name: "CustomerKey",
    description: "Unique identifier for customer dimension",
    isHidden: true
  }]
)
```

### Create Relationship
```
relationship_operations(
  operation: "Create",
  definitions: [{
    fromTable: "Sales",
    fromColumn: "CustomerKey",
    toTable: "Customer",
    toColumn: "CustomerKey",
    crossFilteringBehavior: "OneDirection"
  }]
)
```

## When to Use Microsoft Learn MCP

Research current best practices using `microsoft_docs_search` for:
- Latest DAX function documentation
- New Power BI features and capabilities
- Complex modelling scenarios (SCD Type 2, many-to-many)
- Performance optimisation techniques
- Security implementation patterns
