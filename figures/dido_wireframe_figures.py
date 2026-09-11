"""White-on-black wireframe figures for the Dido exotic-surface campaign.

Renders, for each of five manifolds, three panels showing the selected region
and its fixed-length boundary at successive stages of the experiment.

The geometry is not illustrative.  Every curve drawn here is produced by the
campaign modules themselves:

  * hyperbolic cusp, paraboloid, ring torus
        Genuine SLSQP iterates.  `scipy.optimize.minimize` is temporarily
        wrapped inside the owning module so the module's own objective,
        bounds, and constraints run untouched while the iterate sequence is
        recorded.  Panels show the seed, a mid-run iterate, and the converged
        optimizer.

  * capped Gabriel horn, Hamilton cigar
        These modules carry no optimizer, by design: their result is that no
        optimum exists.  Length is solved exactly by `brentq` on a
        one-parameter family and the region center is swept outward, so area
        escapes at fixed length.  Panels show three centers along that sweep
        and the third is labelled ESCAPING, not OPTIMIZED.

Every number printed on a panel is measured by the owning module's own
length / area / jerk routines at that exact frame.

Python 3.10+.  Dependencies: NumPy, SciPy, Matplotlib.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
from matplotlib.patches import Rectangle

def _locate_campaign_modules() -> None:
    """Find dido_horn / dido_cigar / dido_cusp / dido_paraboloid / dido_torus.

    They live inside the reproducibility bundle.  This script runs either from
    within that bundle or from a figures/ directory beside it.
    """
    here = Path(__file__).resolve().parent
    candidates = [here, here.parent,
                  here / "dido_exotic_surfaces_reproducibility",
                  here.parent / "dido_exotic_surfaces_reproducibility"]
    for candidate in candidates:
        if (candidate / "dido_horn.py").is_file():
            sys.path.insert(0, str(candidate))
            return
    raise SystemExit(
        "Cannot find the campaign modules (dido_horn.py and friends).\n"
        "Run this from inside the extracted reproducibility bundle, or place\n"
        "the extracted dido_exotic_surfaces_reproducibility/ directory beside\n"
        "this script.  Searched:\n  " + "\n  ".join(str(c) for c in candidates))


_locate_campaign_modules()

import dido_cigar
import dido_cusp
import dido_horn
import dido_paraboloid
import dido_torus


TAU = 2.0 * math.pi

# ---------------------------------------------------------------- palette ---

BG = "#04060A"
PANEL_EDGE = "#16222E"
MESH_FAR = np.array([0.13, 0.26, 0.38])
MESH_NEAR = np.array([0.58, 0.87, 1.00])
CURVE_RGB = np.array([1.00, 0.74, 0.30])
FILL_RGB = np.array([1.00, 0.62, 0.18])
TEXT = "#DCE9F4"
TEXT_DIM = "#5D7487"
TEXT_ACCENT = "#FFC46B"

STAGE_NAMES = ("INITIAL", "INTERMEDIATE", "OPTIMIZED")


# ----------------------------------------------------------------- camera ---


def camera(az_deg: float, el_deg: float, roll_deg: float = 0.0):
    az = math.radians(az_deg)
    el = math.radians(el_deg)
    d = np.array([math.cos(el) * math.cos(az),
                  math.cos(el) * math.sin(az),
                  math.sin(el)])
    u = np.array([-math.sin(az), math.cos(az), 0.0])
    v = np.cross(d, u)
    if roll_deg:
        # In-plane rotation only.  Elongated surfaces (horn, cigar) are laid
        # along the panel diagonal so a square frame is not mostly empty.
        c, s = math.cos(math.radians(roll_deg)), math.sin(math.radians(roll_deg))
        u, v = c * u + s * v, -s * u + c * v
    return u, v, d


def project(points: np.ndarray, cam) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    u, v, d = cam
    p = np.asarray(points, dtype=float)
    return p @ u, p @ v, p @ d


def polyline_segments(xs, ys, depths, close=False):
    if close:
        xs = np.append(xs, xs[0])
        ys = np.append(ys, ys[0])
        depths = np.append(depths, depths[0])
    a = np.stack([xs[:-1], ys[:-1]], axis=1)
    b = np.stack([xs[1:], ys[1:]], axis=1)
    return np.stack([a, b], axis=1), 0.5 * (depths[:-1] + depths[1:])


def depth_key(depths, lo, hi):
    if hi - lo < 1.0e-12:
        return np.full_like(np.asarray(depths, dtype=float), 0.5)
    return np.clip((np.asarray(depths, dtype=float) - lo) / (hi - lo), 0.0, 1.0)


# Shading must key off which way the surface faces, not the absolute view
# depth p.d.  On an elongated surface (horn, cigar) p.d is dominated by
# position along the axis, which would light the far tip and darken the near
# bell.  The outward normal's alignment with the view direction is the
# quantity that actually separates the front of the surface from its back.


def revolution_facing(axis: str):
    e = np.array([1.0, 0.0, 0.0]) if axis == "x" else np.array([0.0, 0.0, 1.0])

    def facing(points, view):
        p = np.asarray(points, dtype=float)
        radial = p - (p @ e)[..., None] * e
        norm = np.linalg.norm(radial, axis=-1, keepdims=True)
        return (radial / np.where(norm < 1.0e-12, 1.0, norm)) @ view

    return facing


def torus_facing(major_radius: float):
    def facing(points, view):
        p = np.asarray(points, dtype=float)
        phi = np.arctan2(p[..., 1], p[..., 0])
        center = np.stack([major_radius * np.cos(phi),
                           major_radius * np.sin(phi),
                           np.zeros_like(phi)], axis=-1)
        n = p - center
        norm = np.linalg.norm(n, axis=-1, keepdims=True)
        return (n / np.where(norm < 1.0e-12, 1.0, norm)) @ view

    return facing


def facing_key(values):
    return np.clip(0.5 + 0.5 * np.asarray(values, dtype=float), 0.0, 1.0)


# --------------------------------------------------------------- surfaces ---


def revolve(axial: np.ndarray, radius: np.ndarray, theta: np.ndarray,
            axis: str = "z") -> np.ndarray:
    """Grid of a surface of revolution, shape (len(axial), len(theta), 3)."""
    c = np.cos(theta)[None, :]
    s = np.sin(theta)[None, :]
    r = np.asarray(radius, dtype=float)[:, None]
    a = np.asarray(axial, dtype=float)[:, None] * np.ones_like(c)
    if axis == "z":
        return np.stack([r * c, r * s, a], axis=-1)
    return np.stack([a, r * c, r * s], axis=-1)


def cigar_axial(rho: np.ndarray) -> np.ndarray:
    """z(rho) for the cigar soliton embedded as a surface of revolution.

    The metric is drho^2 + tanh(rho)^2 dtheta^2, so the profile radius is
    tanh(rho) and the axial coordinate satisfies z' = sqrt(1 - sech(rho)^4).
    """
    grid = np.linspace(0.0, float(np.max(rho)), 4000)
    integrand = np.sqrt(np.clip(1.0 - np.cosh(grid) ** -4, 0.0, None))
    primitive = np.concatenate([[0.0], np.cumsum(
        0.5 * (integrand[1:] + integrand[:-1]) * np.diff(grid))])
    return np.interp(rho, grid, primitive)


def cusp_axial(r: np.ndarray) -> np.ndarray:
    """z(r) for the hyperbolic cusp dr^2 + exp(-2r) dtheta^2 (a tractricoid)."""
    grid = np.linspace(0.0, float(np.max(r)), 4000)
    integrand = np.sqrt(np.clip(1.0 - np.exp(-2.0 * grid), 0.0, None))
    primitive = np.concatenate([[0.0], np.cumsum(
        0.5 * (integrand[1:] + integrand[:-1]) * np.diff(grid))])
    return np.interp(r, grid, primitive)


# ----------------------------------------------------- iterate collection ---


class TracedMinimize:
    """Record every SLSQP iterate produced inside a campaign module.

    The module's own objective, bounds, and constraints are untouched; only
    the iterate sequence is captured.
    """

    def __init__(self, module):
        self.module = module
        self.frames: list[np.ndarray] = []

    def __enter__(self):
        original = self.module.minimize
        frames = self.frames

        def wrapper(fun, x0, *args, **kwargs):
            frames.append(np.array(x0, dtype=float).copy())

            def record(xk, *_a, **_k):
                frames.append(np.array(xk, dtype=float).copy())

            kwargs["callback"] = record
            return original(fun, x0, *args, **kwargs)

        self._original = original
        self.module.minimize = wrapper
        return self

    def __exit__(self, *exc):
        self.module.minimize = self._original
        return False


def pick_three(frames: list[np.ndarray], final: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """Seed, a genuinely intermediate iterate, and the converged coefficients.

    SLSQP often reaches the optimum well before it stops iterating, so the
    iterate at the halfway *index* is frequently identical to the final one.
    The middle panel is instead the iterate that has travelled about half the
    coefficient-space distance from the seed to the optimum.
    """
    if not frames:
        return [(0, final), (0, final), (0, final)]
    last = len(frames) - 1
    if last < 2:
        return [(0, frames[0]), (last, frames[last]), (last, final)]
    stack = np.asarray(frames, dtype=float)
    distance = np.linalg.norm(stack - np.asarray(final, dtype=float)[None, :], axis=1)
    interior = distance[1:last]
    mid = 1 + int(np.argmin(np.abs(interior - 0.5 * distance[0])))
    return [(0, frames[0]), (mid, frames[mid]), (last, final)]


# ------------------------------------------------------- panel definitions ---


def build_horn(points: int = 1024):
    metric = dido_horn.HornMetric()
    target = 3.0
    centers = (3.0, 6.0, 12.0)
    frames = []
    for center in centers:
        graph = dido_horn.solve_exact_length(metric, center, target, points)
        x, _, _ = graph.samples()
        frames.append({
            "theta": graph.theta,
            "coord": x,
            "L": dido_horn.metric_length(metric, graph),
            "A": dido_horn.enclosed_tail_area(metric, graph),
            "J": dido_horn.jerk_energy(metric, graph),
            "note": "center X = {:.0f}".format(center),
        })

    far = float(max(f["coord"].max() for f in frames)) * 1.18
    axial = np.geomspace(1.0, far, 150)
    mesh = revolve(axial, 1.0 / axial, np.linspace(0.0, TAU, 132), axis="x")

    def region(frame):
        # HornMetric.tail_area_primitive is documented as the integral of the
        # area density from x=1 to x, so the selected set is the band between
        # the cap circle and the boundary, {x <= graph(theta)} -- not the
        # region beyond it, which has infinite area.  The compact cap itself
        # is unspecified in the module and is not drawn.
        s = np.linspace(0.0, 1.0, 44)[:, None]
        grid = 1.0 + s * (frame["coord"][None, :] - 1.0)
        theta = frame["theta"][None, :] * np.ones_like(grid)
        return np.stack([grid, np.cos(theta) / grid, np.sin(theta) / grid], axis=-1)

    def curve(frame):
        x, theta = frame["coord"], frame["theta"]
        return np.stack([x, np.cos(theta) / x, np.sin(theta) / x], axis=-1)

    return {
        "key": "gabriel_horn",
        "name": "Capped Gabriel horn",
        "caption": "fixed length, area escapes to infinity",
        "metric": r"$g=(1+x^{-4})\,dx^{2}+x^{-2}d\theta^{2}$",
        "mesh": mesh, "region": region, "curve": curve, "frames": frames,
        "stages": ("INITIAL", "INTERMEDIATE", "ESCAPING"),
        "escape": True, "target": target,
        "az": -76.0, "el": 15.0, "roll": 26.0,
        "facing": revolution_facing("x"),
    }


def build_cigar(points: int = 1024):
    metric = dido_cigar.CigarMetric()
    target = TAU
    centers = (2.0, 3.2, 4.6)
    frames = []
    for center in centers:
        graph = dido_cigar.solve_exact_length(metric, center, target, points)
        rho, _, _ = graph.samples()
        frames.append({
            "theta": graph.theta,
            "coord": rho,
            "L": dido_cigar.metric_length(metric, graph),
            "A": dido_cigar.enclosed_area(metric, graph),
            "J": dido_cigar.jerk_energy(metric, graph),
            "note": "center ρ = {:.1f}".format(center),
        })

    far = float(max(f["coord"].max() for f in frames)) * 1.16
    rho = np.linspace(0.0, far, 130)
    mesh = revolve(cigar_axial(rho), np.tanh(rho),
                   np.linspace(0.0, TAU, 132), axis="x")

    def region(frame):
        # Selected set is the compact cap {rho <= graph(theta)}.
        s = np.linspace(0.0, 1.0, 44)[:, None]
        grid = s * frame["coord"][None, :]
        theta = frame["theta"][None, :] * np.ones_like(grid)
        z = cigar_axial(grid.ravel()).reshape(grid.shape)
        r = np.tanh(grid)
        return np.stack([z, r * np.cos(theta), r * np.sin(theta)], axis=-1)

    def curve(frame):
        rho_c, theta = frame["coord"], frame["theta"]
        r = np.tanh(rho_c)
        return np.stack([cigar_axial(rho_c), r * np.cos(theta),
                         r * np.sin(theta)], axis=-1)

    return {
        "key": "hamilton_cigar",
        "name": "Hamilton cigar soliton",
        "caption": "fixed length, area escapes while J → 0",
        "metric": r"$g=d\rho^{2}+\tanh^{2}\!\rho\,d\theta^{2}$",
        "mesh": mesh, "region": region, "curve": curve, "frames": frames,
        "stages": ("INITIAL", "INTERMEDIATE", "ESCAPING"),
        "escape": True, "target": target,
        "az": -76.0, "el": 15.0, "roll": 20.0,
        "facing": revolution_facing("x"),
    }


def build_cusp(modes: int = 6, points: int = 512, seed: int = 20260909):
    target = 2.0
    loop = dido_cusp.CuspLoop(modes, points)
    exact_radius = math.log(TAU / target)
    initial = loop.circle(exact_radius)
    rng = np.random.default_rng(seed)
    perturb = rng.normal(0.0, 0.16, 2 * modes) / np.arange(1, 2 * modes + 1)
    initial[1:] = perturb
    for _ in range(8):
        initial[0] += math.log(dido_cusp.metric_length(loop, initial) / target)

    with TracedMinimize(dido_cusp) as trace:
        result = dido_cusp.optimize_tail(loop, target, initial)
    picks = pick_three(trace.frames, result.x)

    frames = []
    for stage, (index, coefficients) in enumerate(picks):
        radius, _, _ = loop.evaluate(coefficients)
        frames.append({
            "theta": loop.theta,
            "coord": radius,
            "L": dido_cusp.metric_length(loop, coefficients),
            "A": dido_cusp.tail_area(loop, coefficients),
            "J": dido_cusp.jerk_energy(loop, coefficients),
            "note": "seed" if stage == 0 else "SLSQP iterate {}".format(index),
        })
    frames[-1]["note"] = "converged, {} iterations".format(int(result.nit))

    far = float(max(f["coord"].max() for f in frames)) + 1.25
    r = np.linspace(0.0, far, 130)
    mesh = revolve(cusp_axial(r), np.exp(-r), np.linspace(0.0, TAU, 132))

    def region(frame):
        # Selected set is the noncompact tail {r >= graph(theta)}.
        s = np.linspace(0.0, 1.0, 44)[:, None]
        grid = frame["coord"][None, :] + s * (far - frame["coord"][None, :])
        theta = frame["theta"][None, :] * np.ones_like(grid)
        rad = np.exp(-grid)
        z = cusp_axial(grid.ravel()).reshape(grid.shape)
        return np.stack([rad * np.cos(theta), rad * np.sin(theta), z], axis=-1)

    def curve(frame):
        rr, theta = frame["coord"], frame["theta"]
        rad = np.exp(-rr)
        return np.stack([rad * np.cos(theta), rad * np.sin(theta),
                         cusp_axial(rr)], axis=-1)

    return {
        "key": "hyperbolic_cusp",
        "name": "Hyperbolic cusp",
        "caption": "noncompact tail, finite area, χ = 0",
        "metric": r"$g=dr^{2}+e^{-2r}d\theta^{2},\; K=-1$",
        "mesh": mesh, "region": region, "curve": curve, "frames": frames,
        "stages": STAGE_NAMES, "escape": False, "target": target,
        "az": 28.0, "el": 13.0,
        "facing": revolution_facing("z"),
        "result": result,
    }


def build_paraboloid(modes: int = 6, points: int = 512, seed: int = 20260909):
    target = 6.0
    loop = dido_paraboloid.RadialLoop(modes, points)
    radius = target / TAU
    initial = loop.circle(radius)
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, 0.13 * radius, 2 * modes)
    noise /= np.tile(np.arange(1, modes + 1), 2) ** 1.5
    initial[1:] = noise
    initial[0] = radius

    with TracedMinimize(dido_paraboloid) as trace:
        result = dido_paraboloid.optimize_area(loop, target, initial)
    picks = pick_three(trace.frames, result.x)

    frames = []
    for stage, (index, coefficients) in enumerate(picks):
        rr, _, _ = loop.evaluate(coefficients)
        frames.append({
            "theta": loop.theta,
            "coord": rr,
            "L": dido_paraboloid.metric_length(loop, coefficients),
            "A": dido_paraboloid.enclosed_area(loop, coefficients),
            "J": dido_paraboloid.jerk_energy(loop, coefficients),
            "note": "seed" if stage == 0 else "SLSQP iterate {}".format(index),
        })
    frames[-1]["note"] = "converged, {} iterations".format(int(result.nit))

    far = float(max(f["coord"].max() for f in frames)) * 1.16
    rr = np.linspace(0.0, far, 120)
    mesh = revolve(rr ** 2, rr, np.linspace(0.0, TAU, 132))

    def region(frame):
        # Selected set is the intrinsic disk {r <= graph(theta)}.
        s = np.linspace(0.0, 1.0, 44)[:, None]
        grid = s * frame["coord"][None, :]
        theta = frame["theta"][None, :] * np.ones_like(grid)
        return np.stack([grid * np.cos(theta), grid * np.sin(theta),
                         grid ** 2], axis=-1)

    def curve(frame):
        rad, theta = frame["coord"], frame["theta"]
        return np.stack([rad * np.cos(theta), rad * np.sin(theta),
                         rad ** 2], axis=-1)

    return {
        "key": "paraboloid",
        "name": "Paraboloid",
        "caption": "positive control, circle recovered, no escape",
        "metric": r"$g=(1+4r^{2})dr^{2}+r^{2}d\theta^{2}$",
        "mesh": mesh, "region": region, "curve": curve, "frames": frames,
        "stages": STAGE_NAMES, "escape": False, "target": target,
        "az": 42.0, "el": 21.0,
        "facing": revolution_facing("z"),
        "result": result,
    }


def build_torus(modes: int = 4, points: int = 1024, maxiter: int = 600):
    torus = dido_torus.RingTorus(3.0, 1.0)
    loop = dido_torus.FourierLoop(modes, points)
    target = 4.0
    # Seed on the side of the tube (theta0 = pi/2) rather than at the outer
    # equator.  This is one of the module's own multistart centers, and the
    # optimizer migrates the region to theta = 0, where K is maximal.  It
    # lands on the same champion area as the theta0 = 0 start.
    initial = loop.local_metric_circle(torus, 0.5 * math.pi, 0.0, target / TAU)
    initial = dido_torus.fit_initial_length(torus, loop, initial, target)

    with TracedMinimize(dido_torus) as trace:
        result = dido_torus.optimize_area(torus, loop, target, initial, maxiter)
    picks = pick_three(trace.frames, result.x)

    def embed(theta, phi):
        a = torus.parallel_radius(theta)
        return np.stack([a * np.cos(phi), a * np.sin(phi),
                         torus.minor_radius * np.sin(theta)], axis=-1)

    frames = []
    for stage, (index, coefficients) in enumerate(picks):
        theta, phi, *_ = loop.evaluate(coefficients)
        frames.append({
            "theta_c": theta, "phi_c": phi,
            "L": dido_torus.metric_length(torus, loop, coefficients),
            "A": dido_torus.enclosed_area(torus, loop, coefficients),
            "J": dido_torus.jerk_energy(torus, loop, coefficients),
            "note": "{}   θ centre = {:+.3f}".format(
                "seed" if stage == 0 else "SLSQP iterate {}".format(index),
                float(np.arctan2(np.sin(np.mean(theta)), np.cos(np.mean(theta))))),
        })
    final_theta, *_ = loop.evaluate(picks[-1][1])
    frames[-1]["note"] = "converged, {} iterations   θ centre = {:+.3f}".format(
        int(result.nit),
        float(np.arctan2(np.sin(np.mean(final_theta)), np.cos(np.mean(final_theta)))))

    grid_theta = np.linspace(0.0, TAU, 96)
    grid_phi = np.linspace(0.0, TAU, 156)
    tt, pp = np.meshgrid(grid_theta, grid_phi, indexing="ij")
    mesh = embed(tt, pp)

    def region(frame):
        theta, phi = frame["theta_c"], frame["phi_c"]
        tc, pc = float(np.mean(theta)), float(np.mean(phi))
        s = np.linspace(0.0, 1.0, 40)[:, None]
        th = tc + s * (theta[None, :] - tc)
        ph = pc + s * (phi[None, :] - pc)
        return embed(th, ph)

    def curve(frame):
        return embed(frame["theta_c"], frame["phi_c"])

    return {
        "key": "ring_torus",
        "name": "Ring torus",
        "caption": "compact, contractible champion attained",
        "metric": r"$g=r^{2}d\theta^{2}+(R+r\cos\theta)^{2}d\varphi^{2}$",
        "mesh": mesh, "region": region, "curve": curve, "frames": frames,
        "stages": STAGE_NAMES, "escape": False, "target": target,
        "az": 38.0, "el": 30.0,
        "facing": torus_facing(3.0),
        "result": result,
    }


# --------------------------------------------------------------- rendering ---


def draw_panel(ax, spec, index, *, show_name: bool) -> None:
    cam = camera(spec["az"], spec["el"], spec.get("roll", 0.0))
    view = cam[2]
    facing = spec["facing"]
    frame = spec["frames"][index]

    mesh = spec["mesh"]
    mx, my, _ = project(mesh.reshape(-1, 3), cam)
    mx = mx.reshape(mesh.shape[:2])
    my = my.reshape(mesh.shape[:2])
    mf = facing(mesh, view)

    ax.set_facecolor(BG)

    # --- wireframe, split into a back half and a front half -----------------
    segments, values = [], []
    step_a = max(1, mesh.shape[0] // 34)
    step_b = max(1, mesh.shape[1] // 44)
    for j in range(0, mesh.shape[1], step_b):
        seg, val = polyline_segments(mx[:, j], my[:, j], mf[:, j])
        segments.append(seg)
        values.append(val)
    for i in range(0, mesh.shape[0], step_a):
        seg, val = polyline_segments(mx[i, :], my[i, :], mf[i, :], close=True)
        segments.append(seg)
        values.append(val)
    segments = np.concatenate(segments, axis=0)
    t = facing_key(np.concatenate(values, axis=0))

    for mask, zorder in ((t < 0.5, 1), (t >= 0.5, 6)):
        if not np.any(mask):
            continue
        tt = t[mask]
        rgb = MESH_FAR[None, :] + (MESH_NEAR - MESH_FAR)[None, :] * tt[:, None] ** 1.25
        alpha = 0.045 + 0.52 * tt ** 1.9
        width = 0.28 + 0.80 * tt ** 2.1
        colors = np.concatenate([rgb, alpha[:, None]], axis=1)
        ax.add_collection(LineCollection(segments[mask], colors=colors,
                                         linewidths=width, zorder=zorder,
                                         capstyle="round"))

    # --- selected region, painted back to front -----------------------------
    patch = spec["region"](frame)
    px, py, pd = project(patch.reshape(-1, 3), cam)
    px = px.reshape(patch.shape[:2])
    py = py.reshape(patch.shape[:2])
    pd = pd.reshape(patch.shape[:2])
    pf = facing(patch, view)
    quads = np.stack([
        np.stack([px[:-1, :-1], py[:-1, :-1]], axis=-1),
        np.stack([px[1:, :-1], py[1:, :-1]], axis=-1),
        np.stack([px[1:, 1:], py[1:, 1:]], axis=-1),
        np.stack([px[:-1, 1:], py[:-1, 1:]], axis=-1),
    ], axis=-2).reshape(-1, 4, 2)
    qd = (0.25 * (pd[:-1, :-1] + pd[1:, :-1] + pd[1:, 1:] + pd[:-1, 1:])).ravel()
    qf = (0.25 * (pf[:-1, :-1] + pf[1:, :-1] + pf[1:, 1:] + pf[:-1, 1:])).ravel()
    order = np.argsort(qd)
    qt = facing_key(qf[order])
    face = np.concatenate([np.tile(FILL_RGB, (len(qt), 1)),
                           (0.030 + 0.165 * qt ** 1.5)[:, None]], axis=1)
    ax.add_collection(PolyCollection(quads[order], facecolors=face,
                                     edgecolors="none", zorder=4,
                                     antialiased=True))

    # A translucent fill vanishes where the selected set is a thin noncompact
    # tail (horn, cusp), so the region carries its own accent wireframe, drawn
    # above the surface mesh so the tail still reads as selected.
    rsegs, rvals = [], []
    step_ra = max(1, patch.shape[0] // 9)
    step_rb = max(1, patch.shape[1] // 30)
    for j in range(0, patch.shape[1], step_rb):
        seg, val = polyline_segments(px[:, j], py[:, j], pf[:, j])
        rsegs.append(seg)
        rvals.append(val)
    for i in range(0, patch.shape[0], step_ra):
        seg, val = polyline_segments(px[i, :], py[i, :], pf[i, :], close=True)
        rsegs.append(seg)
        rvals.append(val)
    rsegs = np.concatenate(rsegs, axis=0)
    rt = facing_key(np.concatenate(rvals, axis=0))
    rcol = np.concatenate([np.tile(FILL_RGB, (len(rt), 1)),
                           (0.07 + 0.42 * rt ** 1.6)[:, None]], axis=1)
    ax.add_collection(LineCollection(rsegs, colors=rcol,
                                     linewidths=0.35 + 0.60 * rt,
                                     zorder=6.5, capstyle="round"))

    # --- boundary curve, glow pass ------------------------------------------
    loop = spec["curve"](frame)
    cx, cy, _ = project(loop, cam)
    cf = facing(loop, view)
    csegs, cval = polyline_segments(cx, cy, cf, close=True)
    ct = facing_key(cval)
    for near, zorder in ((False, 5), (True, 9)):
        mask = (ct >= 0.5) if near else (ct < 0.5)
        if not np.any(mask):
            continue
        tt = ct[mask]
        rgb = np.tile(CURVE_RGB, (len(tt), 1))
        rgb = rgb + (1.0 - rgb) * (0.40 * tt[:, None] ** 2)
        for offset, (width, strength) in enumerate(
                ((11.0, 0.030), (7.0, 0.055), (4.2, 0.10), (2.3, 0.32), (1.25, 1.0))):
            alpha = strength * (0.14 + 0.86 * tt)
            colors = np.concatenate([rgb, alpha[:, None]], axis=1)
            ax.add_collection(LineCollection(csegs[mask], colors=colors,
                                             linewidths=width,
                                             zorder=zorder + offset * 0.1,
                                             capstyle="round"))

    # --- framing ------------------------------------------------------------
    span_x = float(mx.max() - mx.min())
    span_y = float(my.max() - my.min())
    pad = 0.07 * max(span_x, span_y)
    cx0 = 0.5 * float(mx.max() + mx.min())
    cy0 = 0.5 * float(my.max() + my.min())
    half = 0.5 * max(span_x, span_y) + pad
    ax.set_xlim(cx0 - half, cx0 + half)
    ax.set_ylim(cy0 - half * 1.02, cy0 + half * 1.02)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_color(PANEL_EDGE)
        side.set_linewidth(0.8)

    # --- typography ---------------------------------------------------------
    stage = spec["stages"][index]
    ax.text(0.045, 0.945, " ".join(stage), transform=ax.transAxes,
            color=TEXT_ACCENT if stage in ("OPTIMIZED", "ESCAPING") else TEXT,
            fontsize=8.5, fontweight="bold", va="top", ha="left")
    ax.text(0.045, 0.898, frame["note"], transform=ax.transAxes,
            color=TEXT_DIM, fontsize=7.0, va="top", ha="left")

    if show_name:
        ax.text(0.955, 0.945, spec["name"], transform=ax.transAxes,
                color=TEXT, fontsize=9.5, va="top", ha="right")
        ax.text(0.955, 0.898, spec["caption"], transform=ax.transAxes,
                color=TEXT_DIM, fontsize=7.0, va="top", ha="right",
                style="italic")

    block = "L = {:.6f}\nA = {:.6f}\nJ = {:.3e}".format(
        frame["L"], frame["A"], frame["J"])
    ax.text(0.045, 0.055, block, transform=ax.transAxes, color=TEXT,
            fontsize=7.4, family="DejaVu Sans Mono", va="bottom", ha="left",
            linespacing=1.55)
    ax.text(0.955, 0.055,
            "length constraint  L = {:g}".format(spec["target"]),
            transform=ax.transAxes, color=TEXT_DIM, fontsize=6.6,
            family="DejaVu Sans Mono", va="bottom", ha="right")


# ------------------------------------------------------------------- driver ---


def main(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    panels = outdir / "panels"
    panels.mkdir(exist_ok=True)

    builders = (build_horn, build_cigar, build_cusp, build_paraboloid,
                build_torus)
    specs = []
    for builder in builders:
        print("building {} ...".format(builder.__name__))
        specs.append(builder())

    summary = {}
    for spec in specs:
        summary[spec["key"]] = {
            "name": spec["name"],
            "target_length": spec["target"],
            "no_optimizer_by_design": spec["escape"],
            "optimizer_success": (None if "result" not in spec
                                  else bool(spec["result"].success)),
            "frames": [
                {"stage": spec["stages"][i], "note": f["note"],
                 "length": f["L"], "area": f["A"], "J": f["J"]}
                for i, f in enumerate(spec["frames"])
            ],
        }
        for index in range(3):
            fig, ax = plt.subplots(figsize=(6.4, 6.4), facecolor=BG)
            fig.subplots_adjust(0.0, 0.0, 1.0, 1.0)
            draw_panel(ax, spec, index, show_name=True)
            name = "{}_{}_{}.png".format(spec["key"], index + 1,
                                         spec["stages"][index].lower())
            fig.savefig(panels / name, dpi=300, facecolor=BG)
            plt.close(fig)
            print("  wrote panels/{}".format(name))

    fig, axes = plt.subplots(5, 3, figsize=(13.2, 22.6), facecolor=BG)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.947, bottom=0.022,
                        wspace=0.035, hspace=0.045)
    for row, spec in enumerate(specs):
        for col in range(3):
            draw_panel(axes[row][col], spec, col, show_name=False)
        axes[row][0].text(-0.055, 0.5, spec["name"].upper(),
                          transform=axes[row][0].transAxes, color=TEXT,
                          fontsize=11.5, fontweight="bold", rotation=90,
                          va="center", ha="center")
        axes[row][0].text(-0.019, 0.5, spec["caption"],
                          transform=axes[row][0].transAxes, color=TEXT_DIM,
                          fontsize=7.4, rotation=90, va="center", ha="center",
                          style="italic")
    fig.text(0.075, 0.975, "Dido relaxation on five exotic manifolds",
             color=TEXT, fontsize=19, ha="left", va="center")
    fig.text(0.075, 0.958,
             "selected region and its fixed-length boundary  ·  "
             "initial → intermediate → optimized",
             color=TEXT_DIM, fontsize=9.5, ha="left", va="center")
    fig.savefig(outdir / "dido_manifold_wireframes.png", dpi=200, facecolor=BG)
    plt.close(fig)
    print("wrote dido_manifold_wireframes.png")

    (outdir / "wireframe_frame_metrics.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print("wrote wireframe_frame_metrics.json")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("figures")
    raise SystemExit(main(target))
