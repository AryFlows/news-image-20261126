# Frost Front Page 26 Nov

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/AryFlows/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/AryFlows/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page newspaper front page summing up the world's news of Thursday 26 November 2026: a lead story on the deadly fuel-tanker fire on Cairo's ring road, twelve story cards spanning trade, war, space, sport and business, and a compact "Also today — in brief" list for breadth. Every story happened or was first reported on 26 November 2026, checked against AP, CNN, BBC, Reuters and The Guardian. The image is drawn entirely in code with PIL — no photographs — and stays legible at about 300 pixels wide.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `entry.png` (1024x1024, under 1 MiB) to the output directory. `build_image.py` is the script that drew the page.

---

Entered on [make.fun](https://make.fun/bounty/news-image-20261126).
