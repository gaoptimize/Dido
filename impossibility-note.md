# Dido: precise obstructions to a universal boundary-based solution

Working proof note, 11 October 2026. Pending independent mathematical review.

Typeset version: [dido_obstructions.pdf](dido_obstructions.pdf). This editable companion makes explicit the perturbation-class qualification in Section 2.1, documented in the [PDF review](https://github.com/gaoptimize/Dido/blob/main/audit/dido_obstructions_review.md).

This note develops the smooth-sphere construction already present in Section 8 of the repository's exotic-surface paper and in its argument-audit source. It makes the boundary-information obstruction explicit, supplies a direct nonlinear stability proof, and gives analytic descriptions of two failures of attainment.

Read alongside the [condition audit PDF](dido_audit.pdf) and the [publication review](https://github.com/gaoptimize/Dido/blob/main/audit/dido_audit_review.md).

The statements concern a specified admissible class of selected regions. Write
$$
P(D)=\operatorname{Length}(\partial D),\qquad
A(D)=\operatorname{Area}(D),\qquad
J(\partial D)=\int_{\partial D}(\partial_s\kappa_g)^2\,ds.
$$
For multiple components, sum the energy over components. A selected side is part of the state.

## 1. Main obstruction

**Theorem.** There is a smooth compact rotationally symmetric Riemannian sphere containing two selected embedded disks $D_1,D_2$ such that:

1. both boundaries have length $2\pi$;
2. selected-side-preserving neighborhoods of the boundaries are isometric;
3. both boundaries have constant geodesic curvature $1/2$, boundary Gaussian curvature zero, and $J=0$;
4. both disks are regular, strictly stable, strict local area maximizers at exact length, with the same local geometry;
5. $A(D_2)-A(D_1)=8\pi$.

Consequently boundary-local intrinsic geometry, even supplemented by selected disk topology and strict local stability, does not determine enclosed area or its global ranking. Minimizing $J$ does not universally select a Dido maximum.

The proof does not require either disk to be a global maximizer. The second disk is an admissible witness showing that the first is not global.

### 1.1 An explicit smooth metric

Define a smooth step
$$
H(t)=
\begin{cases}e^{-1/t},&t>0,\\0,&t\leq0,\end{cases}
\qquad
S(t)=\frac{H(t)}{H(t)+H(1-t)}.
$$
Thus $S=0$ for $t\leq0$, and $S=1$ for $t\geq1$. Set
$$
\chi(x)=S\!\left(\frac{1/4-x^2}{3/16}\right).
$$
The function $\chi$ is even, equals one for $|x|\leq1/4$, and vanishes for $|x|\geq1/2$.

On $0\leq r\leq9$, put
$$
\begin{aligned}
a(r)={}&1+S(2-4r)(r-1)
 +S(2-4(9-r))(8-r)\\
&+\tfrac12(r-2)\chi(r-2)
 +\tfrac12(r-6)\chi(r-6).
\end{aligned}
$$
Use the metric
$$
g=dr^2+a(r)^2d\theta^2,\qquad \theta\in\mathbb R/(2\pi\mathbb Z),
$$
collapsing the circles at $r=0$ and $r=9$ to poles.

Near those poles, $a(r)=r$ and $a(r)=9-r$, respectively, so the metric is smooth there. In the pole transition regions, $a$ is a convex combination of positive radii. On each interior bump, its correction has absolute value at most $1/4$; the supports are disjoint. Therefore $a>0$ on $(0,9)$. This defines a smooth compact Riemannian sphere.

"Rotationally symmetric" here is intrinsic; an isometric surface-of-revolution embedding in Euclidean three-space is not needed.

Let
$$
D_i=\{0\leq r\leq r_i\},\qquad r_1=2,\quad r_2=6.
$$
Both selected regions are disks and have the same topological type and oriented isotopy class.

### 1.2 Identical boundary neighborhoods

For $|t|\leq1/4$,
$$
a(r_i+t)=1+\tfrac12t.
$$
The map $(2+t,\theta)\mapsto(6+t,\theta)$ is therefore an isometry of the two boundary collars. It preserves the inward side $t<0$.

At each parallel,
$$
a=1,\quad a'=\tfrac12,\quad a''=0,
$$
and hence, with the cap-side curvature convention,
$$
P=2\pi a=2\pi,\quad
\kappa_g=\frac{a'}a=\tfrac12,\quad
K=-\frac{a''}a=0,\quad J=0.
$$
The length derivative under constant outward speed is $2\pi a'=\pi\neq0$, so the constraint is regular.

Collar isometry gives more than agreement of finitely many curvature invariants: the full metric germs and all intrinsic local variation formulas agree. In addition, Gauss–Bonnet gives the same integrated bulk curvature $\int_{D_i}K\,dA=\pi$, despite the different areas.

### 1.3 The exact area gap

The area element is $a(r)\,dr\,d\theta$. Between 2 and 6 the pole corrections vanish. The positive half of the odd bump at 2 cancels the negative half at 6:
$$
\begin{aligned}
\int_2^6a(r)\,dr
&=4+\tfrac12\int_0^{1/2}t\chi(t)\,dt
       +\tfrac12\int_{-1/2}^{0}t\chi(t)\,dt\\
&=4.
\end{aligned}
$$
Thus
$$
A(D_2)-A(D_1)=2\pi\int_2^6a(r)\,dr=8\pi.
$$

### 1.4 Strict nonlinear local maximality

A nearby boundary is a normal graph $r=r_i+u(\theta)$. Assume
$$
\|u\|_\infty\leq1/8,\qquad \|u'\|_\infty\leq1/8,
$$
so it stays in the linear collar. Its exact length and area difference are
$$
L(u)=\int_0^{2\pi}\sqrt{(1+u/2)^2+(u')^2}\,d\theta,
$$
$$
\Delta A(u)=A(D_u)-A(D_i)
=\int_0^{2\pi}\left(u+\tfrac14u^2\right)d\theta.
$$

Put $b=1+u/2$, $d=\sqrt{b^2+(u')^2}+b$, and $q=\int(u')^2d\theta$.
When $L(u)=2\pi$, rationalizing the square root yields
$$
\int u\,d\theta=-2\int\frac{(u')^2}{d}\,d\theta.
$$
The assumed bounds give
$$
\frac{15}{8}\leq d\leq\frac{17+\sqrt{293}}{16}.
$$
For $m=(2\pi)^{-1}\int u\,d\theta$, this implies
$$
|m|\leq\frac{8q}{15\pi}.
$$
Poincaré's inequality and $q\leq\pi/32$ then give
$$
\int u^2\,d\theta
\leq q+2\pi m^2
\leq\frac{229}{225}q.
$$
Consequently
$$
\Delta A(u)
\leq-\left(\frac{32}{17+\sqrt{293}}-\frac{229}{900}\right)q.
$$
The parenthesized constant is approximately $0.6834977>0$. If $q>0$, the area strictly decreases. If $q=0$, exact length forces $u=0$. This proves strict local maximality directly for the indicated graph neighborhood.

For smooth curves sufficiently close in $C^1$, the tubular projection gives such a graph after reparametrization. This specific witness therefore has a direct $C^1$ local-maximality proof; it does not enlarge the scope of the original paper's general $W^{3,2}$ theorem.

The Jacobi form on mean-zero variations is
$$
Q(u)=\int_0^{2\pi}\left((u')^2-\tfrac14u^2\right)d\theta,
$$
with nonconstant Fourier eigenvalues $n^2-1/4\geq3/4$. Thus both candidates are strictly stable and nondegenerate on the regular constraint slice.

## 2. Two precise consequences

### 2.1 No global deficit estimate from J alone

Let $\mathcal A$ be an admissible disk class containing both examples, and define
$$
A_{\sup}(2\pi)=\sup\{A(D):D\in\mathcal A,\ P(D)=2\pi\}.
$$
This supremum is finite because the ambient sphere is compact. It need not be attained. Nevertheless,
$$
A_{\sup}(2\pi)-A(D_1)\geq8\pi,\qquad J(\partial D_1)=0.
$$
Therefore no bound
$$
A_{\sup}(2\pi)-A(D)\leq\omega(J(\partial D))
$$
can hold throughout this class with $\omega(0)=0$. In particular, every finite-$C$, positive-$\alpha$ bound $CJ^\alpha$ fails on this one fixed smooth compact surface.

This failure persists at positive energies approaching zero, provided $\mathcal A$ contains the following sufficiently small exact-length perturbations of $D_1$ (as the class of all proper smooth selected disks does). Consider
$$
u_\varepsilon=\varepsilon\cos\theta+c(\varepsilon),
$$
where the implicit-function theorem, using $\partial_cL(0)=\pi$, enforces exact length. Expanding the displayed exact graph formulas gives
$$
c(\varepsilon)=-\tfrac12\varepsilon^2+O(\varepsilon^3),\qquad
A(D_{1,\varepsilon})=A(D_1)-\tfrac{3\pi}{4}\varepsilon^2+O(\varepsilon^3).
$$
The linearized curvature is $\delta\kappa_g=-u''-u/4$, so
$$
J(\partial D_{1,\varepsilon})
=\tfrac{9\pi}{16}\varepsilon^2+O(\varepsilon^3)>0
$$
for small nonzero $\varepsilon$. The global deficit remains at least $8\pi-o(1)$. Thus a modulus tending to zero at positive $J\downarrow0$ fails as well.

The original local estimate remains compatible with this: its area comparison is relative to the chosen local maximizer, rather than the global supremum.

### 2.2 No reconstruction or strict ranking from the boundary germ

Let $B(D)$ be the isometry class of a boundary neighborhood with its selected side marked. The construction has
$$
B(D_1)=B(D_2),\qquad A(D_1)\neq A(D_2).
$$
There is no function of $B(D)$ alone that reconstructs $A(D)$ for every such region. Nor can a scalar score depending only on this data strictly rank every pair by area: it must give these two candidates the same score.

Length, boundary curvature jets, boundary Gaussian curvature jets, intrinsic local boundary energies, topology, and the local stability spectrum are all insufficient for this pair. Knowing the total area of the ambient surface also does not distinguish these two candidates on the same surface.

A method using region position, interior metric data, or global area integration lies outside this restriction. The theorem excludes a specified information-limited class of methods, not general global analysis.

## 3. Exact perimeter can fail to attain a maximum even on the round sphere

Consider the unit round sphere and allow all proper smooth selected disk regions. Fix any $L_0>0$ and choose $0<\delta<1$. For large integers $n$, define a star-shaped polar boundary
$$
r(\theta)=\varepsilon(1+\delta\cos n\theta).
$$
Its length in $dr^2+\sin^2r\,d\theta^2$ is the continuous function
$$
\ell_n(\varepsilon)=\int_0^{2\pi}
\sqrt{\varepsilon^2\delta^2n^2\sin^2n\theta+
\sin^2(\varepsilon(1+\delta\cos n\theta))}\,d\theta.
$$
We have $\ell_n(0)=0$ and
$$
\ell_n(\varepsilon)\geq
\int_0^{2\pi}|r'(\theta)|\,d\theta=4\varepsilon\delta n.
$$
At $\bar\varepsilon_n=L_0/(2\delta n)$, this lower bound is $2L_0$. The intermediate-value theorem therefore supplies an exact-length root
$$
0<\varepsilon_n<\bar\varepsilon_n,\qquad
\ell_n(\varepsilon_n)=L_0.
$$
For sufficiently large $n$, these are smooth embedded positive-radius polar graphs bounding disks $E_n$. Their radii tend uniformly to zero, and
$$
A(E_n)\leq2\pi\left[1-\cos((1+\delta)\varepsilon_n)\right]\longrightarrow0.
$$
Their complementary selected disks have the same exact perimeter and areas tending to $4\pi$. Every proper smooth selected disk with nonempty boundary has area strictly below $4\pi$. Hence
$$
A_{\sup}(L_0)=4\pi
$$
is unattained in this class.

The degeneracy is in the admissible sequence, not in the ambient manifold. Additional restrictions, such as a prescribed area branch or a different admissible class, define a different problem. This example explains why compactness alone cannot justify exact-perimeter attainment.

## 4. Cigar: exact length, infinite area supremum, and J tending to zero

Hamilton's cigar has smooth complete polar metric
$$
g=d\rho^2+\tanh^2\rho\,d\theta^2.
$$
For $X>1$ and $0\leq a\leq1$, consider
$$
\rho(\theta)=X+a\cos\theta.
$$
Its length is
$$
\ell_X(a)=\int_0^{2\pi}
\sqrt{a^2\sin^2\theta+\tanh^2(X+a\cos\theta)}\,d\theta.
$$
At $a=0$, it is $2\pi\tanh X<2\pi$. Uniformly for $a\in[0,1]$, as $X\to\infty$,
$$
\ell_X(a)\longrightarrow
F(a)=\int_0^{2\pi}\sqrt{1+a^2\sin^2\theta}\,d\theta.
$$
Since $F(1)>2\pi$, an intermediate-value argument supplies $a_X\in(0,1)$ with $\ell_X(a_X)=2\pi$ for every sufficiently large $X$.

Also $a_X\to0$: any subsequence with a positive limiting amplitude would contradict $F(a)>2\pi$ for $a>0$ and the uniform limit.

The selected compact polar disks have area
$$
A_X=\int_0^{2\pi}\log\cosh(X+a_X\cos\theta)\,d\theta
\geq2\pi\log\cosh(X-1)\longrightarrow\infty.
$$
Thus the exact-length area supremum is infinite and there is no finite-area maximizing disk.

To check the energy conclusion analytically, set $f(\rho)=\tanh\rho$ and
$\sigma=\sqrt{f(\rho)^2+(\rho')^2}$. The signed curvature formula is
$$
\kappa_g=
\frac{f^2f'+2f'(\rho')^2-f\rho''}{\sigma^3}.
$$
Along this family, $f\to1$, all needed positive-order derivatives of $f$ tend uniformly to zero, and $\rho',\rho'',\rho'''\to0$ because $a_X\to0$. Therefore $\partial_\theta\kappa_g\to0$ uniformly and $\sigma\to1$. Hence
$$
J_X=\int_0^{2\pi}\frac{(\partial_\theta\kappa_g)^2}{\sigma}\,d\theta
\longrightarrow0.
$$
The paper gives the sharper asymptotic $J_X\sim8\pi e^{-2X}$; the argument here establishes the structural obstruction without depending on its fitted numerical recovery.

## 5. A finite-sampling obstruction applies to numerical methods too

**Lemma.** Suppose a metric is supplied only through exact point queries of its coefficients and any finite-order derivatives. No deterministic algorithm making finitely many such queries can recover the exact area of every prescribed smooth disk for every smooth metric. Without further quantitative restrictions, it cannot guarantee a fixed finite absolute error either.

**Proof.** Run the algorithm on a smooth metric $g_0$ and let $Q$ be its finite set of queried points. Choose a ball strictly inside the disk whose closure misses $Q$. Take a nonnegative, nonzero smooth bump $h$ supported in that ball, and define
$$
g_t=e^{2th}g_0.
$$
At every queried point, all metric derivatives agree with those of $g_0$, because $h$ vanishes in a neighborhood there. Adaptive queries therefore follow the same transcript and produce the same output.

In dimension two,
$$
A_{g_t}(D)=\int_D e^{2th}\,dA_{g_0}.
$$
This strictly increases and becomes arbitrarily large as $t\to\infty$, while the boundary metric and perimeter stay unchanged. Identical outputs cannot recover all these areas or satisfy a common finite absolute-error guarantee. $\square$

This lemma uses a specific oracle-input model. It does not cover algorithms supplied with a full symbolic metric, certified derivative bounds, or global integral queries. Its point is that finite numerical sampling has information requirements too.

## 6. Smooth degeneracy alone does not provide a power-law inverse

For the scalar smooth residual
$$
R(t)=
\begin{cases}e^{-1/t^2},&t\neq0,\\0,&t=0,\end{cases}
\qquad J(t)=R(t)^2,
$$
the zero set is $\{0\}$. For every $\alpha>0$,
$$
\frac{|t|}{J(t)^\alpha}
=|t|e^{2\alpha/t^2}\longrightarrow\infty.
$$
Thus no bound $|t|\leq C J(t)^\alpha$ holds near zero. Smoothness by itself does not replace the original nondegeneracy or analytic hypotheses.

This is an abstract residual example. A realization by an actual Dido curvature map, with the desired admissibility and length constraints, remains to be constructed before asserting the same geometric counterexample. It is a precise potential next research target, not a completed Dido theorem.

## 7. Status and the next statement to specify

The collar theorem, exact graph stability inequality, round-sphere sequence, cigar argument, and finite-query lemma have analytic proofs above. Numerical crosschecks support the formulas; they do not carry the proofs. No claim of novelty or proof-assistant verification is made.

The definite obstruction is that local boundary data do not contain the global information needed for area selection. A universal answer that must return a maximizing curve is also excluded by explicit nonattainment examples.

A theorem excluding all "nonnumerical techniques" would need a specified meaning of formula or algorithm, an input representation, and a required output. Variational profiles, exact quotient geometry, and analytic nonattainment arguments already account for several of the missing conditions. See [dido_audit.pdf](dido_audit.pdf) for the complete hypothesis list.

Sources:

- [Original paper](dido_merged_2026-09-08.pdf).
- [Exotic-surface paper](dido_relaxation_exotic_surfaces.pdf), especially Sections 7.4 and 8.
- Existing construction: `dido_argument_audit.py` in the [reproducibility archive](https://github.com/gaoptimize/Dido/blob/main/dido_exotic_surfaces_reproducibility.zip).
- [Argument audit output](https://github.com/gaoptimize/Dido/blob/main/audit/argument-audit.json); all 19 checks passed. This is a regression and dependency audit, not formal proof verification.
- [Additional numerical crosschecks](https://github.com/gaoptimize/Dido/blob/main/audit/additional-crosschecks.txt).
