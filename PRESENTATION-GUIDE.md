# Into the Cosmos with Gemini
## Your presentation, explained

**58 slides. About 60 minutes as written.** This is the only file you need on the day.

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
5. **Slide 55, the arsenal.** Stand still and stop talking. That is the slide they photograph.

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
| **44&ndash;46** | The moment it stops being a script. | 3 min |
| **47&ndash;49** | The question from the opening, finally answered. | 4 min |
| **50&ndash;55** | The same loop, pointed at the rest of the solar system. | 5 min |
| **56&ndash;58** | What to build on the train home. | 3 min |

## If you are running long

As written this is **60 minutes**. Cut in this order; none of these breaks the story:

- **Slide 15**, But a URL is not a tool yet. &mdash; the filter is annotated on the whole-tool slide now  `-1 min`
- **Slide 18**, What the model actually gets. &mdash; the docstring is already visible in the real function  `-0.8 min`
- **Slide 30**, Clear is not the same as dark. &mdash; the point survives on the moon chart  `-0.7 min`
- **Slide 42**, night one &mdash; night seven implies it  `-0.5 min`
- **Slide 33**, I was about to write a star catalogue. &mdash; the MCP slide carries the idea alone  `-0.7 min`
- **Slide 44**, Nobody decided anything. &mdash; the decision trace makes the contrast itself  `-0.7 min`
- **Slide 27**, It knows the sky is clear. It has no idea what is in it. &mdash; a pure link slide  `-0.4 min`
- **Slide 50**, first thing &mdash; a pure link slide  `-0.4 min`
- **Slide 26**, whole agent &mdash; a victory lap, lovely, not load bearing  `-0.6 min`
- **Slide 36**, mcp output &mdash; the diagram already made the point  `-0.8 min`
- **Slide 54**, worlds &mdash; pure spectacle, not load bearing  `-0.6 min`
- **Slide 53**, earth day &mdash; same  `-0.7 min`

All twelve come to **8 minutes**, which lands the talk at about **52**.

Never cut slides 16 to 26. That stretch is the talk: the function, the wiring, and the loop that runs it.

## On the morning

```bash
./refresh-live-data.sh
```

It redraws the three charts from live data, re-renders the ISS ground track, checks all six tools and rebuilds. Then read the numbers it prints and fix any slide that names one.

Slides that quote tonight's sky: 13, 28, 31, 45, 47, 51.

---

## Every slide, in order


### A kid, a question, and the agent that finally answered it.

**1. Into the Cosmos with Gemini**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>title</sub>

> Say nothing. Let them settle. Five full seconds of the sky before you open your mouth. The room goes quiet on its own if you let it.

**2. When I was a kid, I wanted to see the sky.**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>kid</sub>

> I grew up in Delhi, the kind of kid obsessed with space. Posters, the order of the planets before my times tables.
>
> And exactly one problem. I never knew WHEN to look. Nobody tells you that. You can read every book about Saturn and still not know whether Saturn is up tonight.
>
> So I asked the only API I had. My mother.
>
> (Do not explain the joke. It pays off in act three.)

**3. She took me up to the terrace.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>terrace</sub>

> She never answered me from the sofa. She got up, climbed the stairs, stood on the terrace, looked at the actual sky, came back down and told me what she saw.
>
> And what she saw was this. Black. No moon. No stars.
>
> STOP HERE. Let the laugh land. Do not talk over it.
>
> Then: the first time, she asked me what I even meant by 'check the sky'. I told her, go up, look straight up, tell me if you can see through it. One sentence. After that she never asked again.
>
> And one family on the fourth floor had an actual telescope. Remember them, they come back later.

**4. milky way**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>milky-way</sub>

> No text on this slide on purpose. Say the line, then give it three full seconds of silence.
>
> 'This is what I thought was up there. Turns out it is. I just could not tell you which night.'
>
> This is a real photograph, taken from the space station. It comes back at the end when you point the agent at the ISS.


### The question, the real answer, and what was missing from it.

**5. Twenty something years later, I asked again.**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>asked-again</sub>

> Twenty something years later I am sitting in Siliguri, which unlike Delhi has an actual sky. And I ask the same question I asked my mother.
>
> Same question. Better API.

**6. “Should I go outside tonight to see the sky?”**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>the-question</sub>

> Read it exactly the way you would say it to a friend. Not as a prompt. No preamble, no system instruction, no role playing.
>
> That is the question. That is the whole product.

**7. what it said**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>what-it-said</sub>

