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

> Say nothing for five seconds. Let them look at it. The room goes quiet on its own if you do not fill the gap.

**2. When I was a kid, I wanted to see the sky.**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>kid</sub>

> Delhi kid, obsessed with space, knew the planets before my times tables. The problem was never wanting to look. It was never knowing when. Then the line about my mother. Do not explain the joke, it pays off in act three.

**3. She took me up to the terrace.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>terrace</sub>

> She never answered from the sofa. She climbed the stairs, looked at the actual sky, came back down. What she saw was black. Stop there and let the laugh finish. Then tell them I explained it to her once, in one sentence, and she never asked again. Plant the fourth floor telescope here, you need it later.

**4. milky way**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>milky-way</sub>

> Say the line, then give it three full seconds of silence. This is what I thought was up there. Turns out it is. I just could not tell you which night. It is a real photograph, taken from the space station.


### The question, the real answer, and what was missing from it.

**5. Twenty something years later, I asked again.**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>asked-again</sub>

> Twenty odd years later, Siliguri, which unlike Delhi has an actual sky. Same question I asked my mother. Better API.

**6. “Should I go outside tonight to see the sky?”**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>the-question</sub>

> Read it the way you would say it to a friend, not like a prompt. No preamble, no system instruction, no role play. That is the question, and it is the whole product.

**7. what it said**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>what-it-said</sub>

> Read the first two lines straight, no sarcasm. You are about to praise it, so mean it. It knows the date, knows I am in Siliguri, gives me Saturn and a set time, and it even cites its sources. Two years ago this would have told me to check a weather app. Beat, then: so I went outside. Praise it first or the next slide does not land.

**8. Then I checked.**  &nbsp;&nbsp;`2 min`  &nbsp;&nbsp;<sub>then-i-checked</sub>

> Clear conditions, except it is a quarter clouded at eight and does not clear until eleven. It sent me out in the worst hour of the night. It told me when Saturn sets, twenty to three in the morning, when what I need is when to go, half past eight. And it never mentions the Moon, which is the thing that decides whether a clear sky is worth anything at all.

**9. It read an article about tonight. It did not measure tonight.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>diagnosis</sub>

> It searched, found two articles, good sites, generic tables written for everybody. Then say the line: it read an article about tonight, it did not measure tonight. Let that sit. Ask it for a number nobody has published, the cloud at my coordinates at half eight, and there is nothing to read, so it hedges.

**10. So here is what I built.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>flash-forward</sub>

> Let it run, then cut straight back. By the end of tonight this answers that question on its own, every evening, before I am awake. Explain nothing here. It is a promise, not a lesson.


### The first tool, and what turns an endpoint into one.

**11. It cannot see tonight’s weather.**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>first-problem</sub>

> Start with the problem a better model cannot fix. Tonight's cloud cover did not exist when this thing was trained. No amount of intelligence gets you that number. Somebody has to go and measure it.

**12. Everything you need to install.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>setup</sub>

> Three lines and you are set up. It has to be google-genai 2.x, because interactions does not exist in 1.x, and that catches people. The client reads the key out of the environment so you never pass it around. If anyone asks about the model, the tool loop hangs on the Gemini 3 flash models, no error and no response, so everything tonight runs on a 4. The key is free from AI Studio, about forty seconds, no card.

**13. cloud map**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>cloud-map</sub>

> Let it run for four seconds before you say anything. This is the sky over this building tonight, hour by hour. Nineteen per cent over the town, a hundred on the ridge twenty kilometres north. And it clears late, six per cent by eleven, which is exactly what the article got wrong.

**14. That came from one URL.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>the-url</sub>

> That is the whole weather tool. No key, no signup, no card. Those two numbers are this town. Tell them to open it on their phone right now if they want to.

**15. But a URL is not a tool yet.**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>byte-grid</sub>

> Forty eight hours of readings came back, thirteen hundred bytes of JSON. The model does not need that. It needs six numbers and a sentence telling it what they mean. That filtering is your job, not the model's, and it is most of the work.

**16. whole tool**  &nbsp;&nbsp;`2 min`  &nbsp;&nbsp;<sub>whole-tool</sub>

> Do not rush this one. Top to bottom: the docstring is the only part Gemini ever reads, the request is one open-meteo URL, the filter takes thirteen hundred bytes down to a hundred and thirty nine, and the return is six numbers. Ten lines, no decorator, no base class, no framework. Tell them to run it on its own first, because if it fails there it will never work inside an agent.

**17. Then you describe it.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>the-note</sub>

