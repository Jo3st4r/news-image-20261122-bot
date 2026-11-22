# 50 stories, one page — the world on 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Jo3st4r/news-image-20261122-bot/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Jo3st4r/news-image-20261122-bot/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up the world's news of Sunday 22 November 2026: **50 verified stories on one page** — three lead stories (Iran strikes a US air base in Kuwait, COP31 deadlocked over fossil fuels in Antalya, Russia's 400-drone + 110-missile barrage on Ukraine), a round-the-world band, and 47 more stories across every region and beat, with a date check at the foot.

## How it works

- `tools/render.py` draws the newspaper front page (`assets/entry.png`, 1024×1024) from the 50 headlines, deterministically — fixed strings, fixed colours, no clock, no random.
- `main.py` (standard library only) copies `assets/entry.png` to `/output/entry.png`. It must stay stdlib-only: the grader runs it in a bare Python image.

## Run it

```sh
python3 tools/render.py   # re-render assets/entry.png
python3 main.py           # copy it to /output/entry.png
```

## Sources

Every story was checked against reporting from Reuters, BBC, AP, CNN, The Guardian or UN News, first reported 21–22 November 2026. Two spot-checks: the Peru quake is magnitude 6.7, USGS-reviewed (early 6.9 readings were superseded); the COP31 draft cover decision dropped every mention of fossil fuels and talks spilled into overtime.

## Entry

- Competition: [news-image-20261122](https://make.fun/bounty/news-image-20261122)
- Repo: Jo3st4r/news-image-20261122-bot
- License: MIT
