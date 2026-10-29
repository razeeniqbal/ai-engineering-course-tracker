# Module 4 — Retrieval experiments and reranking

## E025 · B · Is the #1 embedding model best for your manuals?

**0:00–0:15 · Hook**
*Screen: you on camera; then a public embedding leaderboard with the top model highlighted.*
> There's a leaderboard of embedding models, and everyone picks number one. But is it actually the best model for my warranty documents, with Malay complaints and part numbers mixed in?

**0:15–0:45 · Claim**
*Screen: three criteria: Recall@k on your questions · cost · speed.*
> Pick an embedding model by measuring it on your own labelled questions, alongside what it costs and how fast it is. A public benchmark is built on different text, in different languages, for different tasks. Your data is the only benchmark that matters for your app.

**0:45–1:30 · Show**
*Screen: two embedding models run on the same 15 questions; a table of Recall@3, embedding time and index size. [CAPTURE: your table]*
> I take two embedding models: the leaderboard favourite and a smaller, cheaper one. Same fifteen labelled questions, same chunks. Recall at three: [CAPTURE] for the big one, [CAPTURE] for the small one. Time to embed all my documents: [CAPTURE] versus [CAPTURE]. Index size: [CAPTURE] versus [CAPTURE]. On my data, [CAPTURE: which one wins, and by how much]. That's the number I care about, not the leaderboard rank.

**1:30–1:50 · Gotcha**
*Screen: leaderboard "English web text" vs your data "Malay + part numbers".*
> The trap is trusting a public benchmark built on very different text. A model that's brilliant at English web pages can struggle with Malay complaints and service codes.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Your data is the benchmark."*
> Your data is the benchmark. Next: do you need a separate vector database?

## E026 · B · Do you need a separate vector database?

**0:00–0:15 · Hook**
*Screen: you on camera; then an architecture with Postgres plus a separate vector database, arrows everywhere.*
> Every RAG tutorial adds a separate vector database. But my repair orders and policies already live in PostgreSQL. Do I really need another system?

**0:15–0:45 · Claim**
*Screen: one Postgres table with columns: chunk, dealer, version, embedding.*
> Often you don't. With the pgvector extension, embeddings sit in the same database as the rest of your data. That means the dealer filter and the vector search run in a single query, so there's no way to search first and forget to filter later.

**0:45–1:30 · Show**
*Screen: the table definition; one SQL query that filters by dealer and orders by vector distance; then exact vs. approximate index results compared. [CAPTURE: your query plan and recall]*
> Here's my chunks table: the text, the dealer, the policy version, and an embedding column. And here's one query: where dealer equals the signed-in dealer, order by distance to the question's embedding, limit three. One query, filter and search together. Then I add an approximate index for speed. Exact search gets Recall at three of [CAPTURE]. The approximate index gets [CAPTURE], and drops query time from [CAPTURE] to [CAPTURE]. For my size, that trade-off is [CAPTURE: worth it or not].

**1:30–1:50 · Gotcha**
*Screen: "approximate index: assumed 100% recall" crossed out.*
> The catch: approximate indexes trade some recall for speed. That's often fine, but measure how much you lose instead of assuming it's nothing.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Keep the filter and the search in one place."*
> Keep the filter and the search in one place. Next: the right passage, ranked eighth.

## E027 · B · Right passage, ranked eighth

**0:00–0:15 · Hook**
*Screen: you on camera; then a results list with the correct passage at position 8.*
> My search did find the right passage about warranty mileage. It just ranked it eighth, and the model only reads the top three. Can I fix the order?

**0:15–0:45 · Claim**
*Screen: "Retrieve 20" → "Rerank" → "Keep 3".*
> Yes, with a reranker. First-stage search is fast but rough. A reranker takes each candidate and scores it against the question much more carefully, then reorders them. You retrieve wide, say twenty candidates, and then keep only the best three after reranking. It's slower per passage, which is exactly why you only run it on a short list.

