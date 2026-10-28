# Day 1 → Hired by Mercedes: Learning AI Engineering in Public

Version 8 · Updated 29 October 2026
## A journey video series and learning course for Razeen Iqbal

### What changed in version 8
- **The series is a journey.** Every lesson is published as "Day N", counting from Day 1 until Razeen is hired by Mercedes. The goal is named openly. See Section 1.
- **The running project is automotive.** The Analyst Agent became a **Service Analyst Agent** for three fictional dealership groups: repair orders, warranty claims, service bulletins and recall notices instead of generic company invoices. Every module and episode is unchanged in what it teaches; only the data and examples moved. See Section 6.
- **Titles are hooks.** Each episode title is now the viewer-facing question or promise, not a textbook heading. Episode codes E001–E087 and their order are unchanged, so tracker progress carries over.
- **Three content types.** Lessons (the 87 episodes), *AI explained* videos with an engineer's take, and check-ins. See Section 1.
- **Seasons.** The 16 modules are grouped into five seasons, each with a payoff, so the series can launch, pause and be re-cut by season.
- **Malay examples.** Complaint descriptions and token-count demos include Malay, which few AI channels cover.
- **Framework note.** Module 8 records when to add a LangGraph comparison, after the hand-built loop works.

---

## 1. The series: Day 1 → hired by Mercedes

### The promise
**Headline:** "Day 1 to hired by Mercedes: learning AI engineering in public."

**Who it's for:** Python and data people moving into AI engineering, and anyone curious how a data engineer becomes an AI engineer in automotive.

**Why automotive and Mercedes:** a long-standing interest in cars and motorsport, an automotive AI workshop already delivered for MARii, and a data engineering background that fits after-sales and service analytics. The running project is the kind of system a car company would actually want: an assistant that answers questions about service, warranty and parts data with checkable evidence.

**What stays honest:**
- The demo data is synthetic. It is never Mercedes data, never a real dealer's data and never an employer's data.
- The series is not affiliated with, sponsored by or endorsed by Mercedes-Benz. Say so in every video description.
- Name Mercedes as the goal. Don't use its logo, three-pointed star, fonts, livery or official imagery, and don't put "Mercedes" in the channel name, handle or thumbnail art in a way that looks official.
- Don't claim insider knowledge of how Mercedes builds its systems. Talk about what you built.
- Check your current employment contract and company policy on public content before Day 1.

### How episodes are numbered
- **Day N** is the number of calendar days since the Day 1 video went live, not a count of uploads. Day 1, Day 3, Day 5… is normal.
- Public title format: **"Day N · <episode title>"**, for example "Day 23 · Should AI add up your service revenue?"
- The episode code (E012) stays in the tracker and the description, so a lesson keeps its place in the course whatever day it airs.

### Three content types
| Type | Share | What it is | Example |
|---|---|---|---|
| **Lesson** | 2 per week | One of the 87 episodes in Section 8 | "Day 23 · Should AI add up your service revenue?" |
| **AI explained** | 1 per week | A general AI topic or news item, always with your angle | "Day 25 · Everyone's talking about [new model]. What actually changes for builders?" |
| **Check-in** | About every 2 weeks, replacing that week's Explained | Progress, what was hard, applications and interviews so far | "Day 60 · Two months in: what's working, what isn't" |

**The angle rule for AI explained.** Never just report what happened. Add one of:
- **For builders:** how you would test whether it's actually better.
- **For data people:** where a classifier or a SQL query still beats an LLM (your ML side).
- **For automotive:** how a car company or dealership might use it, or why it wouldn't.
- **For Malaysia:** does it understand Malay, and does it handle ringgit, ICs and local addresses?

Budget each Explained video at 2 hours from idea to upload. Skip a topic rather than let it eat a lesson.

### Seasons
| Season | Modules | Payoff |
|---|---|---|
| **1 · Ask AI about service data, safely** | 0–2 | An API that won't invent your service revenue |
| **2 · Make it find the right document** | 3–4 | Answers from warranty policies and bulletins, with citations, measured |
| **3 · Give it tools, then limits** | 5–10 | A service agent that can't run away |
| **4 · Prove it works** | 11–12 | Evals and safety checks that block bad changes |
| **5 · Run it yourself, then show it** | 13–15 | Local models, fine-tuning and the capstone demo |

### Day 1
Not part of the 87. Film it before the first lesson.
- **Hook:** "Day 1. I work in data. I want to be an AI engineer at Mercedes. Here's the plan."
- **Who:** your background in data engineering and the automotive work you've already done, in two sentences.
- **The goal:** an AI engineering role at Mercedes, named plainly. Any strong automotive AI role along the way counts as progress, and you'll say so honestly.
- **The plan:** 87 two-minute lessons, one real project (an AI service analyst for car dealerships), built and tested in public. Two lessons a week, plus explainers and check-ins.
- **Proof:** every Build lesson shows working code and test results. The course tracker counts the days.
- **Takeaway:** "Follow along; Day 3 is how AI apps really work."

### Check-in template
1. Day number, lessons published, modules finished (from the tracker).
2. One thing that clicked and one thing that was hard.
3. One failure and what fixed it.
4. Job search: applications, conversations, interviews, rejections, as far as you're comfortable sharing.
5. What's next.

### How the story can end
You don't control the ending, so plan for all three honestly:
- **Hired by Mercedes:** the final check-in and a capstone walkthrough.
- **Hired elsewhere in automotive AI first:** "Not Mercedes yet." The series continues toward the original goal, or closes with an honest wrap-up.
- **Still searching after the capstone:** Season 6 becomes the application and interview journey, using the finished project as the portfolio.

---

## 2. Purpose and audience

**Goal:** learn applied AI engineering properly, publish two-minute videos that explain both the theory and the working application, and use the series and the project as the portfolio for an AI engineering role at Mercedes.

**Audience for the series:** Python and data people moving into AI engineering. Assume basic Python and data familiarity. Define everything else at first use: API, schema, token, embedding, RAG, tool, agent, harness, skill, MCP, tenant, adapter, quantization.

**Positioning:** "Day 1 to hired by Mercedes: learning AI engineering in public, one working example at a time." Present what you built and tested. Draw on your data engineering background, but don't imply the prototype runs in production.

**This is a recommended learning sequence, not an accredited qualification.**

---

## 3. Core principles (carried through every module)

1. **Code calculates, the model explains.** Anything that must be exact (totals, filters, permissions, dates) is done in code.
2. **Identity never comes from the model.** Dealer and user come from authenticated context.
3. **The model only knows what's in its context.** Private facts must be supplied through trusted context or an authorized tool.
4. **Limits live in code, not prompts.** Budgets, permissions and stopping rules are enforced by the harness.
5. **Define correctness before you look.** Write expected results before running a change.
6. **Say what's missing.** "The evidence doesn't answer this" is a valid, tested outcome.

---

## 4. How the lessons work

### Episode types
| Type | Purpose | Visual | Typical prep |
|---|---|---|---|
| **C · Concept** | Explain one idea | You on camera for hook and takeaway; diagram, whiteboard or animated table in the middle | Script + diagram |
| **B · Build** | Show the idea working in code | You on camera for hook and takeaway; screen recording of the project, with you in a corner bubble | Working, tested commit + script |

Alternate them where possible: a Concept episode followed by the Build episode that applies it.

Build episodes open with one line of context for new viewers: "I'm building an AI service analyst for car dealerships; today it…"

### Episode spec (every field must be unique)
- **Hook:** a specific question or failure, not a generic one.
- **Claim:** the one idea, in one sentence.
- **Show:** the exact diagram or demo.
- **Gotcha:** the common mistake or limit.
- **Takeaway:** one line, different from the claim.

If you can't fill all five uniquely, the episode isn't ready. The episode title is the public hook; the Hook field is the opening line.

### Two-minute timing
| Time | Section | Content |
|---|---|---|
| 0:00–0:15 | Hook | The question or failure |
| 0:15–0:45 | Claim | Explain the idea in plain language |
| 0:45–1:30 | Show | Diagram walkthrough or demo |
| 1:30–1:50 | Gotcha | The mistake or limit |
| 1:50–2:00 | Takeaway | One line, plus the next episode |

Aim for 220–260 spoken words; use fewer in Build episodes so viewers can read the screen. If a timed rehearsal runs over, split the episode rather than speaking faster.

**Overview episodes.** Some episodes cover several items, such as five workflow patterns or three search methods. Show one representative case on screen and put the rest in the lab or article. A two-minute video is not the complete lab.

### Evergreen vs. versioned
- **Concept episodes** teach principles and should still be true in a year.
- **Build episodes** show the SDK, model identifier and recording date on screen and in the description. Context engineering, caching, harnesses, skills, MCP and training libraries change quickly.

### Lab pattern (every module)
- **Start** from the previous module's tested commit.
- **Build** the module's Build items one at a time. Write the fixture and expected outcome before each change, and test offline before any live call.
- **Evidence:** meet the Checkpoint, and save one successful case and one meaningful failure with its cause.
- **Troubleshoot** by locating the failure first: input validation, authorization, tool execution, retrieval, model output or evaluation. Change the prompt last.
- **Independent exercise:** inject one failure not shown in the video, and show the recovery or an explicit incomplete outcome.

Modules with experiments add specific lab steps.

### Article companion (optional)
Explain the objective, method, fixture, setup and runnable code, with expected output, one failure and the limits. Each video shows one idea; the article connects the steps.

---

## 5. Pace and time

**Learning:** about 6–8 hours for ordinary modules and 10–14 hours for the guided experiments. Plan roughly 18–22 weeks, depending on prerequisites and hardware. These are estimates.

**Publishing:** 3 videos per week: 2 lessons and 1 AI explained or check-in. At 2 lessons a week the 87 lessons take about 44 weeks, so learning stays well ahead of publishing. In weeks where you're ahead, publish a third lesson instead of an Explained video.