> Read the first two lines out loud. Straight. No sarcasm. You are about to praise it.
>
> And honestly, that is a good answer. It knows the date. It knows I am in Siliguri. It says the weather is clear. It gives me Saturn, it gives me a set time, and look at the bottom, it even cites its sources.
>
> Two years ago this would have said 'it depends on your local conditions, check a weather app'. It does not do that any more.
>
> Beat. Then: so I went outside.
>
> THIS IS THE HINGE OF THE TALK. Praising it first is what makes the next slide land. Calling it useless would be a straw man and somebody in the third row would know.

**8. Then I checked.**  &nbsp;&nbsp;`2 min`  &nbsp;&nbsp;<sub>then-i-checked</sub>

> Clear conditions. Except it is a quarter clouded at eight in the evening and it does not clear until eleven. That is a daily summary, and the hour it is sending me outside is the worst hour of the night. It clears LATER, which is the opposite of what the answer implies.
>
> It told me when Saturn SETS. Two forty in the morning. I do not need to know when to stop. I need to know when to go, and that is half past eight.
>
> Then the one that gets me. It never mentions the Moon. Not once. The Moon is the thing that decides whether a clear sky is worth anything at all, and tonight it is sitting right there until twenty six past eight.
>
> And it is hedging on equipment, because it has no idea what I own.

**9. It read an article about tonight. It did not measure tonight.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>diagnosis</sub>

> Here is what actually happened. It searched the web and found two articles. Time and Date, and Star Walk. Good sites. Generic tables, written for everybody.
>
> It read an article about tonight. It did not measure tonight.
>
> THAT IS THE SENTENCE. Let it sit. Everything after this is me teaching it to measure.
>
> And the moment you want a number nobody has published as an article, the cloud cover at my coordinates at half past eight, there is nothing to read, so it hedges.

**10. So here is what I built.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>flash-forward</sub>

> Play it, let it run, then cut straight back.
>
> By the end of tonight this thing answers that question on its own, every evening, before I am awake.
>
> Let me show you how I got from there to here.
>
> Do not explain anything on this slide. It is a promise, not a lesson. They will see every line of it again.


### The first tool, and what turns an endpoint into one.

**11. It cannot see tonight’s weather.**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>first-problem</sub>

> Start with the one that cannot be solved by a better model.
>
> Tonight's cloud cover did not exist when this thing was trained. There is no amount of intelligence that gets you that number. Somebody has to go and measure it.

**12. Everything you need to install.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>setup</sub>

> Three lines and you are set up. pip install google-genai, and it has to be 2.x, because interactions does not exist in 1.x. That one catches people.
>
> Make a client. It reads the key out of the environment, you never pass it around. Pick a model.
>
> The key is free, from aistudio.google.com, about forty seconds, no card. If you are a JavaScript person it is npm i @google/genai and the shapes are the same.
>
> That is the whole setup. Everything else tonight is an ordinary function.

**13. cloud map**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>cloud-map</sub>

> Let it run for four seconds before you say anything.
>
> This is the sky over this building, tonight, hour by hour.
>
> Nineteen per cent average over the town. A hundred on the ridge twenty kilometres north. Point at the band parked on the hills.
>
> And notice it clears LATE. Six per cent by eleven. That is the detail the article got wrong.
>
> They see the result before they see a line of code. That is deliberate. The code is then obviously worth reading.

**14. That came from one URL.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>the-url</sub>

> That is it. That is the whole weather tool.
>
> No API key. No signup. No credit card. No rate limit worth worrying about. Those two numbers are this town.
>
> Open it on your phone right now if you like. It works.

**15. But a URL is not a tool yet.**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>byte-grid</sub>

> Here is what came back. Forty eight hours of readings, hour by hour, thirteen hundred bytes of JSON.
>
> The model does not need thirteen hundred bytes. It needs six numbers and a sentence telling it what they mean.
>
> That filtering is your job. Not the model's. This is the part nobody puts in a tutorial and it is most of the work.

**16. whole tool**  &nbsp;&nbsp;`2 min`  &nbsp;&nbsp;<sub>whole-tool</sub>

> This is the slide the talk was missing, so do not rush it.
>
> Top to bottom. The docstring, which is the only part Gemini ever reads. The request, which is the URL from the slide before. The filter, which is the thirteen hundred bytes coming down to a hundred and thirty nine, and that part is you. And the return, six numbers and nothing else.
>
> Ten lines. No decorator, no base class, no registry, no framework. It is a function with a good docstring, and you can run it on its own with no API key and no Gemini at all.
>
> Run it on its own FIRST. If it does not work here it will never work inside an agent, and you will waste an evening blaming the model.

