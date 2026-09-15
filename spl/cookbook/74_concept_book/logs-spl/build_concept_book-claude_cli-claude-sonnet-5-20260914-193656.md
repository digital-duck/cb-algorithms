# SPL Run: build_concept_book

- **Adapter:** claude_cli
- **Model:** claude-sonnet-5
- **Tokens:** 511 in / 578 out
- **Latency:** 11064ms
- **Timestamp:** 2026-09-14 19:36:56

## Output

```output


---

## Induction Proof

Mathematical induction is the standard method for proving that a statement holds for every natural number, and it maps almost perfectly onto how recursive algorithms work. A proof by induction has two parts. The **base case** verifies the statement for the smallest input (often $n=0$ or $n=1$). The **inductive step** assumes the statement is true for some value $n=k$ — this assumption is called the **induction hypothesis** — and uses it to prove the statement for $n=k+1$. Because the base case anchors the chain and the inductive step lets you climb from any rung to the next, the statement is proven true for all $n$ simultaneously.

In the context of recursive algorithms, this technique earns the informal nickname "the Recursion Fairy": when verifying a recursive function, you are allowed to *assume* that the recursive call on a smaller input already works correctly, exactly as the induction hypothesis assumes the statement holds at $k$. Your job is only to show that the current call, combined with that assumed-correct smaller result, produces the correct output.

**Worked example.** Consider computing $n!$ recursively: `factorial(n)` returns 1 if $n=0$, else returns `n * factorial(n-1)`. To prove correctness by induction: *base case*, `factorial(0) = 1 = 0!` by definition. *Inductive step*, assume `factorial(k)` correctly returns $k!$ (the induction hypothesis). Then `factorial(k+1)` computes `(k+1) * factorial(k)`, which by the hypothesis equals $(k+1) \cdot k! = (k+1)!$. Since both the base case and inductive step hold, `factorial(n)` is correct for all $n \geq 0$.

**Problem-solving application.** This pattern generalizes directly to verifying any recursive algorithm: identify the base case(s), state precisely what the recursive call is assumed to return correctly, and show that the current step combines that assumed result correctly. For example, to verify a recursive binary search, you assume the recursive call correctly searches the smaller subarray, then show that comparing the midpoint and recursing into the correct half preserves correctness. This same reasoning also justifies why recursive code that trusts its own smaller calls — rather than trying to "unfold" the whole recursion mentally — is both easier to write and easier to prove correct.
```
