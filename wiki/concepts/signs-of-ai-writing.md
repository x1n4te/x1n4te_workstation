---
id: signs-of-ai-writing-001
type: concept
created: 2026-04-09
updated: 2026-04-09
last_verified: 2026-04-09
review_after: 2026-07-09
stale_after: 2026-10-09
confidence: high
status: active
source_refs:
  - https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
tags:
  - ai-detection
  - llm
  - cybersecurity
  - social-engineering
  - content-analysis
related:
  - concepts/llm-security-learning-path
  - concepts/slm-log-reading-pipeline
  - sources/software-dev/owasp-top-10-2025
---

# Signs of AI Writing — Detection Guide

**Source:** Wikipedia:Signs of AI Writing (en.wikipedia.org)
**Purpose:** Identify AI-generated text in the wild — phishing emails, fake reports, social engineering, threat intel, academic fraud
**Relevance:** Cybersecurity professionals need to detect AI-generated content used in attacks

---

## Why This Matters for Security

AI-generated text is used in:
- **Phishing emails** — perfectly written, contextually relevant lures
- **Social engineering** — automated pretexting at scale
- **Fake threat reports** — AI-generated CVE analyses that look legitimate
- **Disinformation** — synthetic news articles and blog posts
- **Academic fraud** — AI-written papers and assignments
- **Fake reviews/testimonials** — synthetic social proof

Being able to spot AI writing is a cybersecurity skill, not just an editorial one.

---

## Content Signals

### 1. Undue Emphasis on Significance and Legacy

AI overemphasizes importance with phrases like:
- "plays a crucial role in..."
- "has had a profound impact on..."
- "stands as a testament to..."
- "represents a significant milestone in..."
- "continues to shape the landscape of..."

**Human writing** is more specific and less grandiose.

### 2. Superficial Analyses

AI provides surface-level descriptions that sound informed but lack depth:
- Covers "what" but not "why" or "how"
- Lists features without explaining tradeoffs
- Describes processes without technical detail
- Generic statements that could apply to anything

**Example:** "The system uses advanced encryption to protect data" vs "The system uses AES-256-GCM with X25519 key wrapping for data at rest."

### 3. Promotional Language

AI defaults to positive framing even for neutral topics:
- "innovative solution"
- "cutting-edge technology"
- "seamlessly integrates"
- "robust and scalable"
- "leverages the power of"

### 4. Vague Attributions

AI attributes claims vaguely:
- "Experts suggest that..."
- "Studies have shown..."
- "Many believe that..."
- "It is widely accepted that..."
- "Critics argue that..."

**Human writing** names specific sources: "According to Smith et al. (2024)..."

### 5. Outline-Like Conclusions

AI ends sections with generic future-looking statements:
- "Looking ahead, the field is expected to..."
- "As technology continues to evolve..."
- "The future holds great promise for..."
- "Challenges remain, but opportunities abound..."

---

## Language Signals

### 6. High-Density "AI Vocabulary"

Certain words appear disproportionately in AI text:

| Overused | Human Alternative |
|---|---|
| delve | explore, investigate |
| intricate | complex, detailed |
| tapestry | mix, combination |
| landscape | field, area |
| realm | field, domain |
| pivotal | important, key |
| testament | evidence, proof |
| nuanced | detailed, specific |
| foster | support, encourage |
| robust | strong, reliable |
| leverage | use, apply |
| holistic | comprehensive, complete |
| multifaceted | complex, varied |
| paramount | critical, essential |
| underscore | highlight, emphasize |

**Red flag:** Multiple AI vocabulary words in a single paragraph.

### 7. Avoidance of Simple "Is/Are" Phrases

AI rewrites simple statements to sound more sophisticated:
- Instead of "The firewall is configured to..." → "The firewall serves as a critical barrier configured to..."
- Instead of "The report is long" → "The report spans a considerable length"

### 8. Negative Parallelisms

AI loves "not just X, but also Y" constructions:
- "This is not just a technical issue, but also a cultural one"
- "It's not merely about efficiency, but also about security"
- "Not only does it improve performance, but it also enhances reliability"

### 9. Rule of Three

AI groups things in threes reflexively:
- "robust, scalable, and maintainable"
- "identify, assess, and mitigate"
- "efficient, effective, and reliable"

### 10. Elegant Variation

AI avoids repeating words, even when repetition is natural:
- First mention: "the system"
- Second mention: "the platform"
- Third mention: "the solution"
- Fourth mention: "this framework"

**Human writing** repeats the same word when it's the clearest option.