**17. Then you describe it.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>the-note</sub>

> This is the whole tool, as far as Gemini is concerned. A name, one sentence saying when to run it, and what the answer will look like.
>
> My mother needed one sentence from me too, once, and then never asked again. One sentence is genuinely enough to define an errand.
>
> And Gemini never sees your code. Not one line. That sentence is your entire API. Write it badly and the model runs the wrong errand at the wrong moment, and you will spend an evening blaming the model.

**18. What the model actually gets.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>the-decl</sub>

> A name. A sentence. Two parameters.
>
> In the Python SDK you get this for free from the function's own docstring, which means the docstring you were already writing is the thing the model reads.
>
> That is the first tool. The sky is now visible.

**19. Two lines connect everything.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>wiring</sub>

> Here is the bit nobody explains, and it is two lines.
>
> DECLS is the list of descriptions. It is built straight from the docstrings, and it goes OUT with every call as tools=DECLS. That is how Gemini knows the tool exists at all.
>
> IMPL is a dictionary from a name to the actual function. When Gemini says 'sky_conditions', that dictionary is how you find the thing to run. That is the line in the loop you already saw.
>
> And this is the payoff: add a fifth function to TOOLS and it is live. You do not touch the loop. You do not touch anything else. Ever.
>
> THIS is what the arsenal slide at the end is promising. Ten endpoints, ten functions, one list.


### The loop, then the five step recipe for building one.

**20. So how does Gemini use it?**  &nbsp;&nbsp;`1.4 min`  &nbsp;&nbsp;<sub>three-boxes</sub>

> Three things in this picture, and only one of them can go outside.
>
> You ask the question. Gemini reads it and works out which errand it needs run. It cannot run the errand. So it sends you back the NAME of the errand and the arguments, and then it waits.
>
> Your code runs it. Hands the answer back. Gemini carries on from there, and if it needs something else, it asks again.
>
> That is the loop. That is all it is.

**21. Gemini never calls your function.**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>the-mistake</sub>

> Gemini never calls your function. Not once. Not ever.
>
> It has no network connection. It does not have your API key. It cannot run your Python. It says a name and waits.
>
> If you do not run it, nothing happens. The agent just stops, politely, mid thought.
>
> Half the tutorials online draw this arrow. Model straight to API. That arrow does not exist, and it is the single biggest reason people get stuck on day one.
>
> Only one box here has legs, and it is yours. My mother could not tell me about the sky from the sofa either.
>
> ONE SENTENCE OF CALLBACK. Do not extend it.

**22. Five things you write.**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>the-recipe</sub>

> This is the entire job. Not just for this agent. For every agent you will ever write.
>
> And look where you already are. You wrote the function. You wrote the sentence that describes it. Two of the five are done, and neither of them involved Gemini at all.
>
> Three left. Those three are identical for every agent, in every project, forever. Write them once and you are finished thinking about them.
>
> This is the slide the talk was missing. It turns the rest of the act from 'here is some code' into 'here are the three things left'.

**23. step ask**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>step-ask</sub>

> One line. The only new thing is tools=DECLS, which is the list of those sentences you wrote.
>
> Now look at what came back, because this is the moment it clicks.
>
> There is no answer. output_text is empty. You asked a question and Gemini did not answer it. It sent you a request instead. A function name, a dictionary of arguments, and an id.
>
> It worked out that it needs the cloud cover, it worked out the coordinates from 'Siliguri', and now it is waiting for you.

**24. step run**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>step-run</sub>

> Line two is the whole point of this talk. That is you calling your own function, with arguments Gemini chose. Nothing clever. You could put a print in there.
>
> Then you hand it back, and there are exactly two bits of ceremony in the entire API.
>
> reply is a four line helper that says WHICH question you are answering, by id, and what it returned. previous_interaction_id is what makes this the same conversation instead of two strangers talking.
>
> That is it. That is all the protocol there is. It is in the repo exactly like that.

**25. step loop**  &nbsp;&nbsp;`1.5 min`  &nbsp;&nbsp;<sub>step-loop</sub>

> And now the only thing left is to stop doing it by hand.
>
> Wrap it in a while. Keep going while it is still asking. Stop when it asks for nothing, because that is how you know it is finished, and that is when output_text finally has the answer in it.
>
> IMPL is a dictionary from a name to a function. Six entries. That is how it finds the right one.
>
> Read that loop again and notice there is nothing in it about astronomy. Nothing about weather, nothing about planets. Swap the six functions and this exact loop runs your agent instead of mine.

