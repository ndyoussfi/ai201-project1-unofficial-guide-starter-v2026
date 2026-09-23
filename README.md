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
(best distance 0.159, cutoff 0.62)

It costs $1.25 to dry your clothes in Morrow House, according to `housing_morrow_house_laundry.txt` and `housing_morrow_house.txt`.

Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_old_brewhouse_laundry.txt
```

**My relevance cutoff: 0.62**

My five questions resulted in distances between 0.1586 and 0.4180, and the five out of scope questions between 0.825 and 0.934.
There is no overlap, so any cutoff inside that 0.407 gap separates them. I put it at 0.62 because it's near the midpoint, which
leaves about 0.2 of room on each side.

| Question | In corpus? | Best distance |
|---|---|---|
| how much does it cost to dry your clothes in Morrow House | yes | 0.1586 |
| when should students start the CS 340 term project? | yes | 0.2383 |
| how many credits are required to graduate? | yes | 0.2914 |
| how many pages are students allowed to print for free on campus? | yes | 0.3205 |
| when can students declare their majors? | yes | 0.4180 |
| What is the capital of Mongolia? | no | 0.825 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| Who won the 1994 World Cup? | no | 0.886 |
| How do I write a for loop in Rust? | no | 0.896 |
| How do I change the oil in a diesel engine? | no | 0.934 |

## How I Used AI

**1.** I asked Claude to check my first test question, "what shows up on your record if you drop mid semester?", and it approved the question and suggested `expects: "week two"`. I pushed back, because "week two" is not an answer to that question, it is a circumstance, and an answer about adding a course would contain the same string. That disagreement is why I dropped the question entirely and picked a document where the answer and the `expects` string are the same thing.

**2.** Before I ran anything, I asked Claude to help me reason about why my gate criterion should be 4 of 5. It predicted that the ibuprofen and Rust questions would be the two most likely to slip through, because my corpus has a health centre document and several CS course documents. When I actually ran the five out of scope questions, all five were refused, and the Rust question came back at 0.896, the second furthest away of the five. I rewrote the reason around the distances I measured instead of the prediction, and tightened the target to 5 of 5.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

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
