# Module 13 — Fine-tuning: SFT, LoRA and QLoRA

## E076 · C · Should you fine-tune to fix wrong answers?

**0:00–0:15 · Hook**
*Screen: you on camera; then a list of wrong answers from the service analyst.*
> My assistant got some answers wrong, and the internet's advice was simple: fine-tune it on your own data. Is fine-tuning really the fix for wrong answers?

**0:15–0:45 · Claim**
*Screen: four fixes mapped to four failures: retrieval · code · prompt/skill · fine-tuning.*
> Usually not, because "wrong answers" have different causes. Match the fix to the failure. Missing or outdated facts: fix retrieval. Wrong arithmetic: move it into code. A procedure not followed: improve the prompt or write a skill. Fine-tuning is for consistent behaviour you can measure, like always categorising repair orders the same way, or always replying in a strict format. Each of these problems has a cheaper, more direct fix.

**0:45–1:30 · Show**
*Screen: three observed errors from the project, each mapped to a different fix.*
> Here are three real failures from my project. One: it quoted the old warranty mileage limit. That's a missing fact, so the fix is retrieving the right policy version. Two: it added up warranty credits wrongly. That's arithmetic, so the fix is the service revenue function in code. Three: it kept putting "battery won't hold charge" in the engine category instead of electrical, inconsistently, across thousands of complaints. That's a behaviour pattern, and that's where fine-tuning might genuinely help. One problem out of three really needed training.

**1:30–1:50 · Gotcha**
*Screen: a fine-tuning dataset full of warranty terms that change every quarter.*
> The classic mistake is fine-tuning to teach facts that change monthly, like warranty terms or prices. The model learns them once, and then confidently repeats them after they change. Retrieval keeps changing facts current.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Diagnose before you train."*
> Diagnose before you train. Next: teach AI your repair categories, cheaply.

## E077 · C · Teach AI your repair categories, cheaply

**0:00–0:15 · Hook**
*Screen: you on camera; then "7,000,000,000 parameters" in big numbers.*
> Can you teach a model your five repair categories without retraining all seven billion of its parameters, and without a data centre?

**0:15–0:45 · Claim**
*Screen: "SFT: learn from input → output examples" and "LoRA: freeze the base, train small add-on matrices".*
> Yes. Supervised fine-tuning, or SFT, teaches a model from examples of input and the output you want, like a complaint and its category. LoRA makes that cheap. Instead of changing the whole model, it freezes the original weights and trains small extra matrices, called adapters, that sit alongside them. You train a tiny fraction of the parameters, and you can swap adapters in and out. The base model stays exactly as it was.

**0:45–1:30 · Show**
*Screen: a large frozen weight matrix beside two thin trainable matrices; a count of trainable vs total parameters for one small model. [CAPTURE: the real counts for your model]*
> Here's the idea visually. The big grey block is one of the model's weight matrices, frozen, untouched. Next to it, two thin coloured matrices: the LoRA adapter. Multiplied together, they make a small adjustment to the frozen weights. For the small model I'm using, the whole model has [CAPTURE] parameters, and the adapter trains only [CAPTURE]. That's why it can run on modest hardware, and why the saved adapter file is tiny. You can even keep several adapters for different tasks and switch between them.

**1:30–1:50 · Gotcha**
*Screen: 300 examples labelled "teach it our warranty policy", with a red cross.*
> The trap is expecting a few hundred examples to add new facts. Fine-tuning mostly shapes how the model behaves and formats output. Facts still come from retrieval. Shape behaviour with training; supply facts with retrieval.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Adapters change behavior cheaply; retrieval supplies facts."*
> Adapters change behaviour cheaply; retrieval supplies facts. Next: why training needs far more memory than running.

## E078 · C · Why training needs far more memory than running

**0:00–0:15 · Hook**
*Screen: you on camera; then a model running happily on a GPU, then "CUDA out of memory" when training starts.*
> The model runs perfectly on my GPU. The moment I start training it, out of memory. Why does training need so much more memory than running?

**0:15–0:45 · Claim**
*Screen: four stacked blocks: weights · gradients · optimizer state · activations.*
> Running a model mostly needs memory for its weights. Training needs the weights plus gradients, which say how to change each weight, plus optimiser state, the running statistics the training algorithm keeps, plus activations saved from the forward pass. That can be several times the size of the model. QLoRA cuts this down by keeping the frozen base model in four-bit precision and training only the small LoRA adapters.

