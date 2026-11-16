# Install AdFlex Skills (agent runbook)

You are an AI agent installing AdFlex skills for the user. Follow these steps in order. Stop and ask the user only where a step says so.

## 1. Detect the host

- Claude Code: `~/.claude/` exists, or you are running inside Claude Code.
- Cursor: `~/.cursor/` exists.
- Codex: `~/.codex/` exists.

If none match, ask the user which agent they use.

## 2. Get the skills

```bash
git clone --depth 1 https://github.com/adflex-ai/skills.git ~/.adflex-skills 2>/dev/null \
  || git -C ~/.adflex-skills pull --ff-only
```

## 3. Run setup

```bash
~/.adflex-skills/setup --host <claude|cursor|codex>
```

This links all eleven skills (`adflex-generate`, `adflex-product-photo`, `adflex-talking-ad`, `adflex-carousel`, `adflex-video-remix`, `adflex-video-edit`, `adflex-workflows`, `adflex-documents`, `adflex-brand`, `adflex-social-publish` and `adflex-reels`) into the host's skills folder and registers the AdFlex MCP connector. It is idempotent.

If it warns that a skill path already exists and isn't a link, tell the user and don't overwrite it.

## 4. Sign in (needs the user)

The connector uses OAuth. Ask the user to sign in:

- Claude Code: run `/mcp`, select `adflex`, and sign in.
- Codex: `codex mcp login adflex`.
- Cursor: Settings → MCP → adflex → sign in.

Wait for the user to confirm.

## 5. Verify

Call `list_businesses`. Success means the connector works. Report the business names to the user.

- No AdFlex tools available: the host needs a restart to load the new MCP server. Ask the user to restart the agent.
- Auth error: repeat step 4.

## 6. Tell the user what they can do

One short message listing the eleven skills and two example requests, for example "Make a 9:16 product ad" and "Schedule this post for Friday 6pm".

Don't generate anything or spend credits during installation.
