# Module 10 — Skills

## E061 · C · Teach an agent your procedure without a giant prompt

**0:00–0:15 · Hook**
*Screen: you on camera; then a system prompt scrolling for pages with every procedure the service team uses.*
> My service team has procedures for everything: monthly reports, warranty reviews, recall follow-ups. Pasting all of them into the system prompt made it enormous. How do you teach an agent your procedures without a giant prompt?

**0:15–0:45 · Claim**
*Screen: a folder icon labelled "skill".*
> With skills. A skill is a folder of instructions, scripts and resources for one procedure. The agent discovers the skill exists, and only loads its full contents when a task needs it. So the agent can know about many procedures, without carrying all of them in its context all the time. It's how a new hire learns: a short index of procedures, and the full guide only when needed.

**0:45–1:30 · Show**
*Screen: the folder tree: monthly-service-report/ with SKILL.md (name, description, steps), scripts/variance.py, templates/report.md.*
> Here's a skill for my monthly service report. At the top is SKILL.md. Its first lines are the name and a one-line description: "Produce the monthly service report for a dealer: revenue, warranty and top repair categories, with variance against last month." Below that, the step-by-step instructions. Then a scripts folder with a variance calculator, because numbers must come from code. And a templates folder with the report layout. Everything the agent needs for this one job, packaged together.

**1:30–1:50 · Gotcha**
*Screen: a "skill" that's just one huge prompt with no scripts or structure.*
> The mistake is treating a skill as just a long prompt in a file. The power comes from the structure: a clear trigger, focused steps, and scripts for the exact parts. Structure matters.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Skills are procedures, packaged."*
> Skills are procedures, packaged. Next: fifty skills, one context window.

## E062 · C · 50 skills, one context window

**0:00–0:15 · Hook**
*Screen: you on camera; then fifty skill folders.*
> If my agent has fifty skills, wouldn't loading all of them fill the context window before the user even says hello?

**0:15–0:45 · Claim**
*Screen: three levels stacked: description → SKILL.md body → referenced files.*
> No, thanks to progressive disclosure. Only each skill's name and short description sit in the context all the time. The full instructions load only when a task matches that description, and extra files, like scripts or templates, load only when the instructions point to them. The agent pays for detail only when it uses it. It's like a table of contents: you scan the titles, and only open the chapter you need.

**0:45–1:30 · Show**
*Screen: token counts at each level for one skill, and the total for fifty descriptions. [CAPTURE: your counts]*
> Here are the three levels with real token counts. Level one, the description of my monthly report skill: [CAPTURE] tokens. Fifty skill descriptions together: about [CAPTURE] tokens. Affordable. Level two, the full SKILL.md, loaded only when someone asks for a monthly report: [CAPTURE] tokens. Level three, the template and the script output, loaded only when the steps reach them: [CAPTURE] tokens. Most conversations only ever touch level one. That's why the number of skills can grow without slowing every conversation down.

**1:30–1:50 · Gotcha**
*Screen: a vague description "Helps with reports" and the skill never triggering.*
> The catch: because the description is all the agent sees at first, a vague one means the skill never gets used. "Helps with reports" won't trigger for "how did March go?". Write it with the words your users actually say.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "The description is the trigger."*
> The description is the trigger. Next: skill, tool, MCP or subagent?

## E063 · C · Skill, tool, MCP or subagent?

**0:00–0:15 · Hook**
*Screen: you on camera; then four labels in a 2×2 grid.*
> Tools, MCP servers, skills and subagents. Four different ways to add a capability to an agent. When I need something new for my service analyst, which one should I reach for?

**0:15–0:45 · Claim**
*Screen: one line each: Tools act · MCP connects · Skills teach · Subagents isolate.*
> Each one does a different job. Tools perform actions, like calculating revenue. MCP connects your agent to outside systems in a standard way. Skills teach procedures, the "how we do things here". And subagents isolate work, running it in a separate context so the main one stays clean. Match the mechanism to the need. Picking right keeps things simple.

