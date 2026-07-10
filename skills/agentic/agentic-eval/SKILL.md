---
name: agentic-eval
description: >
    Use when designing and implementing evaluation loops for AI agents, including reflection, evaluator-optimiser patterns, rubric scoring, LLM-as-judge review, test-driven refinement, convergence checks, and iteration logging.
metadata:
  skill-author: 'Marie-Lynne Block'
---

# Agentic Evaluation Patterns

Patterns for self-improvement through iterative evaluation and refinement.

## Overview

Evaluation patterns enable agents to assess and improve their own outputs, moving beyond single-shot generation to iterative refinement loops.

```
Generate → Evaluate → Critique → Refine → Output
    ↑                              │
    └──────────────────────────────┘
```

## When to Use

- **Quality-critical generation**: Code, reports, analysis requiring high accuracy
- **Tasks with clear evaluation criteria**: Defined success metrics exist
- **Content requiring specific standards**: Style guides, compliance, formatting
- **Iterative improvement workflows**: Drafts, plans, prompts, or code need critique and refinement before delivery

## Do Not Use This Skill For

- Formal compliance claims, certification, or audit sign-off without approved organisational evidence
- Production monitoring design, runtime governance, access control, or policy enforcement
- Broad statistical evaluation methodology, benchmark design, or model selection studies
- Security, privacy, or safety review where evaluation loops are not the central concern

---

## Expected Outputs

When applying this skill, produce the assets needed to run and inspect an evaluation loop:

- evaluation criteria or rubric
- generator, evaluator, and optimiser responsibilities
- iteration limit and convergence policy
- structured evaluator output format
- failure handling for malformed evaluations or non-improving outputs
- logging fields for debugging and review
- final recommendation or refined output with evaluation history summary

Treat code blocks in this skill as adaptable Python-style skeletons. Replace `llm`, `run_tests`, model settings, and logging functions with project-specific implementations.

## Evaluation History Schema

Log enough detail to explain why the loop stopped and which candidate was selected:

```json
{
    "iteration": 1,
    "candidate_id": "draft-1",
    "overall_score": 0.82,
    "dimension_scores": {"accuracy": 0.8, "clarity": 0.9},
    "feedback": ["Add evidence for the risk rating."],
    "parse_status": "valid",
    "improvement_delta": 0.07,
    "stopping_reason": null
}
```

Use `parse_status` values such as `valid`, `retry_valid`, or `failed_closed`. Final summaries should include the best candidate, the stopping reason, and any evaluator uncertainty or human-review escalation.

## Pattern 1: Basic Reflection

Agent evaluates and improves its own output through self-critique.

```python
import json


def parse_evaluation(raw_response: str, schema_prompt: str) -> dict:
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        retry = llm(f"Return only valid JSON for this schema: {schema_prompt}\nResponse: {raw_response}")
        try:
            return json.loads(retry)
        except json.JSONDecodeError as exc:
            raise ValueError({"parse_status": "failed_closed", "raw_response": raw_response}) from exc


def reflect_and_refine(task: str, criteria: list[str], max_iterations: int = 3) -> str:
    """Generate with reflection loop."""
    output = llm(f"Complete this task:\n{task}")
    schema_prompt = '{"criterion": {"status": "PASS|FAIL", "feedback": "..."}}'
    
    for i in range(max_iterations):
        # Self-critique
        critique = llm(f"""
        Evaluate this output against criteria: {criteria}
        Output: {output}
        Rate each: PASS/FAIL with feedback as JSON.
        """)
        
        critique_data = parse_evaluation(critique, schema_prompt)
        all_pass = all(c["status"] == "PASS" for c in critique_data.values())
        if all_pass:
            return output
        
        # Refine based on critique
        failed = {k: v["feedback"] for k, v in critique_data.items() if v["status"] == "FAIL"}
        output = llm(f"Improve to address: {failed}\nOriginal: {output}")
    
    return output
```

**Key insight**: Use structured JSON output for reliable parsing of critique results, and handle parsing failures as evaluation failures rather than silently accepting the draft.

---

## Pattern 2: Evaluator-Optimizer

Separate generation and evaluation into distinct components for clearer responsibilities.

```python
import json


class EvaluatorOptimizer:
    def __init__(self, score_threshold: float = 0.8):
        self.score_threshold = score_threshold
    
    def generate(self, task: str) -> str:
        return llm(f"Complete: {task}")

    def parse_evaluation(self, raw_response: str) -> dict:
        schema_prompt = '{"overall_score": 0.0, "dimensions": {"accuracy": 0.0, "clarity": 0.0}, "evidence": []}'
        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            retry = llm(f"Return only valid JSON for this schema: {schema_prompt}\nResponse: {raw_response}")
            try:
                return json.loads(retry)
            except json.JSONDecodeError as exc:
                raise ValueError({"parse_status": "failed_closed", "raw_response": raw_response}) from exc
    
    def evaluate(self, output: str, task: str) -> dict:
        raw_evaluation = llm(f"""
        Evaluate output for task: {task}
        Output: {output}
        Return JSON: {{"overall_score": 0-1, "dimensions": {{"accuracy": ..., "clarity": ...}}, "evidence": [...]}}
        """)
        return self.parse_evaluation(raw_evaluation)
    
    def optimize(self, output: str, feedback: dict) -> str:
        return llm(f"Improve based on feedback: {feedback}\nOutput: {output}")
    
    def run(self, task: str, max_iterations: int = 3) -> str:
        output = self.generate(task)
        previous_score = 0.0
        for _ in range(max_iterations):
            evaluation = self.evaluate(output, task)
            current_score = evaluation["overall_score"]
            if current_score >= self.score_threshold:
                break
            if current_score <= previous_score:
                break
            previous_score = current_score
            output = self.optimize(output, evaluation)
        return output
```

