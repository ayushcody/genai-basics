# 1. Foundations: what Generative AI is and how LLMs work

## Generative vs. predictive models

Traditional machine learning models mostly *predict*: they take an input and return a label, a number, or a score. Spam filters, recommenders, and fraud detectors work this way.

Generative models *produce* new content: text, images, audio, video, or code. A large language model (LLM) is a generative model trained on text. Products like ChatGPT, Gemini, and Claude are applications built on LLMs (the GPT, Gemini, and Claude model families); Llama, Mistral, and Gemma are open-weight model families you can run yourself.

The key shift: one generative model can do many tasks (summarize, translate, write code, answer questions) without being trained separately for each one. You steer it with instructions instead of retraining it.

## How an LLM generates text

A text-generating LLM is autoregressive: given some text, it predicts the next token, and everything else comes from repeating that step.

1. Your input is split into **tokens**, small chunks of text. In English, one token is roughly 4 characters or three quarters of a word. "Unbelievable" might be three tokens.
2. The model assigns a probability to every possible next token.
3. One token is sampled from those probabilities and appended.
4. The new text becomes the input, and the loop repeats until the model produces a stop token or hits a limit.

That is the whole mechanism. There is no database lookup and no fact store inside the model. This explains both the power and the main weakness of LLMs: they produce *plausible* text, and plausible text is not guaranteed to be true. A wrong answer stated fluently is a **hallucination**.

## Tokens, context windows, and cost

- **Token limits.** Every model has a **context window**: the maximum number of tokens it can consider at once (your input plus its output). Modern models range from thousands to over a million tokens.
- **Pricing.** APIs charge per token, usually with different rates for input and output. Long prompts and long answers both cost money.
- **Truncation.** If a conversation exceeds the context window, the oldest content must be dropped, summarized, or retrieved on demand (see the RAG chapter).

## Temperature and sampling

When the model picks the next token, it does not have to pick the most likely one. **Temperature** controls how adventurous the sampling is:

- Low temperature (close to 0): sampling concentrates on the most likely tokens, so output tends to be more predictable. It does not make answers more factual, and exact repeatability is not guaranteed.
- High temperature (close to 1 or above): flatter probabilities, more variety and surprise.

Not every model accepts a temperature setting; check the model's docs before relying on it. Related settings like **top-p** (nucleus sampling) restrict sampling to the smallest set of tokens whose combined probability reaches p. In practice, avoid tuning temperature and top-p at the same time.

## What the model knows

An LLM's training happens in stages:

1. **Pretraining.** Next-token prediction over a huge text corpus. This is where language ability and general knowledge come from. It is also where the **knowledge cutoff** comes from: the model cannot be relied on for events after its training data ends, even if later fine-tuning added scattered newer facts.
2. **Instruction tuning / fine-tuning.** Extra training on instruction-and-answer examples so the model follows requests instead of just continuing text.
3. **Preference tuning (e.g. RLHF).** Training on human preference rankings so answers are more helpful and safer.

Consequences to remember:

- The model does not know today's date, your files, or your company data unless you put that information in the prompt.
- **Fine-tuning** (extra training on your examples) changes style and behavior. It is a slow, expensive way to add facts; RAG is usually the better tool for facts.

## Embeddings: text as numbers

An **embedding** is a vector (a list of numbers) that represents a piece of text. Texts with similar meaning get similar vectors, so you can measure semantic similarity with simple math (cosine similarity) instead of keyword matching.

Embeddings power:

- Semantic search ("find documents about X" even when they use different words)
- Retrieval for RAG (chapter 3)
- Clustering, deduplication, and recommendation

Embedding models are separate from generation models: you send text in, you get a vector out, and you store vectors in a vector database.

## Key terms

| Term | Meaning |
| --- | --- |
| Token | Small chunk of text the model reads and writes |
| Context window | Maximum tokens the model can consider at once |
| Temperature | Controls randomness of token sampling |
| Hallucination | Fluent, confident, wrong output |
| Knowledge cutoff | End date of the model's training data |
| Fine-tuning | Extra training on your examples to change behavior |
| Embedding | Vector representation of text for similarity |
| Inference | Running the model to get output (as opposed to training) |

## Common mistakes

- Treating the model as a search engine that knows current facts. It does not; give it the facts or use RAG.
- Assuming a confident tone means correctness. Confidence is style, not evidence.
- Ignoring token limits until long documents silently truncate.
