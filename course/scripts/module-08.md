# Module 8 — Agents

## E047 · C · Who decides the next step: your code or AI?

**0:00–0:15 · Hook**
*Screen: you on camera; then two flowcharts: one fixed, one with a loop and a question mark.*
> Everyone's building "AI agents" now. But here's the question that actually matters: in your app, who decides the next step, your code or the model?

**0:15–0:45 · Claim**
*Screen: "Workflow: you define the path" vs "Agent: the model chooses its actions in a loop".*
> That's the real difference between a workflow and an agent. In a workflow, you define the path in code: step one, then two, then three. In an agent, the model chooses its own next action in a loop, until it decides it's done. Workflows are predictable, cheaper and easier to test. Agents are flexible. So start with workflows, and only add autonomy where you genuinely can't predict the path.

**0:45–1:30 · Show**
*Screen: the question "How did Dealer A's March warranty work compare to February?" handled two ways: fixed routing (resolve periods → call warranty_claims twice → compare) and a dynamic tool loop.*
> Same question, two designs. The workflow: my code resolves the two months, calls the warranty claims tool for each, computes the difference, and asks the model to explain it. Four steps, always the same, easy to test. The agent: the model gets the tools and decides what to do. It might call the tool twice, or first check the policy, or ask for a breakdown by model. For this question, the path is completely predictable, so the workflow is the better choice. The agent earns its place when the questions are open-ended.

**1:30–1:50 · Gotcha**
*Screen: a simple chatbot labelled "AI agent" with a question mark.*
> The common mistake is calling every LLM app an agent. A single prompt with a template isn't an agent, and making it one adds cost without adding value.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Add autonomy only where you can't predict the path."*
> Add autonomy only where you can't predict the path. Next: do you need an agent, or just a pipeline?

## E048 · C · Do you need an agent, or just a pipeline?

**0:00–0:15 · Hook**
*Screen: you on camera; then a monthly service report task.*
> I need my assistant to produce a monthly service report for each dealer. Do I need a full agent for that, or would a simple pipeline do the job better?

**0:15–0:45 · Claim**
*Screen: five small icons: chaining · routing · parallelization · orchestrator-workers · evaluator-optimizer.*
> Most tasks fit one of five workflow patterns. Prompt chaining, where each step feeds the next. Routing, where you classify the request and send it down the right path. Parallelisation, where independent parts run at the same time. Orchestrator-workers, where one model splits a task among helpers. And evaluator-optimiser, where one step drafts and another critiques. Pick the simplest pattern that works. Each is easy to test.

**0:45–1:30 · Show**
*Screen: one diagram per pattern mapped to a service-analyst task; the monthly report demonstrated with parallelization.*
> Mapped to my service analyst: chaining is extract a repair order, then validate, then summarise. Routing sends warranty questions one way and revenue questions another. Parallelisation is my monthly report: revenue, warranty claims and top repair categories are computed at the same time, then combined. Orchestrator-workers could split a review of fifty claims into batches. Evaluator-optimiser drafts the report's commentary, then checks it against the numbers. The full report is just parallelisation plus one chain. No agent required. Choosing the pattern first made the design simple and the testing straightforward.

**1:30–1:50 · Gotcha**
*Screen: an elaborate multi-agent diagram for a task one call could do.*
> The mistake is over-engineering: building an orchestrated multi-step system for something a single well-written call could handle. Start with one call, then add structure only when it fails.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Pick the simplest pattern that works."*
> Pick the simplest pattern that works. Next: what an AI agent actually is, in code.

## E049 · B · What an AI agent actually is, in code

**0:00–0:15 · Hook**
*Screen: you on camera; then the word "agent" surrounded by marketing buzzwords.*
> Strip away the marketing. What actually is an AI agent, in code? It's smaller than you think.

**0:15–0:45 · Claim**
*Screen: a while loop: call model → if tool request, run tool → append result → repeat.*
> An agent is a model choosing tools in a loop that your code runs. And because your code runs the loop, your code also sets the limits: a maximum number of steps, a deadline, and a list of allowed tools. Those limits belong in version one, not as an afterthought.

**0:45–1:30 · Show**
*Screen: a ~30-line Python loop answering "How did March warranty work compare to customer-paid work?"; a forced repeat hitting the 6-step limit and returning "incomplete"; an unlisted tool being rejected. [CAPTURE: your run]*
> Here's my whole agent, about thirty lines. The loop calls the model. If the model asks for a tool, my code checks it's on the allowed list, runs it, and adds the result to the conversation. Then it loops. For "how did March warranty work compare to customer-paid work?", it takes [CAPTURE] steps and answers correctly. Now I force a bug that makes it repeat the same call. At step six, the loop stops and returns status "incomplete", with what it found so far. And when the model asks for a tool that isn't allowed, it's rejected and told why.

**1:30–1:50 · Gotcha**
*Screen: "while not done:" with no other exit.*
> The trap is a loop whose only exit is the model deciding it's done. One confused model, and you've got an infinite loop running up a bill.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "An agent is a loop you control."*
> An agent is a loop you control. Next: did the agent beat the simple pipeline?

## E050 · B · Did the agent beat the simple pipeline?

**0:00–0:15 · Hook**
*Screen: you on camera; then "Agent" vs "Workflow" in a boxing-match graphic.*
> I built the same feature twice: once as a fixed workflow, once as an agent. The agent felt smarter. But did it actually win?

**0:15–0:45 · Claim**
*Screen: four columns: success · steps · cost · latency.*
> Compare them on numbers, not impressions: how often each one succeeds, how many steps it takes, what it costs, and how long it takes. Run both on the same labelled cases, and let the table decide. It's the only fair way to compare two designs that feel different. Same cases for both.

