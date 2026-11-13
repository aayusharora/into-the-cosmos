# Your presentation, explained

**48 slides. 44.5 minutes as written.** This is the only file you need on the day.

---

## The talk in one sentence

> **You ask "is it worth going outside tonight?" The model cannot
> answer it. Ten things are missing. We add them one at a time —
> and then everything you just watched breaks.**

Asked on slide 2, answered on slide 31. Slide 32 turns the talk over.

## The rhythm

Seven times in act one, the deck runs the same three beats:

| | | |
|---|---|---|
| **gap** | deep red, one line | *what it still cannot do* |
| **code** | navy, one function | *the fix, in a few lines* |
| **output** | a real recorded demo | *what actually came back* |

The red slides are the ones people forget to leave room for. Each is
about fifteen seconds of silence while the room gets ahead of you —
that anticipation is the reason they exist. Do not read them twice.

## The shape

| Slides | | Runs |
|---|---|---|
| 1–31 | **Act One.** The question, and the system that answers it | 26 min |
| 32–42 | **Act Two.** Everything you just watched broke | 12.5 min |
| 43–45 | **Coda.** Point the same four moves somewhere else | 3.25 min |
| 46–48 | **Close.** The six rules, and what to build on Monday | 2.75 min |

**Slide 32 is the hinge.** Stop there. The question
is answered and the room has had its payoff — if you simply carry on
they will feel the talk should have ended. Say you are starting the
second half on purpose, then speed up.

## The ten things

| | Needs | Gap | Code | Output |
|---|---|---|---|---|
| 1–3 | Eyes, a loop, a first tool | — | 9 | 11 |
| 4 | Something to look at | 12 | 13 | 14 |
| 5 | A sense of when | 15 | 16 | 17 |
| 6 | Memory | 18 | 19 | 22 |
| 7 | Judgement to chain | 23 | 24 | 24 |
| 8 | The nerve to say nothing | 25 | 26 | 26 |
| 9 | Somebody else's tools | 27 | 28 | 28 |
| 10 | A way to know it was right | 29 | 30 | 30 |

## Cutting to fit

| Cut | Slides | Saves | Leaves |
|---|---|---|---|
| 1 | the coda — 43, 44, 45 | 3.25 | **41.25** |
| 2 | `l2-returns` + `the-traps` — 35, 37 | 1.5 | **39.75** |
| 3 | MCP — 27, 28 | 1.75 | **38** |
| 4 | Google Cloud — 41, 42 | 3 | **35** |
| 5 | `l3-errors` + `l5-retries` — 36, 39 | 2 | **33** |

Cut evidence last. `l2-returns` and `the-traps` are the only two
lessons with no measured number behind them.

**Never cut:** 2, 3, 4, 10, 11, 14, 20, 24, 26, 31, 32, 34 — and never cut a gap slide without cutting its code and output too.

## Three things to say honestly

1. **The tools are real and ran today.** `python demo/tonight.py
   --tools-only` hits four live endpoints with no API key in about
   seven seconds. Every number on slides 11, 14, 17, 30 and 31 came out of it.
2. **There is no recorded agent transcript in this deck, deliberately.**
   The Gemini free tier hung on every attempt — including past a hard
   100-second deadline, with the SDK's own timeout failing to fire.
   Rather than fake one, the deck shows the real tool results and says
   who chose what. If you get a clean run before the talk, add it after
   slide 8.
3. **The sky is computed for 5 November 2026 over Siliguri** and
   **`cloud/` has never been executed.**

## Before you present

- [ ] Re-render the sky, cloud and moon charts for the actual date
- [ ] `python demo/tonight.py --tools-only` — expect 4/4
- [ ] Present from the web view, not a PDF — 10 slides move
- [ ] Screenshot Gemini failing the question from your phone; it beats
      slide 3
- [ ] QR code on slide 48

---


# ACT ONE — the question, and the system that answers it

## 1 · `cover` · 30 sec

**Into the Cosmos with Gemini**  
*animated panel*

The solar system on the right is live. The planets really orbit, at speeds in the right order. Let it run while people file in.

Say almost nothing. Title up, one breath, go.

"Four commands. That's the whole setup. Then we go looking at planets."

Note: animation plays in the web view and while presenting. A PDF or PowerPoint export freezes it to a still frame, which is fine.

## 2 · `the-question` · 1.5 min

**“Is it worth going outside tonight?”** — *The whole talk is one question*  
*animated panel*

This is the spine of the whole talk, so set it up properly and don't rush the list.

