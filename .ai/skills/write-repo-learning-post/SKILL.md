---
name: write-repo-learning-post
description: Turn concrete, verifiable lessons found in a code repository (code, tests, config, docs, history) into a reviewable LinkedIn post draft. Picks one evidence-backed main lesson, decides whether the post continues, starts, or stays outside a series of learnings, and ends every post with the code repository link, then one specific involvement question, then 3–5 relevant hashtags. Use when asked to create, improve, or plan a LinkedIn post about what can be learned from a repo. Drafts only, never publishes.
---

# write-repo-learning-post

## Purpose

Produce `docs/linkedin-posts/<slug>-post.txt`: a LinkedIn post draft about **what can
be learned from this code**, plus the repository evidence behind it and the
questions the user must answer before posting.

The post teaches. It isn't a project announcement, a changelog, or a product
pitch. The repo is the source of the lesson, not the subject being promoted.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Repository | yes | Defaults to the current working directory |
| Focus | no | A topic, file, PR, commit range, or "surprise me" |
| Audience | no | e.g. SDETs, backend devs, engineering leads. If none is given, infer it from the repo's domain and mark it `ASSUMED`. |
| User's role and involvement | no | Needed only for first-person claims ("I built…", "we learned…") |
| Series history | no | Earlier post texts, a series title, or the last installment number |
| Existing draft | no | A post to improve instead of writing from scratch |
| Voice / length | no | Default: plain professional voice, 120–250 words |
| Slug | no | Derive a short kebab-case slug from the main lesson |

## Procedure

### 1. Inspect the repository (not only the README)

Read enough to understand what the code actually does and why:

- **Docs:** `README.md`, any `docs/`, `.ai/context/`, ADRs, contributor guides, agent/tool instruction files.
- **Code:** entry points, core abstractions, anything with an unusual shape (custom pools, listeners, retry logic, wrappers, generators).
- **Tests:** what gets tested, how test data is isolated, how flakiness is handled. Tests often show the real design intent.
- **Config and build:** build files, CI workflows, parallelism, environment and profile handling, quality gates.
- **History (when available):** `git log --oneline -n 50`, commit and PR titles, and the diffs of commits that look like decisions ("move…", "simplify…", "fix flaky…", "enable parallelism…"). `git log -S<term>` finds when something was introduced.

Record each candidate observation with its location (`path:line`, commit hash,
or PR number). Stop exploring once you have enough evidence for 2–4 candidate
lessons. You don't need to read everything.

### 2. Find concrete, supportable lessons

Good candidates, in order of preference:

1. An engineering **decision with a visible tradeoff**, e.g. locking a CSV row per test thread instead of sharing data, so parallel runs stay safe at the cost of a bounded pool.
2. A **debugging or reliability insight** visible in history, e.g. a fix commit and the test that now guards it.
3. A **pattern** that solves a recurring problem, and where it stops working.
4. A **surprising detail** that a practitioner wouldn't expect.

Reject generic advice ("write clean code", "tests matter") unless the repo
shows a specific, non-obvious way of doing it.

### 3. Ground every claim

Label each claim you plan to use:

| Label | Meaning | Allowed in the post as |
|---|---|---|
| `OBSERVED` | Directly visible in files or history | Plain statement |
| `INFERRED` | Reasonable reading of the evidence, not stated anywhere | Hedged ("likely", "the design suggests", "one reason is") |
| `USER` | Stated by the user in this conversation | Plain statement, including first person |
| `UNKNOWN` | Would require invention | Not allowed. Becomes a question for the user. |

Never invent implementation details, outcomes, metrics (speed-ups, flake rates,
hours saved), authorship, team size, dates, or personal experience. Commit
authorship doesn't tell you the user's role or feelings. If the natural voice
of the post is first person and the user hasn't confirmed their involvement,
either ask or write in an observational voice ("In this test framework, …").

### 4. Choose one main lesson