---

## Style Signals

### 11. Overuse of Boldface

AI bolds keywords excessively, especially in lists and introductions.

### 12. Overuse of Em Dashes

AI uses em dashes (—) more than humans. Sentences are often interrupted with parenthetical em-dash phrases.

### 13. Excessive Tables

AI converts prose into tables even when tables aren't needed. Tables with 2 columns and 3 rows could be a sentence.

### 14. Curly Quotes

AI output often uses curly/smart quotes (" ") instead of straight quotes (" "). Most human text editors use straight quotes by default.

### 15. Subject Lines and Headers

AI adds unnecessary headers or subject lines that fragment the text.

---

## Communication Signals

### 16. Collaborative Language

AI uses phrases intended for the reader:
- "Let's explore..."
- "As we can see..."
- "It's important to note that..."
- "Keep in mind that..."
- "To put it simply..."

### 17. Knowledge-Cutoff Disclaimers

AI pre-emptively excuses gaps:
- "As of my knowledge cutoff..."
- "Information may have changed since..."
- "It's worth noting that recent developments..."

### 18. Placeholder Text

AI leaves templates unfilled:
- "[insert statistic here]"
- "[year]"
- "according to [source]"

---

## Markup Signals

### 19. Markdown in Non-Markdown Contexts

AI outputs Markdown formatting (bold with **, headers with #) in contexts that don't support it.

### 20. Broken Links and Citations

AI generates URLs, DOIs, and ISBNs that don't resolve to real resources.

### 21. AI-Specific Markup Artifacts

- `contentReference` tags (from ChatGPT)
- `oaicite` markers
- `turn0search0` / `turn1search3` references
- `+1` citation markers
- `grok_card` references

These are dead giveaways — they're internal to specific AI systems.

---

## Citation Signals

### 22. Invalid DOIs and ISBNs

AI generates plausible-looking but non-existent DOIs and ISBNs.

### 23. Books Without Page Numbers

AI cites books without specific page references — real citations usually include pages.

### 24. Broken External Links

AI fabricates URLs that look real but return 404.

---

## Composite Indicators

No single sign is definitive. Look for **combinations**:

| Confidence | Evidence |
|---|---|
| Low (suspicious) | 1-2 language signals + unusual style |
| Medium (likely) | 3-5 signals across multiple categories |
| High (almost certain) | 6+ signals + markup artifacts + broken citations |
| Definitive | AI-specific artifacts (`oaicite`, `contentReference`, `turn0search0`) |

---

## What AI Detection Tools Can't Do

- **False positives:** Human writing can contain AI-like patterns (especially non-native English speakers, corporate writing, academic writing)
- **False negatives:** Skilled users can edit AI output to remove tells
- **Adversarial evasion:** AI text can be rephrased to avoid detection tools

**Best approach:** Use this guide for human judgment. Don't rely solely on automated detectors.

---

## Signs of Human Writing (Ineffective as AI Indicators)

These are NOT reliable indicators of human writing:
- Typos and grammatical errors (AI can simulate these)
- Personal anecdotes (AI can fabricate these)
- Citations to real sources (AI can cite real papers incorrectly)
- Emotional language (AI can generate emotional text)

---

## Cybersecurity Applications

| Scenario | How to Use This Guide |
|---|---|
| Phishing email analysis | Check for AI vocabulary density, perfect grammar in suspicious emails |
| Threat report verification | Look for superficial analysis, broken citations, vague attributions |
| Social engineering detection | Identify templated language, collaborative tone, placeholder text |
| Academic integrity | Detect outline-like conclusions, rule-of-three patterns, elegant variation |
| Disinformation identification | Spot promotional language, undue significance claims, knowledge-cutoff disclaimers |

---

## Quick Reference Checklist

```
□ Multiple "AI vocabulary" words in one paragraph
□ "Not just X, but Y" negative parallelism
□ Rule of three in lists
□ Vague attributions ("experts say", "studies show")
□ Undue emphasis on significance/legacy
□ Outline-like future-looking conclusions
□ Overuse of em dashes
□ Excessive boldface
□ Collaborative language ("Let's explore...")
□ Knowledge-cutoff disclaimers
□ AI-specific markup artifacts (oaicite, contentReference)
□ Broken DOIs/ISBNs/URLs
□ Books cited without page numbers
```

3+ checks = suspicious. 6+ = likely AI. Artifacts = definitive.

---

*Source: Wikipedia:Signs of AI Writing. Adapted for cybersecurity context.*