---

## Pattern 3: Code-Specific Reflection

Test-driven refinement loop for code generation.

```python
class CodeReflector:
    def reflect_and_fix(self, spec: str, max_iterations: int = 3) -> str:
        code = llm(f"Write Python code for: {spec}")
        tests = llm(f"Generate pytest tests for: {spec}\nCode: {code}")
        
        for _ in range(max_iterations):
            result = run_tests(code, tests)
            if result["success"]:
                return code
            code = llm(f"Fix error: {result['error']}\nCode: {code}")
        return code
```

---

## Evaluator Reliability

Evaluation loops are only useful when the evaluator is harder to fool than the generator. For high-risk or quality-critical work:

- Anchor the evaluator with a concrete rubric and examples of passing and failing outputs.
- Ask for evidence, failure reasons, and uncertainty, not just a score.
- Randomise or blind comparison order when comparing alternatives to reduce position bias.
- Repeat judging or use multiple evaluators when scores are close or the decision is consequential.
- Escalate to human review when evaluator outputs conflict, confidence is low, or policy-sensitive content is involved.
- Track whether scores improve over iterations; stop when improvement stalls to avoid overfitting to the evaluator.

---

## Evaluation Strategies

### Outcome-Based
Evaluate whether output achieves the expected result.

```python
def evaluate_outcome(task: str, output: str, expected: str) -> str:
    return llm(f"Does output achieve expected outcome? Task: {task}, Expected: {expected}, Output: {output}")
```

### LLM-as-Judge
Use LLM to compare and rank outputs.

```python
def llm_judge(output_a: str, output_b: str, criteria: str) -> str:
    return llm(f"Compare outputs A and B for {criteria}. Which is better and why?")
```

### Rubric-Based
Score outputs against weighted dimensions.

```python
RUBRIC = {
    "accuracy": {"weight": 0.4},
    "clarity": {"weight": 0.3},
    "completeness": {"weight": 0.3}
}

def evaluate_with_rubric(output: str, rubric: dict) -> float:
    raw_scores = llm(f"Rate 1-5 for each dimension as JSON: {list(rubric.keys())}\nOutput: {output}")
    try:
        scores = json.loads(raw_scores)
    except json.JSONDecodeError:
        retry = llm(f"Return only valid JSON scores for: {list(rubric.keys())}\nResponse: {raw_scores}")
        scores = json.loads(retry)
    return sum(scores[d] * rubric[d]["weight"] for d in rubric) / 5
```

---

## Best Practices

| Practice | Rationale |
|----------|-----------|
| **Clear criteria** | Define specific, measurable evaluation criteria upfront |
| **Iteration limits** | Set max iterations (3-5) to prevent infinite loops |
| **Convergence check** | Stop if output score isn't improving between iterations |
| **Log history** | Keep full trajectory for debugging and analysis |
| **Structured output** | Use JSON for reliable parsing of evaluation results |
| **Evaluator calibration** | Use examples, rubrics, and evidence requirements to reduce judge drift |
| **Human escalation** | Route low-confidence or high-impact decisions to a reviewer |

---

## Failure Handling

Plan for evaluation failures before running the loop:

- If evaluator JSON is malformed, retry once with the schema and then fail closed with the raw response logged.
- If the evaluator gives no evidence, treat the score as unreliable and request evidence before refining.
- If output quality stops improving, return the best-scored candidate and include the stopping reason.
- If evaluation criteria conflict, pause and ask for priority order rather than optimising against incompatible goals.
- If generated tests or checks are themselves suspect, review or regenerate the tests before trusting the score.

---

## Quick Start Checklist

```markdown
## Evaluation Implementation Checklist

### Setup
- [ ] Define evaluation criteria/rubric
- [ ] Set score threshold for "good enough"
- [ ] Configure max iterations (default: 3)

### Implementation
- [ ] Implement generate() function
- [ ] Implement evaluate() function with structured output
- [ ] Implement optimize() function
- [ ] Wire up the refinement loop

### Safety
- [ ] Add convergence detection
- [ ] Log all iterations for debugging
- [ ] Handle evaluation parse failures gracefully
- [ ] Escalate low-confidence or high-impact decisions to human review
```
