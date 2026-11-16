# 2. Prompt engineering: getting useful output reliably

A prompt is the entire input you give the model. Prompt engineering is structuring that input so the model does what you want the first time, more often. It is the cheapest lever you have: no training, no infrastructure, just better instructions.

## Anatomy of a good prompt

Most useful prompts have some of these parts:

1. **System instructions**: the role, rules, and constraints that apply to every reply ("You are a careful assistant. Answer only from the provided document. If the answer is not in the document, say so.")
2. **Context**: the data the model needs (a document, a user profile, retrieved chunks)
3. **Task**: the specific thing to do, stated as a verb ("Summarize in three bullet points")
4. **Format**: the shape of the output ("Return JSON with keys `name`, `date`, `amount`")
5. **Examples**: one or more input-output pairs showing exactly what you want

You rarely need all five, but a vague task with no format often produces bad output.

## Core techniques

### Zero-shot vs. few-shot

- **Zero-shot**: you ask directly, no examples. Works well for common tasks on capable models.
- **Few-shot**: you include examples of input and desired output. Use it when the output style or format is unusual, or when zero-shot results drift.

### Delimiters and structure

Wrap variable content in clear markers so the model can tell instructions from data:

```
Summarize the article below in 2 sentences.

<article>
...text here...
</article>
```

This reduces confusion between your instructions and the data, but delimiters are not a security boundary: a determined injection can still override them. Chapter 5 covers stronger defenses.

### Ask for reasoning before the answer

For multi-step problems, one option is asking the model to reason step by step before giving a final answer (chain-of-thought prompting, Wei et al. 2022). Whether it helps depends on the task and the model: many current models reason internally or offer a reasoning mode, where explicit step-by-step instructions add little. Treat it as an experiment, not a rule: try it on your own task and model, and keep it only if your tests show it helps. You can also ask for a short rationale field before the final field in structured output, which gives the model room to "think" while keeping the output parseable.

### Structured output

For anything consumed by code, request strict JSON and validate it in your program. Many APIs offer a JSON mode or schema enforcement. Never parse free text with regex when you could have asked for JSON.

## A before-and-after example

Vague:

> Tell me about this error.

Better:

> You are a Python debugging assistant. The traceback below comes from a Flask app running Python 3.11.
>
> 1. State the root cause in one sentence.
> 2. Show the minimal fix as a code block.
> 3. Name one way to prevent it.
>
> <traceback>
> ...
> </traceback>

The second version fixes the role, the context, the task, and the format, so the output is predictable enough to use.

## An iteration loop that works

1. Write the simplest prompt that could work.
2. Run it on 3 to 5 realistic inputs, including one awkward one.
3. Find the failure pattern (wrong format, missed instruction, invented facts).
4. Fix exactly that: add a constraint, an example, or a format requirement.
5. Repeat. Keep the prompt versions so you can compare.

Treat prompts like code: version them, test them, and review changes. Chapter 5 covers how to test prompts systematically.

## Common failure modes

- **Vague task**: "make this better" gives unpredictable results. Name the improvement.
- **Missing context**: the model cannot read your files, your ticket system, or your mind. Paste the relevant data in.
- **No output format**: you get prose when you needed a table or JSON.
- **Overstuffed prompt**: pages of irrelevant text bury the instruction. Keep context focused; retrieve only what matters (RAG, next chapter).
- **Fighting the model with negatives**: "do not use jargon" works worse than showing the plain style you want in an example.
