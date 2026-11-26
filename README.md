[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/hiduplahzomb/news-image-20261126-ka/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/hiduplahzomb/news-image-20261126-ka/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# news-image-20261126-ka

A one-page broadsheet front page summarising world news on Thursday
26 November 2026 — 34 stories across 9 regions, drawn entirely in Python
with PIL vector shapes (no stock images, no AI-generated art).

Layout: giant serif date masthead, red top-stories bar, "The Day in
Numbers" strip of 6 figures (€1.58T EU budget proposal 2028-34 ·
1,000,000 SpaceX satellites · $227M Nigeria meth seizure · 1,990 Canary
arrivals · 76 hostages freed · $94.71 Brent crude), a UTC timeline with
six real timestamps, 3 main panels, 10 feature panels, a 21-item "Also on
Thursday" list in 2 numbered columns (14–34), a numbered world map (pins
1–13) with a proportional region bar, and a red DATE CHECK box that also
lists the big 24 and 25 November stories deliberately excluded.

Every item carries a certainty badge (CONFIRMED / OFFICIAL / REPORTED /
CLAIM); one-sided Houthi and Iran claims are marked CLAIM, and the Brent
$94.71 market figure is kept apart from the claim badge. OFFICIAL is used
only where the named source is an official institution (USTR, Bank of
Korea, FCC, Egypt Health Ministry, NDLEA, OPCW); CONFIRMED needs two or
more outlets. Figures, names and dates follow the brief exactly — the
Bank of Korea's 4.1% 2027 growth forecast, the ~99% Dec 9 Fed hike odds,
and the 76-hostage / 17-hour Cartagena siege were all re-checked against
live sources on 26 Nov 2026.

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
