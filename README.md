# GenAI Basics

A practical introduction to Generative AI for students and developers who want to understand how modern AI systems work and start building with them.

This guide focuses on concepts you will actually use: how large language models generate text, how to prompt them well, how to ground them with your own data (RAG), how to give them tools (agents), and how to check that they work (evaluation).

## Who this is for

- Students taking a GenAI or ML course who want a clear reference alongside lectures
- Developers who can code and want to add AI features to a project
- Anyone preparing for interviews or internships that involve LLMs

You only need basic programming knowledge (any language). The code examples use Python.

## Contents

1. [Foundations: what Generative AI is and how LLMs work](docs/01-foundations.md)
2. [Prompt engineering: getting useful output reliably](docs/02-prompt-engineering.md)
3. [RAG: connecting models to your own data](docs/03-rag.md)
4. [Agents and tools: from chatbot to system](docs/04-agents-and-tools.md)
5. [Evaluation and safety: knowing whether it works](docs/05-evaluation-and-safety.md)
6. [Glossary and further resources](docs/06-glossary-and-resources.md)

Runnable examples live in [examples/](examples/).

## Suggested path

Read the chapters in order the first time. Each one builds on the previous: prompting makes more sense once you know how generation works, RAG is a prompting technique at its core, agents combine tools with prompting, and evaluation wraps around all of it.

After reading, run the examples in [examples/](examples/) and modify them. Changing a working example teaches faster than reading another chapter.
