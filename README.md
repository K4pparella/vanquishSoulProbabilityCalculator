# Monte Carlo Estimation of Combo Accessibility in a Finite Card Deck

![method](https://img.shields.io/badge/method-Monte%20Carlo-blue)
![probability](https://img.shields.io/badge/probability-frequentist-green)
![status](https://img.shields.io/badge/status-research--grade-orange)

---

## Table of Contents
1. [Abstract](#abstract)
2. [Probability Space](#probability-space)
3. [Random Variables and Events](#random-variables-and-events)
4. [Deterministic Base Events](#deterministic-base-events)
5. [Deterministic Enabling Effects](#deterministic-enabling-effects)
6. [Stochastic Effect: Excavate6](#stochastic-effect-excavate6)
7. [Final Combo Probability](#final-combo-probability)
8. [Aggregation and Independence Assumption](#aggregation-and-independence-assumption)
9. [Global Monte Carlo Estimator](#global-monte-carlo-estimator)
10. [Proof Sketches](#proof-sketches)
11. [Discussion and Limitations](#discussion-and-limitations)

---

## Abstract

This repository formalizes a Monte Carlo framework for estimating the probability that a predefined card combo is accessible from a random initial hand. The model combines deterministic logical conditions with stochastic card-reveal effects and approximates conditional probabilities via frequentist estimators. Consistency properties are discussed under explicit modeling assumptions.

---

## Probability Space

### Deck

Let the deck be a finite set of cards:

$$
D = \{c_1, c_2, \dots, c_{40}\}.
$$

Each card is represented as a tuple:

$$
c = (n, a, t, \ell, \alpha, \delta, \kappa),
$$

where `n` is the name, `a` the attribute, `t` the type, `ℓ` the level, `α` the attack, `δ` the defense, and `κ` the category.

---

### Hands

The sample space of opening hands is:

$$
\Omega = \{ H \subseteq D : |H| = 5 \}.
$$

We equip $\Omega$ with the uniform probability measure:

$$
\mathbb{P}(H) = \frac{1}{\binom{40}{5}}.
$$

Hands are sampled i.i.d.:

$$
H_1, \dots, H_N \sim \text{Uniform}(\Omega).
$$

---

## Random Variables and Events

For each combo $C \in \{R, M, H\}$ (Razen, Madlove, Holy Sue), define the indicator random variable:

$$
\mathbf{1}_C(H) =
\begin{cases}
1 & \text{if combo } C \text{ is accessible from } H, \\
0 & \text{otherwise}.
\end{cases}
$$

---

## Deterministic Base Events

Let $F(H)$ and $D(H)$ denote the number of Fire and Dark monsters in $H$.

### Razen

$$
R_{\text{base}} =
\{ H : \text{Razen} \in H \land (F(H)\ge2 \lor D(H)\ge1) \}.
$$

### Madlove

$$
M_{\text{base}} =
\{ H : \text{Madlove} \in H \land F(H)\ge1 \}.
$$

### Holy Sue

$$
H_{\text{base}} =
\{ H : \text{Holy Sue} \in H \land F(H)\ge1 \land D(H)\ge1 \}.
$$

These events are deterministic: once $H$ is fixed, their probability is either 0 or 1.

---

## Deterministic Enabling Effects

Let $D_H = D \setminus H$ be the remaining deck.

### AttrSS

For target combo $C$:

$$
C_{\text{AttrSS}} =
\{ H : \text{AttrSS} \in H \land
\exists \text{ required attribute in } H
\land \text{target} \in D_H \}.
$$

### AddRazen

$$
R_{\text{Add}} =
\{ H : \text{AddRazen} \in H \land
(F(H)\ge1 \lor D(H)\ge1)
\land \text{Razen} \in D_H \}.
$$

### MultiTutor

Define a binary relation:

$$
\mathrm{match}_1(c_i, c_j) = 1
$$

iff $c_i$ and $c_j$ share **exactly one** property among
$\{a,t,\ell,\alpha,\delta\}$.

The MultiTutor event for target $T$ is:

$$
\exists m\in H,\ d\in D_H,\ t\in T :
\mathrm{match}_1(m,d)=1
\land \mathrm{match}_1(d,t)=1.
$$

---

## Stochastic Effect: Excavate6

### Conditional Sampling

Given a hand $H$, define:

$$
S \sim \text{Uniform}\{ S \subset D_H : |S| = 6 \}.
$$

Define the Bernoulli random variable:

$$
X_C(H,S) =
\begin{cases}
1 & \exists c \in S : \text{adding } c \text{ enables } C, \\
0 & \text{otherwise}.
\end{cases}
$$

The true conditional probability is:

$$
p_C(H) = \mathbb{P}(X_C = 1 \mid H).
$$

---

### Monte Carlo Estimator

The program estimates $p_C(H)$ via:

$$
\hat{p}_C(H) =
\frac{1}{K} \sum_{i=1}^{K} X_C(H,S_i),
$$

with $K=40$ i.i.d. samples.

---

## Final Combo Probability

For combo $C$:

$$
P(C \mid H) =
\begin{cases}
1 & H \in C_{\text{base}} \cup C_{\text{enable}}, \\
\hat{p}_C(H) & \text{otherwise}.
\end{cases}
$$

---

## Aggregation and Independence Assumption

The model assumes approximate independence:

$$
R \perp M \perp H.
$$

Thus, the probability that **no combo** is accessible is:

$$
P(\text{none} \mid H) =
(1-p_R)(1-p_M)(1-p_H).
$$

---

## Global Monte Carlo Estimator

Let $H_1,\dots,H_N$ be sampled hands.

$$
\hat{P}(C) =
\frac{1}{N} \sum_{i=1}^{N} P(C \mid H_i).
$$

---

## Proof Sketches

### Proposition 1 — Consistency of Excavate6 Estimator

For fixed $H$:

$$
\hat{p}_C(H) \xrightarrow[K\to\infty]{a.s.} p_C(H).
$$

**Sketch.**  
Conditioned on $H$, the variables $X_C(H,S_i)$ are i.i.d. Bernoulli with
mean $p_C(H)$. The Strong Law of Large Numbers applies directly. ∎

---

### Proposition 2 — Consistency of Global Estimator

$$
\hat{P}(C) \xrightarrow[N\to\infty]{a.s.}
\mathbb{E}[\mathbf{1}_C].
$$

**Sketch.**  
$P(C\mid H)$ is bounded in $[0,1]$ and integrable. The estimator is an
empirical mean over i.i.d. samples, hence converges almost surely. ∎

---

### Proposition 3 — Bias from Independence Assumption

If $R,M,H$ are not independent:

$$
(1-p_R)(1-p_M)(1-p_H)
\neq \mathbb{P}(R^c \cap M^c \cap H^c).
$$

**Sketch.**  
The true joint probability expands via inclusion–exclusion. The product
formula implicitly drops all covariance terms, which are non-zero when
combos share cards or attributes. ∎

---

## Discussion and Limitations

- The estimator is **consistent but biased** with respect to the true game.
- Bias arises from:
  - independence assumption,
  - finite Excavate sampling,
  - logical simplifications.
- The framework is suitable for:
  - sensitivity analysis,
  - deck optimization,
  - extension to dependency-aware models.

---

## License

This document is provided for research and educational purposes.
