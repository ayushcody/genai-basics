# 7. Glossary and further resources

## Glossary

- **Agent**: a system where an LLM decides which tools to call, in a loop, to reach a goal.
- **Chain-of-thought**: prompting the model to reason step by step before the final answer.
- **Chunk**: a passage of a source document, the unit of storage and retrieval in RAG.
- **Context window**: the maximum number of tokens a model can consider at once.
- **Embedding**: a vector that represents text so similar meanings have similar vectors.
- **Eval**: a repeatable test that scores model or system output.
- **Few-shot**: prompting with examples of the input-output behavior you want.
- **Fine-tuning**: additional training of a model on your examples to change its behavior.
- **Function calling / tool use**: the model returns a structured request for your code to run a function.
- **Golden dataset**: curated test inputs with known-good outputs or pass criteria.
- **Hallucination**: fluent, confident output that is wrong.
- **Hybrid search**: combining vector similarity with keyword search.
- **Inference**: running a trained model to produce output.
- **Jailbreak**: input crafted to bypass a model's safety rules.
- **Knowledge cutoff**: the end date of a model's training data.
- **LLM-as-judge**: using a model to score another model's output against a rubric.
- **Prompt injection**: instructions hidden in untrusted input that try to override your prompt.
- **RAG (Retrieval-Augmented Generation)**: retrieving relevant data into the prompt so answers are grounded.
- **Reranking**: reordering retrieved candidates with a second model for better relevance.
- **RLHF**: training on human preference rankings to make answers more helpful.
- **System prompt**: standing instructions that apply to every turn of a conversation.
- **Temperature**: sampling setting that controls output randomness.
- **Token**: the small chunk of text a model reads and writes; billing and limits are counted in tokens.
- **Top-p (nucleus sampling)**: sampling limited to the smallest token set covering probability p.
- **Vector database**: a store that indexes embeddings for fast similarity search (FAISS, pgvector, Chroma, Pinecone).
- **Zero-shot**: asking for a task with no examples.

## Further resources

### Interactive and official docs

- OpenAI API docs and cookbook: practical patterns for prompting, function calling, and evals (platform.openai.com/docs, cookbook.openai.com)
- Google AI for Developers: Gemini API quickstarts and guides (ai.google.dev)
- Anthropic docs: Claude prompting guides and tool use (docs.anthropic.com)
- Prompting Guide: community reference of prompting techniques with examples (promptingguide.ai)

### Courses

- Hugging Face NLP course: free, hands-on transformers course (huggingface.co/learn/nlp-course)
- DeepLearning.AI short courses: focused one-to-two-hour courses on RAG, agents, and evals (deeplearning.ai/short-courses)

### Foundational reading

- "Attention Is All You Need" (Vaswani et al., 2017): the transformer architecture modern LLMs are built on (arxiv.org/abs/1706.03762)
- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022): the reasoning-before-answer technique from chapter 2 (arxiv.org/abs/2201.11903)
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020): the original RAG paper behind chapter 3 (arxiv.org/abs/2005.11401)
- "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022): the think-act-observe agent loop from chapter 4 (arxiv.org/abs/2210.03629)
- "Training Language Models to Follow Instructions with Human Feedback" (Ouyang et al., 2022): instruction tuning and RLHF from chapter 1 (arxiv.org/abs/2203.02155)
- "The Curious Case of Neural Text Degeneration" (Holtzman et al., 2019): nucleus sampling (top-p) from chapter 1 (arxiv.org/abs/1904.09751)
- "BLEU" (Papineni et al., 2002, aclanthology.org/P02-1040) and "ROUGE" (Lin, 2004, aclanthology.org/W04-1013): the classic text-overlap metrics mentioned in chapter 5
- 3Blue1Brown's neural network and transformer videos: the clearest visual explanation of what is inside the model

### Tools worth knowing

- RAGAS: RAG evaluation metrics (docs.ragas.io)
- LangChain and LlamaIndex: orchestration and retrieval frameworks
- OpenAI Agents SDK and Google ADK: agent loops with tool use

Pick one resource and build something small with it. Reading about RAG teaches less than one afternoon of making retrieval fail and fixing it.