Say the question out loud like a person, not a demo prompt. It's the most ordinary question in the world and a language model can't answer it. Not because it's stupid. Five separate things are missing, and by the end of the talk you'll have counted ten.

Let the red lines land one at a time. Students recognise every single one of these failures; they have all asked a chatbot something it couldn't know.

Then make the promise on the bottom line and mean it, because the talk delivers it on rung 9: the same question, answered automatically, in your inbox at six in the morning.

Promising the ending here is what makes the middle feel like one thing instead of six demos. Come back to this question explicitly on rungs 3, 8 and 9.

## 3 · `cant-answer` · 1 min

**It’s not dodging the question. It can’t answer it.** — *Ask it cold*

Keep this short and don't mock the model. The point isn't that the model is stupid.

Ask the question cold and you get something fluent and useless. A paragraph about how stargazing depends on conditions. It isn't being evasive. Look at the three things on this slide and notice that none of them is knowledge.

Where you are: you never told it.

Tonight's weather: that measurement didn't exist when the model was trained. There's no amount of reading that fixes it.

And tonight's sky: Saturn is at a specific height above a specific horizon right now. Somebody has to work that out. It isn't a fact you can look up.

So the fix isn't a better model or a cleverer prompt. It's senses and memory, and the rest of this talk is me giving it both, one at a time.

If you want the demo: ask it live from your phone before the talk and screenshot the answer. It'll be politely useless and that lands better than anything I can print here.

## 4 · `ten-things` · 1 min

**Ten things it’s missing**

This is the promise, and the rest of the first half keeps it. Read the headline, then don't read all ten out. Nobody remembers a list of ten read out loud.

Instead: say there are ten, point at number one and number ten, and tell them the counter in the corner of every slide from here will tell them where they are.

Then the bottom line, which is the contract: we add them one at a time, and when the tenth is in, the question answers itself. No slide after this introduces a concept because a textbook puts it next. Each one turns up because the question won't work without it.

If you're running short this is the slide to linger on and the individual code slides to speed through. People remember the shape.

## 5 · `what-were-building` · 1.25 min

**Here’s what we’re building**  
*animated panel*

Walk the dot once, left to right. You ask in English. Gemini picks a tool and its arguments. Your code runs it. Live data comes back.

Then name the two halves, because this is the argument of the whole talk. The blue half is you, the model, and the loop between the two. About fifteen lines, and you'll see all of them in two slides. The orange box is four Python functions I wrote, and that box is where every single thing that went wrong, went wrong.

The bottom line is the instruction for how to watch the next half hour.

One sentence if you're short: the model is the part you don't control, the tools are the part you do.

## 6 · `fifteen-lines` · 1 min

**You write the loop yourself** — *What every tutorial gets wrong*

This is the hinge of the whole talk. Everything after it depends on the room accepting this one fact.

Set it up by admitting the cost: this took you most of a day, because every tutorial and every Stack Overflow answer is written against the old API.

Read the quote out loud, slowly. It's Google's own documentation, verbatim.

Then the part that matters: nobody calls your function for you. Nobody retries. Nobody decides when to stop. All of that is your code now, which means your agent is only ever as good as your tools.

If someone asks whether the old way still works: say you haven't tested it, point them at the docs, and move on. Don't guess on stage.

Verified 5 Nov 2026. Re-check before you present. This API is still changing.

## 7 · `the-declaration` · 1 min

**The model never sees your code** — *1 of 10 · Something it can call*

This slide didn't exist until late and it's the one that makes lesson one inevitable. Spend a minute.

Here is what you actually pass. Not a Python function. A dictionary. A name, a description, and the parameters.

Read the description out loud, including the second half: zero is clear, above about forty there's no point going outside. That sentence isn't for you. It's the only thing telling the model what a useful answer looks like.

Then the line on the right, and say it plainly: the model never sees your function body. It doesn't see your type hints, your tests, or what you meant. It sees three fields.

Which is why the bottom line is true. A function called process, described as "processes data", isn't badly documented. It's invisible. The model has nothing to choose it by.

Hold that thought. It comes back as lesson one with numbers attached.

## 8 · `the-loop` · 1.25 min

**Four moves, and that’s the whole agent** — *2 of 10 · A loop you write yourself*

Do NOT read this code. Read the four numbers on the right, in order, and point at the matching number in the code as you say each one.

One: you ask. The question goes in, your four tools go in with it.

Two: you look at what came back. Each thing the model did is a step. Did any of them ask for a tool?

Three. Stop here, because this is the line everyone gets wrong. YOU call the function. Gemini doesn't. It hands you a name and a dictionary of arguments and waits. Every tutorial you'll find online says otherwise; they were written against the old API.