**0:45–1:30 · Show**
*Screen: a decision table with a service-analyst example in each row.*
> Here's my decision table with real examples. "Calculate warranty totals for a period": that's an action with exact results, so a tool. "Use our tools from a different AI app": a connection problem, so MCP. "Produce the monthly report the way our service manager likes it": a procedure, so a skill. "Read all six policies to find every mention of commercial use": lots of reading I don't want in the main context, so a subagent. Often they combine: the skill tells the agent which tools to call.

**1:30–1:50 · Gotcha**
*Screen: a skill instruction saying "only show your own dealer's data" with a red cross.*
> The mistake is using a skill for something that needs enforced permissions. A skill is guidance the model follows. Permissions must be enforced in code, in tools and hooks. Guidance helps the model; code makes it certain.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Match the mechanism to the need."*
> Match the mechanism to the need. Next: making the monthly service report repeatable.

## E064 · B · Making the monthly service report repeatable

**0:00–0:15 · Hook**
*Screen: you on camera; then three monthly reports, each in a different format.*
> I asked for the monthly service report three months in a row and got three different formats, with three different ways of calculating the variance. How do you make it repeatable?

**0:15–0:45 · Claim**
*Screen: description · steps · script.*
> Write a skill: a precise description so it triggers reliably, step-by-step instructions, and a bundled script for every part that must be exact. The model writes the commentary. The script does the maths.

**0:45–1:30 · Show**
*Screen: building SKILL.md; running it for Dealer A, March; the variance table produced by scripts/variance.py; the model's commentary around it. [CAPTURE: your output]*
> Here's the skill being built. Description: "Use when asked for a monthly service report or how a dealer's month went." Steps: get revenue by pay type, get warranty claims, run the variance script against last month, fill the template, write three sentences of commentary. Now I ask, "how did Dealer A do in March?" The skill triggers, the script produces the warranty versus customer-paid variance table, [CAPTURE: show the numbers], and the model explains it in plain words.

**1:30–1:50 · Gotcha**
*Screen: a downloaded skill with an unread script, highlighted.*
> Important: a skill can run code. So a skill you install but haven't read is code you haven't reviewed. Treat it like any other dependency.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Write it like onboarding notes for a new hire."*
> Write it like onboarding notes for a new hire. Next: does the agent use your skill only when it should?

## E065 · B · Does the agent use your skill only when it should?

**0:00–0:15 · Hook**
*Screen: you on camera; then the report skill triggering on "what's the weather?".*
> My report skill fired when someone asked about opening hours. And it didn't fire when the service manager asked, "how did last month go?" How do you test a skill's triggering?

**0:15–0:45 · Claim**
*Screen: two lists: "should use" and "should not use".*
> Test it like a classifier. Write prompts that should trigger the skill and prompts that shouldn't, run them all, and count the mistakes in both directions. Then improve the description and rerun. Both kinds of mistake matter: a missed trigger and a false one.

**0:45–1:30 · Show**
*Screen: 10 prompts (5 should-use, 5 should-not), a trigger table with ✓/✗; an improved description; the rerun table. [CAPTURE: both runs]*
> Ten prompts. Five should trigger: "monthly report for Dealer A", "how did March go?", and so on. Five shouldn't: opening hours, a single repair order lookup, a policy question. First run: [CAPTURE] correct out of ten. It missed "how did March go?" and fired on [CAPTURE]. So I rewrite the description to mention "how a month went" and to exclude single lookups. Rerun: [CAPTURE] out of ten. Every description change gets rerun against the same ten prompts.

**1:30–1:50 · Gotcha**
*Screen: one happy-path prompt with a single tick.*
> The trap is testing only the happy prompt, the one you wrote the skill for. Real users phrase things differently, and the false triggers matter too. Test the tricky ones.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Evaluate the description, not just the output."*
> Evaluate the description, not just the output. Next season: how do you grade an explanation?
