---
id: matt-pocock-ai-coding-advanced-techniques-2026
type: raw
source_type: video
title: "Advanced AI Coding Techniques"
date: 2026
event: "???"
url: https://youtu.be/-QFHIoCo-Ko
duration: ~1h36m
speaker: Matt Pocock
description: Workshop covering smart zone/dumb zone, session phases, compacting vs clear, grill-me skill, Ralph Wiggum, deep modules, Sand Castle parallelization, QA with taste, doc rot.
confidence: high
tags:
  - ai-coding
  - software-dev
  - agents
  - pocock
  - source-tier-4
---

# Raw Transcript — Matt Pocock: Advanced AI Coding Techniques (~1h36m)

> Source: YouTube, fetched via youtube-transcript-api. Confidence: high.
> This is an immutable raw source — concept pages reference this file.

## Full Timestamped Transcript

0:14 Yeah, we good.
0:17 >> Okay, folks, we're at capacity. Let's
0:20 kick off. I don't want you waiting here
0:22 for 25 more minutes before we some
0:24 arbitrary deadline. So, welcome. My name
0:28 is Matt. Uh I'm a teacher and I suppose
0:31 now I teach AI. Um
0:35 we have a link up here if you've not
0:37 already been to this which is has the
0:39 exercises for the um stuff we're going
0:41 to do today. This is going to be around
0:43 two hours. So we might just sort of kick
0:44 off two hours from now. Is that right
0:46 Mike?
0:48 >> Yeah. Perfect. Um, and the theory behind
0:52 this talk or at least the thesis under
0:53 which I've been operating for the last
0:55 kind of six months or so is that
0:59 we all think that AI is a new paradigm,
1:01 right? AI is obviously changing a lot of
1:03 things. You guys are obviously
1:04 interested in this and that's why you've
1:05 come to this talk. And
1:09 I feel that
1:12 when we talk about AI being a new
1:14 paradigm, we forget that actually
1:17 software engineering fundamentals, the
1:19 stuff that's really crucial to working
1:21 with humans, also works super well with
1:24 AI. And this is what my keynote is on
1:27 tomorrow. Really, I'm going to sort of
1:28 be fleshing that out a lot more. And in
1:30 this workshop, I'm hopefully going to be
1:32 able to direct your attention to those
1:34 things and uh hopefully show you that
1:38 I'm right, but we'll see. Um, can I get
1:41 a quick heads up first? How many of you
1:44 guys um are coding have ever coded with
1:47 AI? Raise your hand if you've ever coded
1:48 with AI. Perfect. Okay. Uh, keep your
1:51 hand raised.
1:53 Uh, let's all uh share those armpits
1:56 with the world. Um,
1:58 how many of you code every day with AI?
2:01 Cool. Okay. Uh, ra keep your hand raised
2:04 if you've ever been frustrated with AI.
2:08 Okay. Very good. You can put your hands
2:10 down. Thank you for that show of
2:12 obedience. I really appreciate that. Um,
2:14 we are also being live streamed to the
2:15 Gilgood room as well. I've not uh did we
2:18 send someone up to the Gilgood room to
2:20 just check they're okay? Don't know. But
2:22 I see you. Uh, and there is a way that
2:25 you can participate which is we have the
2:27 um a Q&A. We're going to be doing kind I
2:30 have a sort of hatred of Q&A's because
2:31 they're not very democratic. The mostly
2:33 the sort of um most talkative people get
2:36 to um get to participate and share. And
2:39 so we're going to be going through this
2:41 um QA here. So why do we have to wait
2:43 till 3:45? The room is packed. The doors
2:45 are closed. 100% agree. And so if you
2:48 want to uh ask a question, we're going
2:50 to be I would like you to pile into this
2:52 async and then we can vote on each
2:53 other's questions and hopefully get the
2:55 best question surface so the for the
2:57 entire room to enjoy.

