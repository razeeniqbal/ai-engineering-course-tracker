# Module 6 — Context engineering

## E037 · C · Turn 2: ringgit. Turn 20: dollars. Why?

**0:00–0:15 · Hook**
*Screen: you on camera; then turn 2 "All amounts are in ringgit." … turn 20 answer in USD. [CAPTURE: reproduce this in your project]*
> On turn two, I told my service agent all amounts are in ringgit. On turn twenty, it answered in dollars. Same model, same session. What happened?

**0:15–0:45 · Claim**
*Screen: one horizontal bar labelled "context window", with segments: instructions, tools, history, documents, tool results.*
> A model doesn't remember your conversation the way you do. On every call, it only sees what's inside its context window: instructions, tool definitions, conversation history, documents and tool results. Context engineering is deciding what goes into that window, in what form, and when. That window is rebuilt from scratch on every single call, so whatever your app leaves out, the model simply never sees.

**0:45–1:30 · Show**
*Screen: the bar fills with large repair-order tables; the oldest messages, including "ringgit", slide out. Then the fixed version: a small pinned "Constraints: currency = MYR" block, a short summary of old turns, compressed tool results.*
> Watch the window fill up. Every tool call adds a big table of repair orders. To make room, my app dropped the oldest messages, including the one about ringgit. The fix wasn't a smarter model. It was a better context: keep lasting constraints in a short pinned section, summarise old turns, and shrink bulky tool results down to what they concluded. None of that needed a new model or a longer prompt, just better decisions about what to keep.

**1:30–1:50 · Gotcha**
*Screen: turn 20 now answers in MYR. Small caption: "One scenario; long contexts can also degrade without trimming."*
> After the fix, turn twenty answers in ringgit. One caution: this is a single scenario. Very long contexts can also lose details without any trimming, simply because important information gets diluted. So keep constraints short, pinned and near the top.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "The model only knows what's in the window."*
> The model only knows what's in the window. Next: why not send the AI everything?

## E038 · C · Why not send the AI everything?

**0:00–0:15 · Hook**
*Screen: you on camera; then a context window size of hundreds of thousands of tokens.*
> Modern models accept enormous contexts, hundreds of pages at once. So why not just send every manual, every policy and every repair order with every question, and let the model sort it out?

**0:15–0:45 · Claim**
*Screen: three costs: money · latency · attention.*
> Because extra context isn't free. You pay for every token, every time. Bigger inputs take longer to process, so answers get slower. And irrelevant material can dilute the model's attention, making it more likely to miss or confuse the passage that actually matters. Bigger isn't automatically better. Large contexts are a capability, not a target. Used carelessly, they make answers slower, pricier and sometimes worse.

**0:45–1:30 · Show**
*Screen: the same question sent two ways: 2 relevant passages vs 2 relevant + 40 irrelevant; a table of accuracy, tokens and latency on a small labelled set. [CAPTURE: your numbers]*
> I run the same set of warranty questions two ways. Version one sends just the two relevant passages. Version two sends those same two, buried among forty irrelevant ones. Accuracy: [CAPTURE] versus [CAPTURE]. Input tokens per question: [CAPTURE] versus [CAPTURE]. Average time to answer: [CAPTURE] versus [CAPTURE] seconds. Even when the model still gets it right, I'm paying [CAPTURE] times more and the advisor waits longer, for no benefit. The cost difference shows up on every question, every day, so it adds up quickly.

**1:30–1:50 · Gotcha**
*Screen: "max context" vs "useful context" as two very different bars.*
> The mistake is treating the maximum window size as the useful size. Just because something fits doesn't mean it helps. Send what helps the answer, and leave out what doesn't.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Every token should earn its place."*
> Every token should earn its place. Next: where each part of your prompt comes from.

## E039 · B · Where does each part of your prompt come from?