Four: you hand the result back, with the call_id matching the step you're answering, and you loop.

That's it. That's an agent. Four moves, fifteen lines, and the next twenty minutes are about the four functions, not about this.

The bottom line is reference material. Say it fast. These are the three things that will cost them an hour on their first attempt. Then promise it's in the repo. Don't explain them.

If someone asks about MCP: it works, remote servers only, Streamable HTTP, and no hyphen in the server name.

## 9 · `cloud-code` · 30 sec

**Will it be clear?** — *3 of 10 · Knowing if it’s cloudy*

Twenty seconds. Two parameters: where, and what you want to know.

This is the first sense you give it. Until now the model has no idea whether it's cloudy anywhere, because that's not knowledge. It's a measurement that didn't exist when it was trained.

Turn the page.

## 10 · `endpoint-to-tool` · 1.25 min

**An API response isn’t a tool yet** — *3 of 10 · Knowing if it’s cloudy*

This is the slide people will photograph, and it's the one I kept forgetting to write.

Everybody can call an API. The question nobody answers is what happens between the response and the model, and the answer is that you do it.

Walk the four rows. NASA sends two days of hourly readings because that's what the endpoint does. Twelve hundred bytes, forty-eight numbers, almost none of them about tonight. Your function throws most of it away and keeps six hours and an average. The docstring tells the model what the numbers mean, including where the threshold is. And then the model sees a hundred and thirty-three bytes it can actually reason about.

Say the ratio out loud: ten times smaller.

And then the rule you can take away: never hand a model a raw API response. It will cost you tokens, it will slow you down, and it will find something in there to be confused by. Shape it first. That's your job.

Every tool in this talk is these four steps and nothing else.

## 11 · `cloud-tonight` · 1 min

**Tonight, over your heads** — *3 of 10 · Knowing if it’s cloudy*  
*recorded demo, animated*

Let it run once. Clouds drift over Bhutan and down into Bangladesh, and the hole stays where we are.

One sentence: three per cent cloud here all evening, and you can see why. The weather is going round us tonight.

Don't labour it. The point is that the agent now knows something about the actual world that no amount of training could have told it.

## 12 · `gap-eyes` · 15 sec

**It knows the sky is clear. It has no idea what’s in it.** — *Next · 4 of 10 · Knowing what’s up there*

Hold this for five seconds. They have just watched the cloud map and it felt like progress. And it was, but it answered half a question.

Knowing the sky is clear tells you nothing about whether there's anything worth looking at. Clear and empty is still a wasted evening.

So the next thing it needs is eyes.

## 13 · `sky-code` · 30 sec

**What’s up there tonight?** — *4 of 10 · Knowing what’s up there*

Thirty seconds. Point at the three parameters, not the URL.

Which body. Where you're standing. What you want to know: how high it is and how bright.

That's a tool. Hand it to Gemini and it can look up at the sky from anywhere on the planet, on any night, past or future.

Then turn the page.

## 14 · `sky-tonight` · 1.25 min

**And here’s what’s in it** — *4 of 10 · Knowing what’s up there*  
*recorded demo, animated*

Say nothing. Let it run one pass, about seven seconds, and let them watch Saturn climb.

Then one sentence: at nine o'clock tonight, Saturn is sixty-four degrees above the southern horizon, which is almost overhead, and the Moon doesn't rise until three in the morning, so the whole evening is properly dark.

Point at the faint arcs: those are the paths of Jupiter and Mars, still climbing. They're a dawn show, not an evening one.

Don't explain the chart. North, east, south, west along the bottom; height up the side. People get it in two seconds.

This is computed from real ephemeris for this date. Re-run refresh-live-data.sh on the morning of the talk or the sky will be wrong.

## 15 · `gap-moon` · 15 sec

**It can point at Saturn. It doesn’t know the Moon will wash it out.** — *Next · 5 of 10 · Knowing when to go out*

Quick. Saturn is sixty-four degrees up and the sky is clear. And if there's a full Moon next to it, you'll see Saturn and almost nothing else.

Clear and dark are two different questions and people conflate them constantly.

Thing five.

## 16 · `moon-code` · 30 sec

**What will wash it out?** — *5 of 10 · Knowing when to go out*

Twenty seconds. The Moon is the thing nobody thinks of and it ruins more observing nights than cloud does.

A full Moon above the horizon washes out everything faint. You can still see planets, but nothing else.

