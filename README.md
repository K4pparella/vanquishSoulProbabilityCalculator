# A Monte Carlo Framework for Estimating Combo Accessibility in a Finite Card Deck

## Abstract

We present a probabilistic framework for estimating the accessibility of predefined card combinations (“combos”) from an initial hand drawn from a finite deck. The method combines deterministic logical conditions with stochastic estimation via Monte Carlo sampling. Conditional probabilities induced by card effects are approximated by frequentist estimators, and global success probabilities are aggregated under an explicit (approximate) independence assumption. We formalize the model using measure-theoretic probability and provide consistency results.

---

## 1. Introduction

Let a deck-based game be defined by a finite multiset of cards and a set of combo-defining rules. Given a random initial hand, we aim to estimate the probability that at least one combo is accessible, accounting for deterministic enabling effects and stochastic effects that reveal additional cards.

---

## 2. Probability Space

### 2.1 Deck and Card Space

Let the deck be a finite set:
$$
D = \{c_1, c_2, \dots, c_{40}\}.
$$

Each card is a tuple:
$$
c = (n, a, t, \ell, \alpha, \delta, \kappa),
$$
where:
- $n$ is the name,
- $a$ the attribute,
- $t$ the type,
- $\ell$ the level,
- $\alpha$ the attack,
- $\delta$ the defense,
- $\kappa \in \{\text{monster}, \text{st}\}$ the category.

---

### 2.2 Sample Space of Hands

Define the sample space:
$$
\Omega = \{ H \subseteq D : |H| = 5 \}.
$$

Equip $\Omega$ with the uniform probability measure:
$$
\mathbb{P}(H) = \frac{1}{\binom{40}{5}}.
$$

---

## 3. Random Variables and Events

For each combo $C \in \{R, M, H\}$ (Razen, Madlove, Holy Sue), define an indicator random variable:
$$
\mathbf{1}_C : \Omega \to \{0,1\},
$$
where $\mathbf{1}_C(H)=1$ iff combo $C$ is accessible from hand $H$.

---

## 4. Deterministic Base Events

### Definition 4.1 (Base Event)

Let $F(H)$ and $D(H)$ denote the number of Fire and Dark monsters in $H$, respectively.

- **Razen base event**
$$
R_{\text{base}} = \{H : \text{Razen}\in H \land (F(H)\ge2 \lor D(H)\ge1)\}.
$$

- **Madlove base event**
$$
M_{\text{base}} = \{H : \text{Madlove}\in H \land F(H)\ge1\}.
$$

- **Holy Sue base event**
$$
H_{\text{base}} = \{H : \text{Holy Sue}\in H \land F(H)\ge1 \land D(H)\ge1\}.
$$

Each base event is deterministic:
$$
\mathbb{P}(C \mid H) \in \{0,1\}.
$$

---

## 5. Deterministic Enabling Events

Let $D_H = D \setminus H$ denote the remaining deck.

### Definition 5.1 (AttrSS Enable)

For a target combo $C$:
$$
C_{\text{AttrSS}} = \{H : \text{AttrSS}\in H \land \exists\ \text{required attribute in } H \land \text{target}\in D_H\}.
$$

### Definition 5.2 (AddRazen Enable)

$$
R_{\text{Add}} = \{H : \text{AddRazen}\in H \land (F(H)\ge1 \lor D(H)\ge1) \land \text{Razen}\in D_H\}.
$$

### Definition 5.3 (MultiTutor Enable)

Define a binary relation:
$$
\operatorname{match}_1(c_i,c_j)=1
$$
iff $c_i$ and $c_j$ share exactly one attribute among $\{a,t,\ell,\alpha,\delta\}$.

The MultiTutor event for target $T$ is:
$$
\exists m\in H,\ d\in D_H,\ t\in T :
\operatorname{match}_1(m,d)=1 \land \operatorname{match}_1(d,t)=1.
$$

All enabling events above satisfy:
$$
\mathbb{P}(C \mid H)=1 \quad \text{if } H \in C_{\text{enable}}.
$$

---

## 6. Stochastic Effect: Excavate6

### 6.1 Conditional Probability Space

Given $H$, define the random variable:
$$
S \sim \text{Uniform}\{S \subset D_H : |S|=6\}.
$$

Define:
$$
X_C(H,S) =
\begin{cases}
1 & \exists c\in S : \text{adding } c \text{ enables } C, \\
0 & \text{otherwise}.
\end{cases}
$$

The true conditional probability is:
$$
p_C(H) = \mathbb{P}(X_C=1 \mid H).
$$

---

### 6.2 Monte Carlo Estimator

The program computes:
$$
\hat{p}_C(H) = \frac{1}{K}\sum_{i=1}^K X_C(H,S_i),
$$
where $S_1,\dots,S_K$ are i.i.d. samples and $K=40$.

---

### Proposition 6.1 (Consistency)

By the Strong Law of Large Numbers:
$$
\hat{p}_C(H) \xrightarrow[K\to\infty]{a.s.} p_C(H).
$$

---

## 7. Final Combo Probability

### Definition 7.1

For combo $C$:
$$
P(C\mid H) =
\begin{cases}
1 & H \in C_{\text{base}} \cup C_{\text{enable}}, \\
\hat{p}_C(H) & \text{otherwise}.
\end{cases}
$$

---

## 8. Aggregation of Combo Events

### Assumption 8.1 (Approximate Independence)

The model assumes:
$$
R \perp M \perp H.
$$

---

### Definition 8.2 (No-Combo Probability)

Let:
$$
p_R=P(R\mid H),\quad p_M=P(M\mid H),\quad p_H=P(H\mid H).
$$

Then:
$$
P(\text{none}\mid H)=(1-p_R)(1-p_M)(1-p_H).
$$

---

## 9. Global Monte Carlo Estimation

Let $H_1,\dots,H_N$ be i.i.d. samples from $\Omega$.

### Definition 9.1

The estimator for combo $C$ is:
$$
\hat{P}(C)=\frac{1}{N}\sum_{i=1}^N P(C\mid H_i).
$$

---

### Proposition 9.2 (Global Consistency)

As $N\to\infty$:
$$
\hat{P}(C)\xrightarrow{a.s.}\mathbb{E}[\mathbf{1}_C].
$$

---

## 10. Discussion

- The estimator is **consistent but biased** due to the independence assumption.
- Deterministic and stochastic components are cleanly separated.
- The framework is extensible to exact enumeration or dependency-aware models.

---

## Keywords

Monte Carlo simulation; conditional probability; finite probability space; card games; stochastic estimation.
