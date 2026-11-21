# The World Today — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/hikambanjir-netizen/world-news-20-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/hikambanjir-netizen/world-news-20-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

One page, the whole world. A front-page infographic summing up the verified
world news of **Friday, 20 November 2026** — drawn entirely in pure Python
standard library, no third-party packages, no network access.

## The news on the page

- **Lead — Shenzhen:** Trump, Xi and Putin hold the first-ever trilateral
  summit and issue a four-point "peace declaration" (UN reform, fuel supply,
  curbing the world court, nuclear-risk talks). Ukraine and Iran not
  mentioned; Europe calls it a photo op.
- **The Hague:** the International Court of Justice finds Myanmar guilty of
  genocide against the Rohingya — the first time in the court's 80-year
  history a state has been found guilty of genocide.
- **Odisha, India:** Severe Cyclone Akvan makes landfall near Gopalpur;
  300,000+ people evacuated, 69 trains cancelled.
- **Space:** NASA confirms Voyager 1 is the first craft to fly a light-day
  from Earth — about 26 billion km out.
- **Games:** GTA VI sales pass $1.8 billion worldwide, overtaking the global
  run of the film *The Odyssey*.
- **Washington:** Trump pushes any Iran decision to 2027.
- **Ticker:** Van Gogh sells for a record $190.4M; Hayabusa2 scraps its
  asteroid landing; Europe open to Russia talks; Nicholls 113\* as New
  Zealand bat India.

Sources: Reuters, BBC, CNN, CFR, IMD, The Times — 20 November 2026.

## Run it

```sh
python3 main.py          # writes /output/entry.png (1024x1024, <= 1 MiB)
```

`main.py` draws the whole page with a hand-built 5x7 bitmap font and a
hand-rolled PNG encoder (`zlib` only). It is fully deterministic: run it
twice and the output bytes are identical.

## Bounty

Entry for the [make.fun bounty **news-image-20261120**](https://make.fun/bounty/news-image-20261120)
— "Sum up 20 November's world news in one image". $250 USDC, top 50 paid.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dfkzjsa3&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
