# Module 5 — Tools and MCP

## E030 · C · Can AI actually run code?

**0:00–0:15 · Hook**
*Screen: you on camera; then a headline: "AI agent queries your database!"*
> You hear it everywhere: the AI queried the database, the AI sent the email, the AI ran the code. Can a language model actually run anything by itself?

**0:15–0:45 · Claim**
*Screen: "Model requests" → "Your code decides and runs".*
> No. A model only produces text. With tool calling, that text is a structured request: "please call service revenue for March". Your code receives the request, checks it, decides whether to run it, runs it, and sends the result back. The model never touches your database directly. Every action passes through code you wrote and control. That's what makes tools safe to use.

**0:45–1:30 · Show**
*Screen: sequence diagram: model → tool request → app validates → app executes SQL → result → model → answer.*
> Here's the sequence in my service analyst. The advisor asks for March revenue. The model replies with a tool request: call service revenue, period March, pay type all. My app validates that request. Is that tool allowed for this user? Are the dates valid? Then the app runs a parameterised SQL query, gets two hundred and fifty ringgit, and hands that result back to the model. Only then does the model write the sentence the advisor reads. At every step, my code is the one acting.

**1:30–1:50 · Gotcha**
*Screen: "The AI deleted the records" with "AI" crossed out and "your code" written in.*
> The mistake is describing the model as having "executed" something. It didn't. Your code did, and that means the responsibility for checks and permissions is yours too. Saying it clearly also helps your team design the right checks.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "The model asks; the app acts."*
> The model asks; the app acts. Next: why AI keeps calling the wrong tool.

## E031 · B · Why AI keeps calling the wrong tool

**0:00–0:15 · Hook**
*Screen: you on camera; then a log of the model calling query_data for a simple revenue question.*
> I asked for March service revenue, and my agent wrote a raw SQL query through a generic tool instead of using the revenue tool I built for exactly that. Why does the model keep picking the wrong tool?

**0:15–0:45 · Claim**
*Screen: a tool definition: name, description, typed parameters.*
> Because a tool's name, description and parameters are its entire interface for the model. That's all it sees when choosing. So write them like documentation for a new colleague on their first day: one clear purpose, plain words, and typed parameters with examples.

**0:45–1:30 · Show**
*Screen: left: query_data(sql: str) "Runs a query". Right: service_revenue(period_start, period_end, pay_type) with a full description. Then a five-question tool-choice table. [CAPTURE: your results]*
> On the left, my first design: one tool called query data, description "runs a query", takes any SQL. On the right: service revenue, with period start, period end, and pay type as customer, warranty, internal or all, and a description saying exactly when to use it. I ask five questions. With the vague tool, the model picks correctly [CAPTURE] times out of five. With narrow, well-described tools, [CAPTURE] out of five, and the answers are also safer.

**1:30–1:50 · Gotcha**
*Screen: two tools with overlapping descriptions: "get revenue" and "get sales".*
> The traps are overlapping tools that sound alike, or one giant tool that does everything. Either way, the model has to guess.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "One clear purpose per tool."*
> One clear purpose per tool. Next: what if the AI asks for another dealer's data?

## E032 · B · What if the AI asks for another dealer's data?

**0:00–0:15 · Hook**
*Screen: you on camera; then a tool call with dealer_id="b" from a Dealer A user.*
> A Dealer A user asks a cleverly worded question, and the model passes dealer ID "b" to my revenue tool. What happens next decides whether my app leaks data.

**0:15–0:45 · Claim**
*Screen: two sources: "Session: dealer A (trusted)" and "Model: dealer b (untrusted)".*
> Validate every argument the model sends, and never take identity from the model at all. The dealer comes from the authenticated session, the signed-in user, and the server injects it into the tool call. The model doesn't get a say in whose data it reads.

**0:45–1:30 · Show**
*Screen: the tampered call having no effect; the server injecting dealer=a; a malformed date rejected with a helpful error. [CAPTURE: your test output]*
> Here's the fix. My tool schema doesn't even have a dealer field. When the call arrives, the server adds the dealer from the session. So when I simulate the tampered request, it still returns Dealer A's numbers, and the attempt gets logged. Same validation for every argument: a date like "March 32nd" is rejected with "use YYYY-MM-DD", which the model can read and fix on its next try. And here's the test proving Dealer B's rows never come back.

**1:30–1:50 · Gotcha**
*Screen: a tool schema with "dealer_id" highlighted in red.*
> The common mistake is putting the dealer ID in the tool schema at all. If the model can fill it in, sooner or later something will make it fill in the wrong one.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Identity never comes from the model."*
> Identity never comes from the model. Next: what does "last quarter" mean on the third of January?

## E033 · C · What does "last quarter" mean on 3 January?

**0:00–0:15 · Hook**
*Screen: you on camera; then a calendar showing 3 January.*
> It's the third of January. The service manager asks for warranty claims "last quarter". Which months is that? And does your model even know today's date?

**0:15–0:45 · Claim**
*Screen: "relative words" → "resolver in code" → "explicit dates".*
> Convert relative time into explicit periods in code, not in the model. A small period resolver turns "last month", "Q1" or "year to date" into exact start and end dates, using today's date and your fiscal-year rules. And when a request is genuinely ambiguous, the resolver asks a clarifying question instead of guessing. Code like this is boring, testable and always gives the same answer, which is exactly what dates need.

