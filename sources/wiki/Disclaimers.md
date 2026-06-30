**The wiki is no longer updated. The latest data is as of Jun 30, 2026.**

***

Here are some disclaimers on AI contributions to Erdős problems.

<a id="disclaimer-1"></a>
### 1. This page is not a benchmark

Erdős problems vary widely in difficulty, by several orders of magnitude, ranging from extremely difficult problems to low-hanging fruits. It is hard to tell in advance which category a given problem falls into. Moreover, a thorough literature review is not always available; see [disclaimer 2](#disclaimer-2). 

However, a problem only stated once in the literature with scant record of followup work may very well be of the second category. In particular, we advise against direct comparison of raw counts of problems solved by different methodologies, as this could be comparing apples to oranges.

<a id="disclaimer-2"></a>
### 2. Many problems on the site lack a thorough literature review

A designation of a problem as "open" is always provisional. It has happened many times that an AI system solved a problem listed as open, only to find that the problem was already solved in the literature; see [section 1(b)](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems#sect-1b). Note this does not automatically imply that the AI utilized the literature results to produce its solution.

On the other hand, AI systems, particularly deep research products, have been helpful in bridging the literature gap. These are recorded in [section 2(a)](https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems#sect-2a).

<a id="disclaimer-3"></a>
### 3. Keep selection bias in mind when drawing conclusions about success rates of AI systems

The reporting of AI contributions in this wiki is most likely incomplete, in particular with regards to negative results.

<a id="disclaimer-4"></a>
### 4. In some cases, Erdős himself or the problem site stated the problem incorrectly

In these cases, the problem as literally stated might be easily solvable, perhaps on a technicality, but this likely was not the actual question Erdős intended.

Working out what Erdős intended may require some expertise in the subject.

<a id="disclaimer-5"></a>
### 5. Absence of past progress may reflect obscurity rather than difficulty

If an Erdős problem was posed $N$ years ago and was recently solved by AI, it may be tempting to conclude: "the problem resisted all human attempts at solution for $N$ years" in order to imply the problem is difficult. Instead, it could be that the problem has received little attention from or is relatively unknown to mathematicians.

On the contrary, if there is literature expending effort on partial results without getting a clear path to a full solution, this is stronger evidence of the problem's difficulty.

<a id="disclaimer-6"></a>
### 6. Contributions should be evaluated holistically

Interest in a problem does not stem purely from their solution but also from insights that the work on the problem shed on related topics and the broader context of its field.

Connections to the rest of the subject are provided through remarks and comments as part of the writing process, including literature review. A solution primarily discovered by AI may lack this additional context. Thus, the final product may have less utility than usual even though it solves the problem.

<a id="disclaimer-7"></a>
### 7. A solution to an Erdős problem does not automatically qualify as publishable paper in a journal

This is especially so if the problem has no significant prior literature and the proofs are minor modifications of existing techniques.

However, it may be worth recording such a solution in literature. One way is to include the solution in a larger paper that makes other contributions.

<a id="disclaimer-8"></a>
### 8. We encourage formalizations of AI proofs in a formal language such as Lean

This increases confidence in the argument and can incentivize experts to invest time into examining the argument. But note there are still possible exploits here. See [this Lean guide](https://leanprover-community.github.io/did_you_prove_it.html) as a starting point.

Some common risks are: 1) introduction of unproved axioms; 2) misformalization of the problem statement. If the formal proof is suspiciously short/long or looks suspiciously trivial, there may be reason to look into it further.

<a id="disclaimer-9"></a>
### 9. This wiki is only a superficial reference and is not definitive verdict or assessment

The data in these tables is only a summary of some aspects of the AI contributions. The nature of each entry contains additional details.

For a fuller picture if desired, visit the linked page on the Erdős problem site.

<a id="disclaimer-10"></a>
### 10. The information provided on this wiki is provisional rather than final

The status of AI contributions is always subject to revision as new information comes in. This could be, for instance, discovery of relevant literature, error found in the argument, or change in problem formulation.

<a id="disclaimer-11"></a>
### 11. Problem solving is only one component of mathematical research

The Erdős problem site and this wiki are focused on problems of Erdős. Solving mathematical problems is an important component of mathematical research, which is relatively easy to quantify. As long as problems and arguments are unambiguous, one can check whether an argument solves a problem. Hence problem solving is an attractive goal for experimentation with AI systems as it provides objective improvement criteria.

Such focus on problem solving may give the impression that this is the *only*, or primary, activity that mathematicians value in research. This is not the case. The complementary activity of *theory building* - construction of frameworks that naturally encapsulate mathematical phenomena - is no less essential but harder to quantify. For further reading, we recommend Thurston's "[On proof and progress in mathematics](https://arxiv.org/abs/math/9404236)" and Timothy Gowers' "[The two cultures of mathematics](https://www.dpmms.cam.ac.uk/~wtg10/2cultures.pdf)".
