"""Offline tests for the examples: all logic except the live API call.

Uses mocked API responses, so no key, no network, no cost:

    python test_examples.py
"""

import os
import runpy
import sys
from unittest.mock import MagicMock, patch

os.environ.setdefault("OPENAI_API_KEY", "test-dummy-key")
os.environ.setdefault("OPENAI_MODEL", "test-model")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np


def fake_embedding(text):
    """Deterministic stand-in embedding: one axis per topic."""
    if "library is open" in text or "weekends" in text:
        return [1.0, 0.0, 0.0]
    if "borrow up to 5" in text:
        return [0.0, 1.0, 0.0]
    return [0.0, 0.0, 1.0]


def fake_embed_create(model, input):
    resp = MagicMock()
    resp.data = [MagicMock(embedding=fake_embedding(t)) for t in input]
    return resp


fake_client = MagicMock()
fake_client.embeddings.create.side_effect = fake_embed_create

with patch("openai.OpenAI", return_value=fake_client):
    import simple_rag


def test_chunking():
    long_text = "\n\n".join(["a" * 100] * 4)
    parts = simple_rag.chunk(long_text, max_chars=150)
    assert len(parts) == 4, parts
    assert all(len(p) <= 150 for p in parts), parts
    joined = "\n\n".join(parts)
    assert joined == long_text  # nothing lost or reordered
    assert simple_rag.chunk("b" * 300, max_chars=150) == ["b" * 300]
    assert simple_rag.chunk("") == []


def test_cosine_similarity():
    a = np.array([[1.0, 0.0]])
    b = np.array([[1.0, 0.0], [0.0, 1.0]])
    sims = simple_rag.cosine_similarity(a, b)[0]
    assert abs(sims[0] - 1.0) < 1e-6 and abs(sims[1]) < 1e-6, sims


def test_retrieve_orders_by_relevance():
    chunks = simple_rag.retrieve("When is the library open on weekends?")
    assert chunks[0].startswith("The library is open"), chunks


def test_answer_builds_grounded_prompt():
    fake_resp = MagicMock()
    fake_resp.choices = [MagicMock(message=MagicMock(content="fake answer"))]
    fake_client.chat.completions.create.return_value = fake_resp

    out = simple_rag.answer("When is the library open on weekends?")
    call = fake_client.chat.completions.create.call_args
    messages = call.kwargs["messages"]
    assert "temperature" not in call.kwargs
    assert "<chunk>" in messages[0]["content"]
    assert "The library is open" in messages[0]["content"]
    assert messages[1]["content"] == "When is the library open on weekends?"
    assert out == "fake answer"


def test_basic_chat_runs_without_temperature():
    with patch("openai.OpenAI", return_value=fake_client):
        runpy.run_path(os.path.join(os.path.dirname(__file__), "basic_chat.py"))
    assert "temperature" not in fake_client.chat.completions.create.call_args.kwargs


if __name__ == "__main__":
    test_basic_chat_runs_without_temperature()
    test_chunking()
    test_cosine_similarity()
    test_retrieve_orders_by_relevance()
    test_answer_builds_grounded_prompt()
    print("ALL TESTS PASSED")
