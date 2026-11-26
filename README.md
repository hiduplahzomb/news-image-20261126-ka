[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/hiduplahzomb/news-image-20261126-ka/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/hiduplahzomb/news-image-20261126-ka/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# news-image-20261126-ka

A one-page broadsheet front page summarising world news on Thursday
26 November 2026 — 34 stories across 9 regions, drawn entirely in Python
with PIL vector shapes (no stock images, no AI-generated art).

Layout: giant serif date masthead, red top-stories bar, "The Day in
Numbers" strip of 6 figures (€1.58T EU budget proposal 2028-34 ·
47.6% UniCredit vote share in Commerzbank · 13 dead in the Java
gold-mine flood · 3.25% Bank of Korea base rate · 76 Cartagena
hostages counted · $94.71 Brent crude), a UTC timeline with six
verified stamps from 01:00 to 07:57 and an honest THROUGH 09:15 UTC
cutoff (the 01:37 Brent print at $94.71 is the Reuters market figure;
no guessed midday hour is shown), 3 main panels, 10 feature panels, a
21-item "Also on Thursday" list in 2 numbered columns (14–34), a numbered
world map (pins 1–13, nearest pair ~18 px apart) with a proportional
region bar whose counts are computed from the story data itself, and a
red DATE CHECK box that also lists the big 24 and 25 November stories
deliberately excluded.

Every item carries a certainty badge (CONFIRMED / OFFICIAL / REPORTED /
CLAIM); one-sided Houthi and Iran claims are marked CLAIM, while the Brent
$94.71 market figure sits in Card 2's label bar tagged MARKET, apart from
the claim badge. CONFIRMED is used on four cards (UniCredit, Java mine,
Macy's parade, Cartagena count), each verified by two outlets. OFFICIAL is
used only where the named source is an official institution (USTR, Bank of
Korea, Egypt Health Ministry, FAA, CME FedWatch, KCNA). Figures, names and
dates were re-checked against live sources on 26 Nov 2026.

Round-4 rebuild: every 24–25 Nov item was taken out of the main slots and
moved to the EXCLUDED lists — FCC's 1M SpaceX satellites, Ofgem's +26%
bills, the Greece strike, the NDLEA $227M seizure, the OPCW Russia
statement, the Swiss expulsion, the Canary 1,990 arrivals, and more. Their
places went to stories verified for 26 Nov UTC: UniCredit clearing the
last Commerzbank hurdle (Reuters · WSJ, 07:28 GMT), the Kenya court ruling
on the Ebola site, the Java mine toll of 13 (Reuters · Xinhua), the
ASEAN+3 payments talks in Kyoto, and the Asia shares bounce. The brief
list was rebuilt the same way — the Poland no-fly plan, the OPCW
statement, the Iran leave warning, the Iraq court ruling, Phala Phala,
the Sudan toll, the Nepal list, the Bangladesh pay rise, the Luma
verdict, the Earth 2°C streak, Abrego Garcia, the Brazil envoy and the
Hera photo all left, replaced by 26 Nov items such as Japan's tariff
protest, the GfK mood reading, the Mumbai 26/11 anniversary, the Kushner
talks and the NFL tripleheader. The DATE CHECK box now names only the
stories that genuinely developed on 26 Nov (USTR tariffs, Cairo toll,
Cartagena count, Macy's storm, Shenzhou crew aboard) and drops the old
Swiss-deadline sentence. The timeline lost the OPCW stamp (a 25 Nov
story) and the "GREER:" colon; Cards 1–3 gained breathing room under
their subtexts and badges; and the region bar now pairs bright amber
against red and bright cyan against green so the neighbours stay apart
at thumbnail size.

Round-5 fixes (final): the Lead #1 ribbon now reads UP TO 35% — the
USTR Section 301 proposal tops out at Vietnam's 35% (India 25%, or 17%
with a deal); the 40% figure sometimes quoted is only China's
conditional fallback rate, not a proposed rate, so it stays out of the
ribbon. The last two stale briefs went out too — the Fed hike-odds item
was built on 25 Nov PCE data with US markets shut on the 26th, and the
FAA flying record was a 24 Nov release — replaced by two Reuters items
first reported on 26 Nov UTC (the split inside the US government over
the Huang spying claims, and the US chip curbs slowing China's AI
models). The thin Lagarde-at-the-summit brief was swapped for the UK
regulator finding errors in its motor-finance payouts (Reuters, 07:15
UTC). DATE CHECK now lists the Java flood toll among the carry-over
stories and dates the range honestly as 23–25 Nov, and KPI #3 reads
JAVA MINE FLOOD TOLL (CONFIRMED). The amber MIDDLE EAST segment now
carries dark digits, Cards 1–3 subtexts sit 2 px higher, and the DATE
CHECK lines run 1 px tighter so the last red line clears the frame.

Two things to know: the Shenzhou-24 crew card is kept on purpose — the
launch and docking were 25 Nov, but the crew is aboard Tiangong through
26 Nov, and the card says so in plain words. And the FedEx brief is
dated by the clock that counts here: the jet slipped off the runway at
20:40 in Miami on Wednesday night, which is 01:40 UTC on Thursday.

## Run

```sh
python3 draw.py      # renders entry.png (1024x1024, < 1 MiB)
python3 main.py      # copies entry.png to $MAKEFUN_OUTPUT_DIR (or /output)
                     # and verifies the copy is byte-identical
```

`main.py` uses only the Python standard library. `draw.py` needs Pillow
and the DejaVu fonts in `/usr/share/fonts/truetype/dejavu/`. Rendering is
deterministic: running `draw.py` twice produces byte-identical PNGs.

## Files

- `draw.py` — renders `entry.png` with PIL
- `main.py` — copies `entry.png` to the output dir and verifies it
- `entry.png` — the 1024x1024 front page
- `README.md` — this file
- `LICENSE` — MIT
