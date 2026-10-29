# Module 14 — Local inference and quantization

## E081 · C · 16-bit or 4-bit: what do you lose?

**0:00–0:15 · Hook**
*Screen: you on camera; then the same model listed twice for download: 16-bit and 4-bit, very different file sizes.*
> I can download the same model in sixteen-bit or four-bit. The four-bit file is about a quarter of the size. So what am I actually giving up?

**0:15–0:45 · Claim**
*Screen: one number stored with fewer and fewer bits.*
> Quantization stores each of the model's weights with lower precision, using fewer bits per number. That cuts memory a lot, and lets bigger models fit on smaller machines. But rounding every weight has a quality cost, and the size of that cost depends on the model and on your task. You have to measure it yourself. For many tasks the loss is small; for some it isn't.

**0:45–1:30 · Show**
*Screen: memory for one model at 16, 8 and 4 bits (labelled estimates); then accuracy on the repair-order set at two precisions. [CAPTURE: your numbers]*
> Here's the memory needed for one model's weights at each precision, as labelled estimates. Sixteen-bit: about [CAPTURE] gigabytes. Eight-bit: about [CAPTURE]. Four-bit: about [CAPTURE]. Now the part that matters: quality on my own task. On the held-out repair-order categorisation set, sixteen-bit scores [CAPTURE] and four-bit scores [CAPTURE]. For this task, that's [CAPTURE: an acceptable or unacceptable drop]. On a harder task, the drop could be bigger. Your result depends on your task, so this test is worth an afternoon.

**1:30–1:50 · Gotcha**
*Screen: "4-bit = faster?" with a question mark.*
> A common assumption is that lower precision is always faster. Not necessarily. Speed depends on your hardware and runtime, and some setups are actually slower at low precision. Test speed on your own machine, not someone else's benchmark.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Measure quality and speed on your own device."*
> Measure quality and speed on your own device. Next: it loaded fine, then ran out of memory.

## E082 · C · It loaded fine, then ran out of memory

**0:00–0:15 · Hook**
*Screen: you on camera; then "Model loaded ✓", then a long prompt and "out of memory".*
> The model loaded fine, with memory to spare. Then I sent it a long repair history, and it ran out of memory. How does a model that fits suddenly not fit?

**0:15–0:45 · Claim**
*Screen: one bar: fixed "weights" segment plus a growing "KV cache" segment.*
> Because serving a model needs memory for two things. The weights, which are fixed. And the KV cache, which stores intermediate values for every token in the context, so the model doesn't recompute them. The KV cache grows with the length of each conversation and with the number of requests you serve at the same time.

**0:45–1:30 · Show**
*Screen: an animated memory bar: weights stay fixed; the KV cache grows as context length increases, then grows again as concurrent users increase, until it hits the GPU limit.*
> Watch the bar. The weights take a fixed chunk, and that's what you saw when the model loaded. Now a short question: the KV cache adds a sliver. A long repair history with every past visit: the KV cache grows a lot. Now four service advisors use it at the same time, each with a long history: four KV caches, and we hit the memory limit. The model didn't get bigger. The context and the concurrency did. That's why serving many users needs much more memory than a single test.

**1:30–1:50 · Gotcha**
*Screen: "model file: 4 GB → buy 4 GB of GPU memory" with a red cross.*
> The trap is sizing hardware from the model file size alone. Always budget extra for the KV cache at your real context lengths and number of users. Plan for your busiest hour.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Budget memory for context and concurrency, not just weights."*
> Budget memory for context and concurrency, not just weights. Next: swap in a local model without touching the app.

## E083 · B · Swap in a local model without touching the app

**0:00–0:15 · Hook**
*Screen: you on camera; then MODEL_PROVIDER=hosted changing to MODEL_PROVIDER=local.*
> Remember the adapter I built in the very first module? Today it pays off. I'm switching my whole service analyst from a hosted model to one running on my own machine, by changing one line.

**0:15–0:45 · Claim**
*Screen: the ModelClient interface with a third implementation: LocalModel.*
> Because only the adapter knows which provider is behind it, a local runtime can plug in behind the same interface, and the same tests and evals run unchanged. The app never knows the difference. This is the whole reason the adapter existed.

**0:45–1:30 · Show**
*Screen: the environment variable switch; the same eval running; outputs and latency compared. Label runtime, model and date. [CAPTURE: your results, runtime, model, date]*
> Here's the switch: one environment variable, from hosted to local. I run the same offline eval, same questions, same graders. Hosted: score [CAPTURE], average latency [CAPTURE]. Local: score [CAPTURE], latency [CAPTURE]. Here are a few answers side by side. Running [CAPTURE: runtime] with [CAPTURE: model] on [CAPTURE: date]. No other code changed. The evals tell me whether local is good enough, not my impression.

**1:30–1:50 · Gotcha**
*Screen: a local model returning malformed tool calls.*
> One thing to check first: some local models don't support reliable tool calling or structured output. If your app depends on those, test them before switching. Run the full eval before you switch for real.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "The adapter from Module 0 pays off here."*
> The adapter from module zero pays off here. Next: faster per request, or more requests per minute?

## E084 · B · Faster per request, or more requests per minute?

**0:00–0:15 · Hook**
*Screen: you on camera; then two configurations: one answers a single question faster, the other handles more questions per minute.*
> One configuration answers a single question faster. The other handles more questions per minute when the whole service team is using it. Which one should I choose?

**0:15–0:45 · Claim**
*Screen: "Latency: time for one request" and "Throughput: work finished per minute".*
> Latency is how long one request takes. Throughput is how much work finishes per minute across everyone. They're different, and they often trade off. Choose a configuration on quality and both of these, measured on your device, at realistic levels of use. A fast single answer means little if the team waits in a queue. Measure both.

**0:45–1:30 · Show**
*Screen: two configurations at 1, 4 and 8 concurrent requests: cold and warm latency, throughput and eval score. [CAPTURE: your table]*
> Two configurations, tested at one, four and eight requests at the same time. Configuration A at one user: [CAPTURE] seconds. At eight users: [CAPTURE] seconds each, throughput [CAPTURE] answers a minute. Configuration B at one user: [CAPTURE], at eight: [CAPTURE], throughput [CAPTURE]. Eval scores: [CAPTURE] and [CAPTURE]. For a team of [CAPTURE] advisors, I'd pick [CAPTURE], because [CAPTURE]. Your team size changes the right answer.

**1:30–1:50 · Gotcha**
*Screen: a benchmark of one warm request labelled "production performance".*
> The trap: benchmarking one warm request and calling it production performance. Real users arrive cold, together, and with long contexts. Test at realistic load.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Choose with the full table, not the fastest number."*
> Choose with the full table, not the fastest number. Next: the capstone — an AI answer you can actually check.
