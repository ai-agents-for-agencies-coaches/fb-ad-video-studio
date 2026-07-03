# split-screen — script scaffold

Vertical split-screen / reaction ad. ~15s. Two stacked clips with a word-synced
caption band on the seam. Replace every [BRACKET]. Keep lines short: captions
must fit the on-seam pill and land on whisper word starts.

## Panels
- TOP (`assets/top.mp4`): [reaction / presenter / talking-head — the CLAIM]
- BOTTOM (`assets/bottom.mp4`): [demo / screen-record / b-roll — the PROOF]
- TOP_LABEL: [e.g. "REACTION" / "BEFORE" / "THE CLAIM"]
- BOTTOM_LABEL: [e.g. "PROOF" / "AFTER" / "LIVE DEMO"]

## VO / captions (retime to whisper word starts)
- 0.4–3.5  (cap-1, hook):   [scroll-stopping claim — say the outcome out loud]
- 3.6–7.0  (cap-2, problem): [the pain they feel right now]
- 7.2–10.5 (cap-3, proof):  [point to the bottom panel — "watch this"]
- 10.6–13.0 (cap-4, payoff): [the result / transformation]

## End lockup (13–15s)
- BRAND: [brand name + one-line tagline]
- CTA / URL: [offer or destination]

## Notes
- Panel videos stay MUTED; VO lives on `audio/vo.mp3` (track 0).
- Re-encode phone clips before dropping them in (see index.html header comment).
- SFX: whoosh on panel-in, ticks on caption swaps, ding on proof, punch on lockup.