**0:45–1:30 · Show**
*Screen: results table from 15 labelled cases for workflow vs agent. [CAPTURE: your table]*
> Fifteen labelled questions about warranty and revenue, run through both. Success rate: workflow [CAPTURE], agent [CAPTURE]. Average steps: [CAPTURE] versus [CAPTURE]. Average cost per question: [CAPTURE] versus [CAPTURE]. Average time: [CAPTURE] versus [CAPTURE] seconds. The agent was better on [CAPTURE: which kinds of questions], and the workflow was better on [CAPTURE]. Overall, for my app, [CAPTURE: your verdict]. Your table might look different, and that's the point of running it.

**1:30–1:50 · Gotcha**
*Screen: "same accuracy, 3× the cost" highlighted.*
> A very common result: the agent reaches the same accuracy, but costs more and takes longer, because it explores steps the workflow never needed. Those extra steps cost real money at scale.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Keep the simpler one unless the numbers say otherwise."*
> Keep the simpler one unless the numbers say otherwise. Next: index everything, or let the agent search?

## E051 · B · Index everything, or let the agent search?

**0:00–0:15 · Hook**
*Screen: you on camera; then two approaches side by side: a search index, and an agent calling a search tool repeatedly.*
> There are two ways to answer from documents. Build a search index in advance, or give an agent a search tool and let it look around. Which one should you use?

**0:15–0:45 · Claim**
*Screen: "Indexed retrieval: large, stable" vs "Agentic search: changing, structured".*
> Indexed retrieval is fast and cheap for large, stable collections: one search, then answer. Agentic search, where the model calls tools several times and refines its queries, suits sources that change often or are structured, like databases or bulletins that update weekly. Pick by your corpus and your latency needs.

**0:45–1:30 · Show**
*Screen: the same warranty question through the Module 4 pipeline and through the agent calling policy_search several times; steps, latency and accuracy compared. [CAPTURE: your numbers]*
> Same question: "Is a commercially used vehicle covered for brake work?" Through my Module 4 pipeline, it's one search, one answer, [CAPTURE] seconds, and it's correct. Through the agent, it searches, reads, searches again for the commercial-use exception, and answers in [CAPTURE] steps and [CAPTURE] seconds. Across fifteen questions, accuracy is [CAPTURE] versus [CAPTURE]. For my six stable policies, [CAPTURE: which wins].

**1:30–1:50 · Gotcha**
*Screen: an agent making 9 search calls for one question.*
> The catch with agentic search: it can be slow and expensive, especially when the model keeps searching because it isn't sure it's found enough.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Choose by corpus and latency needs."*
> Choose by corpus and latency needs. Next: when five agents are worse than one.

## E052 · C · When five agents are worse than one

**0:00–0:15 · Hook**
*Screen: you on camera; then a diagram of five agents all connected to each other.*
> Why would an agent call another agent? And when does splitting work across five agents make your system worse than just using one?

**0:15–0:45 · Claim**
*Screen: "Subagent: fresh context, short result" and "Multi-agent: good for independent reading, bad for shared decisions".*
> A subagent is a helper that explores in its own fresh context and returns just a short result, so the main agent's context stays clean. Multiple agents help when the work is independent, like reading different documents in parallel. They hurt when the work is tightly coupled, like several agents making decisions about the same report. Coordination between agents is where most multi-agent systems break.

**0:45–1:30 · Show**
*Screen: the main agent delegating "find the warranty mileage rule" to a subagent and getting three lines back; then two agents editing one report and producing conflicting totals.*
> Good use: my main agent is writing a monthly report and needs the warranty mileage rule. It delegates "find the mileage rule and cite it" to a subagent. The subagent reads the policies in its own context and returns three lines with a citation. The main agent's context gets three lines instead of six documents. Bad use: I let two agents edit the same report at once. One updated the warranty total, the other wrote commentary on the old total. The report contradicts itself. Reading split well. Deciding didn't.

**1:30–1:50 · Gotcha**
*Screen: a subagent failing because it wasn't told which dealer or month.*
> The traps: splitting work that's tightly coupled, or forgetting to pass the subagent the context it needs, like which dealer and which month. A subagent only knows what you hand it, so brief it like a colleague.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Parallelize reading; centralize deciding."*
> Parallelise reading; centralise deciding. Next: how an agent stays on track for fifteen steps.

## E053 · B · How an agent stays on track for 15 steps

**0:00–0:15 · Hook**
*Screen: you on camera; then an agent trace drifting off-task by step 9.*
> By step nine of a monthly warranty review, my agent had forgotten half of what it was supposed to do. How do you keep an agent on track over fifteen steps?

**0:15–0:45 · Claim**
*Screen: a task list in the agent's state with statuses.*
> Give it an explicit task list that lives in its state. The agent writes the plan at the start, updates each item's status as it works, and checks the list before deciding the next step. That keeps long work focused, and it makes progress visible to you.

**0:45–1:30 · Show**
*Screen: the agent writing a task list for the monthly warranty review; statuses changing from pending to done; the trace showing each update. [CAPTURE: your run]*
> Here's the review with a task list. At step one, the agent writes: get March claims, check each against the policy version in force, flag missing photos, total by repair category, draft the summary. As it works, each item moves from pending to in progress to done, and the trace records every change. At step nine, it checks the list, sees "total by category" still pending, and does that next instead of wandering off. It finishes in [CAPTURE] steps.

**1:30–1:50 · Gotcha**
*Screen: a task list written at step one and never updated.*
> The trap is a plan that nothing ever checks. If the agent writes a list and then ignores it, it's just decoration.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Make progress observable."*
> Make progress observable. Next: same model, two products, very different results.
