# Code Reviewer Learning

A learning plugin for ChatGPT and Codex that demonstrates a repeatable code-review workflow and three read-only MCP tools. The bundled server returns deterministic mock pull-request data; it does not connect to GitHub or modify repositories.

## Requirements

- Windows with Python 3.10 or newer available through the `py` launcher
- Codex CLI or the ChatGPT desktop app with plugin support

Install the MCP dependency:

```powershell
py -m pip install -r plugins/code-reviewer/server-python/requirements.txt
```

## Install from GitHub

Add this repository as a marketplace:

```powershell
codex plugin marketplace add Rishabh2561/code-reviewer-learning
```

Then enter `/plugins`, choose **Code Reviewer Learning**, and install **Code Reviewer**. Start a new session after installation.

## Try it

```text
Use the code-reviewer plugin to review pull request 42 in acme/demo. Fetch the pull-request metadata first, then inspect the changed files. Report findings by severity with file references and recommended fixes.
```

The mock changes intentionally include SQL injection, unsafe audit logging, and sequential database calls for the reviewer to identify.

## Test the MCP server

```powershell
py plugins/code-reviewer/server-python/test_client.py
```

## Repository layout

- `.agents/plugins/marketplace.json` defines the Git-backed marketplace.
- `plugins/code-reviewer/.codex-plugin/plugin.json` defines the plugin.
- `plugins/code-reviewer/skills/review-code/SKILL.md` defines the review workflow.
- `plugins/code-reviewer/server-python/server.py` provides deterministic read-only MCP tools.

## License

MIT