**0:00–0:15 · Hook**
*Screen: you on camera; then a final prompt with no idea where each line came from.*
> I printed the full prompt my app sends to the model, and I honestly couldn't tell where half of it came from. That's a problem.

**0:15–0:45 · Claim**
*Screen: one function "build_context()" with named inputs flowing in.*
> Assemble context in one function, from named sources, with a budget. Then you always know what's in the window, how big each part is, and where to change it, instead of hunting through strings glued together across the codebase. It's the same idea as keeping your database access in one place.

**0:45–1:30 · Show**
*Screen: build_context() with sections: rules, dealer facts, tool definitions, recent history; a printed budget report showing tokens per section. [CAPTURE: your report]*
> Here's my build context function. It takes four named sources: the rules, facts about the signed-in dealer, the tool definitions, and recent history. Each section has a token budget. Before every call, it prints a report: rules [CAPTURE] tokens, dealer facts [CAPTURE], tools [CAPTURE], history [CAPTURE]. When history goes over budget, it trims there, and only there. One place to look, one place to change. Debugging a strange answer now starts with one printed report instead of guesswork. Changes become one-line edits.

**1:30–1:50 · Gotcha**
*Screen: five files each adding a string to the prompt.*
> The trap is prompt strings concatenated in five different files. Nobody knows the full prompt, and every change risks breaking something else. Centralise it early.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "One function owns the context."*
> One function owns the context. Next: should AI read every manual first?

## E040 · C · Should AI read every manual first?

**0:00–0:15 · Hook**
*Screen: you on camera; then six policy documents being loaded into a prompt.*
> Before answering any question, should my assistant read all six policy documents, just in case? Or should it go and look things up only when it needs them?

**0:15–0:45 · Claim**
*Screen: two columns: "Preload" and "Fetch just in time".*
> It depends on what the information is like. Preload small, stable facts that are almost always relevant, like the dealer's name and opening hours. Give the model tools to fetch large or changing information when it actually needs it, like a specific policy section or this month's repair orders. Most good systems do both. The trick is deciding which is which for each piece of information. Getting that wrong wastes tokens or misses facts.

**0:45–1:30 · Show**
*Screen: version A: six policies preloaded into every prompt. Version B: just the policy titles preloaded, plus the policy_search tool. A table of tokens per question. [CAPTURE: your numbers]*
> Version A preloads all six policies into every request. Version B preloads only the list of policy titles and gives the model the policy search tool. For a question like "what's the labour rate for warranty work?", version A uses [CAPTURE] tokens. Version B uses [CAPTURE], because it fetches only the rate card. The model knows what exists from the titles, and fetches the contents when needed. For a simple greeting, version B costs almost nothing. The model only pays for what each question actually needs.

**1:30–1:50 · Gotcha**
*Screen: an extra round trip shown on a timeline.*
> The trade-off: fetching just in time adds extra steps and a bit of latency. For tiny, always-needed information, preloading is simpler and faster. So use both, and measure the token cost per question.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Load identifiers; fetch contents."*
> Load identifiers; fetch contents. Next: keeping a fifty-turn chat from overflowing.

## E041 · B · Keeping a 50-turn chat from overflowing

**0:00–0:15 · Hook**
*Screen: you on camera; then a conversation counter hitting turn 50 and a "context full" warning.*
> A service manager spends an hour with my assistant reviewing the month's warranty claims. Fifty turns in, the context is full. Do I just delete the oldest messages?

**0:15–0:45 · Claim**
*Screen: old turns compressing into a short summary block.*
> Better: compaction. When the conversation crosses a token threshold, summarise the older turns into a short note that keeps the decisions made, the constraints set and the tasks still open, and drop the raw messages. The conversation continues with the summary in place of the detail. Done well, the user never notices it happened.