Note the second half of the docstring, because that's the part doing the work: if it rises late, the early night is the good part. That sentence is what lets the model say "go now" instead of just reporting a time.

Same JPL endpoint as the planets, body code 301.

## 17 · `moon-tonight` · 1 min

**The Moon doesn’t turn up until three** — *5 of 10 · Knowing when to go out*  
*chart from live data*

One sentence and let them read the chart. The shape says it without you.

The white line is the Moon's height. It's below the horizon all evening and doesn't cross until three in the morning. Everything shaded is properly dark sky.

So tonight is about as good as it gets: ten hours of darkness, and when the Moon finally turns up it's a thin crescent, fifteen per cent lit, which barely matters.

The agent needs this because "is it clear" isn't the same question as "is it dark". You can have a perfectly clear sky and see almost nothing because there's a full Moon in it.

That's thing five.

## 18 · `gap-memory` · 15 sec

**Every night it asks where you live. And what you own. And what you’ve already seen.** — *Next · 6 of 10 · Remembering you*

This is the one everybody has felt. Say it as a user complaint, not an engineering problem.

It works. It's accurate. And every single night it starts by asking you three questions you've already answered. That's not an assistant. That's a form with better manners.

Thing six.

## 19 · `memory-code` · 30 sec

**It shouldn’t have to ask twice** — *6 of 10 · Remembering you*

Thirty seconds, and the docstring is the whole slide.

Notice what it says: call this FIRST. That's not documentation, it's instruction, and it's the only way the model knows the order to do things in.

Then the distinction, which is worth being precise about because people conflate them. previous_interaction_id keeps tonight's conversation together: what you said two messages ago. It does nothing for next week. Facts that outlive the conversation need somewhere to sit, and in my case that's a JSON file with three keys in it.

Turn the page and show them the difference it makes.

## 20 · `where-state-lives` · 1.25 min

**What it remembers, and for how long** — *6 of 10 · Remembering you*

Memory is the word everyone uses for three completely different things, and conflating them is why agents feel forgetful.

Left: the model itself holds nothing. Not a thing. Every call starts from zero, and people are genuinely surprised by this.

Middle: previous_interaction_id keeps tonight's conversation together, and Google holds that thread for you. It's the right tool for "what did I just say". It's the wrong tool for anything that should outlive the session.

Right: facts that survive. Where you live. What you own. What you've already seen. Nobody holds those for you. You store them, and it can be as small as you like.

Then the orange line, which is the actual failure mode: people reach for the conversation id to do the third job. It works beautifully in testing, because testing is one session. Then a real user comes back a week later and the agent has never heard of them.

Mine is a JSON file with three keys. That's the entire memory system in this talk, and it's enough.

## 21 · `memory-night-one` · 45 sec

**It knows nothing, so it asks** — *6 of 10 · Remembering you*

Both of these outputs are real. I ran the store twice with a week of imagined time between them.

First night, recall comes back empty. It has no choice but to ask: where are you, and what are you looking through. That's a perfectly good question to ask once.

Then watch the next two lines. It doesn't just use the answers, it stores them. Two calls to remember, and that's the entire mechanism.

Set up the turn: the interesting slide is the next one, because that's where the memory earns its place.

## 22 · `memory-night-two` · 45 sec

**No questions at all** — *6 of 10 · Remembering you*

A week later it opens knowing three things, and the third is the one that matters.

Location and kit stop it asking. Fine, that's convenience. But "seen: Saturn" changes what it recommends. It moves you on to something you haven't looked at.

That's the difference between a tool that answers and an assistant that knows you.

Be straight about provenance: the recall output is real, the sentence in the green box is how the system is built to answer. The free tier wouldn't complete a live run while I was making this, so take the wording as mine and the data as real.

Land the bottom line hard. Everyone in this room has filled in the same form twice and hated it.

## 23 · `gap-chain` · 15 sec

**Four tools. Four answers. Nobody decided anything.** — *Next · 7 of 10 · Deciding what to ask next*

Careful here. This is the slide that separates what they have built from what they think they want.

So far you could have written this as four function calls in a row. Call all four, print the results. That's a script, and scripts are fine.

An agent is different because what comes back changes what it asks next. If the sky is eighty per cent cloud, there's no point looking up where Saturn is.

Thing seven.

## 24 · `the-chain` · 1.5 min

**This is where it becomes an agent** — *7 of 10 · Deciding what to ask next*

Every number in the middle column is a real tool result from tonight.

Walk down it slowly, one row at a time, and say the right-hand column out loud. That's the decision each result forces.

