# Contributing

## Workflow

1. Branch from `main`: `feat/<short-name>` or `fix/<short-name>`.
2. Make the change. Keep each `SKILL.md` under about 300 lines and move detail into `references/`.
3. Run the local checks below.
4. Open a PR using the template. CI must pass.

Don't bump `VERSION` on a feature branch.

## Local checks

```bash
# frontmatter has name, version, description with "Use when" and "NOT for"
for d in adflex-*/; do head -20 "$d/SKILL.md" | grep -q "Use when" || echo "missing Use when: $d"; done

# every references/*.md is linked from its SKILL.md
for d in adflex-*/; do for f in "$d"references/*.md; do grep -q "$(basename "$f")" "$d/SKILL.md" || echo "orphan: $f"; done; done

# setup parses, scripts compile
bash -n setup
python3 -m py_compile adflex-*/scripts/*.py
```

CI (`.github/workflows/validate-skills.yml`) runs the full set: frontmatter, version sync, marketplace listing, references, self-containment and setup.

## Adding a new skill

1. Create `adflex-<name>/SKILL.md` with frontmatter:
   ```yaml
   ---
   version: <same as VERSION>
   name: adflex-<name>
   description: |
     What it does. Use when: "trigger phrase", "trigger phrase".
     Chain with <other skill> for <what>. NOT for: <boundary> (use <skill>).
   argument-hint: "[...]"
   allowed-tools: Bash
   ---
   ```
   The description must stay under 1,024 characters.
2. Start the body with the connection step (copy it from an existing skill).
3. Add a routing table and decision rules. Put parameter detail in `references/`.
4. Add the folder to `.claude-plugin/marketplace.json` (`plugins[0].skills`), the `SKILLS` array in `setup`, and the table in `README.md`.
5. Add at least three scenarios to `evals/scenarios.md`.

## When AdFlex changes a tool

The AdFlex MCP server is the source of truth. When a tool is added, renamed, or its parameters or approval rules change:

1. Update the routing table in the owning `SKILL.md` if routing changed.
2. Update the matching `references/` file.
3. Add or adjust an eval scenario.

## Writing style

- Plain, short sentences. Tell the agent what to do, not what the tool "allows".
- Name real tools and parameters only. Never invent model IDs, voices or node types; point to the live lookup tool.
- Keep credit and posting confirmation rules intact in every skill that spends credits or posts.