**Before committing to a schedule, produce Day 1 and the 4-episode pilot** (Section 10) and time each step: scripting, demo preparation, recording, editing, review. Adjust the pace from your actual numbers.

**Articles are optional.** Use them for setup instructions and full code, not to restate the videos.

---

## 6. Project, depth and dependencies

### The running project: Service Analyst Agent
You build one project from scratch in plain Python, and each module adds a capability. The demo domain is synthetic after-sales data for three fictional multi-brand dealership groups: **Dealer A** (Kuala Lumpur), **Dealer B** (Penang) and **Dealer C** (Johor Bahru). No real brands, dealers, customers or vehicles.

- 3 dealers (tenants), 12 months, about 300 repair orders, 150 parts and expense records and 6 short policy documents.
- Repair orders carry labour and parts lines, a pay type (customer-paid, warranty or internal), a synthetic VIN and mileage.
- The six documents: warranty policy (two versions, changed in July), goodwill policy, labour rate card, parts return policy, service bulletin SB-23-04 (brake noise) and one recall notice.
- Deliberately messy: duplicate repair orders, missing VINs, warranty credit notes, conflicting bulletin versions, a month with no data, one SGD-priced record at the Johor dealer.
- Define before writing any eval: gross vs. net service revenue, customer-paid vs. warranty vs. internal work, currency (MYR), repair-order open vs. close date, when warranty reimbursement counts, fiscal year start, and who may see what (staff see only their own dealer).

### Completion levels
| Level | Modules | What completion means |
|---|---|---|
| **Core** | 0–5, 11, 12, 15 | Implement and evaluate |
| **Practical introduction** | 6–10 | Build a working example and justify whether it belongs in the final system |
| **Guided experiment** | 13, 14 | Run one bounded experiment on measured hardware. Mark unsupported parts deferred |
| **Optional advanced** | Not in this course | Distillation, pretraining, DPO and RL, complex multi-agent systems: understand their purpose, specialise later |

An API-only learner can finish every Core and Practical module. They must not claim to have completed local adapter training.

### Build dependencies
| Module | Project increment |
|---|---|
| 0 | Model adapter (mock and real), usage and cost logging |
| 1 | Repair-order classifier, baseline and duplicate-aware splits |
| 2 | FastAPI service, trusted dealer context, typed responses, service revenue function, repair-order extraction, offline 10-case eval |
| 3 | Dealer-scoped policy retrieval with provenance, citations and abstention |
| 4 | PostgreSQL with pgvector, embedding comparison, reranking, version selection |
| 5 | Narrow SQL-backed tools, period resolver, MCP server |
| 6 | Context assembler, compaction, tool-result clearing, notes memory |
| 7 | Stable-prefix caching, preload variant, dealer- and version-aware cache keys |
| 8 | First agent with step limit, deadline and allowed-tool validation; workflow comparison; subagent |
| 9 | Time, token and cost budgets; approvals; sandbox; hooks; traces; checkpoints |
| 10 | `monthly-service-report` skill with trigger tests |
| 11 | Consolidated dev and held-out sets, graders, trajectory checks, CI |
| 12 | Injection and isolation tests, observability, cost per successful task, Docker |
| 13 | One LoRA run compared with prompting |
| 14 | Local model behind the same adapter, two configurations compared |
| 15 | Combined demo, scorecard, reproducible README |

Trusted identity checks and offline evals start in Modules 1 and 2. Regression cases carry forward, and Modules 11 and 12 consolidate them rather than introducing them.

### Stack and hardware
Python, FastAPI, Pydantic, pytest, scikit-learn (Module 1), PostgreSQL with pgvector (from Module 4), Docker and GitHub Actions. Use one provider's current official SDK behind a small adapter so model calls can be mocked. Frameworks are optional; build the loop yourself first (see the framework note in Module 8). Fine-tuning adds current compatible PyTorch, Transformers, PEFT and a trainer such as TRL. Record dependency versions, model revisions and licenses.

Check your actual RAM and VRAM before choosing a model. Start small, use short sequences and run a smoke test first. A budgeted cloud GPU is an option, not a requirement.

### Required experiment reports
| Experiment | Module | Comparison | Report |
|---|---|---|---|
| Retrieval | 4 | Baseline vs. one controlled change | Recall@k, citation support, latency |
| Context reuse | 7 | Retrieval per request; uncached preload; verified cache reuse | Correctness, evidence, freshness, cold and warm latency, usage, cost |
| Adaptation | 13 | Zero- and few-shot prompting vs. LoRA on the same base model; QLoRA only if supported | Held-out metrics, invalid outputs, trainable parameters, memory |
| Inference | 14 | Two supported model, precision or runtime configurations | Quality, total memory, cold and warm latency, bounded concurrency |

**About CAG.** Here, cache-augmented generation means the cited paper's idea: preload a bounded corpus and reuse the cached inference state. Provider prefix caching supports a related experiment but is not an exact reproduction of the paper's KV-cache method. Cached final answers are a separate mechanism. A run without verified cache hits must be labeled uncached.

---

## 7. Module map

| # | Module | Level | Season | Episodes | Count |
|---|---|---|---|---|---:|
| 0 | How LLMs actually work | Core | 1 | E001–E006 | 6 |
| 1 | ML foundations and baselines | Core | 1 | E007–E011 | 5 |
| 2 | The application boundary and structured output | Core | 1 | E012–E018 | 7 |
| 3 | Retrieval | Core | 2 | E019–E024 | 6 |
| 4 | Retrieval experiments and reranking | Core | 2 | E025–E029 | 5 |
| 5 | Tools and MCP | Core | 3 | E030–E036 | 7 |
| 6 | Context engineering | Practical introduction | 3 | E037–E043 | 7 |
| 7 | Caching and CAG | Practical introduction | 3 | E044–E046 | 3 |
| 8 | Agents | Practical introduction | 3 | E047–E053 | 7 |
| 9 | Harness engineering | Practical introduction | 3 | E054–E060 | 7 |
| 10 | Skills | Practical introduction | 3 | E061–E065 | 5 |
| 11 | Evaluation | Core | 4 | E066–E070 | 5 |
| 12 | Safety and production | Core | 4 | E071–E075 | 5 |
| 13 | Fine-tuning: SFT, LoRA and QLoRA | Guided experiment | 5 | E076–E080 | 5 |
| 14 | Local inference and quantization | Guided experiment | 5 | E081–E084 | 4 |
| 15 | Capstone | Core | 5 | E085–E087 | 3 |
| | **Total** | | | | **87** |

About 174 minutes of finished lesson viewing. Labs and reference viewing are additional. Episode specs are planning outlines; full scripts still need real outputs and a timed rehearsal.

---

## 8. Modules and episodes

### Module 0 — How LLMs actually work
**Depth:** Core
**Learn:** tokens, context windows, next-token prediction, sampling, cost and latency.
**Build:** a `ModelClient` interface with `MockModel` and one real provider, selected by environment variable; log tokens, duration and estimated cost per call.
**Checkpoint:** explain why a dealer's private service figures need supplied evidence or an authorized tool, and show a logged call with usage.

**E001 · C · Why AI demos break in real life** *(pilot)*
- Hook: Why does a chatbot look brilliant in a demo and fail in production?
- Claim: The model is one component; the application around it decides what is trusted, allowed and checked.
- Show: Diagram: service advisor → app → context builder → model → tools and data → validator → response.
- Gotcha: Treating the model as the whole system.
- Takeaway: Draw the boxes before choosing a model.

**E002 · C · Why didn't my 40-page manual fit?**
- Hook: Why didn't a 40-page service manual "fit"?
- Claim: Models read tokens, and instructions, history, documents and tool results all share one finite window.
- Show: Token counts for an English complaint, a part number and the Malay complaint "brek berbunyi bila tekan", against a window bar.
- Gotcha: Assuming word count ≈ token count, especially for part numbers, VINs and non-English text.
- Takeaway: Budget in tokens, not pages.

**E003 · B · Why would AI invent a warranty claim number?**
- Hook: Why would a model make up a warranty claim number?
- Claim: A model generates text from learned patterns and supplied context, and plausible isn't the same as verified.
- Show: Ask for Dealer A's March warranty total with no data supplied and capture the real response. A refusal is also a valid result; label any constructed wrong answer as an illustration.
- Gotcha: Believing lower temperature fixes hallucination.
- Takeaway: Supply facts or compute them; never ask the model to remember them.

**E004 · B · Same question, different answers. Is it a bug?**
- Hook: Same prompt, different answers — is that a bug?
- Claim: Sampling settings trade variety for consistency, but no setting guarantees identical output.
- Show: One repair-order summary prompt run five times at two temperatures, outputs side by side.
- Gotcha: Writing tests that expect exact text.
- Takeaway: Check properties of model prose; check exact values from code.

**E005 · B · Use any AI model without getting locked in**
- Hook: How do you call a model without locking your code to one provider?
- Claim: A thin adapter makes the model swappable and mockable.
- Show: `ModelClient` interface, `MockModel` and real client; switch with one environment variable.
- Gotcha: SDK calls scattered across the codebase.
- Takeaway: Only one file should know your provider.

**E006 · B · What did that one AI answer cost?**
- Hook: How much did that one answer cost, and how long did it take?
- Claim: Log usage and duration for every call, and mark missing usage and failed calls explicitly.
- Show: Structured log line with input tokens, output tokens, duration and cost from rates recorded with a date.
- Gotcha: Estimating cost from characters or an old price list.
- Takeaway: Log usage per request; price it at run time.

