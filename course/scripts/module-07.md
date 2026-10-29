# Module 7 — Caching and CAG

## E044 · C · "We cache it." Cache what, exactly?

**0:00–0:15 · Hook**
*Screen: you on camera; then a meeting slide: "Don't worry, we cache it."*
> In every AI architecture meeting, someone says "don't worry, we cache it." But cache what, exactly? Because there are at least three very different things that word can mean, and each one breaks in its own way.

**0:15–0:45 · Claim**
*Screen: three boxes: Response cache · Prefix cache · KV reuse.*
> A response cache stores final answers and returns them again for the same question. A prefix cache, offered by some providers, reuses the processing of a prompt's opening section that stays the same across calls. And KV reuse keeps a model's internal state, the key-value cache, so a local model doesn't redo work. Each one stores something different, and each one goes stale for a different reason.

**0:45–1:30 · Show**
*Screen: one request path from the service advisor through the app to the model, with the three caches marked where they sit; each labelled "stores…" and "stale when…".*
> Here's one request through my service analyst, with each cache marked where it sits. The response cache sits in my app: it stores "March warranty total for Dealer A equals this answer". It goes stale when new repair orders arrive. The prefix cache sits at the provider: it stores the processed system prompt and tool definitions. It breaks the moment any of that text changes. KV reuse sits inside a model runtime I host myself: it stores the model's working state for a preloaded document set, and goes stale when those documents change. Three caches, three invalidation rules.

**1:30–1:50 · Gotcha**
*Screen: a cache key "march_warranty_total" without a dealer, serving Dealer A's answer to Dealer B.*
> The dangerous one: a response cache keyed without the dealer. Dealer B asks the same question and gets Dealer A's answer, instantly and confidently.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Name the cache before you trust it."*
> Name the cache before you trust it. Next: stop paying twice for the same prompt.

## E045 · B · Stop paying twice for the same prompt

**0:00–0:15 · Hook**
*Screen: you on camera; then a usage log showing the same 3,000-token system prompt billed on every call.*
> Every call to my assistant sends the same long system prompt and the same tool definitions. Thousands of identical tokens, paid for at full price, on every single request. Why?

**0:15–0:45 · Claim**
*Screen: prompt laid out as "stable prefix" then "variable suffix".*
> Because I hadn't ordered the prompt for caching. Put stable content first, the instructions and tools that never change, and variable content last, like the user's question. A provider that supports prefix caching can then reuse the processed prefix at a lower cost, and the usage fields tell you whether it actually did.

**0:45–1:30 · Show**
*Screen: the reordered prompt; a cold first call and a warm second call, each with cached-token counts and latency from usage. Label SDK and date. [CAPTURE: your numbers, SDK, date]*
> Here's the prompt reordered: system instructions, then tool definitions, then dealer facts, and only then the question. First call, cold: cached tokens [CAPTURE], time [CAPTURE] milliseconds. Second call with a different question, warm: cached tokens [CAPTURE], time [CAPTURE]. Those numbers come straight from the usage fields in the response, not from my guess. Recorded with [CAPTURE: SDK and version] on [CAPTURE: date].

**1:30–1:50 · Gotcha**
*Screen: "Current time: 14:32:07" at the top of the system prompt, cache hits at zero.*
> The classic mistake is a timestamp at the top of the prompt. It changes every second, so the prefix is never the same, and the cache never hits.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "No verified cache hit, no caching claim."*
> No verified cache hit, no caching claim. Next: everything fits in the window — do you still need RAG?

## E046 · B · Everything fits in the window. Still need RAG?

**0:00–0:15 · Hook**
*Screen: you on camera; then six policy documents fitting comfortably inside a context window bar.*
> All six of my policy documents fit inside the context window with room to spare. So why bother with retrieval at all? Why not preload everything and cache it?

**0:15–0:45 · Claim**
*Screen: two approaches: "Retrieve per question (RAG)" vs "Preload + cache (CAG)".*
> For a small, stable, authorised set of documents, preloading with cache reuse, sometimes called cache-augmented generation, can match retrieval in fewer steps. But it isn't automatically better. Measure quality, freshness and cost on the same questions, then decide. The question is which costs and risks matter more for your documents.

**0:45–1:30 · Show**
*Screen: the same 15 questions by retrieval and by preload: quality, tokens, cold and warm latency; then a warranty policy update and which approach goes stale. [CAPTURE: your table]*
> Same fifteen questions, two ways. Retrieval: quality [CAPTURE], average tokens [CAPTURE], latency [CAPTURE]. Preload with verified cache hits: quality [CAPTURE], tokens [CAPTURE], cold latency [CAPTURE], warm [CAPTURE]. Then I update the warranty policy. The retrieval version picks up the new section on the next question. The preload version keeps serving the old text until I [CAPTURE: rebuild the preload and invalidate the cache]. Measure both.

**1:30–1:50 · Gotcha**
*Screen: a preloaded bundle containing Dealer B's goodwill policy, sent to a Dealer A user.*
> The traps: preloading documents a dealer isn't allowed to see, or keeping the cache alive after a policy changes. Fast and wrong is still wrong. Rebuild the preload whenever its sources change.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Choose by corpus size, change rate and permissions."*
> Choose by corpus size, change rate and permissions. Next: who decides the next step — your code or AI?