**26. whole agent**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>whole-agent</sub>

> Fifteen lines, and this never changes again for the rest of the talk.
>
> Everything after this is me writing step one and step two over and over, with different functions. Steps three, four and five are done forever.


### Two more tools, fast, now that the pattern is known.

**27. It knows the sky is clear. It has no idea what is in it.**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>whats-in-it</sub>

> Clear sky, nothing to look at, is a wasted evening.
>
> So. Second errand. And watch how fast this goes now, because you already know the shape.

**28. Saturn**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>sky-chart</sub>

> Saturn. Sixty four degrees up. Half past eight tonight.
>
> Sixty four degrees means almost overhead, which means you are looking through less atmosphere than at any other time tonight.
>
> Through binoculars it will not look like the posters. It will look like a tiny oval, and the first time you see that oval is genuinely a moment.
>
> Magnitude plus zero point five, so you will see it from a lit street.

**29. No key. No account.**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>horizons</sub>

> That is the Jet Propulsion Laboratory's own ephemeris service. The one they use to point spacecraft.
>
> Any body in the solar system, from any point on Earth, down to the arcsecond, free, no account.
>
> Same shape as before. A URL, a filter, and a sentence saying what the errand is for.

**30. Clear is not the same as dark.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>clear-not-dark</sub>

> Third errand, and this one I only learned by going outside and being disappointed.
>
> A full moon is a floodlight. The sky can be perfectly clear and you will still see almost nothing, because the Moon has drowned it.
>
> Same sky on both sides of this slide. Same cloud cover. One of them is worth leaving the house for.

**31. moon chart**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>moon-chart</sub>

> Tonight the Moon sets at twenty thirty six. Which means from twenty to nine onwards, the entire night is dark.
>
> Clear sky, Saturn overhead, no moon. Tonight is as good as it gets, and I would not have known any of that an hour ago.
>
> RE-RENDER THIS ON THE MORNING. If the Moon is near full, say so, and let the agent tell you to stay in. That is more convincing, not less.

**32. The same endpoint. One number changed.**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>one-number</sub>

> And the moon tool is the planet tool with one number changed. Three hundred and one instead of six ninety nine.
>
> Three errands, same pattern, about twenty minutes of actual work.
>
> Move fast here. They have the idea. Do not linger.


### Tools you did not write, and why you reach for them.

**33. I was about to write a star catalogue.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>the-wall</sub>

> Next I wanted deep sky objects. Nebulae, clusters, the things actually worth binoculars.
>
> And I sat down to write a star catalogue tool. And then I stopped, because this list does not end. I would be writing tools for a year.

**34. I did not build a telescope. I knocked on their door.**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>mcp</sub>

> Remember the family on the fourth floor with the telescope.
>
> I did not build a telescope. I knocked on their door.
>
> That is what MCP is. Somebody has already built the tool, better than I would, and they have put it on a URL. You hand your agent the address, and from that moment it can send errands up there too.
>
> Your four tools and their forty arrive at the same place. The loop does not know the difference and does not care.

**35. It goes in the same list.**  &nbsp;&nbsp;`1.7 min`  &nbsp;&nbsp;<sub>mcp-code</sub>

> This is the slide that was missing, so take it slowly.
>
> DECLS is the list you already built, your four functions. OBSERVATORY is four lines of dictionary describing somebody else's server. A type, a name, a URL.
>
> And then look at the last line, because that is the whole point. You add them together. Your four and their forty go into the same tools argument, in the same create call you have been looking at since the loop. Nothing else in the program changes. Not the loop, not the handler, not one line.
>
> One honest caveat, because I checked this in the SDK this week and not in a blog post: it is remote only. The type holds a URL, and there is nowhere to put a local process. Say that out loud. It buys you credibility for the whole talk.

**36. mcp output**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>mcp-output</sub>

> Four tools I wrote. Any number I did not.
>
> And the loop did not change. Still fifteen lines.
>
> That is the whole promise of the protocol, and it is the reason to reach for it instead of writing your own.

**37. Nine things can go in that list.**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>tools-nine</sub>

