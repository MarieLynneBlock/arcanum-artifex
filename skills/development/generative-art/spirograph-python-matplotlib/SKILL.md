---
name: spirograph-python-matplotlib
description: Create easy Python scripts that generate beautiful, unique spirograph-style generative art with Matplotlib, support multi-colour or gradient background and main palettes, and always save the result as a PNG. Use when the user asks for creative coding, spirographs, procedural art, or quick art scripts with tunable inputs.
metadata:
  skill-author: 'arcanum-artifex'
---

# Spirograph Python Matplotlib

## What this skill does

This skill creates beginner-friendly Python scripts for creatives to generate spirograph-inspired artwork using Matplotlib.

The scripts produced by this skill:

- Accept user inputs for geometry and style.
- Ask for both background colour and main colour inputs.
- Support multiple colours for each palette and gradient blending.
- Ensure each output is unique by combining deterministic parameters with a uniqueness mechanism.
- Always save a PNG output file.

## When to use it

Use this skill when the user asks for:

- Spirograph or hypotrochoid/epitrochoid-style art in Python.
- Generative art scripts that are easy to run and modify.
- Colourful creative outputs with gradients.
- Script-first workflows where PNG exports are required.

Do not use this skill for:

- Real-time GPU rendering pipelines.
- 3D engines or game frameworks.
- Non-Python stacks unless explicitly requested.

## Inputs the generated script should support

At minimum, the generated script should ask for:

- Geometry controls:
  - `R` (outer radius)
  - `r` (inner radius)
  - `d` (offset)
  - `points` (sampling density)
  - `rotations` (curve coverage)
- Uniqueness controls:
  - `seed` (optional deterministic repeatability)
  - `variation_strength` (small randomized perturbation)
  - `output_name` (PNG filename stem)
- Styling controls:
  - `background_colors` (one or more colours)
  - `main_colors` (one or more colours)
  - `use_gradient` (`yes`/`no`)
  - `line_width`
  - `alpha`
  - `figure_size`

Colour input can be hex (`#1f77b4`), CSS-like names (`gold`), or comma-separated lists.

## Instructions

1. Confirm objective and constraints.

- Restate that the script will be easy to run, produce unique outputs, and save PNG files every run.

2. Generate a single-file Python script first.

- Prefer one script (for example, `spirograph_art.py`) with clear sections:
  - input parsing
  - colour parsing and gradient helpers
  - curve generation
  - rendering
  - PNG export

3. Implement spirograph math with stable defaults.

- Use a parametric curve (hypotrochoid or epitrochoid) and expose `R`, `r`, `d`, `points`, and `rotations`.
- Validate numeric ranges and provide beginner-safe defaults.

4. Enforce uniqueness per output.

- If `seed` is provided, use it for deterministic uniqueness.
- If no `seed` is provided, derive one from time + entropy.
- Apply controlled perturbations (`variation_strength`) to one or more geometry or style parameters.
- Include the seed in the output filename or metadata text on-canvas.

5. Implement background and main colour systems.

- Parse single or multi-colour input lists.
- If multiple colours are supplied and gradient is enabled:
  - interpolate smoothly across the background and/or stroke colours.
- If gradient is disabled:
  - cycle or randomly choose from provided palettes in a seed-controlled way.

6. Render for visual quality.

- Use a high DPI figure.
- Hide axes and margins.
- Use anti-aliased lines.
- Centre and scale composition for balanced framing.
- Prefer dark-on-light or light-on-dark contrast checks when possible.

7. Always export PNG.

- Save output on every run with `bbox_inches='tight'` and consistent DPI.
- Confirm save path in terminal output.
- Never skip file export, even if display fails.

8. Add usage instructions.

- Provide run command and one example input set.
- Keep explanation concise and creative-focused.

## Quality checks

Before finalising, verify:

- Script runs with Python + Matplotlib only (unless user asks for extras).
- Both background and main colour prompts exist.
- Multi-colour and gradient behaviour works for both palettes.
- Two consecutive runs produce different outputs when no fixed seed is set.
- Same seed reproduces the same image.
- PNG file is always written.

## Output format

When using this skill, produce:

1. File edits:
- A runnable Python script (or minimal set of scripts) in the requested location.

2. Short run instructions:
- Dependencies and command to execute.

3. Save confirmation behaviour:
- Explain where PNGs are written and how names are generated.

4. Optional creative presets:
- Include 2-3 input presets (for example: neon bloom, monochrome etch, sunset ribbon).

## Example prompts

- "Create an easy Python spirograph script with gradient background and always save PNG."
- "Make a creative coding script for unique spirograph art; ask me for multiple background and line colours."
- "Build a Matplotlib spirograph generator with seed control and deterministic reruns."

## Ambiguities to confirm with the user

If not specified, ask these before final implementation:

- Should this be CLI prompts, command-line arguments, or both?
- Should gradients apply to background only, main lines only, or both?
- Should uniqueness rely mostly on geometry variation, colour variation, or both?
- Preferred default canvas size and DPI?

If the user does not answer, default to:

- CLI prompts
- gradient support for both background and main lines
- mixed geometry + colour variation
- `figsize=(8, 8)`, `dpi=300`