Pick the lesson with the strongest evidence and the widest relevance to the
audience. State it in one sentence before drafting. At most one or two
secondary points may appear, and only when they support the main lesson.
Anything else goes to "Other lessons found" for future posts.

### 5. Decide on series handling

Look for series evidence, in this order: user-supplied history, earlier drafts
in `docs/linkedin-posts/`, and series mentions in the repo (e.g. a "Learnings #3"
note in docs).

- **An existing series:** keep its exact title format, numbering, and structural habits (opening line, sign-off, recurring hashtag). Use the next number, and cite where you found the previous one.
  - **Recap bridge:** if the post refers back to the previous installment's learning, the same bridge must also state this post's learning, so a reader sees both in one place. Keep it to 1–2 short lines right after the hook, e.g. "Learning 2: run tests fully parallel within the backend's rate limits. Learning 3: lock each pooled resource to one test at a time, and release it even when the test fails." Take the previous learning from that post's text, not from memory. Never mention only the previous learning.
- **No series, but one adds value:** add value means the repo clearly holds several distinct lessons worth their own posts. Suggest a series title and a tentative label (e.g. "Lessons from a test automation repo, Part 1"). Mark it `SUGGESTED`. Never write "last time", "in my previous post", or anything else implying earlier installments exist.
- **A series would feel forced:** e.g. only one real lesson, or a one-off topic. Write a standalone post and say why.

### 6. Draft the post