> This is the slide to photograph after the arsenal.
>
> Everything arrives at the same door. The tools argument takes nine kinds of thing, and you have now seen two of them.
>
> The first is the function you wrote yourself, which is the one worth learning because nobody else can write your filter. The second is somebody else's server on a URL.
>
> The other seven are already built and are a line each. Google search puts the live web in. Code execution lets it write python and run it. Computer use lets it drive a browser.
>
> Do not teach these. Just let the room see that the door is wider than they thought, and that they already know how to open it.


### Memory, and the bug almost everybody ships.

**38. It asked me the same three questions.**  &nbsp;&nbsp;`0.9 min`  &nbsp;&nbsp;<sub>it-keeps-asking</sub>

> Where are you. What equipment do you have. What have you already seen.
>
> Every night. Every single night.
>
> My mother asked me those questions once, in about 1998, and then never again for twenty years.
>
> That is the difference between an assistant and a form.

**39. Almost everybody ships the wrong one.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>two-forgettings</sub>

> There are two kinds of memory in an agent and almost everyone ships the wrong one.
>
> The model holds nothing. It learned nothing about you.
>
> The middle one is free and it feels like memory. It carries one conversation beautifully and it is gone by morning.
>
> The third one does not come with the SDK, because it is not the SDK's business. It is a file on your disk and you decide what goes in it.
>
> The bug everybody ships is using the second one and hoping it is the third.

**40. memory file**  &nbsp;&nbsp;`1.1 min`  &nbsp;&nbsp;<sub>memory-file</sub>

> Three keys. That is the entire memory system in this talk. A JSON file and two tools, one to read it and one to write it.
>
> And look at the docstring, because it is doing real work. Call this FIRST. That sentence is the only thing stopping it asking me where I live for the eighth time.
>
> This is step two again. The sentence is the API.

**41. Memory is not a feature. It is a parameter.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>memory-code</sub>

> Here is the whole thing in one call, and it is the same call you have been looking at all evening.
>
> Tools is what it can DO. That line has your four functions and their server in it, and it has not changed since the last act.
>
> The two new ones are the memory. system_instruction is what it knows about me, and I build that string from the JSON file on disk, every single run. That is the one that lasts. Delete the file and it forgets me.
>
> previous_interaction_id is what was said five minutes ago. Point at the amber box and say it plainly: this is the one almost everybody ships thinking it is memory. It is real, it is useful, and it is gone by morning.
>
> Three arguments became four. There is still no framework anywhere in this program.

**42. night one**  &nbsp;&nbsp;`0.5 min`  &nbsp;&nbsp;<sub>night-one</sub>

> Night one it interrogates me. Fine. Once is fine.
>
> Let them read it. Do not narrate it.

**43. night seven**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>night-seven</sub>

> Night seven, no questions.
>
> But read the second half, because this is the bit that got me.
>
> It did not just stop asking. It stopped recommending Saturn.
>
> Nobody wrote that rule. There is no 'do not repeat yourself' code anywhere in this project. It read its own notebook, saw Saturn on the fifth, and moved on.
>
> That is the first moment this felt less like a script and more like somebody who had been paying attention.


### The moment it stops being a script.

**44. Nobody decided anything.**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>just-a-script</sub>

> I want to be honest about what I had at this point, because it is not an agent yet.
>
> Four errands that got run in order. I could have written that as four function calls in a row and skipped Gemini entirely. That is a script with a very expensive wrapper.
>
> Here is the night it stopped being that.

**45. Each answer decided the next question.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>watch-it-choose</sub>

> Read the right hand column, because that column is the whole talk.
>
> It checked who I was, so it did not ask. It saw nineteen per cent, so it was worth carrying on. If that had said ninety, it would have stopped there and told me to stay in, and it would never have called the other two tools at all.
>
> It found the Moon setting early, so the night was dark. And only then did it go looking for something to point me at.
>
> Each answer decided the next question. Nobody wrote that order down.

**46. left out**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>left-out</sub>

> One more. It checked the aurora forecast, got well under one out of nine, and then never mentioned it.
>
> It did not tell me there was no aurora. It did not pad the answer.
>
> A tool that comes back empty is not a wasted call. It is the reason the answer is short.


### The question from the opening, finally answered.

**47. the answer**  &nbsp;&nbsp;`1.4 min`  &nbsp;&nbsp;<sub>the-answer</sub>

> Same question as the start. Same evening. Same model underneath.
>
> On the left, go outside, it is clear. On the right: yes, but wait until twenty to nine. The Moon sets at 20:36 and the cloud is still at a quarter until then. Saturn is sixty four degrees up at half past eight and it is the best thing in the sky tonight.
>
> That is the difference four tools make. Not a smarter model. The same model, with legs.
>
> RE-RENDER THESE FOUR NUMBERS ON THE MORNING.

