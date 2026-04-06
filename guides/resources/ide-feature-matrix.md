# GitHub Copilot — IDE Feature Matrix

Canonical feature availability matrix for this repository.

Use this page as the single source of truth. Setup guides and the cheat sheet should link here instead of duplicating the table.

---

## Legend

- **Yes**: Supported and generally available
- **Basic**: Supported with notable limitations
- **Partial**: Supported inconsistently; verify by version
- **No**: Not supported

---

## Feature availability by IDE

| Feature | VS Code | IntelliJ IDEA | PyCharm | Visual Studio 2022 | Eclipse |
| --- | --- | --- | --- | --- | --- |
| Inline completions | Yes | Yes | Yes | Yes | Yes |
| Copilot Chat | Yes | Yes | Yes | Yes | Yes |
| `.github/copilot-instructions.md` | Yes | Yes | Yes | Yes | Partial |
| Prompt files (`.prompt.md`) | Yes | No | No | No | No |
| Agent mode | Yes | Yes | Yes | Yes | Yes |
| MCP servers | Yes | Yes | Yes | Yes | Yes |
| Next Edit Suggestions | Yes | No | No | Yes | Yes |
| `@workspace` | Yes | No | No | No | No |
| Copilot Extensions (`@docker`, `@azure`) | Yes | No | No | No | No |

---

## Notes

- Validated against official docs on 2026-04-06.
- Visual Studio agent mode and MCP require Visual Studio 17.14+.
- Eclipse agent mode and MCP require Eclipse 2024-09+ and latest GitHub Copilot extension.
- Prompt files in this repository remain VS Code-only because they use `.prompt.md` workflow documented in VS Code customization docs.
- `@workspace` and Copilot extension participants (`@docker`, `@azure`) remain VS Code-specific features in this lab's documentation scope.
- If a feature is marked **Partial**, add version-specific notes in the relevant setup guide.

## Official sources

- GitHub: Copilot features
	https://docs.github.com/en/copilot/get-started/features
- GitHub: Chat in IDE (tool-specific pages)
	https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide?tool=vscode
	https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide?tool=jetbrains
	https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide?tool=visualstudio
	https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide?tool=eclipse
- GitHub: Extend Copilot Chat with MCP (tool-specific pages)
	https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp?tool=vscode
	https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp?tool=jetbrains
	https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp?tool=visualstudio
	https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp?tool=eclipse
- GitHub: IDE code suggestions (tool-specific pages)
	https://docs.github.com/en/copilot/how-tos/get-code-suggestions/get-ide-code-suggestions?tool=vscode
	https://docs.github.com/en/copilot/how-tos/get-code-suggestions/get-ide-code-suggestions?tool=jetbrains
	https://docs.github.com/en/copilot/how-tos/get-code-suggestions/get-ide-code-suggestions?tool=eclipse
- VS Code docs: customization, prompt files, MCP servers
	https://code.visualstudio.com/docs/copilot/customization/overview
	https://code.visualstudio.com/docs/copilot/customization/prompt-files
	https://code.visualstudio.com/docs/copilot/customization/mcp-servers