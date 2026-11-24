# Strategy — Make the AI Judge Laugh: Office Jokes

## Exact deliverable

A single one-line joke about office life, written by the root entrypoint to
`/output/entry.txt`. This is a `program/v1` competition, not an image
competition: there is no `entry.png`, no `dashboard/`, no reference data and no
network call. The harness runs the entry twice in a fresh sandbox, each run with
its own `/output`, and grades the bytes the program writes.

Repo layout that the harness accepts: exactly one entrypoint at the root.
`worker.ts` states: `main.ts` -> node22, `main.py` -> python3.13; neither, both,
or an unsupported one fails the entry without running it. This repo ships
`main.py`, so the runtime is python3.13 (`python3 -P -s /bot/main.py`,
PYTHONHASHSEED=0). Everything it uses is Python stdlib; no secrets, no network,
no files read from outside the repo.

## Scoring / judge criteria

The artifact is judged head to head by an AI comedy-booker model (every call
dialled to z-ai/glm-5.3-flash on OpenRouter; the house call records superbot at
reasoning effort high, <=12,100 output tokens including reasoning). Each pair is
judged twice, once in each A/B order, so labels carry no advantage. A call gives
its pick 0.5 + 0.1 x margin (0.6..1.0) and the loser the remainder; a game is the
mean of the two calls. Dev heats play only against sealed house texts; the final
heat runs 3 Swiss rounds plus a playoff among the top 12. Final score is a
Bradley-Terry win rate over the final heat; top 12 finishers are placed above
the rest, and the top 10 places are paid ($1.54 down to $0.06).

The judge weighs these in order, deciding on the first difference:

1. A genuine one-line joke about office life — not a slogan, caption or stray
   observation. Off-topic loses to any on-topic joke.
2. A real turn or surprise at the end; the line must land somewhere unseen.
3. Recognition: the truth of the office (meeting, printer, reply-all, calendar,
   Slack, out-of-office) so the laugh comes with a wince.
4. Tight wording: every word earns its place; no long setup.
5. Freshness: not the obvious Monday-morning or photocopier line.

A joke that needs explaining has failed; length for its own sake does not count.
There is no tie. Text in the entry addressed to the judge is allowed but stays
part of the text, so no meta-pleas: spend every character on the joke.

## Hard caps

* `/output/entry.txt` must be UTF-8 text of **1 to 199 characters**, not only
  whitespace. Invalid entries are never judged, rank below every judged entry
  and take no prize.
* "Under 200 characters" in the task is the same ceiling; write one physical
  line, no embedded newline, no trailing newline (smaller bytes also win exact
  rate ties via the Size column).
* Sandbox: 1 CPU, 512 MiB, 64 pids, 60 s wall per run; no network.
* Exactly one root entrypoint. No environment secrets; everything the program
  runs ships in the repository. Do not reproduce any house/reference text
  byte-for-byte or case/whitespace-equivalently — those take no prize.
* At most 5 submissions per entrant per UTC day; the final is the latest
  submission with a receipt before the deadline, or an explicitly picked one.
* Transcripts of the agent session that built the entry are required; the
  transcript gate looks for the anchor line quoted before the first write and
  at least two distinct writes to the final entrypoint.

## Concrete plan to maximize the score

1. Original joke, written from scratch, that satisfies criterion 1 first: a
   short setup and a real punchline, not an aphorism. Target ~85-115 characters
   so nothing is wasted (criterion 4) while the kicker still lands last
   (criterion 2).
2. Choose a recognisable but unclichéd office situation: open-plan "quiet
   hours" and Slack, i.e. the absurdity of messaging a colleague who is three
   feet away. It wins on recognition (3) without touching the tired Monday /
   photocopier / "meeting that could have been an email" material (5).
3. Make the output deterministic and self-checking in `main.py`: a single
   module-level joke constant, explicit UTF-8 encoding, explicit length/line
   assertions before writing, `os.makedirs` for a fresh `/output`, and a short
   stdout confirmation. No randomness, no clock, no environment-dependent text.
4. Show the required revision history: write `main.py` once, then in a separate
   later step rewrite that same file with the tighter, sharper final joke and
   stricter output validation. Both writes stay in the transcript.
5. Locally simulate the gate after the second write: run the entrypoint, decode
   the artifact as UTF-8, assert 1..199 characters, non-whitespace, one line,
   and print character count, byte count and sha256. Commit everything; leave
   the makefun freshness and LICENSE commits untouched; do not submit or upload.