**48. Is it actually right, though?**  &nbsp;&nbsp;`0.8 min`  &nbsp;&nbsp;<sub>is-it-right</sub>

> One command. Seven seconds. Runs in CI, needs no key, no mocks, and no Gemini call at all, because it is not testing the model. It is testing the legs.
>
> Cheapest safety net you will ever add to an agent.

**49. Agents fail quietly.**  &nbsp;&nbsp;`1.3 min`  &nbsp;&nbsp;<sub>fails-quietly</sub>

> This caught me yesterday morning.
>
> My moon tool was reading a Moon that was SETTING as a Moon that was RISING. Perfectly formed JSON. Plausible number. Completely wrong, and it turned a perfect night into 'don't bother'.
>
> Nothing crashed. Nothing logged. I would have presented that number to you tonight.
>
> Agents fail quietly. They do not throw. They hand you a well formatted lie, and your model repeats it with total confidence, because why would it doubt you.
>
> Test the legs, not the brain.


### The same loop, pointed at the rest of the solar system.

**50. first thing**  &nbsp;&nbsp;`0.4 min`  &nbsp;&nbsp;<sub>first-thing</sub>

> Everything after this uses the same fifteen lines. I am only adding errands.
>
> This stretch is almost no talking. Let the pictures run.

**51. iss**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>iss</sub>

> Real orbit, fetched this morning, propagated with a physics library that is one pip install.
>
> It passes over this building at one in the morning, sixty eight degrees up. Go and look. It is bright enough to spot from a balcony with no equipment at all. It will look like a plane that does not blink.
>
> CHECK THIS RE-RENDERED. It names a time for tonight.

**52. olympus**  &nbsp;&nbsp;`0.9 min`  &nbsp;&nbsp;<sub>olympus</sub>

> Largest volcano in the solar system. Three Everests tall. As wide as France.
>
> Nobody at NASA built this flyover for you. They published the tiles and went home. The flyover is forty lines of Python.

**53. earth day**  &nbsp;&nbsp;`0.7 min`  &nbsp;&nbsp;<sub>earth-day</sub>

> Thirteen actual photographs from a satellite parked between us and the Sun. Not a render. Not a composite. That is today.
>
> Say the last line and stop. Let it spin.

**54. worlds**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>worlds</sub>

> Every confirmed planet outside this solar system. Six thousand four hundred and fifty one of them, and the number went up while I was building this talk.
>
> One SQL query. No key.

**55. Ten ways into space. No key. No signup.**  &nbsp;&nbsp;`1.6 min`  &nbsp;&nbsp;<sub>the-arsenal</sub>

> This is the slide they will photograph, so stand still and stop talking for a moment. Let them get it.
>
> Then say the only thing that matters: every single demo tonight came off this slide. No key, no signup, no credit card.
>
> Point at the four headings. Look up is the sky from where you are standing. Look down is this planet. Look out is everything further away. And the red one is the Sun trying to ruin it.
>
> Then the bottom line, which is the whole talk in nine words: each one is a function and a docstring away from being a tool. You already know how to write a function. You learned the docstring part tonight.


### What to build on the train home.

**56. Tonight. Ten minutes.**  &nbsp;&nbsp;`1 min`  &nbsp;&nbsp;<sub>go-build</sub>

> Install it. Get a free key, forty seconds, no card.
>
> Then write one tool. Will I see an aurora this week. One endpoint, NOAA's Kp index. The whole thing is a function and a docstring, and you now know exactly what sentence to put in the docstring.
>
> Ten minutes. Tonight. Not this weekend, tonight.

**57. Nothing tonight was really about astronomy.**  &nbsp;&nbsp;`1.2 min`  &nbsp;&nbsp;<sub>the-point</sub>

> Nothing tonight was really about astronomy. I used space because it is beautiful and because NASA gives it away.
>
> But the shape is always the same. The model is always fluent and always blind, and it is always waiting for somebody to go and look. That part never changes, whatever you point it at.
>
> Point it at your repository. Your tickets. Your database. Your company's own ugly internal API that nobody has documented since 2019.
>
> The loop does not change.

**58. repo**  &nbsp;&nbsp;`0.6 min`  &nbsp;&nbsp;<sub>repo</sub>

> Everything is in here. The tools, the loop, the memory file, the renderers for every visual you saw, and the tool check.
>
> Go and point it at something. Thank you.
>
> Then stop talking and take questions.