### Module 1 — ML foundations and baselines
**Depth:** Core
**Learn:** when rules, classical ML or an LLM fit; training vs. inference; attention at a conceptual level; embeddings and similarity; duplicate-aware splits; precision, recall and macro-F1; baselines.
**Build:** a repair-order classifier: 100 labeled synthetic complaint descriptions in English and Malay, grouped by template, across five categories (brakes, tyres, electrical, engine, body); a majority-class baseline, TF-IDF with logistic regression, and an embedding similarity check.
**Checkpoint:** a split manifest with no template shared between training and held-out data, a confusion matrix, and macro-F1 for the baseline and the classifier.

**Lab steps**
1. Write 100 complaint descriptions across five categories, some in Malay, and tag each with its template group.
2. Split by group and reserve held-out cases before training anything.
3. Score a majority-class baseline.
4. Train TF-IDF with logistic regression.
5. Report macro-F1 and read the errors class by class.

If the score looks suspiciously high, check for templates shared across the split.

**E007 · C · Brake squeal: do you even need AI?**
- Hook: "Squeal when braking at low speed" is a brake job. Do you need AI to know that?
- Claim: Use rules for fixed logic, ML for patterns you can label, and an LLM for open-ended language, starting with the simplest that meets the target.
- Show: Three complaint lines sorted by a keyword rule, a trained classifier and an LLM, and where each one breaks.
- Gotcha: Reaching for an LLM when a keyword table already gets 98% right.
- Takeaway: The baseline decides whether complexity is worth it.

**E008 · C · Is the AI learning from my chats?**
- Hook: When you chat with a model, is it learning from you?
- Claim: Training changes a model's weights from data; inference uses fixed weights to produce output, so your chat doesn't retrain it.
- Show: Two panels: dataset → training loop → weights; then locked weights + prompt → output.
- Gotcha: Mistaking context or a product's memory feature for the model learning.
- Takeaway: Context changes the answer; training changes the model.

**E009 · C · How does AI know what "it" means?**
- Hook: In "the car was towed in because it wouldn't start," how does a model know "it" means the car?
- Claim: Attention lets each token weigh every other token in the context when building its representation.
- Show: The sentence with weighted lines from "it" to other words, then the same idea across a long repair history.
- Gotcha: Reading attention weights as the model's reasoning; they're one internal signal, not an explanation.
- Takeaway: Everything in the window can influence everything else, which is why context choices matter.

**E010 · B · "Squeaky brakes" vs "noise when stopping": same thing?**
- Hook: "Squeaky brakes" and "noise when stopping" share no words. How does a system know they're related?
- Claim: Embeddings turn text into vectors, and cosine similarity measures how close two meanings are.
- Show: Embed six complaint descriptions, including two in Malay, show the similarity matrix, and find the nearest neighbor of "bunyi bila brek".
- Gotcha: Close isn't the same: "brake pad replacement" and "brake pad recall" score as similar but one is customer-paid and one is warranty.
- Takeaway: Similarity finds candidates; your logic decides.

**E011 · B · My classifier scored 99%. I didn't believe it.**
- Hook: My classifier scored 99%. Why didn't I believe it?
- Claim: Split by template group, compare with a majority baseline, and read per-class errors before trusting a score.
- Show: Random split 99% → group split 81%; majority baseline 40%; confusion matrix where "electrical" and "engine" get mixed up on no-start complaints.
- Gotcha: Near-duplicate examples on both sides of the split inflate the score.
- Takeaway: A score means nothing without its split and its baseline.

### Module 2 — The application boundary and structured output
**Depth:** Core
**Learn:** deterministic responsibilities, trusted request context, typed contracts, failure paths, prompts with examples, structured output, business checks, a first eval.
**Build:** FastAPI service with `/health` and `/ask`; dealer taken from request context through a development auth stub, never from the request body; four response statuses; `service_revenue`; repair-order extraction with schema and arithmetic checks; a 10-case JSONL eval that runs offline in pytest with the mock model.
**Checkpoint:** the API works offline with mocks and no API key, a test shows a dealer named in the request body is ignored, and a prompt change is judged by the eval, not by eye.

**E012 · B · Should AI add up your service revenue?** *(pilot, scripted in Section 10)*
- Hook: Should the model add up your service revenue?
- Claim: Exact work belongs to code; the model interprets the question and explains the result.
- Show: Dealer A's 100 + 200 − 50 = 250 MYR with Decimal, Dealer B's 9999 MYR excluded, model explains the returned total.
- Gotcha: The plausible wrong answer (10,249 MYR) mixes another dealer's data.
- Takeaway: If it must be exact, compute it.

**E013 · B · What should an AI app say when it can't answer?**
- Hook: What should the app return when it can't answer?
- Claim: A typed response distinguishes answered, needs more information, blocked and failed.
- Show: Pydantic response model and the four statuses in `/docs`.
- Gotcha: Returning HTTP 200 with "Sorry!" for everything.
- Takeaway: Make every outcome a named state.

**E014 · B · What users see when your AI app breaks** *(pilot)*
- Hook: Blank question, giant paste, provider down — what does the service advisor see?
- Claim: Validate at the boundary and map each failure to an explicit response.
- Show: Whitespace-only input rejected with 422; simulated timeout returns 503 with a fallback message; the tests for both.
- Gotcha: Provider exceptions leaking as 500 stack traces.
- Takeaway: Test the failure before the success.

**E015 · C · Why does AI ignore your formatting rules?**
- Hook: Why does the model ignore your formatting rules?
- Claim: A clear role, plain rules and one or two well-chosen examples shape output more than a long list of "don'ts."
- Show: Vague prompt vs. sectioned prompt with one example; repair-order summaries compared.
- Gotcha: Examples so narrow the model copies their content.
- Takeaway: Show the shape; vary the content.

**E016 · B · From a messy repair order to clean data**
- Hook: How does a paragraph of repair-order notes become data?
- Claim: Request a schema, then validate the result before using it.
- Show: Extract repair-order number, date, VIN, mileage, labour lines, parts and total into a Pydantic model; a malformed date fails validation.
- Gotcha: Treating the provider's structured-output mode as validation.
- Takeaway: Parse, then validate.

**E017 · C · Valid JSON, wrong total**
- Hook: The JSON parsed — so it's correct?
- Claim: A schema proves the shape of an answer, not its truth.
- Show: Schema-valid extraction with total 3,500 while labour and parts lines sum to 350; the business check flags it for review.
- Gotcha: Equating "no errors" with "correct."
- Takeaway: Add business checks after parsing.

**E018 · B · Did my prompt change help, or just look better?**
- Hook: Did your prompt change help, or does it just look better?
- Claim: Ten fixed cases with expected values beat any number of eyeballed demos.
- Show: JSONL cases, a runner, field-level scores; prompt v1 vs. v2.
- Gotcha: Writing the expected answer after seeing the output.
- Takeaway: References first, runs second.

### Module 3 — Retrieval
**Depth:** Core
**Learn:** retrieval vs. generation, chunking with provenance, keyword, embedding and hybrid search, Recall@k, citations, abstention.
**Build:** six policy documents with version and dealer metadata; the dealer filter applied inside the retrieval query; a keyword (BM25) baseline; embedding and hybrid search in memory; citations from stored metadata; abstention on five absent topics.
**Checkpoint:** Recall@3 for keyword, embedding and hybrid search on 15 labeled questions; correct abstention on the five absent topics; no chunk from another dealer is ever retrieved.

**E019 · C · How AI answers from your documents**
- Hook: How can a model answer from your warranty policy?
- Claim: Retrieval selects evidence; generation explains it — and each stage fails differently.
- Show: Pipeline diagram with one failure at each stage.
- Gotcha: Judging only the final answer.
- Takeaway: Evaluate retrieval separately.

**E020 · B · The chunk that lost the warranty exception**
- Hook: Can a chunk lose the exception that voids the warranty?
- Claim: Chunk on meaningful boundaries and keep document ID, version, dealer and location with every chunk.
- Show: A broken boundary splitting "covered for 100,000 km" from "except commercial use"; fixed version with metadata.
- Gotcha: Chunks with no source information can't be cited.
- Takeaway: No provenance, no citation.

**E021 · B · Which search finds bulletin "SB-23-04"?**
- Hook: Which search finds service bulletin "SB-23-04"?
- Claim: Keyword and embedding search tend to win on different queries, so compare both and a hybrid on your own corpus.
- Show: Same three queries through all three methods; Recall@3 table.
- Gotcha: Replacing keyword search entirely with embeddings.
- Takeaway: Start with keywords; measure before adding more.

**E022 · C · Wrong answer: bad search or bad model?**
- Hook: The answer was wrong. Was it the search or the model?
- Claim: Recall@k checks whether the labeled relevant passage appears in the top k results, before any model is involved.
- Show: 15 labeled questions, including one where the right passage ranks fifth, so Recall@3 misses it and the answer fails.
- Gotcha: Labeling relevant passages after seeing what the search returned.
- Takeaway: Measure retrieval before blaming generation.

**E023 · B · Does this source really say that?**
- Hook: Does this source really support the answer?
- Claim: A citation is only useful if the cited passage contains the claimed fact.
- Show: Open each cited passage and check the mileage limit or labour rate.
- Gotcha: A real citation attached to an unsupported claim.
- Takeaway: Check the claim, not just the link.

**E024 · C · When the manual doesn't say**
- Hook: What should the assistant do when the answer isn't there?
- Claim: Abstaining with a clear reason is a correct, testable outcome.
- Show: Absent-topic question answered with "not covered" plus what would be needed.
- Gotcha: Measuring only answerable questions.
- Takeaway: Test the unanswerable too.

### Module 4 — Retrieval experiments and reranking
**Depth:** Core
**Learn:** choosing embedding models on your own data, vector indexes and approximate search, reranking, version freshness, when advanced RAG techniques help.
**Build:** move chunks into PostgreSQL with pgvector; compare two embedding models; add a reranker; select the policy version that applies to the question's date; add one query-rewriting step only if a measured failure pattern justifies it.
**Checkpoint:** the retrieval experiment report: one controlled improvement on development questions, confirmed on held-out questions, with Recall@k, citation support and latency reported separately.

