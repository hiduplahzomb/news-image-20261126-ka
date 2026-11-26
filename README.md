[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/hiduplahzomb/news-image-20261126-ka/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/hiduplahzomb/news-image-20261126-ka/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# news-image-20261126-ka

A one-page broadsheet front page summarising world news on Thursday
26 November 2026 — 34 stories across 9 regions, drawn entirely in Python
with PIL vector shapes (no stock images, no AI-generated art).

Layout: giant serif date masthead, red top-stories bar, "The Day in
Numbers" strip (€1.58T EU budget proposal 2028-34 · 1,000,000 SpaceX satellites ·
$227M Nigeria meth seizure · 1,990 Canary arrivals · 76 hostages freed),
a UTC timeline, 3 main panels, 10 feature panels, a 21-item "Also on
Thursday" list, a numbered world map (pins 1–13), and a red DATE CHECK box
that also lists the big 25 November stories deliberately excluded.

Every item carries a certainty badge (CONFIRMED / OFFICIAL / REPORTED /
CLAIM); one-sided Houthi and Iran claims are marked CLAIM. Figures, names
and dates follow the brief exactly. Of the 25 candidate one-liners, 4 were
dropped to reach the 34-story total: India Constitution Day, Australia's
2035 emissions-target projection, the Flinders fire, and the Hong Kong
fire anniversary.

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
