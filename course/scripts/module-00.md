# Module 0 — How LLMs actually work

## E001 · C · Why AI demos break in real life

**0:00–0:15 · Hook**
*Screen: you on camera.*
> A chatbot looks brilliant in a demo. Then real users show up, and it starts making things up, showing the wrong customer's data, or falling over completely. Why does that keep happening?

**0:15–0:45 · Claim**
*Screen: one box labelled "model", then a dotted outline appears around it labelled "application".*
> Because the model is only one part of an AI application. The application around it decides what the model is trusted with, what it's allowed to do, and how its answers get checked. In my experience, most real-world failures come from those missing parts, not from the model being stupid. The model is the engine. The application is everything that makes it safe to drive.

**0:45–1:30 · Show**
*Screen: diagram builds left to right: service advisor → app → context builder → model → tools and data → validator → response.*
> Here's the system I'm building in this series: an AI service analyst for car dealerships. A service advisor asks a question. The app checks who they are and which dealer they work for. A context builder picks only the facts they're allowed to see. The model reads that context and decides what it needs. Tools fetch exact numbers from the database. And a validator checks the answer before anyone sees it. In most demos, you only ever see the middle box, which is why they look so easy.

**1:30–1:50 · Gotcha**
*Screen: every box except "model" greys out.*
> The classic mistake is treating the model as the whole system. Swap in a smarter, more expensive model, and the missing boxes are still missing: no permissions, no checks, and no source of truth.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding the card "Draw the boxes before choosing a model."*
> Draw the boxes before choosing a model. Next: why my forty-page manual didn't fit.

## E002 · C · Why didn't my 40-page manual fit?

**0:00–0:15 · Hook**
*Screen: you on camera; then an error: "context length exceeded".*
> I pasted a forty-page service manual into a chatbot and got told it was too long. Forty pages really isn't that much. So what does "too long" actually mean?

**0:15–0:45 · Claim**
*Screen: one horizontal bar labelled "context window", split into: instructions, history, documents, tool results.*
> Models don't read pages, or even words. They read tokens: small chunks of text, often a piece of a word. And everything you send shares one fixed budget called the context window: your instructions, the whole conversation so far, any documents you attach, and the results of every tool call. When the total goes over the limit, something has to be cut, or the request fails.

**0:45–1:30 · Show**
*Screen: a tokenizer view. Three inputs with token counts: an English complaint, a part number, the Malay complaint "brek berbunyi bila tekan". [CAPTURE: real token counts from your tokenizer]*
> Let's count with a real tokenizer. An English complaint like "brakes squeak when stopping" is just a handful of tokens. Now a part number. Codes get chopped into lots of tiny pieces, so they cost more than they look. And here's the same complaint in Malay: "brek berbunyi bila tekan". Same meaning, but it uses [CAPTURE] tokens, because the tokenizer saw far less Malay text while it was being built. Now multiply that across forty pages of tables, part numbers and footnotes, and you can see exactly where the budget goes.

**1:30–1:50 · Gotcha**
*Screen: "1 word ≠ 1 token" crossed through a word-count estimate.*
> The mistake is estimating from word count. Part numbers, VINs, prices and non-English text all cost more tokens than you'd expect, so your estimate comes out too low every time.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Budget in tokens, not pages."*
> Budget in tokens, not pages. Next: why AI would invent a warranty claim number.

## E003 · B · Why would AI invent a warranty claim number?

**0:00–0:15 · Hook**
*Screen: you on camera; then a chat asking for Dealer A's March warranty total.*
> I asked a model for Dealer A's warranty claims in March, and I gave it no data at all. Watch what came back.