**0:45–1:30 · Show**
*Screen: a resolver table: input phrase → start date → end date, for "last month", "Q1", "YTD", "last quarter"; then "compare March" producing a question.*
> Here's my resolver, with today's date passed in. On the third of January, "last quarter" means the first of October to the thirty-first of December. "Last month" is December. "Year to date" is just three days so far, which is worth telling the user. If our fiscal year started in April, "Q1" would mean April to June, and the resolver knows that rule. Now, "compare March". Which March? The resolver asks: "March this year or last year?" The model then uses these exact dates when it calls the tools.

**1:30–1:50 · Gotcha**
*Screen: the model saying "Today is 14 June 2024" with a red cross.*
> The trap is letting the model guess today's date. It might use its training cutoff, and quietly report the wrong year with full confidence. Pass it in.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Pass the date in; resolve periods deterministically."*
> Pass the date in; resolve periods in code. Next: does "no data" mean zero revenue?

## E034 · B · Does "no data" mean zero revenue?

**0:00–0:15 · Hook**
*Screen: you on camera; then an answer: "Dealer C's service revenue in June was RM 0."*
> My assistant said Dealer C made zero ringgit in service revenue in June. Actually, June's data hadn't been loaded yet. Those are very different answers.

**0:15–0:45 · Claim**
*Screen: three outcomes: value · no_records · error.*
> Tools should return explicit outcomes: a value, no records found, or an error, each with a message the model can act on. Never let "nothing found" or "something broke" quietly become a zero. Each outcome should come with a short message written for the model, so it knows what to do next.

**0:45–1:30 · Show**
*Screen: the tool returning {"status": "no_records"} for June; the answer saying so; then a validation error with the correct format, and the model retrying. [CAPTURE: your run]*
> Here's the fixed tool. For June, it returns status "no records", with "no repair orders loaded for this period". Now the answer says: "I don't have any June data for Dealer C yet," not "zero ringgit". And when the model sends a badly formatted date, the error says exactly what's expected: "period start must be YYYY-MM-DD". Watch the model read that and [CAPTURE: retry with the correct format]. The error message became an instruction.

**1:30–1:50 · Gotcha**
*Screen: a raw Python traceback being sent to the model.*
> The mistake is sending raw stack traces back to the model. They're long, confusing and might expose internal details, and the model can't fix anything from them. Keep errors short and fixable.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Errors are instructions; make them actionable."*
> Errors are instructions; make them actionable. Next: what is MCP, really?

## E035 · C · What is MCP, really?

**0:00–0:15 · Hook**
*Screen: you on camera; then three AI apps, each with its own custom connector to the same database.*
> I built a revenue tool for my service analyst. Now I want to use it from a coding assistant and a desktop chat app too. Do I really have to rewrite the integration for every single AI app?

**0:15–0:45 · Claim**
*Screen: "Model Context Protocol" with the hub-and-spoke diagram.*
> That's the problem the Model Context Protocol, MCP, solves. It's an open standard for connecting AI applications to tools, data and prompts. You build an MCP server once, and any app that supports MCP can connect to it, a bit like how one USB port works with many devices.

**0:45–1:30 · Show**
*Screen: diagram: AI application (host, with an MCP client) ↔ several MCP servers, each exposing tools, resources and prompts.*
> Here's the shape. On the left, an AI application, called the host, which contains an MCP client. On the right, MCP servers. Each server can expose three kinds of things: tools, which are actions like calculating service revenue; resources, which are data like a warranty policy document; and prompts, which are reusable templates. The host discovers what each server offers, and the model can then use those capabilities. Write the server once, and every compatible app gets it. Many AI apps and coding tools already support it, so one server reaches all of them.

**1:30–1:50 · Gotcha**
*Screen: "MCP = secure?" with a red question mark.*
> The big misconception is that MCP makes a tool secure. It doesn't. It standardises the connection. Who's allowed to call what, and on whose data, is still entirely your job. That part stays with you.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "MCP standardizes the connection; you still own authorization."*
> MCP standardises the connection; you still own authorisation. Next: let any AI app use your tools.

## E036 · B · Let any AI app use your tools

**0:00–0:15 · Hook**
*Screen: you on camera; then a different AI app calling your service_revenue tool.*
> This isn't my app. It's a completely different AI client, calling the service revenue tool I built last week. Here's how.

**0:15–0:45 · Claim**
*Screen: existing tool functions wrapped in an "MCP server" box.*
> Wrapping your existing tools in a small MCP server makes them reusable across any client that speaks MCP. You don't rewrite the logic. The same narrow, validated function now has a standard doorway. That's the payoff of keeping tools narrow from the start: they move easily.

**0:45–1:30 · Show**
*Screen: a short MCP server file registering service_revenue; the client config; the client listing tools and calling service_revenue for March. Label SDK version and date. [CAPTURE: your run, SDK version, date]*
> Here's the server, about thirty lines. It imports my existing service revenue function and registers it as an MCP tool, with the same name, description and typed parameters. Then I point an MCP client at it. The client lists the available tools, picks service revenue, and calls it for March. Result: [CAPTURE]. Same validation, same dealer injection from the session, same tests. Recorded with [CAPTURE: SDK and version] on [CAPTURE: date]. If I change the function, both my app and every MCP client get the fix.

**1:30–1:50 · Gotcha**
*Screen: an MCP server exposing "run_any_sql" with a warning sign.*
> The temptation is exposing broad database access because it's quick: one "run any SQL" tool. That throws away every safety decision you made. Keep the doorway narrow too.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Same narrow tools, new doorway."*
> Same narrow tools, new doorway. Next: turn two ringgit, turn twenty dollars — why?
