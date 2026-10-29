# Module 2 — The application boundary and structured output

## E012 · B · Should AI add up your service revenue?

**0:00–0:15 · Hook**
*Screen: you on camera; then chat answer "Dealer A's March service revenue was 10,249 MYR." [CAPTURE: use your real captured answer; if the model got it right, change the hook to "Would you trust this?"]*
> I asked an AI for a dealership's March service revenue. Ten thousand two hundred forty-nine ringgit. Confident, nicely formatted — and wrong. Let's see why.

**0:15–0:45 · Claim**
*Screen: two-column table. Code: filter, add, check permissions. Model: understand the question, explain the result.*
> A language model predicts likely text. That's great for understanding a question and explaining an answer. But it isn't a calculator, and it doesn't know which records you're allowed to see. So we split the job: code does anything that must be exact, and the model explains what the code returns.

**0:45–1:30 · Show**
*Screen: four rows (A 100, A 200, A −50 warranty credit, B 9999). Then the `service_revenue` function. Then terminal output `250.00`.*
> Here's the data. Dealer A has two repair orders and a fifty ringgit warranty credit. Dealer B has one big job. The wrong answer added everything, including another dealer's data. This function filters by dealer and month, then adds with Python's Decimal type, so amounts like ten sen add up exactly. Result: two hundred fifty ringgit. The model only receives that result, and turns it into a sentence for the service manager.

**1:30–1:50 · Gotcha**
*Screen: 250.00 highlighted beside 10,249 crossed out.*
> Same data, correct answer, and now it's testable. One limit: this filter is just a function. In the real app, the dealer must come from the signed-in user — never from the model.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "If it must be exact, compute it."*
> If it must be exact, compute it. Next: what an AI app should say when it can't answer.

## E013 · B · What should an AI app say when it can't answer?

**0:00–0:15 · Hook**
*Screen: you on camera; then an API response: HTTP 200, "Sorry, I couldn't help with that!"*
> My API returned "Sorry, I couldn't help" with a success code. Was that a success? A failure? Something the user should fix? Nobody can tell.

**0:15–0:45 · Claim**
*Screen: four labelled states: answered · needs_more_info · blocked · failed.*
> A good AI API gives every outcome a name. In my service analyst there are four: answered, needs more information, blocked, and failed. Each one tells the front end and the user exactly what happened, and what to do next.

**0:45–1:30 · Show**
*Screen: the Pydantic response model with a status field; then /docs showing four example responses. [CAPTURE: your /docs page]*
> Here's the response model in Pydantic. A status field that can only be one of those four values, plus an answer, a reason, and the evidence used. In the docs page, you can see an example of each. "Answered" comes with the total and the repair orders behind it. "Needs more information" asks which month. "Blocked" means you asked for another dealer's data. "Failed" means something broke on our side, so try again.

**1:30–1:50 · Gotcha**
*Screen: five different "Sorry!" messages all with HTTP 200.*
> The trap is returning HTTP 200 with a friendly "sorry" for everything. It looks polite, but your monitoring sees only successes, and the front end can't react properly.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Make every outcome a named state."*
> Make every outcome a named state. Next: what users see when your AI app breaks.

## E014 · B · What users see when your AI app breaks

**0:00–0:15 · Hook**
*Screen: you on camera; then three cards: blank question · giant paste · provider down.*
> A blank question. A giant paste of an entire manual. The AI provider goes down. What does the service advisor actually see?

**0:15–0:45 · Claim**
*Screen: a boundary line between "outside world" and "app", with checks on the line.*
> Validate everything at the boundary, the moment a request enters your app, and map every failure to an explicit response. Users should get a clear message and the right status code, never a stack trace or a spinning wheel.

**0:45–1:30 · Show**
*Screen: three requests and responses, then the pytest file with the tests passing. [CAPTURE: your test run]*
> Test one: a question that's only spaces. Validation rejects it with a 422 and "please type a question". Test two: a fifty-thousand-character paste. Rejected with a size limit message, before we spend a single token on it. Test three: I simulate the provider timing out. The app catches it and returns a 503 with "the assistant is busy, please try again in a minute". And here are the tests for all three, passing, so none of this quietly breaks later.

**1:30–1:50 · Gotcha**
*Screen: a raw 500 error with a Python traceback.*
> The common mistake is letting provider exceptions escape as raw 500 errors with stack traces. That's confusing for users and can leak details about your system.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Test the failure before the success."*
> Test the failure before the success. Next: why AI ignores your formatting rules.

## E015 · C · Why does AI ignore your formatting rules?

**0:00–0:15 · Hook**
*Screen: you on camera; then a prompt with ten "do not" rules and an output that breaks three of them.*
> I gave the model ten rules about formatting. "Do not use bullet points. Do not exceed three sentences." It broke half of them. Why?

**0:15–0:45 · Claim**
*Screen: three blocks: Role · Rules · One example.*
> Long lists of "don'ts" are hard to follow. What works better is a clear role, a few plain rules written as what you want, and one or two well-chosen examples of the output. Models are excellent at copying the shape of an example, much better than at obeying a pile of prohibitions. Think of it as briefing a new colleague: who they are, what good looks like, and one sample of finished work.