It recalls, so it doesn't ask. It checks the sky, finds it clear, and that's what makes continuing worthwhile. If that had come back at eighty per cent, the right move is to stop here and say so. It checks the Moon and finds it stays down until three, which means the whole evening is usable rather than just the early part. Then it finds Saturn high at nine.

Four calls, and not one of them is on a fixed list. The order falls out of what came back.

There's a fifth call. It's on the next slide, and it's the interesting one.

## 25 · `gap-silence` · 15 sec

**It tells you everything it found. Including the nothing.** — *Next · 8 of 10 · Knowing what to leave out*

Short and a little funny. Everybody has used an assistant that answers a yes-or-no question with four paragraphs.

It checked space weather and found nothing interesting. The bad version reports that. The good version says nothing at all about aurorae, and the answer is shorter and better for it.

Thing eight.

## 26 · `the-silence` · 1 min

**Leaving it out is a decision too** — *8 of 10 · Knowing what to leave out*

Give this a whole slide and a whole beat. It's the best idea in the talk and it goes past people if you bury it in a list.

The agent checks space weather. Kp is nought point six seven, which is about as quiet as it gets. There will be no aurora over north-east India tonight, and there was never going to be.

So what does it do with that? Nothing. It doesn't mention aurorae at all.

That's the bit worth sitting with. We spend all our time making agents produce more: more tools, more detail, more words. The good answer tonight is short precisely because one of the five calls told it what to leave out.

If you want the general rule: a tool returning "no" hasn't failed and hasn't wasted your money. It has bought you a shorter, better answer. Most agent output is long because nobody taught it to be quiet.

## 27 · `gap-mcp` · 15 sec

**You won’t write every tool. Somebody’s already built the one you need.** — *Next · 9 of 10 · Tools you didn’t write*

Keep this to twenty seconds and don't oversell MCP.

Everything so far is mine: four functions, about a hundred lines. In real work you won't own all of them. Someone has already built the thing you need and you would rather plug it in than rewrite it.

Thing nine.

## 28 · `mcp` · 1.5 min

**Somebody else’s tools, plugged in** — *9 of 10 · Tools you didn’t write*

Ninety seconds, and don't oversell it.

Everything so far has been tools I wrote. In real life you won't own all of them. Somebody has already built the one you need, and MCP is how you plug it in without writing it.

The shape is the slide. A name and a URL. From the loop's point of view nothing changes: the model still asks for a tool by name, you still run the round trip, you still hand the result back.

Then the three constraints, and all three came out of the SDK this afternoon rather than from a blog post.

Remote only. There's no stdio transport in the type at all, so the local servers people run on their laptops aren't what this is.

Streamable HTTP, a url and headers, and that's the entire surface.

And the one to say slowly, because half this room will be on Google Cloud: the SDK's own docstring says this type isn't supported in Vertex AI. So the enterprise path and the MCP path aren't the same path today. Worth checking before you design around it.

If someone asks for a public server to try: don't name one from memory. Test it the morning of.

## 29 · `gap-right` · 15 sec

**It sounds right. Is it?** — *Next · 10 of 10 · A way to check it was right*

Slow down. This is the last thing and it's the one people skip.

Everything they have watched produces confident, well-formatted, plausible output. So does a broken version. Nothing on the screen distinguishes them.

That's the default failure mode of every agent anybody ships: fluent and wrong, and nobody notices for a month.

Thing ten, and the reason the second half of this talk exists.

## 30 · `real-transcript` · 1 min

**Does it actually work?** — *10 of 10 · A way to check it was right*  
*terminal output*

Hold this up for a few seconds. It's the least glamorous slide in the talk and it's the one I'd keep.

Four tools, four live endpoints, no API key, about seven seconds. That's the whole instrument panel.

Walk the four results and point back at the answer slide as you go: three per cent cloud, Saturn at sixty-four degrees at nine, Moon up at three, Kp nought point six seven. Every number the agent told us came from one of these lines. The model supplied the sentence, not the facts.

Then the practical note for anyone writing this down: this mode needs no key, so it runs in CI. That's the cheapest safety net you'll ever put on an agent.

## 31 · `the-answer` · 1.5 min

**Yes. Go outside.** — *The question, answered*

This is the slide the talk has been walking towards since the second minute. Don't hurry it. Read the headline, then stop. Then the four numbers, slowly, one each: three per cent cloud all evening. Saturn sixty-four degrees up at nine. Geomagnetically quiet, so don't bother looking north for an aurora. And the Moon stays out of the way until three in the morning. Then the line that closes the loop with the opening: not one of those four numbers was in the model. It didn't know where I live, what the weather is, or where Saturn is tonight. Four small functions gave it senses, and the loop let it use them in the order it chose. If you want one beat of theatre: ask whether anyone is going to go and look. Somebody always says yes.


