# Into the Cosmos with Gemini
## Your presentation, explained

**47 slides. About 50 minutes as written.** This is the only file you need on the day.

> Generated from the deck. Every word below is the speaker note on the slide itself, so this file cannot drift from what you present. Edit `build-slides.py`, not this.

---

## The talk in one sentence

> **A kid who could not see the sky, an AI that could not answer him, and the agent he built until it could.**

Every capability arrives because the story breaks without it, not because a list says it is next.

## The five things to get right

1. **Slide 3, the Delhi joke.** Stop talking. Let the laugh finish. It buys you the next three minutes.
2. **Slide 7, praise the answer.** Gemini did well. Say so and mean it. If you mock it, the room stops trusting you.
3. **Slide 19, DECLS and IMPL.** This is the bridge from an endpoint to a tool, and it is the thing developers came for. Do not rush it.
4. **Slide 21, the red X.** Gemini never calls your function. This is the one fact most of the room has wrong.
5. **Slide 46, the answer.** This is the question you opened with, finally answered. Do not hurry off it.

## The shape

| Slides | Act | Runs |
|---|---|---|
| **1&ndash;4** | A kid, a question, and the agent that finally answered it. | 3 min |
| **5&ndash;10** | The question, the real answer, and what was missing from it. | 6 min |
| **11&ndash;19** | The first tool, and what turns an endpoint into one. | 10 min |
| **20&ndash;26** | The loop, then the five step recipe for building one. | 9 min |
| **27&ndash;32** | Two more tools, fast, now that the pattern is known. | 5 min |
| **33&ndash;37** | Tools you did not write, and why you reach for them. | 6 min |
| **38&ndash;43** | Memory, and the bug almost everybody ships. | 7 min |
| **44&ndash;45** | The moment it stops being a script. | 2 min |
| **46&ndash;46** | The question from the opening, finally answered. | 1 min |
| **47&ndash;47** | What to take home. | 1 min |

## If you are running long

As written this is **50 minutes**. Cut in this order; none of these breaks the story:

- **Slide 15**, But a URL is not a tool yet. &mdash; the filter is annotated on the whole-tool slide now  `-1 min`
- **Slide 18**, What the model actually gets. &mdash; the docstring is already visible in the real function  `-0.8 min`
- **Slide 30**, Clear is not the same as dark. &mdash; the point survives on the moon chart  `-0.7 min`
- **Slide 42**, night one &mdash; night seven implies it  `-0.5 min`
- **Slide 33**, I was about to write a star catalogue. &mdash; the MCP slide carries the idea alone  `-0.7 min`
- **Slide 44**, Nobody decided anything. &mdash; the decision trace makes the contrast itself  `-0.7 min`
- **Slide 27**, It knows the sky is clear. It has no idea what is in it. &mdash; a pure link slide  `-0.4 min`
- **Slide 26**, whole agent &mdash; a victory lap, lovely, not load bearing  `-0.6 min`
- **Slide 36**, mcp output &mdash; the diagram already made the point  `-0.8 min`

All twelve come to **6 minutes**, which lands the talk at about **44**.

Never cut slides 16 to 26. That stretch is the talk: the function, the wiring, and the loop that runs it.

## On the morning

```bash
./refresh-live-data.sh
```

It redraws the three charts from live data, re-renders the ISS ground track, checks all six tools and rebuilds. Then read the numbers it prints and fix any slide that names one.

Slides that quote tonight's sky: 13, 28, 31, 45, 46.

---

## Every slide, in order


### A kid, a question, and the agent that finally answered it.

**1. Into the Cosmos with Gemini**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>title</sub>

> Say nothing yet.
> · five seconds of sky before you open your mouth
> → the room goes quiet on its own. let it.

**2. When I was a kid, I wanted to see the sky.**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>kid</sub>

> Delhi. Space-obsessed kid.
> · posters. knew the planets before my times tables
> · one problem, and nobody warns you about it: WHEN to look
> " you can read every book about Saturn and still not know
>   whether Saturn is up tonight
> " so I asked the only API I had. My mother.
> → do NOT explain the joke. it pays off in act three.

**3. She took me up to the terrace.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>terrace</sub>