**Lab steps**
1. Label relevant passages for 15 development questions, and reserve held-out questions.
2. Record keyword and embedding baselines.
3. Change one thing at a time: embedding model, chunk size, then reranking.
4. Measure retrieval and answer support separately for each change.
5. Run the held-out questions once, for the final configuration only.

A reranker can't recover a passage that never entered its candidate list. Check candidate recall first.

**E025 · B · Is the #1 embedding model best for your manuals?**
- Hook: Is the model at the top of the leaderboard the best one for your warranty documents?
- Claim: Pick an embedding model by Recall@k on your own labeled questions, alongside its cost and speed.
- Show: Two embedding models on the same 15 questions; Recall@3, embedding time and index size side by side.
- Gotcha: Trusting a public benchmark built on different text and languages.
- Takeaway: Your data is the benchmark.

**E026 · B · Do you need a separate vector database?**
- Hook: Do you need a separate vector database?
- Claim: With pgvector, embeddings sit next to your data, so the dealer filter and the vector search run in one query.
- Show: A table of chunk, dealer, version and embedding; one SQL query that filters by dealer and orders by distance; exact vs. approximate index results compared.
- Gotcha: Approximate indexes trade some recall for speed; measure it instead of assuming.
- Takeaway: Keep the filter and the search in one place.

**E027 · B · Right passage, ranked eighth**
- Hook: The right passage was retrieved, but ranked eighth. Can you fix the order?
- Claim: A reranker scores each retrieved candidate against the question more carefully and reorders them.
- Show: Top 20 candidates → reranker → top 3; Recall@3 before and after, plus the added latency.
- Gotcha: A reranker can't recover a passage that never made the candidate list.
- Takeaway: Retrieve wide, rerank narrow.

**E028 · B · The warranty policy changed in July**
- Hook: The warranty policy changed in July. Why did the assistant quote the March version?
- Claim: Store version and effective dates with each chunk, and select the version that applies to the question's date.
- Show: Two versions of the warranty policy; an August claim answered from version 2, a May claim from version 1.
- Gotcha: Always picking "latest" breaks questions about past periods.
- Takeaway: Freshness is a rule, not a sort by date.

**E029 · C · Query rewriting, multi-query, graph RAG: do you need them?**
- Hook: Should you add query rewriting, multi-query search and graph RAG?
- Claim: Add an advanced technique only to fix a failure pattern you've measured, then confirm it on held-out questions.
- Show: A failure log grouped by cause; one cause (codes like "SB-23-04" asked as "the brake noise bulletin") fixed by query expansion, while the other causes stay unchanged.
- Gotcha: Stacking techniques that each add latency without moving the score.
- Takeaway: Diagnose the miss, then pick the fix.

### Module 5 — Tools and MCP
**Depth:** Core
**Learn:** tool calling, tool design, argument validation, trusted identity, period resolution, tool errors, MCP.
**Build:** three narrow tools (`service_revenue`, `warranty_claims`, `policy_search`) backed by parameterized SQL; a period resolver with fiscal-year rules; explicit tool outcomes; the same tools exposed through a small MCP server.
**Checkpoint:** a tampered dealer argument has no effect, "last quarter" resolves correctly, and another MCP client can call `service_revenue`.

**E030 · C · Can AI actually run code?**
- Hook: Can a model actually run code?
- Claim: The model only requests a tool; your code decides whether and how to run it.
- Show: Sequence diagram: request → validate → execute → result → answer.
- Gotcha: Describing the model as having "executed" something.
- Takeaway: The model asks; the app acts.

**E031 · B · Why AI keeps calling the wrong tool**
- Hook: Why does the model keep calling the wrong tool?
- Claim: Names, descriptions and typed parameters are the tool's interface for the model, so write them like docs for a new colleague.
- Show: `service_revenue(period_start, period_end, pay_type)` vs. a vague `query_data(sql)`; tool choice on five questions.
- Gotcha: Overlapping tools, or one tool that does everything.
- Takeaway: One clear purpose per tool.

**E032 · B · What if the AI asks for another dealer's data?**
- Hook: What if the model passes `dealer_id="b"`?
- Claim: Validate every argument, and take dealer identity from the authenticated session — never from the model.
- Show: Tampered call has no effect; dealer injected by the server; malformed date rejected with a helpful error.
- Gotcha: Putting `dealer_id` in the tool schema at all.
- Takeaway: Identity never comes from the model.

**E033 · C · What does "last quarter" mean on 3 January?**
- Hook: What does "last quarter" mean on 3 January?
- Claim: Convert relative time into explicit periods in code, and ask a clarifying question when it's ambiguous.
- Show: Resolver for "last month," "Q1," "YTD" with a fiscal-year rule; "compare March" with no year triggers a question.
- Gotcha: Letting the model guess today's date.
- Takeaway: Pass the date in; resolve periods deterministically.

**E034 · B · Does "no data" mean zero revenue?**
- Hook: Does "no data" mean zero service revenue?
- Claim: Tools should return explicit outcomes — value, no records, or error — with messages the model can act on.
- Show: An empty month returns `no_records`; the answer says so instead of "0 MYR"; a validation error tells the model the correct format.
- Gotcha: Returning raw stack traces to the model.
- Takeaway: Errors are instructions; make them actionable.

**E035 · C · What is MCP, really?**
- Hook: Why rewrite the same integration for every AI app?
- Claim: The Model Context Protocol is an open standard for connecting AI applications to tools, data and prompts through servers.
- Show: Diagram: AI application (host and client) ↔ MCP servers exposing tools, resources and prompts.
- Gotcha: Assuming MCP makes a tool secure.
- Takeaway: MCP standardizes the connection; you still own authorization.

**E036 · B · Let any AI app use your tools**
- Hook: Can another AI app use your service revenue tool?
- Claim: Wrapping existing tools in an MCP server makes them reusable across clients.
- Show: A small MCP server exposing `service_revenue`, connected to a client and called (label SDK version and date).
- Gotcha: Exposing broad database access because it's easy.
- Takeaway: Same narrow tools, new doorway.

### Module 6 — Context engineering
**Depth:** Practical introduction
**Learn:** context as a finite budget, assembling context in code, preload vs. just-in-time, compaction, clearing tool results, external memory.
**Build:** `build_context()` with named sections and a token budget report; compaction at a threshold; clearing old results from the Module 5 tools; a notes file the assistant reads across sessions.
**Checkpoint:** a 20+ turn conversation that keeps a constraint from turn 2, with a token breakdown before and after.

**E037 · C · Turn 2: ringgit. Turn 20: dollars. Why?** *(pilot, scripted in Section 10)*
- Hook: On turn 2 I said "amounts in ringgit." On turn 20 my agent answered in dollars. Why?
- Claim: The model only sees its context window; context engineering is deciding what goes in, in what form, and when.
- Show: Animated window filling with tool results until the currency instruction is trimmed; fixed version with a pinned constraints section.
- Gotcha: Thinking it just means writing longer prompts.
- Takeaway: The model only knows what's in the window.

**E038 · C · Why not send the AI everything?**
- Hook: If models accept huge contexts, why not send every manual?
- Claim: Extra context costs money and latency, and can dilute the model's attention to what matters.
- Show: The same question with 2 relevant passages vs. 2 relevant plus 40 irrelevant; accuracy, tokens and latency on a small labeled set.
- Gotcha: Treating the maximum window size as the useful size.
- Takeaway: Every token should earn its place.

**E039 · B · Where does each part of your prompt come from?**
- Hook: Where does each part of your prompt actually come from?
- Claim: Assemble context in one function from named sources, with a budget.
- Show: `build_context()` with rules, dealer facts, tool definitions and history; a printed budget report per section.
- Gotcha: Prompt strings concatenated in five different files.
- Takeaway: One function owns the context.

**E040 · C · Should AI read every manual first?**
- Hook: Should the assistant read every policy before answering?
- Claim: Preload small, stable facts; give the model tools to fetch large or changing information when it needs it.
- Show: Six policies preloaded vs. the `policy_search` tool; tokens per question compared.
- Gotcha: Just-in-time fetching adds steps and latency.
- Takeaway: Load identifiers; fetch contents.

**E041 · B · Keeping a 50-turn chat from overflowing**
- Hook: How do you keep a 50-turn session from overflowing?
- Claim: Compaction summarizes older turns while preserving decisions, constraints and open tasks.
- Show: Compaction triggered at a token threshold; the summary keeps "currency = MYR" and the open warranty question.
- Gotcha: A summary that drops the one constraint that mattered.
- Takeaway: Test what your summary must keep.

**E042 · B · What's really eating your context?**
- Hook: What is actually eating your context?
- Claim: Raw tool outputs are often the largest consumer; keep the conclusion, drop the bulk.
- Show: Token breakdown before and after replacing old repair-order tables with one-line summaries and references.
- Gotcha: Clearing a result the model still needs.
- Takeaway: Keep findings, not payloads.

**E043 · C · How can AI remember across sessions?**
- Hook: How can an assistant remember across sessions?
- Claim: Memory is external storage the application writes and reads — notes, files, records — not the model learning.
- Show: The assistant writes a notes file with progress on a warranty review; a fresh session reads it and continues.
- Gotcha: Saving unverified model claims as facts, or mixing dealers in one memory store.
- Takeaway: Memory is data; govern it like data.

