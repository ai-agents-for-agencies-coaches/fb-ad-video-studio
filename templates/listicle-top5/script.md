# VO script — listicle-top5

Generic scaffold for the "Top 5 / 5 Reasons" fast-cut listicle ad.
Problem-first hook, five punchy item lines, one CTA. Keep every beat ≤ 5s.
Swap all [BRACKET] copy. Tune the SSML `<break>` pacing to taste (≤ 0.4s — long
breaks add ad-killing dead air). Generate with `scripts/tts.py`, then
`scripts/whisper-words.py`, then retime the beats in `index.html` to the real
word starts.

Target: ~24s, vertical 1080x1920. Delivery: brisk, confident, list cadence.

---

## HOOK (title card) — 0.0-3.0s
[Number] [reasons/ways] [big promise or thing your prospect wants].
<break time="0.25s" /> Here they are.

## ITEM 1 — 3.0-6.5s
Number one. <break time="0.2s" /> [Item 1 headline in 3-5 words].
<break time="0.15s" /> [One supporting line — the payoff or proof].

## ITEM 2 — 6.5-10.0s
Number two. <break time="0.2s" /> [Item 2 headline in 3-5 words].
<break time="0.15s" /> [One supporting line — the payoff or proof].

## ITEM 3 — 10.0-13.5s
Number three. <break time="0.2s" /> [Item 3 headline in 3-5 words].
<break time="0.15s" /> [One supporting line — the payoff or proof].

## ITEM 4 — 13.5-17.0s
Number four. <break time="0.2s" /> [Item 4 headline in 3-5 words].
<break time="0.15s" /> [One supporting line — the payoff or proof].

## ITEM 5 — 17.0-20.5s
And number five. <break time="0.2s" /> [Item 5 headline in 3-5 words].
<break time="0.15s" /> [One supporting line — the payoff or proof].

## CTA (lockup) — 20.5-24.0s
[CTA — the one action]. <break time="0.2s" /> [Offer / URL / handle].
