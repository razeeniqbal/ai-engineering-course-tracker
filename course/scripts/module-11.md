# Module 11 — Evaluation

## E066 · B · How do you grade an explanation?

**0:00–0:15 · Hook**
*Screen: you on camera; then an answer: a correct total plus two sentences of explanation.*
> Checking that my assistant's warranty total is right is easy: compare the number. But how do you grade the explanation that comes with it?

**0:15–0:45 · Claim**
*Screen: three graders: code · rubric · model.*
> Use the right grader for each part. Code graders for exact values, like totals and dates. Rubrics, a short checklist, for written answers. And model graders, another model doing the scoring, only where you've checked that they agree with humans. Each grader has a cost, so use the simplest one that gives a trustworthy score.

**0:45–1:30 · Show**
*Screen: one warranty question's answer scored three ways: code grader on the total, a 3-point rubric on the explanation, a model grader on clarity, with agreement noted. [CAPTURE: your scores]*
> One answer, three graders. The code grader checks the total against the expected value: pass. The rubric checks the explanation: does it name the period? Does it separate warranty from customer-paid work? Does it cite the policy? [CAPTURE] out of three. The model grader rates clarity from one to five: [CAPTURE]. I trust the first two immediately. The third I only use because I checked it against my own ratings on twenty answers first. The cheap checks run on every change.

**1:30–1:50 · Gotcha**
*Screen: a grader failing "RM 12,480" because it expected "12480.00 MYR".*
> The opposite trap: graders so strict they reject valid answers. "RM 12,480" and "12,480 ringgit" are the same fact. Normalise formats before comparing.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Use the cheapest grader that's reliable."*
> Use the cheapest grader that's reliable. Next: should another AI be the judge?

## E067 · C · Should another AI be the judge?

**0:00–0:15 · Hook**
*Screen: you on camera; then an "LLM judge" giving every answer 9 out of 10.*
> Grading hundreds of answers by hand is slow, so a lot of teams ask another model to be the judge. It's fast and cheap. But should it be the final authority on quality?

**0:15–0:45 · Claim**
*Screen: "Judge = another imperfect model".*
> A model judge is just another imperfect model. It has its own biases: it often prefers longer answers, more confident wording, or answers that sound like itself. So before you trust its scores, calibrate it: compare its judgements with human labels on a sample, and measure how often they agree. Then use it only where it agrees.

**0:45–1:30 · Show**
*Screen: judge vs. human labels on 20 answers; an agreement percentage; three disagreements shown in detail. [CAPTURE: your agreement and examples]*
> I took twenty answers from my service analyst and rated each one myself as good or bad. Then I asked a model judge to rate the same twenty. They agreed on [CAPTURE] out of twenty. Look at the disagreements. Here, the judge passed an answer that sounded confident but cited the wrong policy version. Here, it failed a correct but very short answer. That tells me exactly where the judge can't be trusted, so I add a code check for policy versions and keep the judge for tone and clarity only. Without that comparison, I'd have trusted it everywhere.

**1:30–1:50 · Gotcha**
*Screen: a dashboard of judge scores with no human comparison anywhere.*
> The trap is trusting judge scores you never validated. A dashboard full of nines feels great, until you read the answers yourself. Re-check the judge whenever you change it or the task.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Check the judge before trusting it."*
> Check the judge before trusting it. Next: right answer, wasteful route.

## E068 · B · Right answer, wasteful route

**0:00–0:15 · Hook**
*Screen: you on camera; then two agent runs, both ending with the correct answer.*
> Two agent runs, same question, same correct answer. One of them made three tool calls. The other made twelve. If you only check the final answer, they look identical.

**0:15–0:45 · Claim**
*Screen: "outcome" + "path: tools, steps, errors, budget".*
> Agent evaluations should check the outcome and the path: which tools were used, how many steps it took, any errors along the way, and how much of the budget it spent. The path tells you about cost, speed and risk.