**0:45–1:30 · Show**
*Screen: left: the vague prompt and its messy summary. Right: a sectioned prompt with one example and its clean summary. [CAPTURE: real outputs]*
> On the left, my first prompt: "Summarise this repair order. Don't be long. Don't use jargon." The output is [CAPTURE: describe it]. On the right, a sectioned prompt: role, "You write customer summaries for a dealership service team". Rules, "Three short sentences: what was wrong, what we did, what it cost." And one example summary. Now the output is [CAPTURE: describe it], and it follows the shape every time I run it.

**1:30–1:50 · Gotcha**
*Screen: the example's specific details ("Honda", "RM 350") showing up in an unrelated output.*
> Watch out for examples that are too narrow. If your example mentions brake pads and three hundred and fifty ringgit, the model may copy those details into answers where they don't belong. Use two examples that differ, so the model learns the pattern, not the details.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Show the shape; vary the content."*
> Show the shape; vary the content. Next: turning a messy repair order into clean data.

## E016 · B · From a messy repair order to clean data

**0:00–0:15 · Hook**
*Screen: you on camera; then a paragraph of handwritten-style repair notes.*
> Here's a paragraph of messy repair-order notes, typed by a busy technician. How do you turn that into data a system can actually use?

**0:15–0:45 · Claim**
*Screen: arrow from paragraph to a typed form with fields.*
> Ask the model for a specific schema, the exact fields and types you need, and then validate what comes back before you use it. Asking is step one. Checking is what makes it safe. That way the rest of your system can rely on clean, typed fields instead of free text.

**0:45–1:30 · Show**
*Screen: the Pydantic RepairOrder model: number, date, VIN, mileage, labour lines, parts, total; then the extracted JSON; then a malformed date failing validation. [CAPTURE: your real extraction]*
> Here's my RepairOrder model: repair-order number, date, VIN, mileage, a list of labour lines, a list of parts, and the total. I send the notes and ask for JSON matching that schema. Out comes [CAPTURE: summarise the extracted fields]. Then Pydantic validates it. When I feed in notes with the date written as "31/02", validation fails with a clear error, so a bad record never reaches the database. Bad records go to a review queue, where a person can fix them in seconds.

**1:30–1:50 · Gotcha**
*Screen: "structured output mode = on" with a question mark.*
> The trap is treating the provider's structured-output mode as validation. It helps a lot with the shape, but you still need your own checks for values and rules.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Parse, then validate."*
> Parse, then validate. Next: valid JSON, wrong total.

## E017 · C · Valid JSON, wrong total

**0:00–0:15 · Hook**
*Screen: you on camera; then green text "✓ JSON valid".*
> The extraction parsed perfectly. Every field present, every type correct. So it's correct, right?

**0:15–0:45 · Claim**
*Screen: two layers: "Schema: shape" and "Business rules: truth".*
> No. A schema only proves the shape of an answer: that the total is a number and the date is a date. It can't tell you whether that number is true. For that, you need business checks after parsing, rules that come from how your domain actually works. A schema is like a form with the right boxes. It can't tell you whether someone wrote the right number in the box.

**0:45–1:30 · Show**
*Screen: an extracted repair order: labour 200, parts 150, total 3,500. A business check runs: "labour + parts = 350 ≠ 3,500 → flag for review".*
> Here's an extraction that passed the schema. Labour two hundred ringgit, parts one hundred and fifty, total three thousand five hundred. Perfectly valid JSON. Perfectly wrong. Probably the model misread a decimal point or grabbed a different number. So after parsing I run business checks: do the lines add up to the total? Is the mileage higher than at the last visit? Is the date inside the reporting month? This one fails the first check and goes to a human for review instead of into the monthly report. Each check is a few lines of code, and each one catches a whole class of mistakes.

**1:30–1:50 · Gotcha**
*Screen: a dashboard showing "0 errors" with a wrong total underneath.*
> The mistake is equating "no errors" with "correct". The most dangerous outputs are the ones that look completely fine. Silence isn't evidence.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Add business checks after parsing."*
> Add business checks after parsing. Next: did my prompt change help, or just look better?

## E018 · B · Did my prompt change help, or just look better?

**0:00–0:15 · Hook**
*Screen: you on camera; then prompt v1 and v2 side by side.*
> I rewrote my extraction prompt and the output looked better. But did it actually get better, or did I just like the new wording?

**0:15–0:45 · Claim**
*Screen: a table of ten cases with expected values.*
> Ten fixed test cases with expected answers beat any number of demos you eyeball. That's your first evaluation, or eval. Write the expected values first, then run both prompts against them, and let the scores decide. It doesn't need to be big. It needs to be fixed, so every version sits the same exam.

**0:45–1:30 · Show**
*Screen: a JSONL file of 10 repair-order cases; the runner script; a results table of field-level scores for v1 and v2. [CAPTURE: your scores]*
> Here's my eval set: ten repair-order notes in a JSONL file, each with the correct number, date, mileage and total written down before I ran anything. The runner sends each case through the extractor and scores every field. Prompt one gets [CAPTURE] out of forty fields right. Prompt two gets [CAPTURE]. And look closer: version two fixed the dates but broke [CAPTURE: what regressed]. I'd never have spotted that by eye. Ten cases are quick to write.

**1:30–1:50 · Gotcha**
*Screen: an expected value being typed in after the output appears.*
> The big mistake is writing the expected answer after seeing the output. You'll unconsciously accept whatever the model said, and the eval stops meaning anything. Write the answers first, then run.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "References first, runs second."*
> References first, runs second. Next season: how AI answers from your documents.