### Module 7 — Caching and CAG
**Depth:** Practical introduction
**Learn:** response caching, provider prefix caching and KV-state reuse; the cache-augmented generation (CAG) idea of preloading a bounded corpus; measuring cold and warm requests; invalidation when versions or permissions change.
**Build:** stable-prefix ordering; a preload variant that puts the six policies in the prompt; prefix caching where the provider supports it, with hits verified from usage fields; dealer- and version-aware keys for response caching.
**Checkpoint:** the context reuse experiment report (Section 6), plus passing tests that a policy version change and a permission change both stop stale reuse.

**Lab steps**
1. Freeze one authorized policy corpus, model and question set.
2. Run retrieval per request.
3. Run full preload with no caching.
4. Add supported prefix caching, or local KV reuse if you run a local model.
5. Verify cache hits from usage data, and measure cold and warm requests separately.
6. Change a policy version and a dealer's permissions, and test invalidation.

If you can't verify cache hits, label the run uncached.

**E044 · C · "We cache it." Cache what, exactly?**
- Hook: "We cache it" — but cache what, exactly?
- Claim: A response cache stores final answers, a prefix cache reuses processed prompt prefixes, and KV reuse keeps a model's internal state, and each goes stale in a different way.
- Show: One request path with the three caches marked where they sit, each labeled with what it stores and what makes it stale.
- Gotcha: A response cache keyed without the dealer serves one dealer's answer to another.
- Takeaway: Name the cache before you trust it.

**E045 · B · Stop paying twice for the same prompt**
- Hook: Why pay full price for the same system prompt on every call?
- Claim: Putting stable content first lets a supporting provider reuse the prefix, and the usage fields show whether it did.
- Show: Stable prefix → variable suffix; a cold first call vs. a warm second call, with cached-token counts and latency from usage (label the SDK and date).
- Gotcha: A timestamp at the top of the prompt breaks the cache every time.
- Takeaway: No verified cache hit, no caching claim.

**E046 · B · Everything fits in the window. Still need RAG?**
- Hook: All six policies fit in the window. Do you still need retrieval?
- Claim: For a small, stable, authorized corpus, preloading with cache reuse can match retrieval in fewer steps, so measure quality, freshness and cost on the same questions.
- Show: The same 15 questions by retrieval and by preload: quality, tokens, cold and warm latency; then a warranty policy update shows which approach goes stale.
- Gotcha: Preloading documents a dealer isn't allowed to see, or keeping the cache after a policy changes.
- Takeaway: Choose by corpus size, change rate and permissions.

### Module 8 — Agents
**Depth:** Practical introduction
**Learn:** workflows vs. agents, workflow patterns, the agent loop with enforced limits, comparing approaches, agentic search, subagents and multi-agent trade-offs, plan state.
**Build:** a minimal agent loop with a step limit, deadline and allowed-tool validation from its first version; a fixed workflow for the same questions; a comparison on 15 cases; an agentic search variant of policy lookup; a policy research subagent; a task list in agent state.
**Checkpoint:** a table comparing agent and workflow on success, steps, cost and latency, and a test where the loop hits its step limit and returns an explicit incomplete outcome.

**Framework note.** Once the hand-built loop passes its checkpoint, consider two extra lessons after E050: the same agent rebuilt in LangGraph and run on the same 15 cases, then a Concept episode on framework vs. hand-built (lines of code, debuggability, test results, what happened when something broke). Decide when you reach this module; agent frameworks change quickly. They are not in the 87 yet.

**E047 · C · Who decides the next step: your code or AI?**
- Hook: Who decides the next step — your code or the model?
- Claim: Workflows follow paths you define; agents choose their own actions in a loop. Start with workflows.
- Show: The same question handled by fixed routing and by a dynamic tool loop.
- Gotcha: Calling every LLM app an agent.
- Takeaway: Add autonomy only where you can't predict the path.

**E048 · C · Do you need an agent, or just a pipeline?**
- Hook: Do you need an agent, or just a pipeline?
- Claim: Prompt chaining, routing, parallelization, orchestrator-workers and evaluator-optimizer cover most tasks.
- Show: One small diagram per pattern, each mapped to a service-analyst task (demonstrate one; the rest go in the article).
- Gotcha: Over-engineering a task one call could do.
- Takeaway: Pick the simplest pattern that works.

**E049 · B · What an AI agent actually is, in code**
- Hook: What actually is an agent, in code?
- Claim: An agent is a model choosing tools in a loop that your code runs, so your code also sets the step limit, deadline and allowed tools.
- Show: A minimal Python loop answers "How did March warranty work compare to customer-paid work?"; a forced repeat hits the 6-step limit and returns "incomplete"; an unlisted tool is rejected.
- Gotcha: A loop whose only exit is the model deciding it's done.
- Takeaway: An agent is a loop you control.

**E050 · B · Did the agent beat the simple pipeline?**
- Hook: Did the agent beat the workflow?
- Claim: Compare on success, steps, cost and latency — not impressions.
- Show: Results table from 15 labeled cases.
- Gotcha: Agents often cost more for the same accuracy.
- Takeaway: Keep the simpler one unless the numbers say otherwise.

**E051 · B · Index everything, or let the agent search?**
- Hook: Index everything in advance, or let the agent search?
- Claim: Indexed retrieval is fast for large, stable collections; agentic search with tools suits changing or structured sources.
- Show: The same warranty question through the Module 4 pipeline and through the agent calling `policy_search` several times; steps, latency and accuracy.
- Gotcha: Agentic search can be slow and expensive.
- Takeaway: Choose by corpus and latency needs.

**E052 · C · When five agents are worse than one**
- Hook: Why would an agent call another agent — and when are five agents worse than one?
- Claim: A subagent explores in its own fresh context and returns a short result; multiple agents help with independent reading, not shared decisions.
- Show: The main agent delegates "find the warranty mileage rule" and gets three lines back; two agents editing one report produce conflicting totals.
- Gotcha: Splitting tightly coupled work, or forgetting to pass the context the subagent needs.
- Takeaway: Parallelize reading; centralize deciding.

**E053 · B · How an agent stays on track for 15 steps**
- Hook: How does an agent stay on track over 15 steps?
- Claim: An explicit task list in the agent's state keeps long work focused and makes progress visible.
- Show: Agent writes a task list for a monthly warranty review, updates statuses, and the trace shows each change.
- Gotcha: A plan nothing ever checks.
- Takeaway: Make progress observable.

### Module 9 — Harness engineering
**Depth:** Practical introduction
**Learn:** what a harness is, budgets beyond step counts, permissions and approvals, sandboxing, hooks, traces and checkpoints, how real agent products are built.
**Build:** time, token and cost budgets alongside the Module 8 step limit; risk-tiered tools with an approval gate; a sandboxed code tool; pre- and post-tool hooks; JSON traces with checkpoint and resume.
**Checkpoint:** a budget overrun stopped by the harness, an approval pause, a blocked out-of-scope action, and a resumed task.

**E054 · C · Same model, two products, very different results**
- Hook: Same model, two products, very different reliability. Why?
- Claim: The harness — the code that runs the loop, assembles context, executes tools and enforces limits — shapes behavior as much as the model does.
- Show: Diagram: model at the centre, surrounded by loop, context manager, tool executor, permission gate, budgets and logger.
- Gotcha: Crediting or blaming the model for harness decisions.
- Takeaway: The model is the engine; the harness is the car.

**E055 · B · One step cost more than the other five combined**
- Hook: The agent stopped after 6 steps, but one step cost more than the other five combined. Now what?
- Claim: Step limits aren't enough; enforce time, token and cost budgets in code, and end with an explicit outcome when any runs out.
- Show: A huge repair-order export exceeds the token budget at step 3; the harness stops and returns "incomplete: token budget" with what it found so far.
- Gotcha: "Please be concise" in the prompt as your cost control.
- Takeaway: Limits live in code.

**E056 · B · Should the agent send that report without asking?**
- Hook: Should the agent send that report to the dealer principal without asking?
- Claim: Classify tools by consequence: read freely, ask before side effects, block what's never allowed.
- Show: `export_report` pauses for approval and resumes after a yes; a forbidden tool is blocked.
- Gotcha: Asking for approval on everything until users click yes without reading.
- Takeaway: Gate by consequence.

**E057 · C · What if the agent runs a dangerous command?**
- Hook: What if the agent runs a dangerous command?
- Claim: Run code-executing tools in an isolated environment with limited files and network.
- Show: Container with no network and a read-only mount; a write attempt fails safely.
- Gotcha: Trusting the model to avoid harmful commands.
- Takeaway: Contain the blast radius.

**E058 · B · Enforcing a rule every single time**
- Hook: How do you enforce a rule every single time?
- Claim: Hooks run your code on events — before or after a tool call — to log, block or redact deterministically.
- Show: A pre-tool hook blocks an out-of-scope query; a post-tool hook redacts a customer's IC number and phone number.
- Gotcha: Putting enforcement in prompts.
- Takeaway: If it must always happen, make it a hook.

**E059 · B · Step 9 of 10 failed. Start over?**
- Hook: Step 9 of 10 failed. Where did it go wrong — and do you start over?
- Claim: A trace of each step's tool, arguments, result and timing shows what went wrong, and a checkpoint after each step lets you resume from there.
- Show: A JSON trace pinpoints the bad argument at step 3; a simulated crash at step 9 resumes from the step-8 checkpoint.
- Gotcha: Replaying a side effect twice on resume.
- Takeaway: Log actions, and make side effects safe to repeat.

**E060 · C · What's inside the coding agents everyone uses?**
- Hook: What's inside the coding agents everyone uses?
- Claim: Coding agents combine every harness piece: context files, tools, permissions, sandboxes, hooks, subagents and compaction.
- Show: Annotated diagram mapping product features to harness concepts (state the date observed).
- Gotcha: Copying features without the problem they solve.
- Takeaway: Learn harnesses by reading good ones.

