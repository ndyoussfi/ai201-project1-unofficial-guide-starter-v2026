# The Unofficial Guide

Noureddine Youssfi - campus_life corpus

---

# Unit 1

## What This Does

This is a question answering system searching through campus_life, which includes 88 brief writings from students concerning their university, covering dorm buildings, dining hall lines, workloads in specific courses, and important registration deadlines. You simply ask a question, such as the price of laundry in one dorm, and the system finds the posts most relevant to your inquiry, lets you know what those posts have to say, and points you to the actual file from which the answer comes. If the closest chunk is further away than my 0.62 cutoff, the question is refused before it ever reaches the model, so the system says it does not have enough information instead of generating an answer based on general knowledge.

## Chunking Strategy

**Chunk size: 600** 
**Overlap: 0**

My documents are short posts containing between 178 and 549 characters. Each one contains a title and a few sentences on a single place or course. I set the chunk size to 600 so that every single post stays whole, and the overlap to 0 because I don't want to split anything. I considered splitting each of the posts where the paragraphs break since many of them cover more than a single topic. I decided against that for two reasons. First, the hall or course name appears only in the title line, so a laundry paragraph split off from housing_morrow_house.txt would not say "Morrow House" anywhere and it would be indistinguishable from the same paragraph in six of the other halls. Second, every piece would come out under 150 characters, which my fourth criterion rules out.

This costs me something. 23 of my 88 chunks are base documents covering 4 or 5 topics at once, like housing_aldridge_hall.txt, which packs the building, its location, a broken elevator, laundry prices and noise into 380 characters. Those chunks match every question about that hall a little and no question well, and I accepted that in exchange for keeping the hall name attached to every fact.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

**Question:** how much does it cost to dry your clothes in Morrow House?

**Answer:**

```
(best distance 0.232, cutoff 0.62)

It costs $1.25 to dry your clothes in Morrow House, according to `housing_morrow_house_laundry.txt` and `housing_morrow_house.txt`.

Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt
```

**My relevance cutoff: 0.62**

My five questions resulted in distances between 0.232 and 0.4180, and the five out of scope questions between 0.825 and 0.934.
There is no overlap, so any cutoff inside that 0.407 gap separates them. I put it at 0.62 because it's near the midpoint, which
leaves about 0.2 of room on each side.

| Question | In corpus? | Best distance |
|---|---|---|
| how much does it cost to dry your clothes in Morrow House? | yes | 0.2323 |
| when should students start the CS 340 term project? | yes | 0.2383 |
| how many credits are required to graduate? | yes | 0.2914 |
| how many pages are students allowed to print for free on campus? | yes | 0.3205 |
| when can students declare their majors? | yes | 0.4180 |
| What is the capital of Mongolia? | no | 0.825 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| Who won the 1994 World Cup? | no | 0.886 |
| How do I write a for loop in Rust? | no | 0.896 |
| How do I change the oil in a diesel engine? | no | 0.934 |

**Corrected in unit 2:** the Morrow House row originally read 0.1586, which was measured with `app.py retrieve` on the question without its question mark, while `questions.py` stores it with the question mark, so `run_eval.py` embedded a different string and returned 0.2323. Same file at rank 1 both times. The question mark alone moved the distance by 0.074.

## How I Used AI

**1.** I asked Claude to check my first test question, "what shows up on your record if you drop mid semester?", and it approved the question and suggested `expects: "week two"`. I pushed back, because "week two" is not an answer to that question, it is a circumstance, and an answer about adding a course would contain the same string. That disagreement is why I dropped the question entirely and picked a document where the answer and the `expects` string are the same thing.

**2.** Before I ran anything, I asked Claude to help me reason about why my gate criterion should be 4 of 5. It predicted that the ibuprofen and Rust questions would be the two most likely to slip through, because my corpus has a health centre document and several CS course documents. When I actually ran the five out of scope questions, all five were refused, and the Rust question came back at 0.896, the second furthest away of the five. I rewrote the reason around the distances I measured instead of the prediction, and tightened the target to 5 of 5.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. No chunk shorter than 150 characters | all chunks | 178 | 178 | 178 | MET |
| 5. Source named is the source the answer came from | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

### Real output

**Criteria 1 and 3** — produced by `run_eval.py::main` and `run_eval.py::check_out_of_scope`, scored by `scorer.py::judge`. Full file:
`results/run_2026-09-28_1824_before.md`.

