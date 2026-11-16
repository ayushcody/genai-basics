# 4. Agents and tools: from chatbot to system

## From answering to doing

A chatbot answers. An **agent** acts: it can call tools, look things up, write to systems, and chain several steps toward a goal. "Book the cheapest flight tomorrow morning and add it to my calendar" needs search, comparison, a booking action, and a calendar write. No single prompt does that; a loop does.

## The agent loop

The core pattern is a cycle:

1. **Think**: the model decides what to do next, given the goal and what it knows.
2. **Act**: it calls a tool (search, database, API, calculator, email).
3. **Observe**: the tool result comes back into the context.
4. Repeat until the goal is done or the model gives up.

This is often called the ReAct pattern (reason + act). The model never executes anything itself; your code runs the tools and feeds results back.

## Function calling

Modern APIs support **function calling** (tool use): you describe available functions with names, descriptions, and JSON schemas for their arguments. The model replies with a structured request like `{"name": "search_flights", "arguments": {"date": "2026-11-17"}}` instead of free text. Your code validates and executes it, then returns the result.

Write tool descriptions the way you would write API docs for a new teammate: what it does, when to use it, what each argument means, and what it returns. When tool use misbehaves, vague descriptions are one of the first things to check.

## What makes agents fail

- **Ambiguous stopping**: without a clear definition of "done", agents loop or stop early.
- **Tool errors swallowed**: if a tool fails and the agent is not told clearly, it hallucinates success.
- **Compounding errors**: each step is mostly right, and ten steps later the result is wrong. Validate intermediate state, not just the final output.
- **Too many tools**: twenty overlapping tools confuse selection. Start with a few well-described ones.

## Guardrails are not optional

An agent can take real actions, so scope its power:

- Give each tool the minimum access it needs (read-only where possible).
- Validate every argument the model produces against your own rules, not just the JSON schema.
- Require human approval for irreversible or expensive actions: payments, deletions, sending messages.
- Log every tool call with inputs and outputs so you can replay and debug runs. Redact secrets and personal data and restrict access to the logs, because tool payloads can carry sensitive data.
- Set hard limits: maximum steps, maximum cost, timeouts.

## Multi-agent setups

Complex systems sometimes split work across specialized agents (a planner, a researcher, a writer, a reviewer) that pass results between them. This can help when one context window or one role gets overloaded, but it adds coordination overhead and new failure modes. Start with one agent and a few tools; add agents only when a single loop clearly cannot carry the task.

## Frameworks

You can write the loop yourself in a hundred lines, and doing so once is the best way to understand it. Frameworks add structure when you need it: LangChain and LlamaIndex for orchestration and retrieval, the OpenAI Agents SDK and Google's Agent Development Kit (ADK) for tool-calling agent loops. Judge any framework by whether you can still see and control the underlying loop.