### Module 10 — Skills
**Depth:** Practical introduction
**Learn:** what a skill is, progressive disclosure, choosing between skills, tools, MCP and subagents, writing a skill with a bundled script, testing whether it triggers, trust.
**Build:** a `monthly-service-report` skill with `SKILL.md`, a variance script and a report template; a 10-prompt trigger test.
**Checkpoint:** the skill triggers on relevant prompts, stays quiet on unrelated ones, and produces the same totals as your tools.

**E061 · C · Teach an agent your procedure without a giant prompt**
- Hook: How do you teach an agent your service team's procedure without a giant prompt?
- Claim: A skill is a folder of instructions, scripts and resources that an agent discovers and loads when relevant.
- Show: Folder tree: `SKILL.md` with name and description, `scripts/`, `templates/`.
- Gotcha: Treating a skill as just a long prompt.
- Takeaway: Skills are procedures, packaged.

**E062 · C · 50 skills, one context window**
- Hook: Can an agent have 50 skills without filling its context?
- Claim: Only each skill's name and description sit in context; the full instructions and extra files load only when needed.
- Show: Three levels — description, `SKILL.md` body, referenced files — with token counts at each.
- Gotcha: A vague description means the skill never triggers.
- Takeaway: The description is the trigger.

**E063 · C · Skill, tool, MCP or subagent?**
- Hook: Four ways to add capability. Which one?
- Claim: Tools perform actions, MCP connects systems, skills teach procedures, subagents isolate work.
- Show: Decision table with a service-analyst example for each.
- Gotcha: Using a skill for something that needs enforced permissions.
- Takeaway: Match the mechanism to the need.

**E064 · B · Making the monthly service report repeatable**
- Hook: How do you make "monthly service report" repeatable?
- Claim: A precise description, step-by-step instructions, and a bundled script for the parts that must be exact.
- Show: Build the skill; the warranty vs. customer-paid variance table comes from the script, and the model writes the commentary around it.
- Gotcha: A skill can run code, so a skill you haven't read is code you haven't reviewed.
- Takeaway: Write it like onboarding notes for a new hire.

**E065 · B · Does the agent use your skill only when it should?**
- Hook: Does the agent use your skill when it should — and only then?
- Claim: Test triggering with should-use and should-not-use prompts, like a classifier.
- Show: 10 prompts, trigger table, improved description, rerun.
- Gotcha: Testing only the happy prompt.
- Takeaway: Evaluate the description, not just the output.

### Module 11 — Evaluation
**Depth:** Core
**Learn:** grader types, model-judge limits, trajectory evaluation, development vs. held-out sets, CI. This module consolidates the evals you started in Modules 1 and 2.
**Build:** dev and held-out sets for answers and agent runs, drawn from earlier modules; code, rubric and model graders; trajectory checks; offline tests in GitHub Actions.
**Checkpoint:** a deliberately broken change is blocked by CI, and a held-out score is reported with its sample size.

**E066 · B · How do you grade an explanation?**
- Hook: How do you score an explanation, not just a number?
- Claim: Use code graders for exact values, rubrics for written answers, and model graders only where they've been checked.
- Show: One warranty question scored three ways.
- Gotcha: Graders so strict they reject valid alternative wordings.
- Takeaway: Use the cheapest grader that's reliable.

**E067 · C · Should another AI be the judge?**
- Hook: Should another model be the final authority?
- Claim: A model judge is another imperfect model; calibrate it against human labels.
- Show: Judge vs. human labels on 20 answers; agreement and disagreements.
- Gotcha: Trusting judge scores you never validated.
- Takeaway: Check the judge before trusting it.

**E068 · B · Right answer, wasteful route**
- Hook: The answer was right — but did the agent get there sensibly?
- Claim: Agent evals check outcomes plus the path: tools used, steps, errors and budget.
- Show: Two runs with the same answer — one efficient, one with 9 wasted calls.
- Gotcha: Requiring one exact path when several are valid.
- Takeaway: Score the outcome; inspect the path.

**E069 · B · Did I improve, or just overfit?**
- Hook: Did you improve, or just overfit to your examples?
- Claim: Tune on the development set; report on a held-out set you never iterate against.
- Show: Dev score rises while held-out stays flat.
- Gotcha: Peeking at held-out failures and fixing them.
- Takeaway: Reserve the test set before you start.

**E070 · B · Stop a bad change before it ships**
- Hook: How do you stop a bad change before it ships?
- Claim: Run deterministic and authorization checks on every change; run paid model evals separately with spending limits.
- Show: A broken fixture fails the CI check.
- Gotcha: Paid API calls on every push.
- Takeaway: Offline checks on every commit; live evals on purpose.

### Module 12 — Safety and production
**Depth:** Core
**Learn:** prompt injection, authorization below the model, isolation testing across every data path, observability, cost per successful task, model choice.
**Build:** an injected service bulletin; access checks on retrieval, citations, traces and caches; request IDs and structured logs; a two-model comparison; Docker packaging.
**Checkpoint:** 20 adversarial cases with expected outcomes, and a cost-per-successful-task comparison.

**E071 · C · Can a document give your agent orders?**
- Hook: Can a service bulletin give your agent orders?
- Claim: Retrieved text and tool results are untrusted data, not instructions.
- Show: A planted instruction in a synthetic bulletin; the system treats it as evidence and permissions don't change.
- Gotcha: Believing a stronger system prompt solves it.
- Takeaway: Untrusted input can't grant permissions.

**E072 · B · Is a polite refusal proof nothing leaked?**
- Hook: Is a polite refusal proof that no data leaked?
- Claim: Enforce access in services and queries; a refusal message doesn't show protected rows were never fetched.
- Show: Cross-dealer attempt blocked at the query layer, confirmed in the database log.
- Gotcha: Guardrail filtering standing in for access control.
- Takeaway: Enforce access where the data lives.

**E073 · B · Could Dealer B see Dealer A's data?**
- Hook: Could Dealer B see Dealer A's citations, traces or cached answers?
- Claim: Test every path to data — retrieval, citation links, traces and caches — not just the chat.
- Show: Four direct tests, including a cache key without the dealer failing first (show one; the rest go in the article).
- Gotcha: Testing only through the conversational interface.
- Takeaway: Test below the conversation.

**E074 · B · "The assistant is slow today." Where do you look?**
- Hook: "The assistant is slow today." Where do you look?
- Claim: Request IDs, structured logs and per-step timings separate model, tool and database problems.
- Show: Follow one slow request through its logs to a slow query.
- Gotcha: Treating HTTP success as answer quality.
- Takeaway: Measure operations and quality separately.

**E075 · C · Is the cheapest model the cheapest result?**
- Hook: Is the cheapest model the cheapest result?
- Claim: Measure cost per successful task, including retries and failures, not cost per call.
- Show: Two configurations: the cheaper per call costs more per success.
- Gotcha: Comparing list prices only.
- Takeaway: Price outcomes, not calls.

### Module 13 — Fine-tuning: SFT, LoRA and QLoRA
**Depth:** Guided experiment
**Learn:** when fine-tuning is the right fix, supervised fine-tuning, LoRA adapters, QLoRA and training memory, preparing adaptation data, comparing an adapter with prompting.
**Build:** one bounded LoRA run on synthetic repair-order categorization (the Module 1 data, extended to 200–500 examples in English and Malay), compared with zero- and few-shot prompting of the same base model.
**Checkpoint:** the adaptation experiment report: held-out macro-F1, invalid outputs, trainable parameters, peak memory and the saved run configuration. Run QLoRA only where your measured hardware supports it; otherwise mark it deferred.

**Lab steps**
1. Record your actual RAM, VRAM and runtime support.
2. Choose a small, licensed model, or a budgeted cloud GPU.
3. Prepare 200–500 diverse examples and group templates before splitting.
4. Measure the base model with zero- and few-shot prompting.
5. Run a short LoRA smoke test, then record trainable parameters and peak memory.
6. Train the adapter and evaluate it on held-out examples.
7. Attempt QLoRA only if supported.

On out-of-memory errors, reduce model size, sequence length or batch size, or use gradient accumulation.

**E076 · C · Should you fine-tune to fix wrong answers?**
- Hook: Should you fine-tune to fix wrong answers?
- Claim: Match the fix to the failure: retrieval for missing facts, code for arithmetic, prompts or skills for procedures, fine-tuning for consistent behavior you can measure.
- Show: Three observed errors mapped to three different fixes.
- Gotcha: Fine-tuning to teach facts that change monthly, like warranty terms.
- Takeaway: Diagnose before you train.

**E077 · C · Teach AI your repair categories, cheaply**
- Hook: Can you teach a model your repair categories without retraining billions of parameters?
- Claim: Supervised fine-tuning learns from input-output examples; LoRA freezes the base model and trains small low-rank update matrices instead.
- Show: A frozen weight matrix beside two thin trainable matrices; trainable vs. total parameter count for one small model.
- Gotcha: Expecting a few hundred examples to add new facts rather than shape output behavior.
- Takeaway: Adapters change behavior cheaply; retrieval supplies facts.

**E078 · C · Why training needs far more memory than running**
- Hook: Why does a model need far more memory to train than to run?
- Claim: Training holds weights, gradients, optimizer state and activations; QLoRA saves memory by keeping the frozen base in 4-bit and training only the adapters.
- Show: Stacked memory bars for full fine-tuning, LoRA and QLoRA at one model size, with the assumptions labeled.
- Gotcha: 4-bit training depends on your GPU and library support; check before planning around it.
- Takeaway: Measure your hardware before choosing the method.

**E079 · B · 97% accurate, but was the test in training?**
- Hook: The fine-tuned model scored 97%. Were the test examples also in training?
- Claim: Consistent formatting, checked labels and template-grouped splits decide whether an adapter's score means anything.
- Show: Examples in chat-format JSONL; a label audit catches six mislabeled rows; a group split by template; a class balance table.
- Gotcha: Generating synthetic examples from one template and testing on its near-copies.
- Takeaway: Clean data beats more epochs.