**0:45–1:30 · Show**
*Screen: top 20 candidates → reranker → top 3; a before/after Recall@3 table, plus added latency. [CAPTURE: your numbers]*
> Here's the pipeline. Embedding search returns the top twenty. The reranker scores all twenty against the question, and the mileage passage jumps from eighth to [CAPTURE: its new rank]. Across my fifteen questions, Recall at three goes from [CAPTURE] to [CAPTURE]. The cost is extra time: [CAPTURE] milliseconds more per question. For a service advisor waiting on an answer, that's [CAPTURE: acceptable or not]. Try it on your own questions.

**1:30–1:50 · Gotcha**
*Screen: a passage missing from the 20 candidates, with "reranker can't see this".*
> One hard limit: a reranker can only reorder what the first stage found. If the right passage never made the candidate list, no reranker can save you.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Retrieve wide, rerank narrow."*
> Retrieve wide, rerank narrow. Next: the warranty policy changed in July.

## E028 · B · The warranty policy changed in July

**0:00–0:15 · Hook**
*Screen: you on camera; then two documents: "Warranty policy v1 (from Jan)" and "v2 (from July)".*
> Our warranty policy changed in July. Then someone asked about a claim from August, and the assistant quoted the old March version. Why?

**0:15–0:45 · Claim**
*Screen: each chunk tagged with "effective from" and "effective to" dates.*
> Because nothing told it which version applied. Store the version and its effective dates with every chunk, and select the version that was in force on the date the question is about, not just the newest one, and not just whichever ranks highest. Then retrieval only searches the passages that were actually true on that day.

**0:45–1:30 · Show**
*Screen: an August claim answered from version 2; a May claim answered from version 1, each with its citation. [CAPTURE: your two answers]*
> Each chunk now carries "effective from" and "effective to". When a question mentions a date, or the claim has a repair date, the search filters to the version in force on that day. An August claim gets answered from version two: [CAPTURE: the v2 rule]. A May claim gets version one: [CAPTURE: the v1 rule]. Both answers cite the right version, and an auditor can see why. That's what makes it auditable.

**1:30–1:50 · Gotcha**
*Screen: "ORDER BY version DESC LIMIT 1" with a red cross.*
> The tempting shortcut is always picking the latest version. That works for new questions and silently breaks every question about the past. Past questions need past rules.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Freshness is a rule, not a sort by date."*
> Freshness is a rule, not a sort by date. Next: query rewriting, multi-query and graph RAG — do you need them?

## E029 · C · Query rewriting, multi-query, graph RAG: do you need them?

**0:00–0:15 · Hook**
*Screen: you on camera; then a pile of buzzwords: query rewriting, multi-query, HyDE, graph RAG.*
> Query rewriting. Multi-query search. Graph RAG. Every week there's a new advanced RAG technique. Should you be adding all of them to your app?

**0:15–0:45 · Claim**
*Screen: "Measured failure pattern → one technique → confirm on held-out".*
> Only when you can name the problem it fixes. Add an advanced technique only to fix a failure pattern you've actually measured, then confirm the improvement on held-out questions you didn't tune on. Otherwise you're just adding cost and latency in the hope that something gets better. Each technique solves a specific kind of miss, so you need to know which kind of miss you have.

**0:45–1:30 · Show**
*Screen: a failure log grouped by cause: "code asked by description" (4), "wrong version" (2), "absent topic" (1). Query expansion fixes the first group only.*
> Here's my failure log, grouped by cause. The biggest group: people asking for codes by description, like "the brake noise bulletin" instead of "SB-23-04". That's four failures. For exactly that pattern, query expansion makes sense: rewrite the question to include likely codes before searching. I add it, and those four get fixed. But look: the version failures and the absent-topic failure don't change at all, because they have different causes. And graph RAG wouldn't have fixed any of them. The lesson is to group failures by cause first, then pick tools.

**1:30–1:50 · Gotcha**
*Screen: latency bar growing with each stacked technique, accuracy flat.*
> The trap is stacking techniques because they sound clever. Each one adds latency and cost, and often the score doesn't move at all. Measure each addition on held-out questions, and remove anything that doesn't earn its place.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Diagnose the miss, then pick the fix."*
> Diagnose the miss, then pick the fix. Next season: can AI actually run code?