# ACT TWO — everything you just watched broke

## 32 · `what-it-cost` · 30 sec

**Everything you just watched broke at least once** — *Now the honest part*

This is the hinge of the talk. The question is answered, the room has had its payoff, and if you just carry on they'll feel the talk should have stopped.

So stop, and tell them you're starting the second half deliberately.

Say it plainly: everything they watched in the last twenty minutes broke at least once while I was building it. Not the model. The model was fine. Not the loop. The loop is fifteen lines and it worked the first time. The four functions in the orange box.

Then the promise, and keep it: six of them, in the order they actually happened, and every one is a real bug with a real diff. No hypotheticals.

This is also your permission to speed up. The first half was a story and you took your time. The second half is craft and it should move.

## 33 · `the-six` · 1 min

**Six ways your tools break** — *All six happened to me building this talk*

This is the map. Promise it, then deliver it in order.

The line that earns their attention: every one of these six happened to me while building the demos for this talk. Not hypotheticals. Real bugs with real diffs.

Point at the split on the bottom line. One to three you fix by typing better Python. Four to six you can't fix on a laptop at all, and that's the honest reason Google Cloud is in this talk. Not because it's a Google event, but because a ten-minute tool and a five-hundred-star evaluation are infrastructure problems.

If you're running over, spend an extra ten seconds here and cut elsewhere. This is the slide that makes the rest feel like one argument instead of six tips.

## 34 · `l1-docstring` · 2 min

**Ask for Mars, get a spacecraft** — *Lesson 1*

This is where the talk stops being advice and starts being evidence. Say that.

The model does the obvious thing: it asks for Mars. And JPL comes back with four things called Mars: the barycentre, the planet, and two spacecraft that are orbiting it right now. Ask for Mars, get a spacecraft.

Now the part that matters: that's not an error. No exception, no 400, no "bad request". It's a perfectly successful HTTP response containing a menu. Your code reads it looking for an ephemeris, finds none, and returns nothing useful. The model has no idea why.

The fix is one sentence on the parameter: it takes a JPL code, not a name, and here are two examples.

Then make it theirs, slowly: nobody's model has heard of your internal service names, or that your customers table is called accounts. There's no recovery path for those. The description is the only place that knowledge can exist.

If asked whether this is just prompt engineering: no. It's on the function, so it travels with the tool into every agent that imports it.

## 35 · `l2-returns` · 45 sec

**Empty is an answer** — *Lesson 2*

Short. Forty seconds.

A night with no planets up isn't an error. It's a fact about tonight, and it's one the model can work with. It can still tell you the sky is dark and clear and point you at something else.

Raise instead, and you don't just lose that tool. You lose the whole answer, including the three tools that worked.

The rule: your tool should only raise when the caller genuinely can't continue. "I looked and there was nothing" isn't that.

## 36 · `l3-errors` · 1.25 min

**Write the error for the model** — *Lesson 3 · this one really happened*

This is a real traceback from the first time I ran the four tools. NOAA changed shape on me. I expected rows with a header, it sends a list of dictionaries.

Read it out and then ask: what is a language model supposed to do with that? It's a sentence about Python internals. It can't fix my parser and it can't tell the user anything useful.

The fix isn't to hide the failure. It's to say what failed, in words aimed at the reader, who is now a model, and whether the rest of the job can go on.

Then it answers with three tools instead of four and tells the user the aurora check was unavailable. That's a good night's work, not a crash.

The sentence to leave them with: once you hand tools to a model, your error strings stopped being for you.

## 37 · `the-traps` · 45 sec

**Three things that’ll cost you an hour** — *On your first attempt*

Reference slide. Forty seconds, don't explain them deeply. Promise the repo and move on.

The call_id one: each thing the model did is a step with an id, and when you hand back a result you've to say which step you're answering. Get it wrong and your result goes nowhere; the model waits, then gives up.

The result one catches everyone, including me. It's not a string. It's a list of content blocks, and if you pass a string it's simply ignored.

And the third is a documentation problem rather than a design one. Structured output is response_format. A great deal of what is online says response_schema, because that's what the older API used, and it won't work.

The bottom line is the reason this slide exists at all: none of these raise anything useful. They fail silently, which is the worst way for anything to fail, and you'll lose an evening to each one.

## 38 · `l4-latency` · 1.25 min

**A slow tool can’t sit inside the loop** — *Lesson 4 · measured*