**0:45–1:30 · Show**
*Screen: token counter crossing the threshold; the generated summary shown in full, with "currency = MYR" and "open: claim WC-1182 pending approval" highlighted. [CAPTURE: your summary]*
> Here's the trigger: at [CAPTURE] tokens, compaction runs. The older turns become this summary: [CAPTURE: show the summary]. It kept "all amounts in ringgit", the decision to exclude internal jobs, and the one claim still waiting for approval. The token count drops from [CAPTURE] to [CAPTURE], and the next answer still respects every constraint. I also keep a test that checks those three facts survive every compaction. It runs on every change.

**1:30–1:50 · Gotcha**
*Screen: a summary missing "currency = MYR", and the next answer in USD.*
> The danger is a summary that drops the one constraint that mattered. It reads well, it's short, and it silently loses the rule. Decide what must survive, then test it.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Test what your summary must keep."*
> Test what your summary must keep. Next: what's really eating your context?

## E042 · B · What's really eating your context?

**0:00–0:15 · Hook**
*Screen: you on camera; then a context window nearly full after only a few turns.*
> My context window was almost full after just six turns. The conversation was short. So what was actually eating all the space?

**0:15–0:45 · Claim**
*Screen: a pie chart of context by section, with "tool results" taking most of it.*
> Usually it's raw tool outputs. Every tool call can dump a big table into the conversation, and those tables stay there long after they're useful. Keep the conclusion, drop the bulk. A table that answered one question five turns ago is usually just weight now.

**0:45–1:30 · Show**
*Screen: a token breakdown before and after replacing old repair-order tables with one-line summaries and references. [CAPTURE: your breakdown]*
> Here's the breakdown before: instructions [CAPTURE] tokens, conversation [CAPTURE], and old tool results [CAPTURE]. Those are full tables of repair orders from earlier questions. Now I replace each old tool result with a one-line summary and a reference: "March warranty total RM 12,480 from 41 repair orders, result ID 7". After that, tool results take [CAPTURE] tokens, and if the model needs the full table again, it can fetch it by ID. The model still knows what it found; it just stops carrying the raw table around.

**1:30–1:50 · Gotcha**
*Screen: the model asking about a row that was cleared.*
> The risk is clearing a result the model still needs, like the list it's in the middle of reviewing. Clear old results, not the current task's. Be deliberate.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Keep findings, not payloads."*
> Keep findings, not payloads. Next: how can AI remember across sessions?

## E043 · C · How can AI remember across sessions?

**0:00–0:15 · Hook**
*Screen: you on camera; then a fresh session: "Hi! How can I help?"*
> Yesterday my assistant and I got halfway through reviewing warranty claims. Today I open a new session and it has no idea. How do you give an AI memory across sessions?

**0:15–0:45 · Claim**
*Screen: "Memory = data the app writes and reads".*
> Memory isn't the model learning. It's external storage that your application writes to and reads from: notes, files or database records. At the end of a session, the app saves what matters. At the start of the next one, it loads the relevant notes back into the context. The model itself stays exactly the same; it's the application that remembers.

**0:45–1:30 · Show**
*Screen: the assistant writing notes.md: "Reviewed claims 1–20; 3 flagged; next: claims 21–41"; a new session reading it and continuing from claim 21.*
> Here's how mine works. During the review, the assistant writes a short notes file: claims one to twenty reviewed, three flagged for missing photos, next up claim twenty-one. That file is saved under this user and this dealer. Tomorrow, a fresh session starts, the app loads those notes into the context, and the assistant says: "Last time we reviewed twenty claims and flagged three. Shall we continue with claim twenty-one?" No retraining, just data. The user can also read and edit those notes, which matters for trust.

**1:30–1:50 · Gotcha**
*Screen: a memory store mixing Dealer A and Dealer B notes; and an unverified claim saved as fact.*
> Two traps. Saving the model's unverified claims as facts, so mistakes become permanent. And mixing dealers in one memory store, so one dealer's notes show up for another. Store verified facts, scoped to one user and one dealer.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Memory is data; govern it like data."*
> Memory is data; govern it like data. Next: "we cache it" — cache what, exactly?