**0:45–1:30 · Show**
*Screen: stacked memory bars for full fine-tuning, LoRA and QLoRA at one model size, with the assumptions labelled. [CAPTURE: your estimates and assumptions]*
> Here are three bars for the same model size, with my assumptions written on screen. Full fine-tuning: weights, gradients and optimiser state for every parameter, about [CAPTURE] gigabytes. LoRA: the base weights stay frozen, and gradients and optimiser state are only needed for the small adapters, so about [CAPTURE]. QLoRA: the frozen base stored in four bits, adapters on top, about [CAPTURE]. On my machine with [CAPTURE] of GPU memory, only [CAPTURE: which options] fit. Those numbers decide the whole plan before writing any training code.

**1:30–1:50 · Gotcha**
*Screen: "QLoRA: requires supported GPU + library versions".*
> A real gotcha: four-bit training depends on your GPU and library support. Check before you plan around QLoRA, and if it isn't supported, say it's deferred. Check support first.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Measure your hardware before choosing the method."*
> Measure your hardware before choosing the method. Next: ninety-seven percent accurate, but was the test in training?

## E079 · B · 97% accurate, but was the test in training?

**0:00–0:15 · Hook**
*Screen: you on camera; then "Fine-tuned accuracy: 97%".*
> My fine-tuned repair-order classifier scored ninety-seven percent. Before celebrating, I had to ask: were the test examples also in the training data?

**0:15–0:45 · Claim**
*Screen: four checks: format · labels · group split · class balance.*
> Whether an adapter's score means anything is decided by the data, not the training run. Consistent formatting, checked labels, splits grouped by template so near-copies stay on one side, and a look at class balance. Most surprising scores trace back to one of these four checks.

**0:45–1:30 · Show**
*Screen: chat-format JSONL examples; a label audit catching mislabelled rows; a group split by template; a class balance table. [CAPTURE: your audit results]*
> Here's my data in chat-format JSONL: the complaint as the user message, the category as the answer. First, a label audit: I review a sample and find [CAPTURE] mislabelled rows, like a battery complaint marked as engine. Next, a group split by template, because my synthetic examples came from templates, and near-copies on both sides would inflate the score. Finally, class balance: body work has only [CAPTURE] examples, so I expect it to be weakest. After all that, the honest score is [CAPTURE]. A lower, honest number is far more useful than a high, misleading one.

**1:30–1:50 · Gotcha**
*Screen: 500 synthetic examples all generated from one template.*
> The trap: generating synthetic examples from one template and testing on its near-copies. The model learns the template, not the task.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Clean data beats more epochs."*
> Clean data beats more epochs. Next: fine-tuning versus a well-written prompt.

## E080 · B · Fine-tuning vs. a well-written prompt

**0:00–0:15 · Hook**
*Screen: you on camera; then "LoRA adapter" vs "a good prompt" in a match-up graphic.*
> I spent an evening training a LoRA adapter for repair-order categories. Did it actually beat a well-written prompt on the same base model? Let's find out honestly.

**0:15–0:45 · Claim**
*Screen: three contenders: zero-shot · few-shot · LoRA, all on the same base model.*
> Compare the adapter with zero-shot and few-shot prompting of the same base model, on held-out examples it has never seen. Judge on held-out results, not on training loss, which only tells you it fit the training data. Prompting is cheaper to change, so the adapter has to clearly win to justify itself.

**0:45–1:30 · Show**
*Screen: the smoke test, then the short training run; a table of macro-F1, invalid outputs, latency and memory for zero-shot, few-shot and LoRA. Label hardware. [CAPTURE: your table and hardware]*
> First, a short smoke test to check everything runs and fits in memory. Then the real training run. Now the comparison, on [CAPTURE] held-out complaints. Zero-shot: macro-F1 [CAPTURE], invalid outputs [CAPTURE]. Few-shot with five examples: [CAPTURE], [CAPTURE]. LoRA adapter: [CAPTURE], [CAPTURE]. Latency and memory are in the table too. On my hardware, [CAPTURE], the verdict is [CAPTURE: whether the adapter earned its place]. Same examples for all three.

**1:30–1:50 · Gotcha**
*Screen: a training loss curve going down while the held-out score stays flat.*
> Watch for this: training loss keeps falling while the held-out score stays flat. That means the model is memorising the training set, not learning the task. Trust the held-out table.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Keep the adapter only if it wins on held-out data."*
> Keep the adapter only if it wins on held-out data. Next: sixteen-bit or four-bit, what do you lose?
