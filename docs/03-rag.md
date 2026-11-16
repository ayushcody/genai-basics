# 3. RAG: connecting models to your own data

## The problem RAG solves

An LLM only knows its training data. It does not know your company wiki, your college notes, or last week's policy update, and it will confidently invent answers about them. Retraining is slow and expensive.

**Retrieval-Augmented Generation (RAG)** fixes this at inference time: find the relevant pieces of your data, put them into the prompt, and ask the model to answer from them. The model stays the same; you change what it sees.

## The pipeline

```
Documents -> chunk -> embed -> store in vector DB
Question  -> embed -> search vector DB -> top-k chunks
Chunks + question -> prompt -> LLM -> grounded answer
```

1. **Ingest.** Collect source documents (PDFs, web pages, notes, tickets).
2. **Chunk.** Split them into passages small enough to embed and quote, typically a few hundred tokens, often with some overlap so ideas are not cut in half.
3. **Embed.** Run each chunk through an embedding model to get a vector.
4. **Store.** Save vectors plus the original text and metadata (source, page, date) in a vector database: FAISS or pgvector for libraries you run yourself, Chroma (open source: run it locally, self-host it, or use its cloud service), or managed services like Pinecone and Weaviate Cloud.
5. **Retrieve.** Embed the user's question and find the top-k most similar chunks.
6. **Augment.** Insert the chunks into the prompt with an instruction like "Answer using only the context below."
7. **Generate.** The model writes an answer grounded in the retrieved text.

## Chunking matters more than you think

Retrieval quality is mostly decided before the question is ever asked.

- Too large: chunks dilute the relevant sentence with noise and waste context.
- Too small: chunks lose the surrounding meaning and retrieve out of context.
- Structure-aware splitting (by heading, section, or paragraph) beats splitting every N characters.
- Keep metadata with every chunk so answers can cite sources and stale documents can be filtered out.

## Retrieval quality knobs

- **Top-k**: how many chunks to retrieve. More chunks give coverage but add noise and cost. Start with 3 to 5.
- **Hybrid search**: combine vector similarity with keyword (BM25) search; vectors miss exact terms like part numbers and names.
- **Reranking**: after an initial retrieval, a second model reorders the candidates by relevance. Cheap accuracy gain.
- **Query rewriting**: rephrase the user's question into a better search query before embedding it, especially for follow-up questions that refer to earlier conversation.

## Failure modes

- **Nothing relevant retrieved**: the model either hallucinates or should say "I do not know." Instruct it explicitly to admit missing context.
- **Wrong chunks retrieved**: embedding similarity is not relevance. Check retrieval separately from generation (see chapter 5).
- **Context stuffing**: dumping 20 chunks into the prompt buries the answer. Retrieve less, rerank, and trim.
- **Stale data**: retrieval happily returns outdated documents. Track document dates and re-embed on changes.

## RAG vs. fine-tuning

| Goal | Better tool |
| --- | --- |
| Add or update facts and knowledge | RAG |
| Give access to private or current data | RAG |
| Change style, tone, or output format | Fine-tuning |
| Teach a specialized vocabulary or task pattern | Fine-tuning |
| Cite sources in answers | RAG |

Many production systems use both: fine-tune for behavior, RAG for knowledge.

## Try it

[examples/simple_rag.py](../examples/simple_rag.py) implements this whole pipeline in about 60 lines with no vector database, so you can see every step.