3:00 So I want to talk about first the kind
3:02 of weird constraints that LLMs have and
3:07 those weird constraints are sort of what
3:09 we have to base a lot of our work
3:11 around. Now,
3:14 there's a guy called Dex Hy who runs a
3:16 company called Human Layer, and he came
3:18 up with this idea, which is that
3:21 when you're working with LLMs, they have
3:24 a smart zone and a dumb zone. When
3:28 you're first kind of like working with
3:30 an LM and it's like you just started a
3:32 new conversation, you start from
3:34 nothing. That's when the LLM is going to
3:35 do its best work because in that
3:37 situation, the attention relationships
3:39 are the least strained. Every time you
3:41 add a token to an LLM, it's kind of like
3:44 you're adding a team to a football
3:45 league. You think of the number of
3:47 matches that get added every time you
3:50 add a team to a football league. It just
3:51 go scales quadratically. And that's
3:54 because you have attention relationships
3:55 going from essentially each token to the
3:58 other that are positional and the sort
4:00 of meaning of the individual token. And
4:02 so this means that by around sort of 40%
4:05 or around I would say around 100k is
4:08 kind of my new marker for this because
4:09 it doesn't matter whether you're using 1
4:11 million uh context window or 200k. It's
4:15 always going to be about this.
4:17 It starts to just get dumber. So as you
4:21 continually keep adding stuff to the
4:23 same context window, it just gets dumber
4:25 and dumber until it's making kind of
4:26 stupid decisions. Raise your hand if
4:28 that feels familiar to you. Yeah. Cool.
4:31 So this means that we kind of want to
4:34 size our tasks in a way that sticks
4:37 within the smart zone, right? We don't
4:39 want the AI to bite off more than it can
4:41 chew. And this goes back to old advice
4:44 like Martin Fowler in refactoring uh
4:46 like uh the pragmatic programmer talks
4:48 about this. Don't bite off more than you
4:50 can chew. Keep your tasks small so that
4:53 you as a developer, a human developer
4:55 don't freak out and don't start acting
4:57 and going into the dumb zone.

5:01 But how do you tackle big tasks? How do
5:04 you take a large task like I don't know
5:07 cloning a company or something or just
5:09 doing something crazy? And how do you
5:12 break it into small tasks so they all
5:13 fit into the dumb zone? One way of
5:16 course you could do is I mean kind of
5:18 what the AI companies maybe want you to
5:20 do or the natural way of doing it is
5:21 just keep going and going and going. You
5:23 end up in the dumb zone charging you
5:24 tons of tokens per request. You then
5:26 compact back down. We'll talk about
5:29 compacting properly in a minute. And you
5:31 keep going, keep going, keep going,
5:32 compact back down, keep going, keep
5:33 going, keep going. And I think that's
5:36 doesn't really work very well because
5:38 the more sediment, we'll talk about that
5:40 in a minute. So the theory here is then,
5:43 and this is what I was doing for a
5:44 while, is I would use these kind of
5:48 multi-phase plans where I would say,
5:50 okay, we have this sort of number four
5:53 thing here, this large large task. Let's
5:55 break it down into small sections so
5:57 that we can then kind of chunk it up and
5:59 do each little bit of work in the smart
6:01 zone. Raise your hand if you've ever
6:03 used a multi-phase plan before. Yeah,
6:06 really common practice, right? This is
6:08 kind of how we've been doing it.
6:09 Certainly, this is how I was doing it up
6:11 until December last year really.
6:14 And any developer worth their salt will
6:16 look at this and go, "This is a loop,
6:19 right? This is a loop. We've just got
6:21 phase one, phase two, phase three, phase
6:23 four. Why don't we just have phase n,
6:27 right?
6:29 Phase n where we essentially just say,
6:31 okay, we have, let's say, a plan
6:33 operating in the background and then we
6:35 just say to the AI just make a small
6:37 change make a small change that gets us
6:39 closer and closer to there and Ralph
6:41 works okay but I prefer a little bit
6:43 more structure so that's kind where we
6:45 got to in terms of thinking about the
6:47 smart zone. And that's kind where I
6:49 want you to first start thinking about
6:51 here.

7:52 Another weird constraint of LLM is
7:53 LLM are kind of like the guy from
7:54 Momento, right? They just continually
7:55 forget. They could just keep resetting
7:56 back to the base state. Let me pull up
7:58 this diagram.

8:00 So let's say another concept I want you
8:02 to have is that every session with an
8:03 LLM kind of goes through the same
8:05 stages. You have first of all the system
8:07 prompt here. This gray box here is
8:09 essentially the stuff that's always in
8:10 your context. You want this to be as
8:11 small as possible because if you have a
8:13 ton of stuff in here, if you have 250k
8:14 tokens, like I have seen people put in
8:15 there, then that you're just going to go
8:16 straight into the dumb zone without even
8:17 being able to do anything. So you want
8:18 this to be tiny. You then go into a kind
8:19 of exploratory phase. This blue is sort
8:20 of where the coding agent is going out
8:21 and exploring the codebase. Then you go
8:22 into implementation and then you go into
8:23 testing and kind of making sure that it
8:24 works, running your feedback loops and
8:25 things like this. Raise your hand if
8:26 that feels familiar based on what you've
8:27 done. Yep. Sort of the like the the main
8:28 cornerstones of any session. And when
8:30 you clear the context, you go right back
8:31 to the system prompt. Bof, you go right
8:32 back there. So you delete everything
8:33 that's come before.

