# GitHub Copilot — Getting Started for Analysts

You have been granted access to GitHub Copilot. This guide is for data analysts, business analysts, and BI developers. No software development background required.

---

## Step 1 — Install the extension

Go to your IDE's setup guide:

- [VS Code](../setup/vscode.md) — recommended for Python, R, notebooks
- [IntelliJ IDEA](../setup/intellij.md)
- [PyCharm](../setup/pycharm.md) — recommended if you write Python

**Done when:** you see the Copilot icon in the status bar without a strikethrough.

---

## Step 2 — What Copilot can do for you

As an analyst, Copilot is most useful for:

| Task | How |
| --- | --- |
| Writing SQL queries | Describe what you need in a comment, Copilot writes the query |
| Explaining SQL you didn't write | Select the query → `/explain` in chat |
| Python / R data transformations | Describe the transformation, Copilot suggests the code |
| Writing regex patterns | Describe the pattern in plain language |
| Explaining error messages | Paste the error into chat and ask what it means |
| Generating test / sample data | Ask Copilot to generate rows matching a schema |
| Writing formulas | Describe the formula logic, Copilot writes it |
| Documenting your analysis | Ask Copilot to summarise what a notebook or script does |

---

## Step 3 — Your first SQL query

Open a `.sql` file or a notebook SQL cell. Write a comment describing what you want:

```sql
-- monthly revenue per product category for the last 12 months
-- grouped by category, sorted by revenue descending
-- tables: orders (order_date, product_id, amount), products (product_id, category)
```

Wait 1–2 seconds. A grey suggestion appears. Press `Tab` to accept, `Esc` to dismiss.

**Tip:** the more you tell Copilot about your table names and columns, the better the query.

---

## Step 4 — Try Copilot Chat

Open the chat panel (shortcut in the [cheat sheet](../resources/cheat-sheet.md)).

Try these:

1. Paste a SQL query → ask `explain this query step by step`
2. Paste an error message → ask `what does this error mean and how do I fix it?`
3. Describe a transformation → `write a pandas function that pivots this table from long to wide format`
4. Ask for a regex → `write a regex that matches a Belgian IBAN number`

---

## Step 5 — Read the privacy quick card

Before using Copilot with real data: [privacy-quick-card.md](../resources/privacy-quick-card.md)

Key rules:
- Never paste real customer names, emails, or IDs into chat.
- Never paste credentials or connection strings.
- Use anonymised or synthetic data when asking Copilot for help.

---

## Week 1 goals

- [ ] Generated at least one SQL query with Copilot
- [ ] Used `/explain` on a query or script you didn't write
- [ ] Asked Copilot to explain an error message
- [ ] Read the [privacy quick card](../resources/privacy-quick-card.md)

---

## Resources

| Resource | Link |
| --- | --- |
| Prompt library | [prompt-library.md](../resources/prompt-library.md) |
| Cheat sheet | [cheat-sheet.md](../resources/cheat-sheet.md) |
| Privacy quick card | [privacy-quick-card.md](../resources/privacy-quick-card.md) |
| FAQ | [faq.md](../resources/faq.md) |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |
