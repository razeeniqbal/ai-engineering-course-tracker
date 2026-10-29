# Module 1 — ML foundations and baselines

## E007 · C · Brake squeal: do you even need AI?

**0:00–0:15 · Hook**
*Screen: you on camera; then a repair-order line: "Squeal when braking at low speed."*
> "Squeal when braking at low speed." Any service advisor knows that's a brake job. So do you really need AI to sort it into the right category?

**0:15–0:45 · Claim**
*Screen: three columns: Rules · Machine learning · LLM, each with "best for…" underneath.*
> Not always. There are three tools here. Rules are perfect for fixed logic, like "if it says brake, it's brakes". Machine learning is great for patterns you can label with examples. And a large language model handles open-ended, messy language. The skill is starting with the simplest one that actually meets your target, and only moving up when it doesn't.

**0:45–1:30 · Show**
*Screen: three complaint lines run through a keyword rule, a trained classifier and an LLM, with a tick or cross for each.*
> Let's test three complaints. "Brake squeal at low speed": the keyword rule gets it, the classifier gets it, the LLM gets it. "Grinding noise from the front when I stop": no "brake" keyword, so the rule misses it, but the classifier and LLM catch it. "Kereta bunyi pelik bila nak berhenti": Malay, and only the LLM handles it, unless you trained the classifier on Malay too. Each tool breaks in a different place, and each one costs more than the last.

**1:30–1:50 · Gotcha**
*Screen: "98% with a lookup table" next to "LLM: slower, pricier".*
> The mistake is reaching for an LLM when a simple keyword table already gets ninety-eight percent right. You'd pay more and wait longer for almost nothing. Start with the cheap baseline, measure it, and only add the expensive layer where the numbers show the cheap one failing.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "The baseline decides whether complexity is worth it."*
> The baseline decides whether complexity is worth it. Next: is the AI learning from my chats?

## E008 · C · Is the AI learning from my chats?

**0:00–0:15 · Hook**
*Screen: you on camera.*
> When you correct a chatbot and it says "thanks, I'll remember that", is the model actually learning from you?

**0:15–0:45 · Claim**
*Screen: two words: "Training" and "Inference".*
> There are two very different phases. Training is when a model's weights, its billions of internal numbers, get adjusted using huge amounts of data. Inference is when you use the finished model: the weights are locked, and it just produces output. Your chat happens during inference, so it doesn't retrain the model. That's an important distinction for privacy too, because it decides what happens to your data.

**0:45–1:30 · Show**
*Screen: left panel: dataset → training loop → weights. Right panel: locked weights + your prompt → output.*
> On the left: training. Data goes in, the training loop nudges the weights again and again, and out comes a model file. That happens once, it's expensive, and it's done by the provider. On the right: inference. The weights are frozen. Your prompt goes in, text comes out. When it seems to remember something you said earlier in the conversation, that's because your earlier messages are still in its context window, not because it learned. Close the conversation, start a new one, and that earlier context is gone, unless the app saved it somewhere.

**1:30–1:50 · Gotcha**
*Screen: a product "memory" setting toggle, labelled "saved notes, not training".*
> The confusing part is product memory features. Those save notes about you and quietly add them to future prompts. Useful, but that's context being reused, not the model being retrained. Check what a product saves before you share anything sensitive.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Context changes the answer; training changes the model."*
> Context changes the answer; training changes the model. Next: how AI knows what "it" means.

## E009 · C · How does AI know what "it" means?

**0:00–0:15 · Hook**
*Screen: you on camera; then the sentence "The car was towed in because it wouldn't start."*
> "The car was towed in because it wouldn't start." You know "it" means the car, not the tow truck. How does a model work that out?

**0:15–0:45 · Claim**
*Screen: the word "it" with faint lines to every other word.*
> Through a mechanism called attention. When the model builds its understanding of each token, it looks at every other token in the context and decides how much each one matters. "It" pays a lot of attention to "car" and "start", and very little to "towed". That's how meaning gets resolved across a sentence. It's the core idea inside the transformer, the architecture behind today's language models.