> She never answered from the sofa.
> · got up, climbed the stairs, stood on the terrace, LOOKED
> · came back down and told me what she saw
> · what she saw: black. no moon. no stars.
> → STOP TALKING. let the laugh finish.
> · first time, she asked what "check the sky" even meant
> · I said: go up, look straight up, tell me if you can see through it
> · one sentence. she never asked again.
> · fourth floor had a real telescope — plant this, you need it later

**4. milky way**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>milky-way</sub>

> No text on this slide on purpose.
> " this is what I thought was up there. Turns out it is.
>   I just could not tell you which night.
> → then three full seconds of silence. count them.
> · real photograph, taken from the space station


### The question, the real answer, and what was missing from it.

**5. Twenty something years later, I asked again.**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>asked-again</sub>

> Twenty-odd years later. Siliguri, which unlike Delhi has a sky.
> · same question I asked my mother
> · same question. better API.

**6. “Should I go outside tonight to see the sky?”**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>the-question</sub>

> Read it like you would say it to a friend.
> · not a prompt. no preamble, no system instruction, no role play
> · that is the question. that is the whole product.

**7. what it said**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>what-it-said</sub>

> Read the first two lines out loud. Straight. No sarcasm.
> → you are about to PRAISE it. mean it.
> · knows the date. knows I am in Siliguri. says it is clear.
> · gives me Saturn, gives me a set time, even cites sources
> · two years ago: "it depends on local conditions, check an app"
> · it does not do that any more
> · beat. then: "so I went outside."
> → THIS IS THE HINGE. praise first or the next slide dies.
> → mock it and somebody in row three stops trusting you.

**8. Then I checked.**  &nbsp;&nbsp;`2 min`  &nbsp;&nbsp;<sub>then-i-checked</sub>

> Clear conditions. Except.
> · 26% at eight. does not clear till eleven.
> · daily summary. it sent me out in the WORST hour.
> · clears LATER — opposite of what the answer implies
> · it told me when Saturn SETS. 2:40am.
> · I do not need to know when to stop. I need when to GO. 8:30.
> · and the one that gets me: never mentions the Moon. not once.
> · the Moon decides whether a clear sky is worth anything
> · also hedging on gear, because it has no idea what I own

**9. It read an article about tonight. It did not measure tonight.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>diagnosis</sub>

> What actually happened:
> · it searched, found two articles. Time and Date, Star Walk.
> · good sites. generic tables. written for everybody.
> " it read an article about tonight. It did not measure tonight.
> → THAT IS THE SENTENCE. let it sit. do not rush on.
> · want a number nobody published — cloud at my coords at 8:30 —
>   there is nothing to read, so it hedges

**10. So here is what I built.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>flash-forward</sub>

> Play it. Let it run. Cut back.
> · by tonight this answers that question on its own, every evening,
>   before I am awake
> " let me show you how I got from there to here
> → explain NOTHING here. it is a promise, not a lesson.


### The first tool, and what turns an endpoint into one.

**11. It cannot see tonight’s weather.**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>first-problem</sub>

> Start with the one a better model cannot fix.
> · tonight's cloud did not exist when this thing was trained
> · no amount of intelligence gets you that number
> · somebody has to go and measure it

**12. Everything you need to install.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>setup</sub>

> Three lines and you are set up.
> · pip install google-genai — must be 2.x
> · interactions does not exist in 1.x. this catches people.
> · client reads the key from the environment. never pass it around.
> · pick a model.
> · key is free, aistudio.google.com, ~40 seconds, no card
> · JS people: npm i @google/genai, same shapes

**13. cloud map**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>cloud-map</sub>

> Let it run four seconds before you say anything.
> · the sky over this building, tonight, hour by hour
> · 19% average over town. 100% on the ridge 20km north.
> → point at the band parked on the hills
> · and it clears LATE. 6% by eleven.
> · that is the detail the article got wrong.
> → they see the result before a line of code. deliberate.

**14. That came from one URL.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>the-url</sub>

> That is the whole weather tool.
> · no key. no signup. no card. no rate limit worth worrying about.
> · those two numbers are this town
> " open it on your phone right now if you like. it works.

**15. But a URL is not a tool yet.**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>byte-grid</sub>

