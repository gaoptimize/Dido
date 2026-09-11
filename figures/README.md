# Visualizations

Wireframe campaign for Dido relaxation on five exotic manifolds.

Claude 5 (Anthropic), visualizations · Grok Heavy (xAI), editor

Generator: [`dido_wireframe_figures.py`](dido_wireframe_figures.py) — Claude 5, 11 September 2026.

Every curve is produced by the campaign modules (SLSQP iterates on the cusp, paraboloid, and torus; exact length-constrained sweeps on the horn and cigar, which have no optimizer by design). Numbers on each panel are measured by that module’s own length / area / jerk routines.

## Layout

- [`dido_manifold_wireframes.png`](dido_manifold_wireframes.png) — summary (5 manifolds × 3 stages)
- [`wireframe_frame_metrics.json`](wireframe_frame_metrics.json) — L, A, J at each frame
- `panels/<manifold>/` — the 15 individual panels

| Manifold | Stages |
|---|---|
| [`gabriel_horn`](panels/gabriel_horn/) | initial, intermediate, escaping |
| [`hamilton_cigar`](panels/hamilton_cigar/) | initial, intermediate, escaping |
| [`hyperbolic_cusp`](panels/hyperbolic_cusp/) | initial, intermediate, optimized |
| [`paraboloid`](panels/paraboloid/) | initial, intermediate, optimized |
| [`ring_torus`](panels/ring_torus/) | initial, intermediate, optimized |

Re-running the generator writes flat names `panels/{manifold}_{n}_{stage}.png` next to this tree (it looks for `dido_horn.py` and friends in the extracted reproducibility bundle).
