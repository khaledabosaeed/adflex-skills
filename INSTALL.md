# Install AdFlex Skills

Two pieces are needed:

1. **The AdFlex MCP connector**: `https://api.adflex.ai/api/mcp` (HTTP, OAuth sign-in with your AdFlex account).
2. **The skills**: the `adflex-*` folders in this repo.

## Option 1: `npx skills` (recommended)

```bash
npx skills add adflex-ai/skills
```

Then add the connector for your agent (see "Connector by agent" below).

## Option 2: `gh skill install`

GitHub CLI v2.90+:

```bash
gh skill install adflex-ai/skills                 # all skills
gh skill install adflex-ai/skills adflex-generate # one skill
```

Each skill folder is self-contained, so you can install only the ones you need.

## Option 3: Claude Code marketplace

```
/plugin marketplace add adflex-ai/skills
/plugin install adflex@adflex
```

The plugin includes the connector. Run `/mcp`, pick `adflex`, and sign in.

## Option 4: Setup script

```bash
git clone --depth 1 https://github.com/adflex-ai/skills.git adflex-skills
cd adflex-skills
./setup                 # auto-detects Claude Code, Cursor or Codex
./setup --host codex    # or force a host
./setup --skip-mcp      # only link the skills
```

It links each skill into your agent's skills folder and registers the connector. Safe to run again.

## Option 5: Manual

Copy or symlink the `adflex-*` folders into your agent's skills directory:

| Agent | Skills directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |
| Codex | `~/.agents/skills/` |

## Connector by agent

| Agent | Command |
|---|---|
| Claude Code | `claude mcp add --transport http --scope user adflex https://api.adflex.ai/api/mcp`, then `/mcp` to sign in |
| Codex | `codex mcp add adflex --url https://api.adflex.ai/api/mcp`, then `codex mcp login adflex` |
| Cursor | Add `{"mcpServers": {"adflex": {"url": "https://api.adflex.ai/api/mcp"}}}` to `~/.cursor/mcp.json`, then sign in from Settings → MCP |
| claude.ai / ChatGPT | Add a custom connector with the URL above |

## Check it works

Ask your agent: "List my AdFlex businesses." It should call `list_businesses` and show your brands. If it says there are no AdFlex tools, the connector isn't loaded; if it gets an auth error, sign in again.