> What came back: 48 hours, hourly. 1,312 bytes of JSON.
> · the model does not need 1,312 bytes
> · it needs six numbers and a sentence saying what they mean
> · that filtering is YOUR job, not the model's
> · nobody puts this in a tutorial and it is most of the work

**16. whole tool**  &nbsp;&nbsp;`2 min`  &nbsp;&nbsp;<sub>whole-tool</sub>

> The slide the talk was missing. Do not rush it.
> · top to bottom, four things:
> · the docstring — the only part Gemini ever reads
> · the request — one open-meteo URL
> · the filter — 1,312 bytes down to 139. that part is you.
> · the return — six numbers, nothing else
> · ten lines. no decorator, no base class, no registry, no framework.
> · a function with a good docstring. that is all.
> → run it on its own FIRST, with no key and no Gemini
> → if it fails here it will never work in an agent, and you will
>   waste an evening blaming the model

**17. Then you describe it.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>the-note</sub>

> This is the whole tool, as far as Gemini is concerned.
> · a name. one sentence on when to run it. what comes back.
> · my mother needed one sentence too, once. then never again.
> · one sentence is genuinely enough to define an errand.
> · Gemini never sees your code. not one line.
> · that sentence is your entire API
> · write it badly, it runs the wrong errand at the wrong moment

**18. What the model actually gets.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>the-decl</sub>

> A name. A sentence. Two parameters.
> · Python SDK builds this from the docstring you already wrote
> · so the docstring IS the thing the model reads
> · that is the first tool. the sky is now visible.

**19. Two lines connect everything.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>wiring</sub>

> The bit nobody explains. Two lines.
> · DECLS — the descriptions, built from docstrings
> · goes OUT with every call as tools=DECLS
> · that is how Gemini knows the tool exists at all
> · IMPL — name to actual function
> · Gemini says "sky_conditions"; IMPL finds the thing to run
> · payoff: add a fifth function to TOOLS and it is live
> · you do not touch the loop. not ever.


### The loop, then the five step recipe for building one.

**20. So how does Gemini use it?**  &nbsp;&nbsp;`1.4 min`  &nbsp;&nbsp;<sub>three-boxes</sub>

> Three things here. Only one can go outside.
> · you ask
> · Gemini works out which errand it needs
> · it CANNOT run it. sends back the name + arguments. waits.
> · your code runs it. hands the answer back.
> · Gemini carries on. needs more? asks again.
> · that is the loop. that is all it is.

**21. Gemini never calls your function.**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>the-mistake</sub>

> Gemini never calls your function. Not once. Not ever.
> · no network. no API key. cannot run your Python.
> · it says a name and waits.
> · you do not run it → nothing happens. it stops, politely, mid thought.
> · half the tutorials draw this arrow: model straight to API
> · that arrow does not exist
> · biggest reason people get stuck on day one
> · only one box here has legs. it is yours.
> · my mother could not tell me about the sky from the sofa either
> → ONE sentence of callback. do not extend it.

**22. Five things you write.**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>the-recipe</sub>

> The entire job. Not just this agent. Every agent.
> · and look where you already are
> · you wrote the function. you wrote the sentence.
> · two of five done, neither involved Gemini at all
> · three left, and those three are the same in every project, forever
> · write them once, stop thinking about them

**23. step ask**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>step-ask</sub>

> One line. Only new thing is tools=DECLS.
> · now look at what came back. this is the moment it clicks.
> · there is no answer. output_text is EMPTY.
> · you asked a question and it did not answer
> · it sent a request instead: name, arguments, id
> · it worked out it needs cloud cover
> · it worked out the coordinates from the word "Siliguri"
> · now it is waiting for you

**24. step run**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>step-run</sub>

> Line two is the whole point of this talk.
> · that is YOU calling your own function
> · with arguments Gemini chose
> · nothing clever. you could put a print in there.
> · then hand it back. two bits of ceremony in the entire API:
> · reply() — which question you are answering, by id, and what it said
> · previous_interaction_id — makes it one conversation, not two strangers
> · that is all the protocol there is. it is in the repo exactly like that.

**25. step loop**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>step-loop</sub>

