# Module 15 — Capstone

## E085 · B · An AI answer you can actually check

**0:00–0:15 · Hook**
*Screen: you on camera; then a service manager reading an answer on a tablet.*
> A service manager reads an answer from my assistant: "Dealer A's March warranty work came to twelve thousand ringgit." Why should she believe it?

**0:15–0:45 · Claim**
*Screen: five labels around an answer: period · currency · metric definition · evidence · trace.*
> Because every answer shows what it's based on: the exact period, the currency, the metric definition, whether that's warranty, customer-paid or internal work, the evidence behind it, and a link to the full trace. A trustworthy answer is one you can check. If any part is missing, the reader has to take it on faith.

**0:45–1:30 · Show**
*Screen: one complete answer in the capstone UI, then clicking through to its trace. [CAPTURE: your real answer and trace]*
> Here's the final app. I ask: how much warranty work did Dealer A do in March? The answer: [CAPTURE]. Underneath: period, first to thirty-first of March. Currency: ringgit. Metric: warranty work only, net of credit notes. Evidence: [CAPTURE] repair orders, each one clickable. And the trace link opens every step: the period resolver, the tool call with its arguments, the SQL result, and the model's explanation. Every number can be traced back to a row. Nothing in the answer is a mystery.

**1:30–1:50 · Gotcha**
*Screen: a polished answer with no caveats, next to one that says "2 repair orders missing mileage".*
> The temptation is hiding uncertainty to look polished. If two repair orders were missing data, say so. That's what makes people trust the rest.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Make answers checkable."*
> Make answers checkable. Next: proof my safeguards actually work.

## E086 · B · Proof my safeguards actually work

**0:00–0:15 · Hook**
*Screen: you on camera; then a CI page with every check green.*
> Every project shows off its green checkmarks. But green only proves that nothing failed today. Can I prove my safeguards actually catch real problems?

**0:15–0:45 · Claim**
*Screen: "break it on purpose → watch it get caught".*
> Show a real broken change being blocked by a meaningful test. A safety net only proves its worth when it catches something, so deliberately break something important and record what happens. Breaking it yourself is the most convincing demo there is.

**0:45–1:30 · Show**
*Screen: a pull request that removes the dealer filter from one tool; the failing check; the isolation test that caught it; the fix and the green rerun. [CAPTURE: your PR, failing test and fix]*
> Here's a pull request that quietly removes the dealer filter from one tool. It looks like a harmless refactor. CI runs, and the check goes red. The failing test is the dealer isolation test: [CAPTURE: the test name and failure message]. Signed in as Dealer B, it got Dealer A's rows. The change can't be merged. I put the filter back, CI turns green, and the pull request merges. That's the safety net doing its job, on camera. The test did exactly what it was written for.

**1:30–1:50 · Gotcha**
*Screen: a demo showing only green builds.*
> The mistake is demonstrating only green builds. Anyone can have tests that pass. What matters is tests that fail when they should. Show a red one.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Show the safety net catching something."*
> Show the safety net catching something. Next: what my AI service analyst can do, and can't.

## E087 · C · What my AI service analyst can do, and can't

**0:00–0:15 · Hook**
*Screen: you on camera; then the course tracker showing all 87 lessons complete.*
> Eighty-seven lessons later, here's the honest answer to one question: what can my AI service analyst actually do now, and what can't it do yet?

**0:15–0:45 · Claim**
*Screen: "results + sample sizes + limitations".*
> Credible engineering shows results with their sample sizes, right next to the known limitations. Not "it's ninety-five percent accurate", but "ninety-five percent on forty held-out questions, and here's where it still fails". That honesty is what makes the results believable. It also shows you understand what you built, which is exactly what an interviewer is listening for.

**0:45–1:30 · Show**
*Screen: the capstone scorecard: question resolution, dealer isolation, grounding, abstention, harness control, each with a percentage and sample size; then three limitations and the next extension. [CAPTURE: your scorecard]*
> Here's my scorecard on the held-out set, run once, without tuning. Question resolution: [CAPTURE], on [CAPTURE] questions. Dealer isolation: [CAPTURE] of [CAPTURE] cases passed. Grounding with correct citations: [CAPTURE]. Correct abstention on unanswerable questions: [CAPTURE]. And three known limitations: [CAPTURE: limitation one], [CAPTURE: limitation two], and [CAPTURE: limitation three]. The next extension I'd build is [CAPTURE], because [CAPTURE]. These numbers come from one run on questions I never tuned on, so they're honest, not polished. That's the project I'll show in interviews.

**1:30–1:50 · Gotcha**
*Screen: "production-ready!" crossed out, "a well-tested prototype" written in.*
> The biggest mistake at the end of a project like this is implying a prototype is production-ready. It isn't. It's a well-tested prototype, and saying so is a strength. Knowing its limits, and saying them out loud, is the most professional thing in this whole series.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Pick one next build with a measurable goal."*
> Pick one next build with a measurable goal. Thanks for following the whole journey. See you in the next one.
