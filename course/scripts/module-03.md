# Module 3 — Retrieval

## E019 · C · How AI answers from your documents

**0:00–0:15 · Hook**
*Screen: you on camera; then a question: "Is a brake noise complaint at 60,000 km covered under warranty?"*
> A service advisor asks: is a brake noise complaint at sixty thousand kilometres covered under warranty? The answer is in our warranty policy, not in the model's training. So how can a model answer from your own documents?

**0:15–0:45 · Claim**
*Screen: two stages: "Retrieve" → "Generate".*
> With a pattern called retrieval-augmented generation, or RAG, and it has two stages. First, retrieval: search your documents and pick the passages most likely to contain the answer. Second, generation: give those passages to the model and ask it to answer using only them. The crucial point is that each stage can fail on its own, and in completely different ways.

**0:45–1:30 · Show**
*Screen: pipeline diagram: question → search over 6 policy documents → top 3 passages → model → answer with citation. Then two red markers: one at retrieval, one at generation.*
> Here's my pipeline. The question goes into a search over my six policy documents. The top three passages come back, and the model writes an answer with a citation. Now, two failures. Failure one, at retrieval: the passage about mileage limits wasn't in the top three, so the model never saw it and answered from the wrong section. Failure two, at generation: the right passage was there, but the model misread "100,000 kilometres or five years, whichever comes first". Same wrong answer on screen, two completely different fixes.

**1:30–1:50 · Gotcha**
*Screen: a single score "Answer correct: 70%" with a question mark over which stage failed.*
> The mistake is only judging the final answer. If you only measure the end result, you can't tell whether to fix your search or your prompt, and you'll probably fix the wrong one.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Evaluate retrieval separately."*
> Evaluate retrieval separately. Next: the chunk that lost the warranty exception.

## E020 · B · The chunk that lost the warranty exception

**0:00–0:15 · Hook**
*Screen: you on camera; then a chunk reading "Covered for 100,000 km." with the next chunk starting "Except vehicles used commercially."*
> My assistant said a taxi's gearbox was covered under warranty. It wasn't. The exception was there in the policy. It just ended up in a different chunk.

**0:15–0:45 · Claim**
*Screen: a document cut into chunks, each tagged with document ID, version, dealer and section.*
> Before retrieval, documents get split into chunks small enough to search and to fit in the context. Chunk on meaningful boundaries, like whole clauses or sections, not every five hundred characters. And keep the document ID, version, dealer and location attached to every single chunk.

**0:45–1:30 · Show**
*Screen: the broken split, then the fixed split with the rule and exception together, then the metadata printed under each chunk. [CAPTURE: your chunker output]*
> Here's my first chunker: fixed size, five hundred characters. It cut the coverage rule from its exception, right in the middle of a clause. Now the fixed version splits on section headings, so "covered for one hundred thousand kilometres, except vehicles used commercially" stays together. And every chunk now carries its metadata: warranty policy, version two, section four point one, Dealer A. Ask the taxi question again, and the answer is [CAPTURE: correct, with the exception cited].

**1:30–1:50 · Gotcha**
*Screen: a chunk with no metadata and a citation that says "source: unknown".*
> The other trap is chunks with no source information. If you don't know where a chunk came from, you can't cite it, and nobody can check the answer.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "No provenance, no citation."*
> No provenance, no citation. Next: which search finds bulletin SB-23-04?

## E021 · B · Which search finds bulletin "SB-23-04"?

**0:00–0:15 · Hook**
*Screen: you on camera; then a search box with "SB-23-04".*
> A technician types "SB-23-04", the code for a service bulletin about brake noise. Which kind of search actually finds it?

**0:15–0:45 · Claim**
*Screen: three columns: Keyword (BM25) · Embedding · Hybrid.*
> There are two main families. Keyword search, like BM25, matches exact words and codes. Embedding search matches meaning. They tend to win on different kinds of questions, so compare both, plus a hybrid that combines them, on your own documents before you pick one. Hybrid search simply runs both and merges the rankings, so you get exact matches and meaning in one list.

**0:45–1:30 · Show**
*Screen: three queries run through all three methods; a Recall@3 table. [CAPTURE: your results]*
> Three queries. "SB-23-04": keyword search finds it straight away, while embedding search [CAPTURE: misses it or ranks it low], because a code has no real meaning to embed. "Grinding noise when braking": embeddings win, since the bulletin says "abnormal brake noise" instead. "Brake bulletin from last year": hybrid does best by combining both. Across fifteen labelled questions, Recall at three is [CAPTURE] for keyword, [CAPTURE] for embeddings and [CAPTURE] for hybrid. Your numbers will differ, so run it.