**E080 · B · Fine-tuning vs. a well-written prompt**
- Hook: Did fine-tuning beat a well-written prompt?
- Claim: Compare the adapter with zero- and few-shot prompting of the same base model on held-out examples, not on training loss.
- Show: The smoke test, then the short training run; a table of macro-F1, invalid outputs, latency and memory for zero-shot, few-shot and LoRA.
- Gotcha: Training loss falling while the held-out score stays flat means memorizing, not learning.
- Takeaway: Keep the adapter only if it wins on held-out data.

### Module 14 — Local inference and quantization
**Depth:** Guided experiment
**Learn:** quantization, memory for weights and the KV cache, local runtimes, a stable serving interface, latency and throughput.
**Build:** a small local model behind the same `ModelClient` adapter from Module 0; two model or precision configurations compared.
**Checkpoint:** the inference experiment report: task quality, peak memory, cold and warm latency and bounded concurrency for two configurations, with runtime versions.

**Lab steps**
1. Record your actual hardware.
2. Choose a supported model and runtime.
3. Estimate memory for weights, KV cache and runtime overhead before loading.
4. Run local inference behind the existing adapter, keeping the endpoint schema unchanged.
5. Compare two configurations at 1, 4 and 8 concurrent requests, cold and warm.

**E081 · C · 16-bit or 4-bit: what do you lose?**
- Hook: Same model at 16-bit or 4-bit. What do you lose?
- Claim: Quantization stores weights at lower precision to cut memory, with a quality cost you have to measure on your own task.
- Show: Memory for one model at 16, 8 and 4 bits (labeled estimates); accuracy at two precisions on the repair-order set.
- Gotcha: Lower precision isn't always faster; it depends on your hardware and runtime.
- Takeaway: Measure quality and speed on your own device.

**E082 · C · It loaded fine, then ran out of memory**
- Hook: The model loaded fine. Why did it run out of memory on long prompts?
- Claim: Serving needs memory for the weights plus a KV cache that grows with context length and concurrent requests.
- Show: A memory bar with fixed weights and a KV cache growing as context and concurrent users increase.
- Gotcha: Sizing hardware from the model file size alone.
- Takeaway: Budget memory for context and concurrency, not just weights.

**E083 · B · Swap in a local model without touching the app**
- Hook: Can you swap a hosted model for one on your own machine without touching the app?
- Claim: Because only the adapter knows the provider, a local runtime plugs in behind the same interface and tests.
- Show: Switch one environment variable from hosted to local; the same eval runs; outputs and latency compared (label runtime, model and date).
- Gotcha: Some local models lack reliable tool calling or structured output; check before switching.
- Takeaway: The adapter from Module 0 pays off here.

**E084 · B · Faster per request, or more requests per minute?**
- Hook: Faster per request, or more requests per minute?
- Claim: Latency is how long one request takes; throughput is how much work finishes per minute; choose a configuration on quality and both, measured on your device.
- Show: Two configurations at 1, 4 and 8 concurrent requests: cold and warm latency, throughput and eval score.
- Gotcha: Benchmarking one warm request and calling it production performance.
- Takeaway: Choose with the full table, not the fastest number.

### Module 15 — Capstone
**Depth:** Core
**Learn:** presenting checkable answers, demonstrating safeguards, reporting results with their limits.
**Build:** combine the modules; add a polished CLI or minimal UI for a service manager; run the held-out evaluation once without tuning on it; write a reproducible README; record a five-minute demo you can show in an interview.
**Checkpoint:** the capstone assessment in Section 9.

**E085 · B · An AI answer you can actually check**
- Hook: What does a service manager need to trust a result?
- Claim: Show the period, currency, metric definition (warranty, customer-paid or internal), evidence and a trace link with every answer.
- Show: One complete answer, then its trace.
- Gotcha: Hiding uncertainty to look polished.
- Takeaway: Make answers checkable.

**E086 · B · Proof my safeguards actually work**
- Hook: Can you prove your safeguards work?
- Claim: Show a real broken change being blocked by a meaningful test.
- Show: Pull request, failing check, the test that caught it, the fix.
- Gotcha: Demonstrating only green builds.
- Takeaway: Show the safety net catching something.

**E087 · C · What my AI service analyst can do, and can't**
- Hook: What can this service analyst agent actually do now?
- Claim: Credible engineering shows results with sample sizes alongside known limitations.
- Show: Scorecard plus three known limitations and the next extension.
- Gotcha: Implying a prototype is production-ready.
- Takeaway: Pick one next build with a measurable goal.

---

## 9. Capstone assessment
Proposed learning targets, not industry standards. Freeze them before the final evaluation.

- **Question resolution:** at least 95% of held-out questions select the right tool and resolve the right period, dealer scope, pay type and currency. (Arithmetic itself is done by code and covered by unit tests.)
- **Dealer isolation:** 100% of defined authorization cases pass across retrieval, citations, traces and caches. Any exposure blocks completion.
- **Retrieval:** one controlled improvement, with passage recall and answer support measured separately.
- **Grounding:** at least 90% of answerable policy questions include a supporting citation that contains the claimed fact.
- **Abstention:** at least 90% of unanswerable cases abstain with a useful reason.
- **Context reuse:** verified cache hits, distinct cold and warm results, and passing freshness and permission-change tests.
- **Harness control:** every defined failure scenario (loops, budget overruns, timeouts, tool errors, denied approvals) ends in a bounded, explicit outcome.
- **Skill triggering:** the skill triggers on all should-use prompts and none of the should-not-use prompts in the test set.
- **Adaptation (guided):** baseline prompting and a trained adapter compared on independent cases, with hardware documented and unsupported QLoRA marked deferred.
- **Inference (guided):** quality and resources compared for two supported configurations.
- **Reproducibility:** a clean setup runs all offline checks from the README.
- **Explanation:** defend three design decisions and state three known limitations, as you would in an interview.

Report sample sizes with every percentage. A score from a handful of cases doesn't generalize.

---

## 10. Pilot: Day 1 plus four lessons before committing to a schedule

| Episode | Type | Why it's in the pilot |
|---|---|---|
| Day 1 | Journey | Sets the goal; measures on-camera recording time |
| E001 Why AI demos break in real life | C | Diagram-only; measures concept production time |
| E037 Turn 2: ringgit. Turn 20: dollars. Why? | C | Scripted below; the series' signature topic |
| E012 Should AI add up your service revenue? | B | Scripted below; uses existing worked code |
| E014 What users see when your AI app breaks | B | Measures demo preparation for a real API |

For each, record: scripting time, demo preparation, recording takes, editing time, final duration.

### Pilot script — E012 · B · Should AI add up your service revenue?
**Recording setup:** Module 2 project at a tagged commit; the fixture below; terminal and editor at a readable font size. The hook answer must be a real captured output: give a model all four rows with no dealer filter and ask for Dealer A's March service revenue. If the model gets it right, change the hook line to "Would you trust this?" and keep the rest. Never present a constructed answer as a real model output.

**0:00–0:15 · Hook**
*Screen: you on camera; then chat answer "Dealer A's March service revenue was 10,249 MYR."*
> Day twenty-three. I asked an AI for a dealership's March service revenue. Ten thousand two hundred forty-nine ringgit. Confident, nicely formatted — and wrong. Let's see why.

**0:15–0:45 · Claim**
*Screen: two-column table. Code: filter, add, check permissions. Model: understand the question, explain the result.*
> A language model predicts likely text. That's great for understanding a question and explaining an answer. But it isn't a calculator, and it doesn't know which records you're allowed to see. So we split the job: code does anything that must be exact, and the model explains what the code returns.

**0:45–1:30 · Show**
*Screen: four rows (A 100, A 200, A −50 warranty credit, B 9999). Then the `service_revenue` function. Then terminal output `250.00`.*
> Here's the data. Dealer A has two repair orders and a fifty ringgit warranty credit. Dealer B has one big job. The wrong answer added everything — including another dealer's data. This function filters by dealer and month, then adds with Python's Decimal type, so amounts like ten sen add up exactly. Result: two hundred fifty ringgit. The model only receives that result, and turns it into a sentence.

**1:30–1:50 · Gotcha**
*Screen: 250.00 highlighted beside 10,249 crossed out.*
> Same data, correct answer, and now it's testable. One limit: this filter is just a function. In the real app, the dealer must come from the signed-in user — never from the model.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding the card "If it must be exact, compute it."*
> If it must be exact, compute it. Next: giving your API a contract.

*About 220 words. Leave reading pauses on the code and output.*

### Pilot script — E037 · C · Turn 2: ringgit. Turn 20: dollars. Why?
**Recording setup:** an animated or stepped diagram of the context window. The before/after must come from a real run of your project: trim history by message count to reproduce the failure, then add a pinned constraints section to fix it. If you can't reproduce the dollar answer, show the trimmed context itself as the failure.

**0:00–0:15 · Hook**
*Screen: you on camera; then turn 2 "All amounts are in ringgit." … turn 20 answer in USD.*
> On turn two, I told my service agent all amounts are in ringgit. On turn twenty, it answered in dollars. Same model, same session. What happened?

**0:15–0:45 · Claim**
*Screen: one horizontal bar labelled "context window", with segments: instructions, tools, history, documents, tool results.*
> A model doesn't remember your conversation the way you do. On every call, it only sees what's inside its context window: instructions, tool definitions, conversation history, documents and tool results. Context engineering is deciding what goes into that window, in what form, and when.

