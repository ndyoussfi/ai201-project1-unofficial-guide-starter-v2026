# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

I picked 4 of 5 because 6 other halls have laundry documents identical to Morrow House's except for the price line, so the retrieval has to tell them apart on the hall name alone. If it picks the wrong hall, then the price will be wrong. The other four ask about facts stated in exactly one document, so they should pass.


---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

All my answers have named their file. Unlike retrieval, this is all or nothing, since an answer either has a reference or it doesn't. Allowing one mistake out of five would mean accepting an answer without a reference, which is the thing referencing exists to prevent.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in all 5 tries.

**Why this target:**
  
All five of my out of scope questions were refused, and the closest one still came back at 0.825 against a cutoff of 0.6. None of them were anywhere near slipping through, so I set the target at 5 of 5. A question my corpus has no documents about lands far enough away that the gate catching it is not in doubt.

---

## 4. No chunk is shorter than 150 characters

No chunk my pipeline produces is shorter than 150 characters

**Why this target:**

My shortest document is 178 characters and my longest is 549, so 150 sits below the shortest whole post in my corpus. Anything under 150 characters is a fragment of a post rather than a whole one, and since each fact in my documents is stated in a single sentence inside a short post, a fragment cannot have an answer in it. I set the floor to be below 183 to make sure that a document that is simply short doesn't count as a failure.

---

## 5. The source named is the source the answer comes from

For at least 4 of my 5 test questions, the file named in the answer is the file that actually contains the fact.

**Why this target:**

Criterion 2 only asks whether an answer names a source, and it passes whether the filename is right or wrong. I set 4 of 5 because Morrow House is the question I expect to miss, so if the retrieval is wrong the citation is wrong as well. 

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
