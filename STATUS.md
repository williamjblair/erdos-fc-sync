# Erdős ↔ Formal Conjectures sync status

*Regenerated 2026-06-26 by [`fc-sync-status.py`](fc-sync-status.py). Do not edit by hand.*

This is a **computed** view, not a hand-kept list. It joins three sources on the problem number so the status can't drift:

- [erdosproblems.com](https://www.erdosproblems.com) status ([`problems.yaml`](https://github.com/teorth/erdosproblems/blob/main/data/problems.yaml))
- Formal Conjectures' own [`conjectures.json`](https://google-deepmind.github.io/formal-conjectures/data/conjectures.json) (has-a-file + `formalProofLink`)
- [`plby/lean-proofs`](https://github.com/plby/lean-proofs/blob/main/data/sources.yaml) (hosted proof + `conditional`/`partial`)

It also folds in the live set of open FC pull requests, so it never points at in-flight work.

Reconciled **1217** problems.

| status | count | meaning |
|---|---:|---|
| `statement` | 80 | **Write the FC statement + link.** A complete hosted proof exists, FC has no file yet. The #3998 batch. |
| `link` | 4 | **Add the `formal_proof` link.** FC already has the statement; the hosted proof just isn't linked. |
| `docstring` | 18 | **Docstring note, not a `formal_proof` tag.** The hosted proof is conditional or partial. |
| `in-pr` | 27 | **Claimed.** An open FC pull request already touches this file. |
| `done` | 86 | Already linked in FC. |
| `no-proof` | 1002 | No hosted Lean proof to link (nothing to do here yet). |


## `statement` — 80 problem(s)

**Write the FC statement + link.** A complete hosted proof exists, FC has no file yet. The #3998 batch.

[24](https://www.erdosproblems.com/24) [31](https://www.erdosproblems.com/31) [34](https://www.erdosproblems.com/34) [45](https://www.erdosproblems.com/45) [46](https://www.erdosproblems.com/46) [47](https://www.erdosproblems.com/47) [93](https://www.erdosproblems.com/93) [94](https://www.erdosproblems.com/94) [115](https://www.erdosproblems.com/115) [150](https://www.erdosproblems.com/150) [164](https://www.erdosproblems.com/164) [199](https://www.erdosproblems.com/199) [202](https://www.erdosproblems.com/202) [206](https://www.erdosproblems.com/206) [214](https://www.erdosproblems.com/214) [224](https://www.erdosproblems.com/224) [226](https://www.erdosproblems.com/226) [246](https://www.erdosproblems.com/246) [280](https://www.erdosproblems.com/280) [281](https://www.erdosproblems.com/281) [296](https://www.erdosproblems.com/296) [314](https://www.erdosproblems.com/314) [315](https://www.erdosproblems.com/315) [333](https://www.erdosproblems.com/333) [337](https://www.erdosproblems.com/337) [363](https://www.erdosproblems.com/363) [369](https://www.erdosproblems.com/369) [401](https://www.erdosproblems.com/401) [419](https://www.erdosproblems.com/419) [426](https://www.erdosproblems.com/426) [429](https://www.erdosproblems.com/429) [435](https://www.erdosproblems.com/435) [443](https://www.erdosproblems.com/443) [453](https://www.erdosproblems.com/453) [476](https://www.erdosproblems.com/476) [481](https://www.erdosproblems.com/481) [484](https://www.erdosproblems.com/484) [487](https://www.erdosproblems.com/487) [497](https://www.erdosproblems.com/497) [498](https://www.erdosproblems.com/498) [502](https://www.erdosproblems.com/502) [519](https://www.erdosproblems.com/519) [537](https://www.erdosproblems.com/537) [540](https://www.erdosproblems.com/540) [582](https://www.erdosproblems.com/582) [618](https://www.erdosproblems.com/618) [621](https://www.erdosproblems.com/621) [639](https://www.erdosproblems.com/639) [646](https://www.erdosproblems.com/646) [648](https://www.erdosproblems.com/648) [649](https://www.erdosproblems.com/649) [666](https://www.erdosproblems.com/666) [674](https://www.erdosproblems.com/674) [692](https://www.erdosproblems.com/692) [698](https://www.erdosproblems.com/698) [751](https://www.erdosproblems.com/751) [753](https://www.erdosproblems.com/753) [756](https://www.erdosproblems.com/756) [760](https://www.erdosproblems.com/760) [762](https://www.erdosproblems.com/762) [775](https://www.erdosproblems.com/775) [785](https://www.erdosproblems.com/785) [798](https://www.erdosproblems.com/798) [818](https://www.erdosproblems.com/818) [844](https://www.erdosproblems.com/844) [862](https://www.erdosproblems.com/862) [867](https://www.erdosproblems.com/867) [898](https://www.erdosproblems.com/898) [905](https://www.erdosproblems.com/905) [907](https://www.erdosproblems.com/907) [914](https://www.erdosproblems.com/914) [947](https://www.erdosproblems.com/947) [958](https://www.erdosproblems.com/958) [966](https://www.erdosproblems.com/966) [967](https://www.erdosproblems.com/967) [974](https://www.erdosproblems.com/974) [990](https://www.erdosproblems.com/990) [1136](https://www.erdosproblems.com/1136) [1190](https://www.erdosproblems.com/1190) [1193](https://www.erdosproblems.com/1193)

## `link` — 4 problem(s)

**Add the `formal_proof` link.** FC already has the statement; the hosted proof just isn't linked.

[351](https://www.erdosproblems.com/351) [499](https://www.erdosproblems.com/499) [613](https://www.erdosproblems.com/613) [678](https://www.erdosproblems.com/678)

## `docstring` — 18 problem(s)

**Docstring note, not a `formal_proof` tag.** The hosted proof is conditional or partial.

[124](https://www.erdosproblems.com/124) [205](https://www.erdosproblems.com/205) [237](https://www.erdosproblems.com/237) [264](https://www.erdosproblems.com/264) [291](https://www.erdosproblems.com/291) [368](https://www.erdosproblems.com/368) [485](https://www.erdosproblems.com/485) [490](https://www.erdosproblems.com/490) [658](https://www.erdosproblems.com/658) [659](https://www.erdosproblems.com/659) [694](https://www.erdosproblems.com/694) [866](https://www.erdosproblems.com/866) [964](https://www.erdosproblems.com/964) [1056](https://www.erdosproblems.com/1056) [1095](https://www.erdosproblems.com/1095) [1148](https://www.erdosproblems.com/1148) [1187](https://www.erdosproblems.com/1187) [1197](https://www.erdosproblems.com/1197)