8:57 And raise your hand if you've heard of
8:58 compacting as well. Yeah. Okay. There
8:59 are some people who've not heard of
9:00 compacting. So let's just quickly show
9:01 what that means. For instance, I've just
9:02 been having a little chat with my LLM.
9:03 Uh, I want to make sure we sort of, you
9:04 know, just cover the basics so we're all
9:05 sort of on the same wavelength here.
9:06 I've just been having a chat with my
9:07 LLM. I've been talking about a thing
9:08 that I want to build. How's the font
9:09 size? Should I bump it up? Folks in the
9:10 back. Bump bump bump bump bump.
9:13 I'm using claw code for this session,
9:14 but you don't need to use claw code. Uh,
9:15 in fact, it's often nice not to use claw
9:16 code. Um, so I've been having a chat
9:17 with the LM just sort of planning out
9:18 what I'm going to do next. It's asking
9:19 me a bunch of questions and I can I
9:20 highly recommend you do this. There's
9:21 this tiny little status line here that
9:22 tells me how many tokens I'm using. The
9:23 exact number of tokens I'm using. Um I
9:24 have a article on my website AI Hero if
9:25 you want to copy this. This is oh wow
9:26 that is that shakes doesn't it? Um, this
9:27 is essential information on every coding
9:28 session because you need to know exactly
9:29 how many tokens you're using so that you
9:30 know how close you are to the dump zone.
9:31 Absolutely essential. And so let's watch
9:32 it. So I've got two options. I can
9:33 either clear
9:34 and go back to nothing or I can compact.
9:35 And when I compact then it's going to
9:36 squeeze all of that conversation which
9:37 admittedly isn't very much into a much
9:38 smaller space. And this in diagram terms
9:39 kind of looks like this where you take
9:40 all of the information from the session
9:41 and you essentially create a history out
9:42 of it, a written record of what
9:43 happened.
9:46 And devs love compacting for some
9:47 reason, but I hate it. I much prefer my
9:48 AI to behave like the guy from Momento
9:49 because this state is always the same.
9:50 Always the same. Every time you do it,
9:51 you clear and you go back to the
9:52 beginning. And so if you're able to do
9:53 that and you're able to optimize for
9:54 that, then you're in a great spot.
9:56 So that's kind of the two things I want
9:57 you to think about with LLM, the two
9:58 constraints that we're working with.
9:59 They have a smart zone and a dumb zone.
10:01 And they're like the guy from Momento.
10:03 So let's take a look at the first
10:05 exercise.

12:19 We're going to start by using a skill
12:20 which is very close to my heart. It's
12:21 the grill me skill. And this grill me
12:22 skill is wonderfully small, wonderfully
12:23 tiny. And it helps prevent one of I
12:24 think the main issues when you're
12:25 working with an AI, which is
12:26 misalignment.
12:37 The uh the sort of silent idea that I'm
12:38 talking against here, that I'm arguing
12:39 against is the specs to code movement.
12:44 Has anyone heard of the specs to code
12:45 movement? Raise your hand. It's not
12:46 really a movement. I suppose it's just
12:47 sort of people saying specs to code. Um,
12:48 what it is is people say, okay, you can
12:49 write a program or you want to build an
12:50 app. The best way to build that app is
12:51 to take some specifications.
12:52 So to write some sort of like document
12:53 and then turn that document into code.
12:55 So just turn it into code. How do you do
12:56 that? You pass it to AI. if there's
12:57 something wrong with the resulting code.
12:58 You don't look at the code, you look
12:59 back at the specs, you change the specs
13:00 and you sort of just keep going like
13:01 this. This is kind of like vibe coding
13:02 by another name where you're essentially
13:03 ignoring the code. You don't need to
13:04 worry about the code. You just sort of
13:05 keep editing the specs and eventually
13:06 you just keep going. And I tried this. I
13:07 really tried it and it sucks. It doesn't
13:08 work because you need to keep a handle
13:09 on the code. You need to understand
13:10 what's in it. You need to shape it
13:11 because the code is your battleground.

16:19 And what this does, and what I noticed
16:20 when I was working with AI, especially
16:21 in plan mode actually, is it would
16:22 really eagerly try to produce a plan for
16:23 me. It would say, "Okay, I think I've
16:24 got enough. I'm just goof plan."
16:26 And what I found was that
16:27 I was really trying to find the words
16:28 for this for what I wanted instead
16:29 of that. And Frederick P. Brooks in the
16:30 design of design he has a great quote uh
16:31 talking about the design concept when
16:32 you're working on something new with
16:33 someone when you're uh all trying to
16:34 build something together
16:35 then there's this shared idea that's
16:36 shared between all participants and that
16:37 is the design concept and that's what I
16:38 realized I needed with Claude I needed
16:39 I needed to reach a shared understanding
16:40 I didn't need an asset I didn't need a
16:41 plan I needed to be on the same
16:42 wavelength as the AI as my agent.

[... transcript continues through the full workshop ...]

1:36:39 And so thank you so much. Thank you for
1:36:40 putting up with the heat. Um hopefully
1:36:41 your body temperatures will reset soon.
1:36:42 Uh thank you very much.