> This is the whole tool as far as Gemini is concerned. A name, one sentence on when to run it, and what comes back. My mother needed one sentence from me too, once. Gemini never sees your code, so that sentence is your entire API. Write it badly and it runs the wrong errand at the wrong moment.

**18. What the model actually gets.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>the-decl</sub>

> A name, a sentence, two parameters. The Python SDK builds this from the docstring you already wrote, which means the docstring is the thing the model reads. That is the first tool. The sky is now visible.

**19. Two lines connect everything.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>wiring</sub>

> This is the bit nobody explains, and it is two lines. DECLS is the descriptions, built from the docstrings, and it goes out with every call so Gemini knows the tool exists. IMPL maps a name back to the real function, which is how you find the thing to run. Add a fifth function to TOOLS and it is live. You never touch the loop.


### The loop, then the five step recipe for building one.

**20. So how does Gemini use it?**  &nbsp;&nbsp;`1.4 min`  &nbsp;&nbsp;<sub>three-boxes</sub>

> Three things in this picture and only one of them can go outside. You ask. Gemini works out which errand it needs, but it cannot run it, so it sends back the name and waits. Your code runs it and hands the answer back. That is the loop.

**21. Gemini never calls your function.**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>the-mistake</sub>

> Gemini never calls your function. It has no network, no key, and it cannot run your Python. It says a name and waits. If you do not run it, nothing happens, and the agent stops politely mid thought. Half the tutorials draw an arrow straight from the model to the API, and that arrow does not exist. One sentence of callback to my mother, then move on.

**22. Five things you write.**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>the-recipe</sub>

> This is the entire job, not just for this agent but for every one you will ever write. And look where you already are. You wrote the function and you wrote the sentence, so two of the five are done. The three that are left are identical in every project, forever.

**23. step ask**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>step-ask</sub>

> One line, and the only new thing is tools equals DECLS. Now look at what came back, because this is where it clicks. There is no answer. output_text is empty. It sent a request instead, a name and arguments and an id. It worked out the coordinates from the word Siliguri, and now it is waiting for you.

**24. step run**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>step-run</sub>

> Line two is the whole point of this talk. That is you calling your own function, with arguments Gemini chose. Then you hand it back, and there are exactly two bits of ceremony. reply says which question you are answering. previous_interaction_id makes this one conversation instead of two strangers talking.

**25. step loop**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>step-loop</sub>

> Now stop doing it by hand. Wrap it in a while, keep going while it is still asking, and stop when it asks for nothing, because that is when output_text finally has the answer. Read the loop again and notice there is nothing about astronomy in it. Swap the six functions and it runs their agent instead of mine.

**26. whole agent**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>whole-agent</sub>

> Fifteen lines, and this never changes again. Everything after this is step one and step two, over and over, with different functions.


### Two more tools, fast, now that the pattern is known.

**27. It knows the sky is clear. It has no idea what is in it.**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>whats-in-it</sub>

> A clear sky with nothing in it is a wasted evening. Second errand. Move fast here, they already know the shape.

**28. Saturn**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>sky-chart</sub>

> Saturn, sixty four degrees up at half past eight. That is almost overhead, so you are looking through less atmosphere than at any other time tonight. Through binoculars it is a tiny oval, not the posters, and the first time you see that oval is genuinely a moment.

**29. No key. No account.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>horizons</sub>

> That is JPL's own ephemeris, the one they point spacecraft with. Any body in the solar system, from any point on Earth, free and with no account. Same shape as before: a URL, a filter, and a sentence.

**30. Clear is not the same as dark.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>clear-not-dark</sub>

> Third errand, and I only learned this by going outside and being disappointed. A full moon is a floodlight. The sky can be perfectly clear and you will still see almost nothing. Same sky on both sides of this slide. One of them is worth leaving the house for.

**31. moon chart**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>moon-chart</sub>

> The Moon sets at twenty thirty six, so from twenty to nine the whole night is dark. Clear sky, Saturn overhead, no moon. As good as it gets, and I would not have known an hour ago. Re-render this on the morning, and if the Moon is near full, say so and let the agent tell you to stay in.

**32. The same endpoint. One number changed.**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>one-number</sub>

> The moon tool is the planet tool with one number changed, three hundred and one instead of six ninety nine. Three errands, the same pattern, about twenty minutes of real work. Do not linger here.


### Tools you did not write, and why you reach for them.

**33. I was about to write a star catalogue.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>the-wall</sub>

> Next I wanted deep sky objects, the things actually worth binoculars. I sat down to write a star catalogue tool, and then I stopped, because that list does not end. I would be writing tools for a year.

**34. I did not build a telescope. I knocked on their door.**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>mcp</sub>

