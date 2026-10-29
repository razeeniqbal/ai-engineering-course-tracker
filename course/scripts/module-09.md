# Module 9 — Harness engineering

## E054 · C · Same model, two products, very different results

**0:00–0:15 · Hook**
*Screen: you on camera; then two AI products side by side, both labelled with the same model name.*
> Two AI products use exactly the same model. One is reliable and pleasant to use. The other forgets things, loops and breaks. If the model is identical, what's actually different?

**0:15–0:45 · Claim**
*Screen: the word "harness" around a model icon.*
> The harness. That's the code around the model that runs the loop, assembles the context, executes tools and enforces the limits. It shapes behaviour just as much as the model does. Two teams can start from the same model and end up with completely different products, because their harnesses make different decisions. When something goes wrong, the harness is usually where you should look first.

**0:45–1:30 · Show**
*Screen: diagram: model at the centre, surrounded by loop, context manager, tool executor, permission gate, budgets and logger, each with a one-line job.*
> Here's the harness I'm building around my service analyst. The loop decides when to call the model and when to stop. The context manager decides what the model sees on each call. The tool executor runs tools safely and formats their results. The permission gate decides what needs approval. Budgets cap time, tokens and money. And the logger records every step so I can debug it later. Swap the model and most of this stays. Remove the harness and even the best model falls apart.

**1:30–1:50 · Gotcha**
*Screen: "The model is bad at long tasks" crossed out, "the loop has no plan or limits" written in.*
> The mistake is crediting or blaming the model for harness decisions. "The model forgot the constraint" often really means "the harness trimmed it from the context". Check the harness first.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "The model is the engine; the harness is the car."*
> The model is the engine; the harness is the car. Next: one step cost more than the other five combined.

## E055 · B · One step cost more than the other five combined

**0:00–0:15 · Hook**
*Screen: you on camera; then a cost-per-step bar chart where step 3 towers over the rest.*
> My agent respected its six-step limit. But one of those steps cost more than the other five combined. A step limit didn't protect me at all. Now what?

**0:15–0:45 · Claim**
*Screen: four meters: steps · time · tokens · cost.*
> Step limits aren't enough on their own. Enforce time, token and cost budgets in code as well. When any one of them runs out, the harness stops the run and returns an explicit outcome, with whatever was found so far.

**0:45–1:30 · Show**
*Screen: a run where a huge repair-order export exceeds the token budget at step 3; the harness stopping and returning "incomplete: token budget" with partial findings. [CAPTURE: your run]*
> Here's the run. At step three, the model asks for every repair order of the year in one tool call. The result is [CAPTURE] tokens, far over my budget of [CAPTURE]. The harness checks the budget before adding the result to the context, stops the run, and returns status "incomplete, token budget exceeded", plus what it had already found: the totals for March. The service manager sees a clear message and a suggestion to narrow the period, not a surprise bill.

**1:30–1:50 · Gotcha**
*Screen: a system prompt saying "Please be concise and economical."*
> The trap is using "please be concise" in the prompt as your cost control. It's a polite request, not a limit, and the model is free to ignore it.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Limits live in code."*
> Limits live in code. Next: should the agent send that report without asking?

## E056 · B · Should the agent send that report without asking?

**0:00–0:15 · Hook**
*Screen: you on camera; then the agent about to email a report to the dealer principal.*
> My agent finished the monthly report and was about to email it straight to the dealer principal. Should it really be allowed to do that without asking first?

**0:15–0:45 · Claim**
*Screen: three tiers: read freely · ask before side effects · block.*
> Classify tools by consequence. Tools that only read data can run freely. Tools with side effects, like sending emails or exporting files, pause and ask a human first. And some actions are never allowed at all. The harness enforces these tiers, not the prompt.

**0:45–1:30 · Show**
*Screen: export_report pausing with an approval card; the user clicking yes; the run resuming. Then a forbidden delete_records tool being blocked. [CAPTURE: your run]*
> Here's it working. The agent calls export report. Because that tool is in the "ask first" tier, the harness pauses the run and shows an approval card: what will be sent, to whom, and why. I click approve, and the run resumes from exactly where it stopped. Then I try a tool from the blocked tier, deleting records. The harness refuses it outright, logs the attempt, and the agent is told it isn't permitted.

**1:30–1:50 · Gotcha**
*Screen: ten approval pop-ups in a row, user clicking "yes" without reading.*
> The opposite trap: asking for approval on everything. People quickly learn to click yes without reading, and the safety check becomes meaningless.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Gate by consequence."*
> Gate by consequence. Next: what if the agent runs a dangerous command?

## E057 · C · What if the agent runs a dangerous command?

**0:00–0:15 · Hook**
*Screen: you on camera; then a code tool about to run "rm -rf" on a shared folder.*
> I gave my agent a tool that runs Python code, so it can do custom analysis on repair data. What happens if it runs something destructive?

**0:15–0:45 · Claim**
*Screen: a sealed box labelled "sandbox" around the code tool.*
> You assume it eventually will, and you make that harmless. Run any code-executing tool inside an isolated environment, a sandbox, with only the files it needs, no network access unless required, and strict time and memory limits. Then the worst case is a failed run, not a damaged system. It's the same principle as giving a new employee access to only what their job needs.