**0:45–1:30 · Show**
*Screen: the bar fills with large repair-order tables; the oldest messages, including "ringgit", slide out. Then the fixed version: a small pinned "Constraints: currency = MYR" block, a short summary of old turns, compressed tool results.*
> Watch the window fill up. Every tool call adds a big table of repair orders. To make room, my app dropped the oldest messages — including the one about ringgit. The fix wasn't a smarter model. It was a better context: keep lasting constraints in a short pinned section, summarize old turns, and shrink bulky tool results down to what they concluded.

**1:30–1:50 · Gotcha**
*Screen: turn 20 now answers in MYR. Small caption: "One scenario; long contexts can also degrade without trimming."*
> After the fix, turn twenty answers in ringgit. One caution: this is a single scenario. Very long contexts can also lose details without any trimming, simply because important information gets diluted.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding the card "The model only knows what's in the window."*
> The model only knows what's in the window. Next: why your context window is a budget.

*About 240 words.*

---

## 11. Worked exercise — first service revenue function
Plain Python, standard library. Use it in E012.

```python
from decimal import Decimal

def service_revenue(rows, dealer_id, reporting_month):
    return sum(
        (
            Decimal(row["amount"])
            for row in rows
            if row["dealer_id"] == dealer_id
            and row["month"] == reporting_month
        ),
        Decimal("0"),
    )

rows = [
    {"dealer_id": "a", "month": "2026-03", "amount": "100.00"},
    {"dealer_id": "a", "month": "2026-03", "amount": "200.00"},
    {"dealer_id": "a", "month": "2026-03", "amount": "-50.00"},
    {"dealer_id": "b", "month": "2026-03", "amount": "9999.00"},
]

assert service_revenue(rows, "a", "2026-03") == Decimal("250.00")
assert service_revenue(rows, "a", "2026-04") == Decimal("0")
```

Teaching convention: amounts are signed repair-order amounts, warranty credits are negative, currency is MYR, and month is the repair-order close month. Decimal adds exactly, but rounding rules for division and tax still need defining. This is a teaching computation, not access control. In the application, `dealer_id` comes from authenticated context and the database enforces the same boundary.

Extend it (Modules 2 and 5):
1. Return an explicit outcome that distinguishes "no records" from "net total is zero."
2. Add currency and reject mixed-currency totals (the Johor dealer's SGD record).
3. Add pay type, and report customer-paid, warranty and internal work separately.
4. Decide and test how duplicate repair-order IDs are handled.
5. Validate malformed amounts and month formats, and return the included repair-order IDs as evidence.

---

## 12. Windows startup checklist
PowerShell and VS Code. Use your installed Python command if `py` isn't available.

```powershell
py --version
mkdir ai-service-analyst
cd ai-service-analyst
git init
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install fastapi uvicorn pytest httpx
.\.venv\Scripts\python.exe -m pip freeze > requirements.txt
```

Create `app/__init__.py`, `app/main.py`, `app/schemas.py`, `app/model_client.py`, `app/service_revenue.py`, `tests/test_api.py` and `tests/test_service_revenue.py`. Add `.venv/`, `__pycache__/`, `.pytest_cache/` and `.env` to `.gitignore`.

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
.\.venv\Scripts\python.exe -m pytest -q
```

Open http://127.0.0.1:8000/health and http://127.0.0.1:8000/docs. These commands don't create the endpoints; the Module 2 build does. Install scikit-learn for Module 1 and the training libraries for Module 13 when you reach them. Check current official docs if syntax differs for your installed versions.

---

## 13. References
Re-check before citing in a video; links and course access terms change. Older videos remain useful for concepts, but their packages, models and demo endpoints may no longer work. Implement from current official docs.

### Core reading (checked 8 October 2026)
| Topic | Reading | Modules |
|---|---|---|
| Agents and workflow patterns | https://www.anthropic.com/engineering/building-effective-agents | 8 |
| Context engineering | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 6, 8 |
| Tool design and tool evals | https://www.anthropic.com/engineering/writing-tools-for-agents | 5, 11 |
| Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 10 |
| Agent Skills open standard | https://agentskills.io/ | 10 |
| Model Context Protocol | https://modelcontextprotocol.io/ | 5 |
| CAG architecture (paper) | https://arxiv.org/abs/2412.15605 | 7 |
| LoRA (PEFT docs) | https://huggingface.co/docs/peft/package_reference/lora | 13 |
| QLoRA-compatible training (PEFT docs) | https://huggingface.co/docs/peft/developer_guides/quantization | 13 |

The last three rows were added in version 6 and checked on 11 October 2026. No verified CAG video is listed; use the paper for the architecture and current provider documentation for caching.

### Video courses
| ID | Course | Link | Modules |
|---|---|---|---|
| V1 | freeCodeCamp: Python API Development (selected sections only) | https://www.youtube.com/watch?v=0sOvCWFmrtA | 2, 12 |
| V2 | Full Stack: LLM Foundations | https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/llm-foundations/ | 0, 1 |
| V3 | DeepLearning.AI: How Transformer LLMs Work | https://www.deeplearning.ai/courses/how-transformer-llms-work | 0, 1 |
| V4 | DeepLearning.AI: Getting Structured LLM Output | https://www.deeplearning.ai/courses/getting-structured-llm-output | 2 |
| V5 | DeepLearning.AI: Evaluating and Debugging Generative AI | https://www.deeplearning.ai/courses/evaluating-debugging-generative-ai | 11 |
| V6 | Full Stack: Augmented Language Models | https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/augmented-language-models/ | 3, 5 |
| V7 | DeepLearning.AI: Building and Evaluating Advanced RAG | https://www.deeplearning.ai/alpha/short-courses/building-evaluating-advanced-rag | 3, 4 |
| V8 | DeepLearning.AI: Advanced Retrieval for AI | https://www.deeplearning.ai/courses/advanced-retrieval-for-ai | 4 |
| V9 | DeepLearning.AI: Function-calling and Data Extraction with LLMs | https://www.deeplearning.ai/courses/function-calling-and-data-extraction-with-llms | 5 |
| V10 | DeepLearning.AI: Evaluating AI Agents | https://www.deeplearning.ai/courses/evaluating-ai-agents | 8, 11 |
| V11 | Hugging Face Agents Course | https://huggingface.co/learn/agents-course/en/unit0/introduction | 8, 9 |
| V12 | DeepLearning.AI: Safe and Reliable AI via Guardrails | https://www.deeplearning.ai/alpha/short-courses/safe-and-reliable-ai-via-guardrails | 12 |
| V13 | Full Stack: LLMOps | https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/llmops/ | 11, 12 |
| V14 | DeepLearning.AI: Finetuning Large Language Models | https://www.deeplearning.ai/courses/finetuning-large-language-models | 13 |
| V15 | Hugging Face smol course (reading and exercises) | https://huggingface.co/learn/smol-course/en/unit0/1 | 13 |
| V16 | DeepLearning.AI: Quantization Fundamentals | https://www.deeplearning.ai/courses/quantization-fundamentals | 14 |
| V17 | Full Stack: UX for Language User Interfaces | https://fullstackdeeplearning.com/llm-bootcamp/spring-2023/ux-for-luis/ | 15 |

V1–V7, V9–V14 and V17 were checked on 7 October 2026. V8, V15 and V16 were added in version 6 and checked on 11 October 2026. Playback and signed-in access weren't tested.

---

## 14. Editorial and technical review
Before publishing an episode:
- Time the final video; split it if it runs well over two minutes.
- One idea per episode, and the screen text is readable on a phone.
- Re-run the demo at its recorded commit; values, currencies and periods match the output.
- Label synthetic data, mocks, live model calls and constructed illustrations clearly.
- Build episodes show the SDK, model identifier and recording date; training and inference episodes also show hardware.
- Evaluation claims state sample size and configuration.
- Describe observed results; never claim universal reliability or security.
- Credit the references used; explain in your own words; don't reuse course scripts or footage.
- No secrets, personal data, employer data, real dealer data or Mercedes data on screen.
- No Mercedes logo, star, fonts, livery or official imagery; the description says the series isn't affiliated with Mercedes-Benz.
- The title follows "Day N · <episode title>", with N counted from the Day 1 publish date.
- Define every technical term at first use.

---

## 15. Tracker

### Per module, record
- Concepts explained in your own words
- Project commit
- Evidence: tests, eval results, one meaningful failure and its cause
- Known limitation
- Episodes scripted, timed and recorded, with actual durations
- Publication links and the Day number each lesson aired

### Per week, record
- Lessons published (target 2) and AI explained or check-in videos (target 1)
- Applications, conversations and interviews, for the check-ins

### Progress
| Module | Learned | Built | Tested | Scripted | Recorded | Published |
|---|---|---|---|---|---|---|
| 0 How LLMs actually work | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 1 ML foundations and baselines | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 2 The application boundary and structured output | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 3 Retrieval | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 4 Retrieval experiments and reranking | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5 Tools and MCP | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 6 Context engineering | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7 Caching and CAG | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 8 Agents | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 9 Harness engineering | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 10 Skills | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 11 Evaluation | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 12 Safety and production | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 13 Fine-tuning: SFT, LoRA and QLoRA | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 14 Local inference and quantization | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 15 Capstone | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

---

## 16. After the series
Choose one extension with a measurable goal, and use the same learn, build, explain structure. Automotive options first:
- **Multimodal:** read dashboard warning-light photos and scanned repair orders, with evaluation.
- **Vehicle telemetry:** classical ML for anomaly detection on synthetic sensor data, with an LLM explaining the flagged cases.
- **Voice in Malay and English:** a service-advisor voice assistant, evaluated on mixed-language requests.
- **Agent engineering:** long-running tasks with durable state, recovery and sandboxed execution.
- **Skills library:** a set of tested skills for after-sales analytics tasks.
- **Advanced adaptation:** distillation or preference tuning (DPO), once the Module 13 baseline is solid.

A finished, measured application is worth more than another framework.
