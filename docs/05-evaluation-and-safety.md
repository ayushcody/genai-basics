# 5. Evaluation and safety: knowing whether it works

## Why evaluation is the hard part

LLM output looks correct even when it is not, so "it seemed fine when I tried it" is not evidence. Real systems need **evals**: repeatable checks that tell you whether a change made things better or worse.

## The basic recipe

1. **Build a golden dataset**: a set of representative inputs with known-good outputs or clear pass criteria. Even a few dozen representative examples give you something repeatable to compare changes against.
2. **Run the system on every example** and record outputs.
3. **Score the outputs** (methods below).
4. **Compare across versions**: when you change a prompt, model, or retrieval setting, rerun the eval and diff the scores.

## Scoring methods

- **Exact checks**: for structured output, validate the schema and compare fields directly. Free and deterministic.
- **Classic metrics**: BLEU and ROUGE compare overlap with reference text. Useful for translation and summarization benchmarks, weak for open-ended quality.
- **LLM-as-judge**: a strong model scores another model's output against a rubric ("Is the answer faithful to the context? 1-5"). Useful for scaling review, but judges can make mistakes and show biases, including favoring certain styles. Check judge scores against human labels. Keep the judge model and rubric fixed during comparisons.
- **Human review**: the ground truth for subjective quality. Expensive, so sample it: review all failures and a slice of passes.

## Evaluating RAG systems

Score retrieval and generation separately, or you will not know which one broke:

- **Context precision / recall**: did retrieval return the right chunks, without junk?
- **Faithfulness**: is every claim in the answer supported by the retrieved context?
- **Response relevancy**: does the answer address the actual question?

The names above follow the RAGAS framework (faithfulness, response relevancy, context precision, context recall), which packages these metrics and is a good starting point.

## Regression testing for prompts

Treat prompts like code under version control. Before shipping a prompt change, rerun the golden dataset. A prompt change can fix one case while breaking another; rerun tests to check. Snapshot tests on structured output catch silent format drift.

## Safety basics

- **Prompt injection**: text inside user input or retrieved documents that tries to override your instructions ("Ignore previous rules and..."). Prompting and delimiters alone cannot reliably prevent injection. Delimiters help organize data, not enforce a security boundary. Limit tool permissions, validate tool arguments and outputs in code, and require approval for consequential actions.
- **Data leakage**: never send secrets, credentials, or personal data to a model unless the task needs it and the terms allow it. Redact what you can.
- **Jailbreaks**: attempts to bypass safety rules. Keep your own guardrails independent of the model's.
- **Over-trust**: put a human approval step in front of irreversible actions. Fluent output can still be wrong.

## Practical minimum for a student project

You do not need a full eval platform. Start with a spreadsheet of test inputs, expected behavior, and a pass/fail column. Rerun it whenever you change the prompt and add cases when you find new failures. A small set is a starting point, not a guarantee of coverage.
