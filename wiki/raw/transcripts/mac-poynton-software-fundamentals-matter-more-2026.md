# Software Fundamentals Matter More Than Ever — Mac Poynton

**Source:** https://youtu.be/v4F1gFy-hqg
**Speaker:** Mac Poynton (aihero.dev)
**Event:** Conference talk (unknown conference, 2026)
**Retrieved:** 2026-04-26

---

## Full Transcript

Hello everyone. Having a good conference so far? Are you having a good conference so far? Good. Wonderful.

I have a message for you that I hope will be a comforting message for folks who believe that their skill set is no longer worth anything in this new age, which is I believe that **software fundamentals matter now more than they actually ever have.**

And I'm a teacher and I've been recently teaching a course called Claude Code for real engineers. Nice and provocative. And in the process of kind of working on this course, I had to come up with a curriculum about AI coding, which is a bit of a nightmare because things are changing all the time, right? AI is a whole new paradigm. We need to chuck out all of the old rules surely so that we can bring in the new stuff.

### Failure Mode 1: Specs-to-Code Doesn't Work

And there's a kind of movement that has come up around this, which is the **specs to code movement**. And the specs to code movement says that okay you can write a specification about how an application is supposed to work then you can use AI to turn it into code. If there's a problem with the application you then go back to the spec. You don't really look at the code. You just change the spec. You run the compiler again and you end up with more code.

And what I noticed was I would run it and I would try not to look at the code but I would look at the code and I realized I would get code out first of all and then I would run it I would get worse code and then I did it again I got even worse code and I got it again I kept running the compiler kept running the compiler and I would just end up with garbage.

I don't think this works. The idea that we can just ignore the code and just have the code let it manage itself is just sort of vibe coding by another name.

### The Design Concept (Brooks)

And I didn't believe that back then I thought okay how do I fix the compiler how do I make it so that it doesn't produce bad code each time or worse code and so I thought okay I need to explain to the LLM in English what a good codebase looks like let me dig out one of my old favorite books which is **A Philosophy of Software Design by John Ousterhout** — go on Amazon get it. And he has a definition for what bad code looks like. He calls it complex code. **Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system.** So a bad codebase is a codebase that's hard to change. If you can't change a codebase without causing bugs, then it's a bad codebase. Good code bases are easy to change.

So I thought, oh, that was good. Let's try another book. Let's try **The Pragmatic Programmer**. Go on Amazon, get it. They have a whole chapter on something called **software entropy**. And this is exactly what I was seeing. Entropy is the idea that things tend towards disaster and floating away from each other and collapse. And this is exactly how most software systems behave too is that every time you make a change to a codebase, if you're only thinking about that change, not thinking about the design of the whole system, your codebase is going to get worse and worse and worse. And that's what I was seeing. Everything inside the specs to code idea that you just run the compiler again and again was making worse code.

Now there's an idea that sort of drives the specs to code movement which is that **code is cheap**. Raise your hand if you've heard that phrase before that code is cheap.

Well, I don't think this is right. I think code is not cheap. In fact, **bad code is the most expensive it's ever been.** Because if you have a codebase that's hard to change, you're not able to take all of the bounty that AI can offer because AI in a good codebase actually does really, really well. And this means good code bases matter more than ever, which means **software fundamentals matter more than ever.** That's the thesis of this talk.

### Failure Mode 1 Fix: "Grill Me" Skill

So the first failure mode is that the AI didn't do what I wanted. I thought I had a good idea in my head and the AI just did something totally different. This is what they say in The Pragmatic Programmer: **no one knows exactly what they want.** You and the AI, there is a communication barrier there. When you're talking to the AI, that's kind of like the AI doing its requirements gathering.

And I realized that there was another book, **Frederick P. Brooks, The Design of Design**, and it talks about this idea called the **design concept** — that when you have more than one person designing something together, you have this idea sort of floating between you, this ephemeral idea of the thing that you're building. And that thing that you're building or the idea of it is called the design concept. It's not an asset. It's not something you can put in a markdown file. It is the invisible sort of theory of what you're building.

So me and the AI don't share a design concept. So I came up with a skill. The skill is very very simple. It's called **"grill me"** and it looks like this:

> Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree resolving dependencies between decisions one by one.

This skill is in a repo containing this skill has like 13,000 stars or something. Went viral. People love this thing. These couple of lines means the AI asks you like 40 questions, 60 questions. I've had it ask people a hundred questions before it's satisfied they've reached a shared understanding. And it means it turns the AI into a kind of adversary where it's just continually pinging you ideas and trying to reach a shared understanding.

Don't at me on this, but I personally believe this is better than the default plan mode in Claude Code. Plan mode is extremely eager to create an asset. It really wants to just create a plan and start working. Whereas I think it's a lot nicer to reach a shared design concept first.

### Failure Mode 2: Verbose AI / Shared Language (DDD)

Failure mode number two is that the AI is just way too verbose. You're almost talking across purposes with the AI. If you've ever been a developer for a long time and you've worked with domain experts, you need to establish some kind of shared language, right? Otherwise they're going to be using terms you don't understand.

So I went back to **Domain-Driven Design (DDD)**. DDD has a concept of a **ubiquitous language**. With ubiquitous language, conversations among developers and expressions of the code and conversations with domain experts are all derived from the same domain model. It's essentially a markdown file full of a list of terms that you and the AI have in common.

I made a skill — the ubiquitous language skill. Basically just scans your codebase, looks for terminology, and then creates a markdown file. What I noticed by reading the thinking traces of the AI, it not only improves the planning, but it allows the AI to think in a less verbose way and actually means that the implementation is more aligned with what you actually planned.

### Failure Mode 3: Feedback Loops & TDD

Let's imagine that you've aligned with the AI. The AI has built the right thing, but it doesn't work. There's an obvious thing we can do: we can use **feedback loops** — static types, browser access for the LLM, automated tests.

The LLM doesn't use them very well. It does way too much at once. It will produce huge amounts of code and then think, "Oh, I should probably type check that." This in The Pragmatic Programmer they describe as **outrunning your headlights** — essentially driving too fast because **the rate of feedback is your speed limit.**

So skill number three is **TDD**. Test-driven development forces the LLM to take small steps. You create a test first. You make that test pass. Then you refactor. Good codebases are easy codebases to test.

### Failure Mode 4: Shallow vs Deep Modules

What does a testable codebase look like? Again we go to **John Ousterhout**. He talks about having **deep modules** in your codebase. Not shallow modules — not lots of modules that expose lots of functions. They should be relatively few large deep modules with simple interfaces.

**Deep modules:** Lots of functionality hidden behind a simple interface, hiding the complexity. You can look inside if you want to, but you don't need to.

**Shallow modules:** Not much functionality, complex interface. A codebase full of shallow modules is really hard for the AI to explore. AI doesn't understand what your code is doing.

### Failure Mode 5: Cognitive Overload

Your brain can't keep up. You as well as the AI need to keep all of that information in your head. Deep modules mean you can treat them as gray boxes — design the interface, delegate the implementation.

### The Takeaway

Code is not cheap. If we think about AI as a really great tactical programmer, a sergeant on the ground making the code changes, you need someone above that. Someone thinking on the strategic level. And that's you. And that requires software fundamental skills that we've been using for 20 years, for longer.

**Invest in the design of the system every day** (Kent Beck).
