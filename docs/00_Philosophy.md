# Camp Command Centre Philosophy

Camp Command Centre exists because camp planning is often spread across spreadsheets, emails, paper forms, Word documents, WhatsApp messages, shared drives and people's memories.

That makes planning fragile.

Important information can be duplicated, forgotten, out of date, hidden in someone’s inbox, or only known by one person.

Camp Command Centre is intended to bring camp planning into one organised place.

---

## What This App Is

Camp Command Centre is a camp planning and operations tool.

It is designed to help Scout leaders plan, prepare, run and close camps, sleepovers and other Nights Away events.

It is not trying to be everything.

It is not a generic database.

It is not only a spreadsheet replacement.

It is not a general Scout membership system.

It is not a replacement for OSM.

It is not a replacement for official Scouts approval processes.

It is a focused tool for organising a specific camp.

---

## The Core Idea

The app should help leaders answer practical questions.

The most important one is:

Are we ready?

Everything in the app should eventually support that question.

---

## The Five Core Questions

Every feature should help answer at least one of these:

1. What are we doing?
2. Who is involved?
3. Who is responsible?
4. What have we forgotten?
5. Are we ready?

If a feature does not help answer one of these questions, it probably does not belong in the MVP.

---

## Camp-Centred Thinking

The main object in the system is a Camp.

Everything is organised around a camp.

Examples:

- people
- sections
- teams
- tasks
- activities
- programme
- risk assessments
- documents
- outputs
- future forms
- future communications
- future archives

The user should not feel like they are managing disconnected tables.

They should feel like they are building and checking one camp.

---

## Local-First

The MVP should stay local-first.

This keeps the project practical.

Local-first means:

- simple to run
- no hosting needed at the start
- no complicated login system yet
- fast to develop
- suitable for early testing
- easier to keep focused

Future online deployment may happen later.

It should not drive the MVP too early.

---

## Simple Before Powerful

The app should be useful before it is clever.

A simple workflow that works is better than a complicated one that is half-finished.

The current priority is not to add every possible module.

The current priority is to make the core workflow trustworthy.

Good early workflow:

- Create Camp
- Add/import People
- Organise Sections
- Create Teams
- Add Tasks
- Build Programme
- Add Risk Assessments
- Print Outputs

Large modules should wait until this core is stable.

---

## People Are Camp-Specific

People in the app are attached to a specific camp.

The app should not try to become a permanent young-person database.

For each camp, the app needs the people relevant to that camp.

This is especially important for:

- attendance
- contact information
- emergency contacts
- allergies
- medication
- medical notes
- dietary requirements
- task assignments
- teams/groups

Future templates must not copy personal data between camps.

---

## Candidate Roster Thinking

The People list should not only represent final attendees.

It should support a candidate roster.

People may be:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Unknown

This supports real planning.

Sometimes you know you will have about 20 Cubs before you know which 20 Cubs.

Sometimes you import a full OSM roster before attendance responses are final.

The app should support both ways of working.

---

## OSM Is a Source, Not the App

OSM is a useful source of information.

The app should be able to import from OSM where useful.

But Camp Command Centre should not try to become OSM.

Good use of OSM:

- import section members
- update camp attendance from an event export
- reduce manual typing
- improve accuracy

Bad use of OSM:

- trying to replace OSM
- becoming a full membership system
- blindly overwriting carefully entered camp data

The app should import carefully, preview changes, and protect existing manual data unless the organiser chooses otherwise.

---

## Safety and Trust

The app may contain sensitive information.

Examples:

- emergency contacts
- allergies
- medication
- medical notes
- dietary requirements
- future welfare or incident records

The app should be designed with care.

Important principles:

- do not expose sensitive data unnecessarily
- do not include personal data in templates
- do not blindly export sensitive data
- make archive/export choices explicit later
- keep sensitive archive fields off by default
- make destructive or bulk actions clear before applying them

Trust matters more than speed.

---

## Preview Before Bulk Change

Bulk actions can save a lot of time.

They can also create big mistakes quickly.

Any bulk import or bulk update should follow this rule:

Preview before apply.

This especially applies to:

- OSM member imports
- OSM attendance updates
- replacing provisional people
- bulk moving people between sections
- future archive/export tools

The user should always understand what will happen before applying a large change.

---

## Readiness Should Come From Real Data

The long-term readiness system should not become a separate manual checklist if the app already has the information.

For example:

If an attending young person has no emergency contact, the app should know that.

If an activity has no risk assessment, the app should know that.

If a task is blocked, the app should know that.

Readiness should be built from real camp data.

This is why the core data needs to be reliable first.

---

## Print and Output Matter

The app is not only for storing data.

It should produce useful outputs.

Examples:

- task sheets
- team work packs
- programme printouts
- risk assessment packs
- leader packs later
- parent packs later
- camp file later

Outputs should be practical and usable by real leaders.

A beautiful database that cannot produce useful camp documents is not enough.

---

## Do Not Replace Judgement

The app should support leaders.

It should not pretend to make decisions for them.

It can highlight missing information, warnings and possible problems.

It can help organise risk assessments.

It can help track readiness.

But leaders still need to use judgement, follow Scouts processes, and make final decisions.

---

## MVP Discipline

The MVP must stay disciplined.

Current priority:

- safer People workflow
- safer Section workflow
- safer OSM imports
- attendance summaries
- import review clarity
- bulk move recovery tools

Do not rush into:

- Food
- Transport
- Finance
- Full forms
- Communications
- Full compliance
- Online collaboration
- Archive/export system

Those modules matter, but not before the core is safe.

---

## Human-Centred Design

The app should be calm and practical.

The user is likely a busy volunteer preparing a real camp.

They may be tired, interrupted, short of time, or trying to fix something late at night.

The app should therefore be:

- clear
- forgiving
- hard to misuse
- plain-English
- predictable
- printable
- easy to recover from

Do not make users fight the software.

---

## Final Principle

The software should help organisers run better camps.

It should not simply store camp information.

It should reduce forgotten work, make responsibilities clearer, make outputs easier to produce, and help leaders feel more confident that the camp is ready.