> Only thing left is to stop doing it by hand.
> · wrap it in a while
> · keep going while it is still asking
> · stop when it asks for nothing — that is how you know it finished
> · that is when output_text finally has the answer
> · IMPL is name to function. six entries.
> · read the loop again: nothing in it about astronomy
> · swap the six functions and it runs YOUR agent instead of mine

**26. whole agent**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>whole-agent</sub>

> Fifteen lines. This never changes again.
> · everything after this is step one and step two, over and over
> · steps three, four, five are done forever


### Two more tools, fast, now that the pattern is known.

**27. It knows the sky is clear. It has no idea what is in it.**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>whats-in-it</sub>

> Clear sky with nothing in it is a wasted evening.
> · second errand
> → move fast. they know the shape now.

**28. Saturn**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>sky-chart</sub>

> Saturn. 64 degrees up. 20:30 tonight.
> · 64 degrees is almost overhead
> · less atmosphere than any other time tonight
> · through binoculars it is a tiny oval, not the posters
> · the first time you see that oval is genuinely a moment
> · magnitude +0.5 — visible from a lit street

**29. No key. No account.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>horizons</sub>

> JPL's own ephemeris. The one they point spacecraft with.
> · any body in the solar system, from any point on Earth
> · to the arcsecond. free. no account.
> · same shape as before: a URL, a filter, a sentence

**30. Clear is not the same as dark.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>clear-not-dark</sub>

> Third errand. Learned this by going outside and being disappointed.
> · a full moon is a floodlight
> · sky can be perfectly clear and you still see nothing
> · same sky both sides of this slide. same cloud.
> · one of them is worth leaving the house for.

**31. moon chart**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>moon-chart</sub>

> Moon sets 20:36. From twenty to nine, the night is dark.
> · clear sky. Saturn overhead. no moon.
> · as good as it gets, and I would not have known an hour ago
> → RE-RENDER ON THE MORNING
> → if the Moon is near full, say so, and let it tell you to stay in.
>   more convincing, not less.

**32. The same endpoint. One number changed.**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>one-number</sub>

> The moon tool is the planet tool with one number changed.
> · 301 instead of 699
> · three errands, same pattern, about twenty minutes of real work
> → do not linger. they have it.


### Tools you did not write, and why you reach for them.

**33. I was about to write a star catalogue.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>the-wall</sub>

> Next I wanted deep sky objects. Nebulae, clusters.
> · sat down to write a star catalogue tool
> · then stopped
> · this list does not end. I would be writing tools for a year.

**34. I did not build a telescope. I knocked on their door.**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>mcp</sub>

> Remember the fourth floor. The telescope.
> · I did not build a telescope. I knocked on their door.
> → NOW SAY THE LETTERS. first time the room sees them.
> · M C P. Model Context Protocol.
> · one agreed shape for publishing a tool
> · so an agent can use somebody else's with no glue code
> · analogy if faces go blank: USB. one plug shape, everything fits.
> · tie it back: DECLS is a menu you wrote
> · an MCP server is that same menu, hosted by somebody else
> · your four and their forty arrive at the same place
> · the loop cannot tell the difference and does not care

**35. It goes in the same list.**  &nbsp;&nbsp;`1.7 min`  &nbsp;&nbsp;<sub>mcp-code</sub>

> Take this slowly.
> · DECLS — the list you already built. your four.
> · OBSERVATORY — four lines describing somebody else's server.
>   a type, a name, a URL.
> · now the last line. this is the whole point.
> · you ADD them. same tools argument. same create call.
> · nothing else changes. not the loop, not the handler, not a line.
> · caveat, worth saying out loud: remote only.
> · the type holds a URL. nowhere to put a local process.
> · checked that in the SDK, not a blog post. say so if challenged.

**36. mcp output**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>mcp-output</sub>

> Four tools I wrote. Any number I did not.
> · and the loop did not change. still fifteen lines.
> · that is the whole promise of the protocol
> · and the reason to reach for it instead of writing your own

**37. Nine things can go in that list.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>tools-nine</sub>