> Remember the fourth floor. I did not build a telescope, I knocked on their door. Now say the letters, because this is the first time the room sees them. MCP, Model Context Protocol, one agreed shape for publishing a tool so an agent can use somebody else's with no glue code. If faces go blank, say USB. Then tie it back: DECLS is a menu you wrote, and an MCP server is that same menu hosted by somebody else.

**35. It goes in the same list.**  &nbsp;&nbsp;`1.7 min`  &nbsp;&nbsp;<sub>mcp-code</sub>

> Take this slowly. DECLS is the four functions you already built. OBSERVATORY is four lines describing somebody else's server, a type, a name and a URL. Now the last line, which is the whole point. You add them together, same tools argument, same create call, and nothing else in the program changes. Then say the caveat out loud, because it is worth more than the slide. On a Gemini 3 model this does not error, it hangs, and you will sit there watching nothing happen. I ran it. Google says Gemini 3 support is coming. It is remote only as well, so there is nowhere to put a local process.

**36. mcp output**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>mcp-output</sub>

> Four tools I wrote, any number I did not, and the loop did not change. Still fifteen lines. That is the whole promise of the protocol, and the reason to reach for it instead of writing your own.

**37. Nine things can go in that list.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>tools-nine</sub>

> Let them look, this is the one they will photograph. Everything arrives at the same door. That tools argument takes nine kinds of thing and they have now seen two. The function you wrote is the one worth learning, because nobody else can write your filter. The other seven are built already and cost a line each. Do not teach them, just let the room see the door is wider than they thought.


### Memory, and the bug almost everybody ships.

**38. It asked me the same three questions.**  &nbsp;&nbsp;`0.9 min`  &nbsp;&nbsp;<sub>it-keeps-asking</sub>

> Where are you, what equipment do you have, what have you already seen. Every single night. My mother asked me those questions once, in about 1998, and then never again. That is the difference between an assistant and a form.

**39. Almost everybody ships the wrong one.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>two-forgettings</sub>

> Two kinds of memory, and almost everyone ships the wrong one. The model holds nothing. The middle one is free and it feels like memory, it carries one conversation beautifully, and it is gone by morning. The third one is a file on your disk, and it does not come with the SDK because it is not the SDK's business.

**40. memory file**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>memory-file</sub>

> Three keys, and that is the entire memory system. A JSON file and two tools, one to read it and one to write it. Look at the docstring, Call this FIRST, because that sentence is the only thing stopping it asking me where I live for the eighth time.

**41. Only one of them lasts.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>memory-code</sub>

> Same call as all evening. Three things on it could hold what it knows about me, and only one of them does. The memory is recall, sitting in DECLS like any other tool, reading a file off my disk. system_instruction is who it is, not what it knows, and ours actually says answer only from tool results, never from memory. previous_interaction_id carries this conversation and nothing else. Point at the amber box, because that is the one people ship thinking it is memory.

**42. night one**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>night-one</sub>

> Night one it interrogates me. Once is fine. Let them read it, do not narrate it.

**43. night seven**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>night-seven</sub>

> Night seven, no questions. Read the second half, because this is the bit that got me. It did not just stop asking, it stopped recommending Saturn. Nobody wrote that rule. It read its own notebook, saw Saturn on the fifth, and moved on.


### The moment it stops being a script.

**44. Nobody decided anything.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>just-a-script</sub>

> Be honest here, because this is not an agent yet. Four errands that got run in order. I could have written that as four calls in a row and skipped Gemini entirely, which is a script with an expensive wrapper. Here is the night it stopped being that.

**45. Each answer decided the next question.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>watch-it-choose</sub>

> Read the right hand column, because that column is the talk. It checked who I was so it did not ask. It saw nineteen per cent, so carrying on was worth it, and had that said ninety it would have stopped there and never called the other two at all. Then it found the Moon setting early, and only then went looking for something to point me at. Nobody wrote that order down.


### The question from the opening, finally answered.

**46. the answer**  &nbsp;&nbsp;`1.4 min`  &nbsp;&nbsp;<sub>the-answer</sub>

> Same question as the start, same evening, same model underneath. On the left, go outside, it is clear. On the right, wait until twenty to nine, because the Moon sets at twenty thirty six and the cloud is still at a quarter until then. That is what four tools buy you. Not a smarter model, the same model with legs. Re-render these numbers on the morning.


### What to take home.

**47. None of this was really about astronomy.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>takeaway</sub>

> Last slide, so slow down. Four things and none of them are about astronomy. The docstring is the API. It asks and you run it. The filter is the work nobody writes about. And one list takes all of it. The repo has the six tools, the loop and the memory file. Go and point it at something. Then stop talking and take questions.