These are measured, on my laptop, on a good connection. Say that.

The interesting one is planets_tonight. It looks like one tool and it's really four HTTP calls in a row, because I wrote a loop over the planets. Nobody reviews that and thinks "this is the slow one". You find out by timing it.

Now put it in context. The model may call tools across several rounds. Seven seconds of tool time, two or three rounds deep, is twenty seconds of someone staring at nothing.

Two fixes and they're both boring. Fan the four requests out concurrently. Or notice that the sky tonight is the same for everyone in this city, compute it once at sunset, and serve it from a row.

The second one is the one that leads into the cloud section.

## 39 · `l5-retries` · 45 sec

**Retry inside the tool** — *Lesson 5*

Three lines, and they're the difference between a demo that works and one that works on stage.

Every one of these endpoints is free and public and occasionally drops a request that succeeds a second later. If that failure reaches the model, it does the polite human thing. It tells the user it couldn't check, and gives up. It won't retry, because nothing told it to.

Then the honest confession, and it's a good one: the model did this to me too. The free tier of gemini-3.8-flash returned 503 over and over while I was building this, and then stopped answering altogether, which is why some of tonight is recorded rather than live.

So the retry belongs one layer down, in the tool, where it's three lines and nobody has to think about it.

## 40 · `l6-scoring` · 1.25 min

**I thought all four tools worked** — *Lesson 6 · the one that matters*

This is the lesson I'd protect over every other one, and today it caught me.

I wrote four tools. I was certain all four worked. I ran the check and three did. NOAA had changed the shape of its response and my parser was wrong.

Now notice what would have happened without the check. Nothing visible. No crash, no red text. The agent would have answered the question perfectly well using three tools and quietly stopped ever mentioning the aurora. I'd have demoed that on this stage and never known.

That's how agents fail. Not loudly. They just get a bit less useful, and nobody notices for a month.

The habit: a command that exercises every tool, with no model and no key, that you run after every change. Mine takes four seconds.

Then the bigger version, if you've time: the real score is whether the answer was right, and for that you need ground truth you held back. Everyone in this room has some: closed tickets, last quarter's forecasts. You already know how all of it turned out.

## 41 · `architecture` · 1.75 min

**Move the slow part off the loop** — *Lesson 4, as a picture*  
*animated panel*

This is lesson four turned into shape. Walk the two lanes, don't talk about syntax.

Top lane runs once, at sunset, and nobody is waiting for it. A Cloud Run Job works through every city you care about. Seven seconds each, hundreds at a time, because none of them depends on the others. It writes one row per city per night into BigQuery.

Bottom lane is what happens when somebody actually asks. The agent reads one row. Forty milliseconds instead of seven seconds.

Then the line at the bottom, which is the whole idea and isn't really about the cloud at all: the sky over this city tonight is the same for everybody in this city tonight. There's no reason to compute it per question.

Same container image, two entry points. That's the trick, and it's the one that makes a slow tool survive contact with real users.

Say honestly that this is architecture. The gcloud commands are in the repo, and I've never run them, because there's no billing account behind this talk.

## 42 · `scoreboard-sql` · 1.25 min

**Was it right?** — *Lesson 6, as one query*

Don't read the SQL. Say what it does: of all the nights it told somebody to go outside, on how many was the sky actually clear?

Then the thing that makes this domain lucky, and point at it: the ground truth turns up on its own. Tomorrow morning, open-meteo publishes what the cloud cover actually was last night. You don't have to label anything. You just have to write down what you said, and check.

That's the whole habit. One row per night: what it advised, and what happened. One query. Run it weekly.

And the consequence is human, not technical. Send somebody out into cloud twice and they stop opening your app. Nothing in your logs tells you that happened.

Finish on the bottom line and make it theirs, because it's the most transferable sentence in the talk. Everybody here already has ground truth and hasn't noticed. Closed tickets. Merged pull requests. Last quarter's forecasts against what actually happened. You already know how all of it turned out. Hold some back and score against it.


# CODA — point the same four moves somewhere else

## 43 · `worlds-live` · 1 min

**Now watch those eight lines run** — *The output · recorded from the live map*  
*recorded demo, animated*

They have just read eight lines of code. This is those eight lines running. Say that first, then stop talking and let the descent play. It's about six seconds and it loops.

Start wide: that whole bruise-shaped feature is Olympus Mons and the aureole of material that has slumped off it over billions of years. Two thousand three hundred kilometres across the frame.

As it closes in, name the scale once: three times the height of Everest, and the base would cover France.

