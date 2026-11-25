# World News — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/andk08/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/andk08/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One image summing up the world's news of **Tuesday 24 November 2026** —
a newspaper front page with six stories from that day, each drawn with a
simple scene and a short factual label. Every fact on the image was
checked against news reported on 24 November 2026.

## The stories

- **Ukraine** — An overnight Russian strike on Zaporizhzhia kills 2 and
  wounds 40, including four children.
- **Gaza** — Israeli airstrikes kill at least six Palestinians, including
  two police officers, medics say.
- **Libya** — Ukraine says its naval drones hit Russian ships off Benghazi
  and sank a warship; first reported on 24 November.
- **Nepal** — A magnitude 5.6 earthquake strikes near the China border at
  7:17 a.m. in Taplejung; felt in Kathmandu, no damage reported.
- **United States** — Virginia and Oregon become the first states to sue
  SpaceX over Grok's sexual deepfakes of real people.
- **Space** — China unveils the Shenzhou-24 crew: Pakistani Zeeshan Ali
  will be the first foreign astronaut aboard the Tiangong station.

## How it works

`draw.py` (build time only, Pillow) draws `entry.png` (1024x1024, PNG).
`main.py` (standard library only) copies the committed `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

Run locally:

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