**1:30–1:50 · Gotcha**
*Screen: keyword search crossed out with "we use AI search now".*
> The mistake is ripping out keyword search entirely because embeddings feel more modern. Codes, part numbers and model names need exact matching.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Start with keywords; measure before adding more."*
> Start with keywords; measure before adding more. Next: wrong answer, bad search or bad model?

## E022 · C · Wrong answer: bad search or bad model?

**0:00–0:15 · Hook**
*Screen: you on camera; then a wrong answer about a warranty labour rate.*
> My assistant quoted the wrong warranty labour rate. Was that the search's fault, or the model's? Guess wrong, and you'll spend a week fixing the part that wasn't broken.

**0:15–0:45 · Claim**
*Screen: "Recall@k = did the right passage appear in the top k?"*
> Recall at k answers that question before any model is involved. You label which passage actually contains the answer for each test question. Then you check whether that passage shows up in the search's top k results. If it doesn't, the model never had a chance, and the problem is retrieval. It's one of the cheapest, most useful measurements in the whole pipeline.

**0:45–1:30 · Show**
*Screen: a table of 15 labelled questions with ✓/✗ for top-3; one row highlighted where the right passage ranks 5th.*
> Here are my fifteen labelled questions, each with the correct passage written down in advance. For each one, I check: is that passage in the top three results? Fourteen times, yes. But look at this row, the labour rate question. The right passage ranks fifth. So Recall at three misses it, the model only sees three other passages, and it confidently quotes an old rate from the wrong document. That's not a prompt problem. That's a search problem, and now I know exactly where to look. Fix the search, rerun, and recall tells you whether it worked.

**1:30–1:50 · Gotcha**
*Screen: labels being added after looking at search results.*
> The trap is labelling the relevant passages after you've seen what the search returned. You'll subconsciously pick what it found, and your recall will look far better than it really is. Label first, search second.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Measure retrieval before blaming generation."*
> Measure retrieval before blaming generation. Next: does this source really say that?

## E023 · B · Does this source really say that?

**0:00–0:15 · Hook**
*Screen: you on camera; then an answer with a neat citation link.*
> The answer came with a citation, linked to a real section of the warranty policy. Looks trustworthy. But does that section actually say what the answer claims?

**0:15–0:45 · Claim**
*Screen: "Citation exists" ≠ "Citation supports the claim".*
> A citation is only useful if the cited passage contains the specific fact being claimed. A real link attached to an unsupported claim is worse than no citation at all, because it makes a wrong answer look verified.

**0:45–1:30 · Show**
*Screen: three answers; for each, the cited passage opens and the claimed number is highlighted or missing. [CAPTURE: your three cases]*
> I open the passage behind each citation and check the exact fact. Answer one says warranty covers a hundred thousand kilometres, and the cited passage says exactly that. Supported. Answer two says the warranty labour rate is ninety ringgit an hour, but the cited passage is about parts returns, with no rate in it. Unsupported. Answer three [CAPTURE: your third case]. So I add a check: for every cited number or condition, it must appear in the cited text, or the answer is flagged.

**1:30–1:50 · Gotcha**
*Screen: a link icon with a green tick, over a wrong number.*
> The trap is checking that citations exist and point somewhere real, without checking what they say. Links are easy. Support is the hard part.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Check the claim, not just the link."*
> Check the claim, not just the link. Next: when the manual doesn't say.

## E024 · C · When the manual doesn't say

**0:00–0:15 · Hook**
*Screen: you on camera; then a question: "What's our policy on EV battery replacement?"*
> Someone asks about our policy on electric vehicle battery replacement. None of our six documents mention it. What should the assistant do?

**0:15–0:45 · Claim**
*Screen: "Not covered" with a green tick.*
> Abstain, clearly. "The documents don't cover this" is a correct answer, not a failure, as long as it comes with a reason and what would be needed. And it's testable: you can measure whether your assistant abstains when it should, just like you measure whether it answers correctly when it can. A good abstention says what's missing and where to find it, so the user isn't left stuck.

**0:45–1:30 · Show**
*Screen: the EV question answered with "Not covered in the current policies. You'd need the EV warranty addendum or a manufacturer bulletin." Then a test table of five absent topics with ✓ for correct abstention.*
> Here's my assistant's answer to the battery question: "The current policies don't cover EV battery replacement. You'd need the EV warranty addendum or a manufacturer bulletin to answer this." That's useful. It's honest, and it tells the advisor where to look. Then I test it properly: five topics I know are not in the documents, from EV batteries to tyre warranties. The assistant should abstain on all five, and I score it just like any other test. An assistant that admits gaps is one people keep trusting when it does answer.

**1:30–1:50 · Gotcha**
*Screen: an eval report with only answerable questions.*
> The mistake is only testing questions that have answers. Then an assistant that confidently invents something for every question can still score perfectly. Include questions with no answer in every eval set.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Test the unanswerable too."*
> Test the unanswerable too. Next: is the top embedding model the best one for your manuals?