**0:15–0:45 · Claim**
*Screen: the real response. [CAPTURE: the model's actual reply; a refusal is also a valid result]*
> [CAPTURE: describe the reply, for example "It gave me a confident total and three claim numbers."] Here's why. A model generates text from patterns it learned in training, plus whatever you put in its context. It doesn't look anything up. Plausible is not the same as verified.

**0:45–1:30 · Show**
*Screen: side by side. Left: no data, the reply. Right: the same question with five synthetic claim rows supplied, and the reply.*
> On the left, no data, and the answer is [CAPTURE: invented, or a refusal]. If it invented claim numbers, notice they look exactly like real ones: same format, same confidence. On the right, I supply five claim rows from my synthetic database, and now the answer only uses those rows. Same model, same question, same settings. The only difference is what was in its context. So the fix isn't a better question. It's making sure the facts the answer needs are actually in front of the model.

**1:30–1:50 · Gotcha**
*Screen: a temperature slider moved to 0, with the invented answer still there.*
> A lot of people think lowering the temperature fixes this. It doesn't. It just makes the model repeat the same guess more consistently.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Supply facts or compute them."*
> Supply facts or compute them; never ask the model to remember them. Next: same question, different answers.

## E004 · B · Same question, different answers. Is it a bug?

**0:00–0:15 · Hook**
*Screen: you on camera; then two different summaries of the same repair order.*
> I sent the exact same prompt twice and got two different answers. Is my app broken?

**0:15–0:45 · Claim**
*Screen: a probability bar over possible next words.*
> No, this is how models work. A model picks each next token from a set of likely options, a bit like rolling weighted dice. Sampling settings like temperature control how adventurous that pick is. Lower means more consistent. Higher means more variety. But no setting guarantees identical output every single time. That variety is useful for brainstorming, and a problem for anything you need to repeat exactly.

**0:45–1:30 · Show**
*Screen: one repair-order summary prompt run five times at temperature 0 and five times at temperature 1, outputs in two columns. [CAPTURE: your ten outputs]*
> Here's one prompt: summarise this repair order for the customer. I run it five times at temperature zero, and five times at temperature one. At zero, the outputs are [CAPTURE: nearly identical, or identical]. At one, the wording changes on every run, and [CAPTURE: note any run that added or dropped a detail]. The main facts mostly survive, but the sentences don't. Facts first, wording second.

**1:30–1:50 · Gotcha**
*Screen: a failing test: assert summary == "Brake pads replaced..."*
> So never write a test that expects exact model text. It will pass today and fail tomorrow, for no real reason at all.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Check properties of prose. Check exact values from code."*
> Check properties of model prose, like "mentions the brake job". Check exact values from code. Next: using any AI model without getting locked in.

## E005 · B · Use any AI model without getting locked in

**0:00–0:15 · Hook**
*Screen: you on camera; then a codebase search showing provider SDK calls in many files.*
> What happens when you want to switch AI providers, and their SDK is called in twenty different files across your app?

**0:15–0:45 · Claim**
*Screen: one box "ModelClient" between "your app" and three plain labels: Provider A, Provider B, Mock.*
> You put one thin layer in between, called an adapter. Your app only ever talks to that interface. Behind it, you can plug in any provider, or a fake model for tests. Only one file in the whole project knows which provider you're using. It's a small file.

**0:45–1:30 · Show**
*Screen: code: the ModelClient interface with a complete() method; MockModel returning a canned answer; the real client; an environment variable MODEL_PROVIDER=mock, then =real. [CAPTURE: your test run]*
> Here's the interface: one method that takes messages and returns text plus token usage. The mock returns a fixed answer instantly, so my tests run offline, with no API key and no cost. The real client wraps the provider's SDK. And this one environment variable decides which one the app gets. Switch it, rerun the app, and nothing else changes at all. It also means I can test the whole app with no internet connection, and every test runs in under a second.

**1:30–1:50 · Gotcha**
*Screen: the same SDK import highlighted in six files.*
> The trap is calling the SDK directly wherever it's convenient. Then every model switch, every price change and every test turns into a hunt across your codebase.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Only one file should know your provider."*
> Only one file should know your provider. Next: what did that one answer cost?

## E006 · B · What did that one AI answer cost?

**0:00–0:15 · Hook**
*Screen: you on camera; then a single chat answer.*
> How much did that one answer cost me, and how long did it take? If you can't answer that, you can't run an AI app for real.

**0:15–0:45 · Claim**
*Screen: a structured log line appears field by field.*
> Every model call should log its usage: input tokens, output tokens, how long it took, and an estimated cost. And when usage is missing, or a call fails, log that explicitly too, so the gaps don't quietly look like zero. That's the minimum for running anything real.

**0:45–1:30 · Show**
*Screen: one JSON log line from your adapter: request ID, model, input tokens, output tokens, duration in ms, cost in USD, price table date. [CAPTURE: a real log line]*
> Here's a real log line from my adapter. [CAPTURE] input tokens, [CAPTURE] output tokens, [CAPTURE] milliseconds. The cost comes from a price table with a date on it, because prices change. And here's a failed call: status "error", usage marked as missing, not zero. With this, I can add up cost per day, per feature, and per dealer. That's how I'll know, months from now, which feature is quietly eating the budget.

**1:30–1:50 · Gotcha**
*Screen: "cost ≈ characters ÷ 4" crossed out.*
> Don't estimate cost from character counts, or from an old price list you copied once. Use the usage numbers the provider returns, and today's price. Old prices make every forecast wrong, in either direction.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Log usage per request; price it at run time."*
> Log usage per request, and price it at run time. Next: brake squeal — do you even need AI?
