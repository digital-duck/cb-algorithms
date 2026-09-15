# SPL Run: build_concept_book

- **Adapter:** claude_cli
- **Model:** claude-sonnet-5
- **Tokens:** 513 in / 586 out
- **Latency:** 11910ms
- **Timestamp:** 2026-09-14 19:39:39

## Output

```output


---

## Reduction

A **reduction** solves problem $A$ by transforming its input into an input for a different problem $B$, feeding that input to an existing algorithm for $B$, and converting $B$'s output back into a valid answer for $A$. The critical property is that the reduction's correctness never depends on *how* the algorithm for $B$ works internally — only on the guarantee that it returns a correct answer for $B$. This is what makes $B$'s algorithm a "black box": you could swap in a completely different implementation of it, and the reduction from $A$ to $B$ would still work.

**Worked example.** Suppose you have a reliable algorithm that finds the median of an unsorted list in linear time, and you want to solve a new problem: given a list of $n$ distinct integers, determine whether more than half of them are less than a given threshold $t$. You don't need to design a new algorithm. Instead, reduce the problem to median-finding: compute the median $m$ of the list using the black-box algorithm, then simply check whether $m < t$. If the median is less than $t$, then by definition at least half the elements are less than $m$, hence less than $t$ — so the count exceeds half. This reduction runs in the time the median algorithm takes, plus one comparison, and its correctness follows purely from the *definition* of a median, not from knowing whether the black box uses quickselect, a heap, or some other method.

**Problem-solving application.** Reductions are the primary tool for reusing solved work instead of reinventing it. When you face a new problem, ask: "Can I map this problem's input to the input format of a problem I already know how to solve, and map that solution back to an answer here?" This habit has two payoffs. First, it saves effort — you inherit the correctness and efficiency of the existing algorithm for free. Second, it reveals structural relationships between problems: if problem $A$ reduces to problem $B$, then $A$ is "no harder than" $B$, since any algorithm for $B$ automatically gives you one for $A$. This idea underlies how computer scientists classify problems by difficulty — for example, showing that a new problem reduces to a known hard problem is exactly how NP-hardness proofs work, though that formal use is a later, more advanced application of the same basic reasoning practiced here.
```