Structure (adapt it, don't force it):

1. **Hook (1–2 lines):** a specific, accurate claim, tension, or question drawn from the lesson. No clickbait, no "You won't believe…", and no promises the post doesn't keep.
   - **Series recap (continued series only, optional):** the recap bridge from step 5, naming the previous learning and this post's learning together.
2. **Context (1–3 short paragraphs):** the problem the code faced, in plain terms. Keep code identifiers to a minimum and explain each one you use.
3. **The lesson:** what the code does, why it works, and the tradeoff.
4. **Why it matters:** to the stated audience, in their terms.
5. **Takeaways (optional):** 2–4 actionable points, and only ones the repo supports. A short list is fine. Don't pad it.
6. **Code repository link:** one line, placed just **before** the involvement question, e.g. `Code: https://github.com/<owner>/<repo>`. Take the URL from `git remote get-url origin` (convert an SSH remote to its `https://` form and drop a trailing `.git`). Never invent or guess a URL: if the repo has no remote, ask the user for the link.
7. **Involvement question:** exactly one question, tied to the main lesson. It should be easy to answer from experience ("How do you keep test data isolated when suites run in parallel: pools, per-test creation, or something else?"). Not "Thoughts?", "Agree?", or "Like if…".
8. **Hashtags:** placed **after** the question, on their own line, usually 3–5. Use specific topic and engineering tags (e.g. `#TestAutomation #Java #TestNG`). Avoid broad or unrelated tags (`#Motivation`, `#Success`, `#AI` when AI isn't the topic). Keep a series tag only if the series already uses one.

Style rules:

- Short paragraphs (1–3 lines) with white space between them. LinkedIn collapses posts after roughly 2–3 lines, so the hook has to work on its own.
- Natural, credible professional voice. Avoid "thought leadership" filler ("In today's fast-paced world", "game-changer", "Here's the thing", "Let that sink in").
- Don't pitch the repo. Mention it only through the repository link line before the closing question.
- Plain text only. LinkedIn doesn't render Markdown, so never use `**bold**`, `#` headings, backticks, or code blocks. Use the LinkedIn formatting below instead.

LinkedIn formatting (apply by default):

- **Hook first:** 1–3 very short lines, each on its own line, that make sense before "…see more" (about the first 200 characters).
- **Section headings:** split the body into short sections, each with a heading on its own line that starts with a marker emoji (`🔹` for sections, `✅` for takeaways) and is written in Unicode sans-serif bold (e.g. `🔹 𝗧𝗵𝗲 𝘀𝗲𝘁𝘂𝗽`). Bold the series label on the first line too (e.g. `𝗥𝗲𝘀𝘁 𝗔𝘀𝘀𝘂𝗿𝗲𝗱, 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴 𝟮`). Map A–Z to U+1D5D4…, a–z to U+1D5EE…, 0–9 to U+1D7EC….
- **Use Unicode bold only for headings and the series label.** Never use it in body text, code identifiers, or hashtags: screen readers may read it letter by letter or skip it, and LinkedIn search doesn't match those words.
- **Lists:** `→` for plain bullets, `1.` `2.` … for ordered steps (e.g. a lifecycle), and `⚠️` at the start of each tradeoff or risk line.
- **Spacing:** put a blank line between sections and after every heading. Keep lines to 1–2 sentences. In the saved file, each blank line is a single `⠀` so it survives pasting (see step 8).
- **Emoji:** use only these structural markers, plus an optional `👇` after the line introducing the sections and after the closing question. Don't add decorative emoji in sentences.
- **Closing:** put the repository link on its own line, then a blank line, then the question on its own lines (a short question line, then the options line if there is one), then a blank line, then the hashtags as normal text.

Example skeleton:

```text
𝗦𝗲𝗿𝗶𝗲𝘀 𝗹𝗮𝗯𝗲𝗹, 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴 𝗻

<hook line 1>
<hook line 2>

<optional recap: previous learning, then this post's learning>

<one-sentence framing> 👇

🔹 𝗦𝗲𝗰𝘁𝗶𝗼𝗻 𝗵𝗲𝗮𝗱𝗶𝗻𝗴

→ point
→ point

🔹 𝗧𝗵𝗲 𝘁𝗿𝗮𝗱𝗲𝗼𝗳𝗳𝘀

⚠️ tradeoff

✅ 𝗧𝗮𝗸𝗲𝗮𝘄𝗮𝘆𝘀

→ takeaway

Code: <repository URL>

<question>?
<options>? 👇

#Tag1 #Tag2 #Tag3
```

### 7. Refine and run the quality checks

Fix the draft until every check passes:

- [ ] The main lesson is about what was learned from the code, not about the project's existence or features.
- [ ] Every factual statement maps to an `OBSERVED`, `INFERRED` (hedged), or `USER` entry in the evidence table.
- [ ] There are no invented metrics, outcomes, authorship, or first-person experience.
- [ ] The hook is accurate, and the body delivers what it promises.
- [ ] There is one main lesson, and secondary points support it.
- [ ] The series label matches the evidence (continued / suggested / standalone), with no implied earlier posts that don't exist.
- [ ] Any mention of the previous installment's learning also states this post's learning in the same bridge.
- [ ] It ends with the code repository link (from the git remote, not invented), then exactly one specific involvement question, then 3–5 relevant hashtags on the line after it.
- [ ] Line breaks survive pasting: blank lines are single `⠀` lines, and there's no hard-wrapping mid-sentence.
- [ ] Paragraphs are short, the post has no Markdown, it follows the LinkedIn formatting above (Unicode-bold headings only, structural emoji only), and it has no filler phrases.
- [ ] Length fits the requested range (default 120–250 words; the step 8 length validation reports PASS: ≤ 2900 target, never over LinkedIn's 3000-character hard limit, counted in UTF-16 units with hashtags included).
- [ ] It contains no secrets, internal hostnames, tokens, customer data, or private details from config files.

### 8. Write the file and report

Write `docs/linkedin-posts/<slug>-post.txt`: a plain-text file containing
**only** the post exactly as it would be pasted into LinkedIn (series label if
any, body, repository link, closing question, hashtags). Rules:

- Plain text, no Markdown (no `#` headings, `**bold**`, backticks, code fences,
  or tables). Format it with the LinkedIn formatting from step 6.
- Aim for at most **2900 characters**, hashtags included. LinkedIn's hard
  limit is **3000**, and a post over it can't be published.
- No metadata, evidence, assumptions, or questions in the file.
- **Line breaks must survive pasting into a LinkedIn draft.** LinkedIn's
  editor drops empty lines on paste, which merges the sections together, and
  it keeps every line break in the file. So:
  - Every blank line holds exactly one `⠀` (U+2800 BRAILLE PATTERN BLANK) and
    nothing else. It shows as empty, and LinkedIn keeps it.
  - Use one blank line between blocks, never two or more in a row.
  - Don't hard-wrap sentences. Each paragraph, bullet, or heading is a single
    line in the file, however long, so the paste doesn't break lines mid-sentence.
  - Use LF line endings and no trailing spaces or tabs. Don't use tabs for
    indentation.

**Mandatory line-break and length validation.** Run this after every write or
edit of the file, and don't report the post as done until it prints PASS. It
first normalizes the line breaks in place (CRLF to LF, trailing whitespace
removed, runs of blank lines collapsed to one `⠀` line), then checks the length:

```bash
python3 - docs/linkedin-posts/<slug>-post.txt <<'EOF'
import sys
path = sys.argv[1]
BLANK = "\u2800"  # braille blank: keeps empty lines when pasted into LinkedIn
raw = open(path, encoding="utf-8").read().replace("\r\n", "\n").replace("\r", "\n")
lines = []
for line in raw.strip("\n").split("\n"):
    line = line.rstrip()
    if line.strip(BLANK + " \t") == "":
        if lines and lines[-1] != BLANK:
            lines.append(BLANK)
    else:
        lines.append(line)
while lines and lines[-1] == BLANK:
    lines.pop()
text = "\n".join(lines)
open(path, "w", encoding="utf-8", newline="\n").write(text + "\n")
units = len(text.encode("utf-16-le")) // 2  # how LinkedIn counts
print(f"{units} characters (LinkedIn count), {len(text)} code points, {lines.count(BLANK)} blank lines kept")
if "\t" in text:
    sys.exit("FAIL: tab characters found. Remove them.")
if units > 3000:
    sys.exit(f"FAIL: {units} > 3000, LinkedIn will reject this post. Shorten it.")
if units > 2900:
    sys.exit(f"FAIL: {units} > 2900 target. Trim it.")
print("PASS")
EOF
```

- Count LinkedIn characters, not `wc -m`. LinkedIn counts UTF-16 code units,
  so each Unicode-bold letter and many emoji (e.g. `🔹`, `✅`, `👇`) count as
  **2**. `wc -m` undercounts formatted posts. Each `⠀` blank line counts as 1.
- On FAIL, shorten the body first (cut secondary points or tighten
  sentences), then un-bold long headings if needed. Never cut the repository
  link, closing question, or hashtags. Rerun until PASS.
- Put the LinkedIn count from the script in the report (`Post file: … (<n>
  characters)`).

Report the evidence, assumptions, and open questions to the user in your
reply instead, using this layout:

```
Post file: docs/linkedin-posts/<slug>-post.txt (<n> characters)
Series: <"Title, Part n"> (CONTINUED / SUGGESTED) or STANDALONE: <reason>
Voice / audience: <voice> / <audience> (ASSUMED / USER)
Main lesson: <one sentence>
Evidence: E-1 <claim>, OBSERVED/INFERRED, `path/File.java:42`; ...
Assumptions: A-1 ...
Questions before posting: Q-1 ...
Other lessons found (future posts): ...
```

The post is a draft: never publish it, and never say or imply that it has been
posted.

## Result block

```
STATUS: DONE | NEEDS_INPUT
OUTPUT: docs/linkedin-posts/<slug>-post.txt
SUMMARY: main lesson "<…>"; series <continued/suggested/standalone>; <n> evidence items, <n> open questions
NEXT: user reviews the draft and answers open questions, then posts it manually, or "none"
```

Use `NEEDS_INPUT` only when an unanswered question would make the post
inaccurate (e.g. it depends on a first-person claim). Otherwise finish with
stated assumptions and list the questions.