**0:45–1:30 · Show**
*Screen: the sentence with weighted lines from "it" (thick to "car", thinner to "start", faint to others); then a long repair history with lines reaching back several lines.*
> Here's a simplified picture. From "it", the thickest line goes to "car", because a car is the kind of thing that wouldn't start. Now scale that up. In a long repair history, a mention of "the same noise as last time" can attend all the way back to a complaint from three visits ago. Every token can look at every other token in the window, and that's both the power and the cost of these models. It's also why longer contexts cost more: more tokens means many more connections to weigh.

**1:30–1:50 · Gotcha**
*Screen: "attention weights ≠ reasoning".*
> One caution: attention weights look like an explanation, but they're just one internal signal among many. Don't read them as the model's reasoning. Treat them as a hint.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Everything in the window can influence everything else."*
> Everything in the window can influence everything else, which is why context choices matter. Next: squeaky brakes versus noise when stopping.

## E010 · B · "Squeaky brakes" vs "noise when stopping": same thing?

**0:00–0:15 · Hook**
*Screen: you on camera; then two phrases side by side.*
> "Squeaky brakes" and "noise when stopping" don't share a single word. So how does a system know they mean the same thing?

**0:15–0:45 · Claim**
*Screen: phrases turning into points on a 2D map.*
> Embeddings. An embedding model turns text into a long list of numbers, a vector, where similar meanings end up close together. Then cosine similarity measures how close two vectors are, from completely unrelated to essentially identical. The model that produces these vectors was trained so that texts used in similar ways land near each other.

**0:45–1:30 · Show**
*Screen: six complaint descriptions, including "bunyi bila brek" and "brek berbunyi", embedded; a 6×6 similarity matrix; nearest neighbour search. [CAPTURE: your similarity scores]*
> I embed six complaints, two of them in Malay, and print the similarity matrix. "Squeaky brakes" and "noise when stopping" score [CAPTURE], high, even with no words in common. Now I search for "bunyi bila brek", which means "noise when braking", and its nearest neighbour is [CAPTURE: the English brake complaint]. That's what makes semantic search and duplicate detection possible across languages. That matters for a Malaysian dealership, where advisors type in both languages.

**1:30–1:50 · Gotcha**
*Screen: "brake pad replacement" vs "brake pad recall", score [CAPTURE], with "customer-paid" and "warranty" labels.*
> But close isn't the same. "Brake pad replacement" and "brake pad recall" score as very similar, yet one is customer-paid and one is warranty. Money moves in opposite directions.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "Similarity finds candidates; your logic decides."*
> Similarity finds candidates; your logic decides. Next: my classifier scored ninety-nine percent, and I didn't believe it.

## E011 · B · My classifier scored 99%. I didn't believe it.

**0:00–0:15 · Hook**
*Screen: you on camera; then "Accuracy: 99%".*
> My repair-order classifier scored ninety-nine percent on its first try. That's exactly when I stopped trusting it.

**0:15–0:45 · Claim**
*Screen: three checks: "Group split", "Baseline", "Per-class errors".*
> A score means nothing on its own. Before trusting it, split the data so similar examples can't sit on both sides, compare against a dumb baseline, and read the errors class by class. My hundred synthetic complaints came from templates, and that's where the trouble was.

**0:45–1:30 · Show**
*Screen: random split result [CAPTURE] → group split result [CAPTURE]; majority-class baseline [CAPTURE]; confusion matrix with "electrical" and "engine" highlighted.*
> With a random split, near-copies from the same template landed in both training and test, so the model just recognised them: [CAPTURE] percent. Split by template group instead, and it drops to [CAPTURE]. A baseline that always guesses the most common category gets [CAPTURE], so the classifier is still clearly better. And the confusion matrix shows where it struggles: "car won't start" complaints get mixed up between electrical and engine, which honestly confuses humans too.

**1:30–1:50 · Gotcha**
*Screen: two nearly identical sentences, one in train and one in test.*
> The trap is near-duplicates on both sides of the split. They inflate your score and hide how the model does on genuinely new complaints.

**1:50–2:00 · Takeaway**
*Screen: you on camera holding "No split and no baseline, no score."*
> A score means nothing without its split and its baseline. Next: should AI add up your service revenue?