Then the ending, and let it sit there: those nested pits are the summit caldera. Not an impact crater. That's where the magma chamber emptied and the roof collapsed, over and over.

The line that matters for a talk about agents is the one at the bottom. Nobody at NASA built this experience. They published map tiles in the same z/y/x format the whole web already uses, and went home. Everything you've watched tonight is someone else's archive, plus a little code.

Say "recorded" once, honestly. It's recorded because the embedded panels in these slides can't reach the network at all, which is worth knowing if anyone asks why you aren't doing it live.

## 44 · `earth-live` · 1 min

**One day of Earth, from a million miles away** — *The output · 13 real photographs · 1 November 2026*  
*recorded demo, animated*

Put it up and say nothing for one full loop. Six seconds. People don't expect this one.

Then: that's not a render, and it's not a composite of archive imagery. Those are thirteen photographs taken on the first of November, in the order they were taken, by a spacecraft sitting a million miles away. The planet is turning because it turned.

Point out what is passing: Australia and the Pacific at the start, then Asia and Africa, then the Atlantic and the Americas. Three hundred and twenty-four degrees. Nearly a whole day.

Then the honest note, because somebody will ask: the fade between frames is mine, to make the rotation read. The thirteen pictures are untouched.

Land on the bottom line and make it theirs: six lines of code, and a spacecraft somebody else paid for. Every one of you can have today's version of this picture before you leave the room.

If they ask whether the agent can use it: it already does. It's latest_earth_image, and it partly answers the question from slide two. Where the clouds are is most of whether it's worth going outside.

## 45 · `worlds-found` · 1.25 min

**Watch the sky fill up** — *One query · no key · every world we know*  
*animated panel*

Let it run a full cycle before you talk. It takes about twenty seconds and it's the biggest number in the talk.

What they're watching: every confirmed planet around another star, placed by its size and the length of its year, appearing in the year we found it.

Call the beats as they pass. 1992: the first two, and they weren't around a sun, they were around a pulsar, the corpse of a star. 1995: the first around a normal star. Then the blue burst from 2009: that's Kepler, and in 2014 and 2016 alone more than three thousand arrive.

Then stop on the final frame and point at Earth, sitting almost on its own in the bottom right. That emptiness isn't a discovery. It's a blind spot. A 58-parts-per-million dip, exactly what they watched fail to show up on the previous slide.

Now the Gemini point, which is why this slide is in a talk about agents and not an astronomy lecture: the panel on the right is the entire tool. One SELECT, one GET, no key. Hand that to a model as a single function and it can answer almost any question anyone asks about planets, but it will also inherit this chart's bias without ever knowing it's there. That's your job, not the model's.


# CLOSE — the six rules, and what to build on Monday

## 46 · `recap-six` · 1 min

**Six rules for agent tools** — *Take a photo of this one*  
*animated panel*

Stand still. Let them photograph it. Read only the amber column. The grey notes are for the photo, not your voice. Then the closing argument, and it's the reason to give this talk at all: not one of those six rules mentions Gemini. They're true of any model you plug in, this year or next. The model is the part that will change and the part you don't control. Your tools are the part you own. Finish with the inversion of where we started: "I showed you the agent in eight lines at the beginning and told you that was the easy part. These six are the hard part, and they're the part that's still yours." If somebody asks which one matters most: one and six. A tool nobody calls, and a system nobody scored.

## 47 · `tonight` · 1 min

**Go and build one of these**

Stand still. Let them photograph this.

Read the three headlines only. The grey lines are for the photo.

The third card is the whole talk. Say it properly: not one thing you saw tonight needed astronomy. It needed a tool and a sentence. Swap NASA for their university timetable, their own repository, a spreadsheet their boss cares about. The six rules don't change.

If one student does the third card this week, this talk worked.

Good closing beat before the last slide: "You now know something that didn't exist as a skill two years ago, and the whole loop is four moves."

## 48 · `close` · 45 sec

**Go and point it at something**

Replace the white box with a real QR code to the repo. Nobody types a URL off a slide.

Say it simply. Everything is in there: the code, these slides, and the failures. And a facts file with the query behind every number, so they can check you weren't making it up.

Then thank them and stop talking. Leave this slide up for the whole Q&A. It answers "where do I start" without you repeating yourself ten times at the coffee break.

The two commands are deliberately the API, not the CLI. An earlier version of this talk used Gemini CLI; if anyone asks about it, the CLI is a different product and the local-MCP trap from the loop slide is the practical difference.

Likely questions and short answers are at the end of EASY-SCRIPT.md.
