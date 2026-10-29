# Step 2 — Wrap It as a Single MCP Tool — Solution

> [Back to the step](../READING_README.md#step-2-wrap-it-as-a-single-mcp-tool) · [Hint 1](step2_mcp_wrapper_hints.md#hint-1) · [Hint 2](step2_mcp_wrapper_hints.md#hint-2)

**Story:** the whole pipeline, exposed as one `deep_research(topic) -> str` tool. The tool's body is just "run the pipeline, return the summary" — the thinnest possible MCP layer. **If not:** putting logic in the tool body (timeouts, formatting) mixes the MCP layer's job with the pipeline's, the mistake this project warns about.

## `mcp_server.py` (new, at the repo root)

**Story:** a `MCPServer` with exactly one tool. The tool builds the model and the config once (module level), then each call runs the pipeline and returns the final summary. **If not:** rebuilding the model and config on every call would be slow and noisy.

```python
# mcp_server.py  (Step 2 version — the thinnest wrapper)
# Exposes the whole Researcher/Fact-Checker pipeline as ONE MCP tool. The
# tool body just runs the pipeline and returns the summary. Logging goes to
# stderr (src/utils/logger.py); nothing prints to stdout -- stdout is the
# MCP protocol channel. Run it with:  mcp dev mcp_server.py
import sys

from mcp.server.mcpserver import MCPServer

from src.config import load_config
from src.models.llm import get_model
from src.pipeline import run_pipeline
from src.utils.logger import get_logger

CONFIG = load_config()
logger = get_logger(__name__)

mcp = MCPServer("deep-research-service")

@mcp.tool()
def deep_research(topic):
    """Research a topic through a fact-checked, multi-round pipeline and
    return a verified summary. One call runs a Researcher and a Fact-Checker
    until the summary is approved or a round cap is reached."""
    logger.info(f"deep_research: {topic}")
    result = run_pipeline(get_model(CONFIG), topic, CONFIG.max_revision_rounds)
    return result.final_summary

if __name__ == "__main__":
    print("deep-research service starting", file=sys.stderr)
    mcp.run(transport="stdio")
```

## Trying it

With the MCP Inspector:

```bash
mcp dev mcp_server.py
```

Then call `deep_research` with `topic = "Retrieval-Augmented Generation (RAG)"`. You get back the plain final summary — the fact-checked one, after the loop ran — with **no trace yet**. A caller sees a single clean answer and has no idea a two-agent revision loop produced it. That's the whole "agent-as-a-service" idea working.

## What's deliberately *not* here yet

- **No trace.** The caller waits on a multi-round call with zero feedback, then gets only the final string. That's a bad experience for a slow tool — Step 3 fixes it by returning a revision trace alongside the summary.
- **No timeout.** A slow or broken run hangs the caller indefinitely — Step 4 adds a timeout and a partial fallback.

Resist adding either now. Keeping Step 2 a two-line tool body proves the wrapping itself is trivial; all the interesting *design* is deciding what a slow, multi-step process should look like from the outside, which is Steps 3 and 4.

**Tests for this step:** the integration test (Step 4's file) confirms a real `deep_research` call returns a non-empty summary — proof the pipeline runs correctly through the MCP layer.