**0:45–1:30 · Show**
*Screen: two traces side by side: an efficient run (3 calls) and one with 9 wasted calls; the trajectory checks that flag the second. [CAPTURE: your traces]*
> Here are both traces. The efficient run: resolve the period, call warranty claims, answer. Three calls. The wasteful run calls the same tool again and again with slightly different dates, tries a tool it's not allowed, and only then answers. [CAPTURE] calls. So I add trajectory checks: no more than five tool calls for this kind of question, no rejected tools, no repeated identical calls. The second run now fails, even though its answer was right.

**1:30–1:50 · Gotcha**
*Screen: a check requiring "exactly: tool A, then tool B" failing a valid alternative path.*
> The opposite trap: requiring one exact path when several are valid. Check limits and forbidden actions, not a single script of steps.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Score the outcome; inspect the path."*
> Score the outcome; inspect the path. Next: did I improve, or just overfit?

## E069 · B · Did I improve, or just overfit?

**0:00–0:15 · Hook**
*Screen: you on camera; then a score chart climbing week after week.*
> For three weeks I tweaked my prompts, and my eval score kept climbing. Then I ran a fresh set of questions, and it was barely better than where I started. What happened?

**0:15–0:45 · Claim**
*Screen: two sets: "Development set (tune on this)" and "Held-out set (never look)".*
> I overfit. I'd been tuning against the same questions I was measuring with. The fix: keep two sets. Tune on a development set as much as you like, and report on a held-out set that you never iterate against. The held-out set is your honest exam; the development set is your practice paper.

**0:45–1:30 · Show**
*Screen: a chart where the dev score rises across versions while the held-out score stays flat. [CAPTURE: your two lines]*
> Here are both scores across five prompt versions. Development set: from [CAPTURE] up to [CAPTURE]. Held-out set: from [CAPTURE] to [CAPTURE]. Nearly flat. My changes taught the prompt my specific dev questions, not the general skill. The fix that finally moved the held-out score was [CAPTURE: the change that generalised], and the held-out set is the only reason I could tell the difference. That's humbling, and useful.

**1:30–1:50 · Gotcha**
*Screen: a held-out failure being opened, fixed, and re-run.*
> The easy mistake: peeking at held-out failures and fixing them. The moment you do, it becomes a development set, and you've lost your honest measure. Keep it sealed.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Reserve the test set before you start."*
> Reserve the test set before you start. Next: stop a bad change before it ships.

## E070 · B · Stop a bad change before it ships

**0:00–0:15 · Hook**
*Screen: you on camera; then a pull request with a small "harmless" change.*
> A one-line change looked harmless. If it had shipped, every dealer would have seen warranty totals with credit notes counted twice. How do you stop that before it ships?

**0:15–0:45 · Claim**
*Screen: two lanes: "every commit: offline + authorization checks" and "on purpose: paid model evals with a spending limit".*
> Run your deterministic tests and authorisation checks automatically on every change, in CI. They're fast, free and offline. Run paid model evaluations separately and deliberately, with spending limits, so cost never stops you from testing. The goal is that a mistake becomes a red check, not a customer complaint.

**0:45–1:30 · Show**
*Screen: the GitHub Actions workflow; a pull request where a broken fixture fails the check; the failing test name and diff. [CAPTURE: your PR and failing check]*
> Here's my GitHub Actions workflow. On every push, it runs the unit tests, the offline eval with the mock model, and the dealer isolation tests. Now watch: I open a pull request that changes how credit notes are summed. The check goes red. The failing test is [CAPTURE: test name]: expected two hundred fifty ringgit, got three hundred. The change can't be merged until it's fixed. That one test protects every dealer's monthly report.

**1:30–1:50 · Gotcha**
*Screen: a CI bill growing because paid API calls run on every push.*
> The trap is running paid API calls on every push. Your bill grows with every typo fix, and eventually someone switches the checks off. Keep paid runs deliberate.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Offline checks on every commit; live evals on purpose."*
> Offline checks on every commit; live evals on purpose. Next: can a document give your agent orders?