> Let them look. This is the one they photograph.
> · everything arrives at the same door
> · tools= takes nine kinds of thing. you have seen two.
> · first: the function you wrote. worth learning — nobody else
>   can write your filter.
> · second: somebody else's server, on a URL
> · other seven are built already, a line each
> · google_search puts the live web in
> · code_execution lets it write python and run it
> · computer_use lets it drive a browser
> → do NOT teach these. just let them see the door is wider.


### Memory, and the bug almost everybody ships.

**38. It asked me the same three questions.**  &nbsp;&nbsp;`0.9 min`  &nbsp;&nbsp;<sub>it-keeps-asking</sub>

> Where are you. What gear. What have you seen.
> · every night. every single night.
> · my mother asked me those once, in 1998, then never again
> · that is the difference between an assistant and a form

**39. Almost everybody ships the wrong one.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>two-forgettings</sub>

> Two kinds of memory. Almost everyone ships the wrong one.
> · the model holds nothing. learned nothing about you.
> · the middle one is free and FEELS like memory
> · carries one conversation beautifully. gone by morning.
> · the third does not come with the SDK. not the SDK's business.
> · a file on your disk. you decide what goes in it.
> · the bug everybody ships: using the second, hoping it is the third

**40. memory file**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>memory-file</sub>

> Three keys. That is the whole memory system.
> · a JSON file and two tools. one reads, one writes.
> · look at the docstring. it is doing real work.
> · "Call this FIRST."
> · that sentence is the only thing stopping it asking where I live
>   for the eighth time
> · step two again. the sentence is the API.

**41. Memory is not a feature. It is a parameter.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>memory-code</sub>

> The whole thing in one call. Same call as all evening.
> · tools= is what it can DO. unchanged since the last act.
> · the two new ones are the memory
> · system_instruction — what it knows about me
> · built from the JSON file, every single run. this is the one that lasts.
> · delete the file and it forgets me.
> · previous_interaction_id — what was said five minutes ago
> → point at the amber box
> · this is the one almost everybody ships thinking it is memory
> · real, useful, gone by morning
> · three arguments became four. still no framework anywhere.

**42. night one**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>night-one</sub>

> Night one it interrogates me. Fine. Once is fine.
> → let them read it. do not narrate.

**43. night seven**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>night-seven</sub>

> Night seven. No questions.
> · read the second half. this is the bit that got me.
> · it did not just stop asking
> · it stopped recommending Saturn
> · nobody wrote that rule. no "do not repeat yourself" code anywhere.
> · it read its own notebook, saw Saturn on the 5th, moved on
> · first moment it felt less like a script and more like somebody
>   who had been paying attention


### The moment it stops being a script.

**44. Nobody decided anything.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>just-a-script</sub>

> Be honest: this is not an agent yet.
> · four errands run in order
> · I could have written that as four calls in a row, no Gemini
> · that is a script with a very expensive wrapper
> · here is the night it stopped being that

**45. Each answer decided the next question.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>watch-it-choose</sub>

> Read the right hand column. That column is the talk.
> · checked who I was, so it did not ask
> · saw 19%, so it was worth carrying on
> · had that said 90, it stops there, tells me to stay in,
>   and never calls the other two at all
> · found the Moon setting early, so the night was dark
> · and ONLY THEN went looking for something to point me at
> · each answer decided the next question
> · nobody wrote that order down


### The question from the opening, finally answered.

**46. the answer**  &nbsp;&nbsp;`1.4 min`  &nbsp;&nbsp;<sub>the-answer</sub>

> Same question as the start. Same evening. Same model underneath.
> · left: go outside, it is clear
> · right: yes, but wait until twenty to nine
> · Moon sets 20:36, cloud still at a quarter until then
> · Saturn 64 degrees at 20:30, best thing in the sky
> · that is what four tools buy you
> · not a smarter model. the same model, with legs.
> → RE-RENDER THESE FOUR NUMBERS ON THE MORNING


### What to take home.

**47. None of this was really about astronomy.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>takeaway</sub>

> Last slide. Slow down.
>
> · four things, none of them astronomy
> · 1 the docstring IS the API
> · 2 it asks, you run it, you answer
> · 3 the filter is the work nobody writes about
> · 4 one list: yours, theirs, the built in ones
> · repo has all six tools + the loop + the memory file
> · "go and point it at something"
> · then STOP. take questions.