```
how many pages are students allowed to print for free on campus?
  run 1: pass  (best distance 0.321)
  run 2: pass  (best distance 0.321)
  run 3: pass  (best distance 0.321)

when can students declare their majors?
  run 1: pass  (best distance 0.418)
  run 2: pass  (best distance 0.418)
  run 3: pass  (best distance 0.418)

how many credits are required to graduate?
  run 1: pass  (best distance 0.291)
  run 2: pass  (best distance 0.291)
  run 3: pass  (best distance 0.291)

when should students start the CS 340 term project?
  run 1: pass  (best distance 0.238)
  run 2: pass  (best distance 0.238)
  run 3: pass  (best distance 0.238)

how much does it cost to dry your clothes in Morrow House?
  run 1: pass  (best distance 0.232)
  run 2: pass  (best distance 0.232)
  run 3: pass  (best distance 0.232)

Out-of-scope questions (the gate should refuse these):
  refused  (best distance 0.825)  What is the capital of Mongolia?
  refused  (best distance 0.934)  How do I change the oil in a diesel engine?
  refused  (best distance 0.886)  Who won the 1994 World Cup?
  refused  (best distance 0.844)  What is the recommended dosage of ibuprofen for a headache?
  refused  (best distance 0.896)  How do I write a for loop in Rust?
  -> gate refused 5 of 5
```

**Criteria 2 and 5** — produced by `generate.py::answer_from_chunks`, citation checked by hand. From the `## Real output` section of the same file:

```
### how much does it cost to dry your clothes in Morrow House? — run 1

- Best distance: 0.2323 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt

It costs $1.25 to dry your clothes in Morrow House (sources: housing_morrow_house_laundry.txt and housing_morrow_house.txt).
```

Three of the five retrieved chunks were other halls' laundry documents, each with a different price. The answer names Morrow House's two files and both contain $1.25, so this counts for criterion 5 as well as criterion 2.

**Criterion 4** — produced by `chunker.py::describe`, via `python app.py index`. This one is not measured by `run_eval.py`.

```
chunked  88 chunks, 317 characters on average (shortest 178, longest 549), produced by chunker.py::split_documents
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | For at least 4 of my 5 test questions, the retrieved chunks include one that contains the answer. | MET | All 3 runs returned 5 of 5 against a target of only 4 of 5, scored by scorer.py::judge. The correct chunk came back first on every question, and the 3 runs are identical because the same question always retrieves the same chunks. |
| 2 | Every answer the system produces names at least one source document. | MET | All the answers from all 3 runs named a file, which I checked in the transcript. The wording changed in every run and the filename was always there. |
| 3 | When I ask a question my documents clearly don't cover, the relevance gate stops it and the system returns "I don't have enough information about that" — in all 5 tries. | MET | All 5 questions refused as measured by `run_eval.py::check_out_of_scope` against the cutoff, with Mongolia being the closest at 0.825, 0.205 above the cutoff. |
| 4 | No chunk my pipeline produces is shorter than 150 characters | MET | None of the chunks produced is shorter than 150 characters, with the shortest being 178, 28 above the floor as measured by chunker.py::describe via python app.py index. My chunker keeps every post whole, meaning the shortest chunk is the shortest document. |
| 5 | For at least 4 of my 5 test questions, the file named in the answer is the file that actually contains the fact. | MET | All the answers from all 3 runs cited the file that actually contains the fact. I checked each file and confirmed the fact is in it. 3 of 5 retrieved chunks for the Morrow House question were other halls' laundry files carrying $1.75 and $1.50 for the cost to dry. compared to $1.25 as expected, yet all 3 runs cited only Morrow House's files. |

## Diagnoses

None of my criteria missed, they all passed in all 3 runs. 3 of 5 could not have failed. 

Criterion 1 is deterministic. The same question always retrieves the same chunks, and the correct chunk came back first on all the questions. 

Criterion 3 has a room of 0.205 since the closest out of scope question came back at 0.825, with a 0.62 cutoff. But all of 5 out of scope questions are from unrelated topics, so testing them was really easy.

Criterion 4 was impossible to miss because my chunker keeps every post whole, so the shortest chunk is the shortest document. No run of the pipeline could produce shorter than 150 because the shortest is 178. 

Criteria 2 and 5 were the only 2 at risk. Both depend on the generated answer, which the model reworded between runs, and all 5 answers from all 3 runs passed. 

My prediction about which question would be hard was wrong. My reasoning for criterion 1 was that Morrow House would be the miss because 6 other halls have laundry documents identical to it except for the price line. Morrow House came back at 0.232, the best distance of my 5 questions, and the closest wrong hall at 0.4099. The hall name in the title line turned out to separate those documents better than I expected.

The criterion I believe I should tighten is criterion 4, not by changing the number, since raising it above 150 would not help, because the floor is not what makes it easy, but keeping every post whole is. A version that bites would name how many topics a chunk covers, since 23 of my 88 chunks cover 4 or 5 topics at once and match every question a little and no question well.

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