**0:45–1:30 · Show**
*Screen: a container with no network and a read-only mount of one CSV; a write attempt failing safely; a network call failing; a time limit stopping a long loop.*
> Here's my sandbox. The code runs in a container with no network, and a read-only copy of just one file: this month's repair orders. When the agent's code tries to write to that file, it fails with "read-only file system". When it tries to call the internet, the connection is refused. When it writes an accidental infinite loop, the ten-second time limit kills it. In every case, the agent gets a clear error back, and my real data is untouched. That's what makes it safe to give an agent a powerful tool at all.

**1:30–1:50 · Gotcha**
*Screen: a system prompt saying "Never run harmful commands."*
> The mistake is trusting the model to avoid harmful commands because you told it to. Instructions can be misunderstood or overridden. Isolation can't. Assume mistakes will happen, and limit the damage.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Contain the blast radius."*
> Contain the blast radius. Next: enforcing a rule every single time.

## E058 · B · Enforcing a rule every single time

**0:00–0:15 · Hook**
*Screen: you on camera; then a tool result containing a customer's IC number.*
> A customer's IC number showed up in a tool result, and the model repeated it in its answer. My prompt said "never show personal data". How do you enforce a rule every single time?

**0:15–0:45 · Claim**
*Screen: two hooks on a timeline: before tool call · after tool call.*
> With hooks. A hook is your own code that runs automatically on an event, like before or after every tool call. It can log, block or redact deterministically, which means it behaves the same way every time, no matter what the model decides.

**0:45–1:30 · Show**
*Screen: a pre-tool hook blocking a query outside the dealer's scope; a post-tool hook redacting an IC number and phone number before the result reaches the model. [CAPTURE: your run]*
> Two hooks. The pre-tool hook checks every call before it runs. When the model asks for repair orders from all dealers, the hook blocks it and returns "out of scope for this user". The post-tool hook checks every result on the way back. A repair order containing a Malaysian IC number and a phone number comes back, and the hook replaces them with "redacted" before the model ever sees them. So the model can't repeat them, because it never had them.

**1:30–1:50 · Gotcha**
*Screen: "Never reveal IC numbers" in the system prompt, with a leaked number below.*
> The trap is putting enforcement in prompts. Prompts are guidance. If a rule must always hold, it needs code that always runs.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "If it must always happen, make it a hook."*
> If it must always happen, make it a hook. Next: step nine of ten failed — start over?

## E059 · B · Step 9 of 10 failed. Start over?

**0:00–0:15 · Hook**
*Screen: you on camera; then a ten-step run failing at step 9.*
> My agent ran nine steps of a monthly warranty review, and then step nine failed. Where did it actually go wrong? And do I really have to start the whole thing over?

**0:15–0:45 · Claim**
*Screen: a trace of steps with tool, arguments, result and timing; checkpoints after each step.*
> Two tools fix this. A trace records each step's tool, arguments, result and timing, so you can see exactly where things went wrong. And a checkpoint saves the agent's state after each step, so you can resume from the last good one instead of starting again.

**0:45–1:30 · Show**
*Screen: a JSON trace pinpointing a bad date argument at step 3; then a simulated crash at step 9 and a resume from the step-8 checkpoint. [CAPTURE: your trace]*
> Here's the trace as JSON. Reading down, the failure at step nine isn't really at step nine. At step three, the agent passed the wrong month to the warranty claims tool, and every step after that built on the wrong data. Without the trace, I'd never have found that. Next, I simulate a crash at step nine. Because state was checkpointed after every step, I resume from step eight, and only the last two steps run again.

**1:30–1:50 · Gotcha**
*Screen: a report email sent twice after a resume.*
> The danger on resume: replaying a side effect twice, like sending the same report email again. Make side effects safe to repeat, or record that they already happened.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Log actions, and make side effects safe to repeat."*
> Log actions, and make side effects safe to repeat. Next: what's inside the coding agents everyone uses?

## E060 · C · What's inside the coding agents everyone uses?

**0:00–0:15 · Hook**
*Screen: you on camera; then a coding agent working in a terminal.*
> Coding agents can now read a codebase, run tests and fix bugs by themselves. What's actually inside them? It turns out you already know every piece.

**0:15–0:45 · Claim**
*Screen: the harness parts from this module, each lighting up.*
> Coding agents combine every harness piece from this module. Context files that describe the project. Tools for reading, editing and running code. Permissions for risky actions. Sandboxes for running commands. Hooks for rules that must always run. Subagents for exploring in parallel. And compaction for long sessions. None of it is magic. It's good harness engineering. Once you see the pieces, these products stop looking like magic.

**0:45–1:30 · Show**
*Screen: an annotated diagram mapping a coding agent's visible features to harness concepts. State the date observed. [CAPTURE: the product(s) and date you observed]*
> Here's a coding agent's features, mapped to what we've built. The project instructions file it reads at startup: that's preloaded context. Asking before it runs a shell command: a permission gate. Running tests in an isolated environment: a sandbox. Auto-formatting after every edit: a post-tool hook. Sending a helper off to search the codebase: a subagent. Summarising when the session gets long: compaction. Observed on [CAPTURE: date] with [CAPTURE: products]. Features change fast, but the concepts stay. Reading a good product this way is one of the fastest ways to learn.

**1:30–1:50 · Gotcha**
*Screen: a feature list copied into a product with no reason attached.*
> The mistake is copying features without understanding the problem each one solves. A sandbox without a threat model, or hooks without rules, just adds complexity. Ask what each feature protects against.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Learn harnesses by reading good ones."*
> Learn harnesses by reading good ones. Next: teach an agent your procedure without a giant prompt.
