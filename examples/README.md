# Examples

Small, runnable scripts that demonstrate the concepts from the guide. No frameworks, so every step is visible.

## Setup

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
export OPENAI_MODEL="a-current-chat-model"  # see platform.openai.com/docs/models
```

The scripts use the OpenAI Python client. You can point them at an OpenAI-compatible endpoint by setting `OPENAI_BASE_URL`, but the endpoint must serve your chosen chat model, and `simple_rag.py` also needs the `text-embedding-3-small` embedding model there (or edit the model name in `embed()`).

## Scripts

| Script | Shows | Chapter |
| --- | --- | --- |
| `basic_chat.py` | A minimal API call: messages and token usage | 1, 2 |
| `simple_rag.py` | The full RAG pipeline (chunk, embed, retrieve, answer) with no vector DB | 3 |
| `test_examples.py` | Offline tests for the RAG logic, using mocked API responses (run `python test_examples.py`) | 5 |

Run them, then break them: drop the context instruction, remove a chunk. Watching a working example fail teaches more than a second reading.

## Verification status

The scripts require API credentials and an OPENAI_MODEL value to make live calls; without them they stop before any API request. They intentionally do not hardcode a chat model, because model availability changes over time. The non-network logic (chunking, retrieval ordering, similarity math, prompt construction, request shapes) is covered by `test_examples.py`, which runs offline against the `openai` Python SDK v3.51 with mocked API responses. Live API calls themselves were not executed while preparing this repo.

Neither script sends a temperature parameter. If you experiment with it, first check whether your chosen model supports it. Endpoint compatibility also depends on support for Chat Completions and the message roles used here.
