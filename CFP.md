# CFP submission — Into the Cosmos with Gemini

## Title

**Into the Cosmos with Gemini: every agent concept, taught by one question**

*Alternatives if there is a character limit:*
- Into the Cosmos with Gemini
- One Question, Every Agent Concept
- Ask for Mars, Get a Spacecraft

## The angle, in one paragraph

Most agent talks are a tour: here is function calling, here is memory, here is
MCP, here is evaluation — each with its own toy demo, none of them connected.
Attendees leave with a list of features and no idea which ones they need.

**This talk teaches the same concepts, but every one of them arrives because a
single question forces it.** We ask something a human answers in ten seconds
and a model cannot answer at all, and then each concept shows up at the exact
moment the question breaks without it. Nothing is introduced because it was
next on a slide.

## Elevator version (50 words)

I asked Gemini if it was worth going outside tonight. It couldn't answer — not
won't, *cannot*. Watch every core agent concept appear in the order that one
question demands it: tools, memory, chaining, restraint, evaluation. Then watch
all six of the ways my tools broke, with the diffs.

## Abstract (≈130 words — for the programme)

"Is it worth going outside tonight?"

A model cannot answer that. It doesn't know where you are, what the sky is
doing, or where Saturn is right now. Those aren't facts it failed to learn —
they are measurements that did not exist when it was trained.

So we build the thing that can, and every agent concept you have read about
turns up on its own schedule: tool calling when the model needs senses, tool
*design* when it asks JPL for "Mars" and gets a spacecraft, memory when it asks
where you live for the second time, chaining when one answer decides the next
question, and restraint when the right move is to say nothing at all.

By the end it answers, from live data. Then: everything you watched broke at
least once, and here are the six fixes.

## The concepts, and where each one arrives

This is the spine of the talk. Each concept is **demonstrated with a real run
or a measurement**, never asserted.

| Agent concept | Arrives when | Shown by |
|---|---|---|
| The tool-calling loop | The model admits it cannot know | 15 lines — and Gemini never calls your function, you do |
| Declarations as the real interface | Before the first tool is written | The dict is all the model ever sees; your code is invisible |
| Tool design and naming | It asks JPL for "Mars" | A menu comes back with **two spacecraft** on it — and it is not an error |
| Return values vs exceptions | A night with nothing in the sky | Raising kills three answers that worked |
| Errors as prompts | A real traceback from my own bug | `'dict' object has no attribute 'index'` means nothing to a model |
| Session state vs durable memory | It asks where you live, twice | Two real runs, a week apart |
| Multi-step chaining | One answer changes the next question | Five calls, each chosen by the last |
| **Restraint** | Geomagnetic activity comes back quiet | It decides to say *nothing* — knowing what to omit is a decision |
| Tool composition (MCP) | You will not own every tool | Verified from the SDK, including a constraint that bites on Vertex AI |
| Latency and architecture | One tool takes 4.31 of 6.99 seconds | Measured, then moved off the loop |
| Evaluation | My tool check says **3 of 4** | I would have sworn it was four. Agents degrade silently |

## What attendees leave with

1. **A mental model of the loop** that survives the next API change — create,
   inspect, execute yourself, hand back
2. **Six rules for writing tools an agent can actually use**, each one a bug
   with a diff, not a best practice
3. **The habit that separates a demo from a system** — scoring against ground
   truth they already have: closed tickets, merged PRs, last quarter's
   forecasts
4. **A repository they can run that evening** — four keyless tools against
   live NASA, NOAA and JPL data. No account, no billing, no sign-up

## Why the cosmos

Because the data is free, public, keyless and genuinely beautiful — and
because nothing in the talk requires knowing any astronomy. The sky is a domain
where every claim can be checked live in front of the room. Swap it for your
ticket system and all eleven concepts hold unchanged, which is the closing
argument.

## Who it's for

Developers who have called an LLM API and now want to build something that
*does* things. Comfortable reading Python. No astronomy, no ML background, no
prior agent experience assumed.

## Format

40 minutes, cuts cleanly to 30 or 20. **Entirely self-contained** — every demo
is recorded from a real run, so nothing depends on conference wifi or on an API
staying up.

## Why me

I built this system while preparing the talk and kept every bug. The six
lessons are not collected wisdom; they are what went wrong, in order, with the
measurements. Where something could not be demonstrated honestly, it is not in
the talk — including one demo I cut rather than fake.
