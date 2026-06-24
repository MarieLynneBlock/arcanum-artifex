---
name: what-context-needed
description: 'Identify which files or folders Copilot needs to inspect before answering a user question, including required context, helpful context, and uncertainties.'
metadata:
  skill-author: 'Marie-Lynne Block'
---

# What Context Do You Need?

Before answering my question, tell me what files you need to see.

## My Question

{{question}}

Replace `{{question}}` with the user's actual question. If no question is provided, ask for it before listing required context.

## Instructions

1. Based on my question, list the files you would need to examine
2. Explain why each file is relevant
3. Note any files you've already seen in this conversation
4. Identify what you're uncertain about

## Output Format

```markdown
## Files I Need

### Must See (required for accurate answer)
- `path/to/file.ts` — [why needed]

### Should See (helpful for complete answer)
- `path/to/file.ts` — [why helpful]

### Already Have
- `path/to/file.ts` — [from earlier in conversation]

### Uncertainties
- [What I'm not sure about without seeing the code]
```

After I provide these files, I'll ask my question again.
