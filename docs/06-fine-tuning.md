# 6. Fine-tuning: teaching the model new behavior

## What fine-tuning is

Prompting changes what the model sees. RAG changes what the model knows at answer time. **Fine-tuning** changes the model itself: you continue training a base model on your own examples so its default behavior shifts.

A fine-tuned model has seen your task many times during training, so it usually needs less instruction at inference time. The flip side: what it learned is baked into its weights. Changing that behavior means another training run, though you can still add fresh knowledge at runtime with RAG (chapter 3) without touching the weights.

## How it works

1. **Collect examples.** Each example is an input paired with its ideal output: a support question with the ideal reply, a sentence with its label, a document with its summary.
2. **Format them** the way the model expects, usually as chat messages (system, user, assistant) in JSONL files.
3. **Split** into three sets: train on the training set, use the validation set to compare runs and settings, and keep the test set untouched for a final check.
4. **Train.** Hosted fine-tuning APIs take the file and return a new model ID. For open-weight models you train yourself, the standard method is **LoRA** (Low-Rank Adaptation): the base weights stay frozen and the trainer learns small low-rank matrices that are added to selected layers. That trains a tiny fraction of the parameters, so it needs much less memory than full fine-tuning.
5. **Evaluate** on the held-out test set with the methods from chapter 5 before shipping anything.

## What fine-tuning is good at

- **More consistent format and style**: structured output and tone become noticeably more reliable than with prompting alone. It is still not a guarantee, so keep validating structured output in code (chapter 5).
- **Narrow classification tasks**: routing messages, labeling tickets, extracting fields, at high volume and low cost per call.
- **Domain vocabulary**: legal, medical, or internal jargon the base model fumbles.
- **Shorter prompts**: behavior that lives in the model does not need to be re-explained in every request.

## What it cannot do

- **Add facts reliably.** A fine-tuned model can still hallucinate, including about the data it was trained on. For knowledge, use RAG (chapter 3).
- **Stay current on its own.** Its baked-in knowledge freezes at training time; pair it with RAG or tools for anything that changes.
- **Replace prompt engineering.** Fine-tuning iterates slowly: every change means new data and a new training run. Get the task working with prompts first (chapter 2), and fine-tune when consistency or cost at scale demands it.

## Your dataset decides the result

The model picks up the patterns in your examples, including their mistakes.

- **Quality over quantity**: a small set of consistent, correct examples usually beats a large sloppy one. Start with a few dozen good examples, measure, and add data where evaluation shows failures.
- **Consistency**: same format, same tone, same rules in every example. Mixed conventions teach mixed behavior.
- **Coverage**: include the awkward cases, not just the easy ones. A pattern that rarely appears in training is learned weakly, if at all.
- **No leakage**: keep validation and test examples out of the training set, or your evaluation lies to you.

A practical workflow: prompt the base model, collect real outputs, correct the bad ones by hand, and use the corrected pairs as training data.

## Choosing between prompting, RAG, and fine-tuning

| Situation | Start with |
| --- | --- |
| Task is new or changing fast | Prompting |
| Needs private or current knowledge | RAG |
| Needs consistent format, style, or classification at scale | Fine-tuning |
| Knowledge plus strict behavior | RAG + fine-tuning |

This matches chapter 3's rule of thumb: fine-tune for behavior, RAG for knowledge.

## Costs and maintenance

- Training costs money or GPU time. Full fine-tuning of large models needs serious memory; LoRA reduces that enough that smaller open-weight models can often be fine-tuned on a single GPU, depending on model size and settings.
- Inference pricing for fine-tuned models varies by provider and model; check the current pricing page before committing.
- Treat behavior changes like code changes: keep the dataset, training configuration, and evaluation results together so you can reproduce or roll back.
- Providers deprecate base models. A fine-tuned model may need retraining when its base model is retired.

## Try it

Build a tiny dataset before touching any training code. Pick one narrow task, for example classifying messages as "question", "complaint", or "other", and write 30 input and ideal-output pairs by hand in chat format. Set 10 aside as your test set.

This is a learning exercise, not a production dataset; real training data needs more examples and careful review. The point is to feel where the difficulty actually is: if writing 30 consistent examples feels hard, the dataset is the bottleneck, not the training. Once the dataset exists, a hosted fine-tuning job or a LoRA script is the mechanical part, and chapter 5 covers how to check whether the result beats your prompt.

## Learn more

- [OpenAI fine-tuning guide](https://platform.openai.com/docs/guides/fine-tuning): how a hosted fine-tuning workflow looks end to end.
- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685): the original LoRA paper, readable after chapter 1.
- [Hugging Face PEFT: LoRA conceptual guide](https://huggingface.co/docs/peft/en/conceptual_guides/lora): practical details for fine-tuning open-weight models yourself.
