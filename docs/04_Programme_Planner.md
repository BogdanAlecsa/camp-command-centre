# Programme Planner

The Programme Planner helps organise the timetable for a camp, sleepover or Nights Away event.

It should support both simple programmes and more complex camp structures with groups, rotations, activity leads and supporting adults.

---

## Current Status

The app now has a working early-MVP Programme module.

Current programme features include:

- programme sessions
- session dates
- start and end times
- session titles
- session types
- linked activities
- participant groups/teams
- locations
- lead person
- supporting staff
- notes
- rotation information
- programme warnings
- rotation summaries
- printable programme outputs

This is a strong baseline, but the workflow still needs polish.

---

## Programme Sessions

A Programme Session is a scheduled block of time.

Examples:

- breakfast
- flag break
- activity session
- wide game
- lunch
- campfire
- leader meeting
- free time
- setup
- pack down
- travel

Programme sessions can link to Activities, but they do not have to.

Some sessions are practical/admin sessions rather than activities.

---

## Session Information

A programme session may include:

- date
- start time
- end time
- title
- session type
- linked activity
- participant group
- location
- lead person
- supporting staff
- notes
- rotation group
- rotation slot number

The app should allow simple sessions to be added quickly, without requiring every field.

---

## Session Types

Useful programme session types include:

- Activity
- Meal
- Travel
- Setup / Pack Down
- Free Time
- Leader / Admin
- Whole Camp
- Group Rotation
- Other

Session type is useful for:

- visual colour-coding
- filtering
- print layout
- warnings
- later readiness checks

---

## Activities and Programme

Activities are reusable planning items.

Programme sessions are scheduled instances.

Example:

Activity:

Archery

Programme sessions:

- Saturday 10:00, Group A, Archery
- Saturday 11:00, Group B, Archery
- Saturday 12:00, Group C, Archery

This distinction matters because one activity may appear multiple times in the programme.

---

## Activity Leads

A programme session can have a lead person.

The linked activity may also have a default activity lead.

The app should make it easy to see who is responsible for each session.

Future improvements should warn when important sessions have no lead.

---

## Supporting Staff

A programme session can have supporting staff.

Supporting staff may include:

- supporting adult
- parent helper
- young leader
- first aider
- observer
- other role

This is separate from the main session lead.

The programme should eventually help identify staffing gaps.

---

## Participant Groups

Programme sessions may apply to:

- whole camp
- one section
- one team
- one activity group
- one patrol/six
- one duty group
- free choice participants

The current app links sessions to teams/groups.

Future improvements should make it easier to filter the programme by section or group.

---

## Rotations

Many camps use rotations.

Example:

- Group A does Fire Lighting
- Group B does Shelter Building
- Group C does Navigation

Then the groups rotate.

The app currently supports rotation information and rotation summaries.

Future rotation planner improvements should include:

- easier creation of rotation blocks
- automatic rotation schedule generation
- better clash checking
- clearer group schedules
- easier editing after generation

---

## Programme Warnings

The Programme module should warn about possible problems.

Current/future warning examples:

- session has no lead person
- activity has no risk assessment
- session has no location
- session has no participant group
- activity needs equipment notes
- overlapping sessions for the same group
- same leader assigned to overlapping sessions
- missing supporting adults

Warnings should help the organiser review the programme without blocking normal editing.

---

## Printable Programme Outputs

Current or near-term outputs include:

- full programme
- young person programme
- group schedule
- leader schedule
- activity leader schedule
- leader board

Different audiences need different programme views.

---

## Full Programme

The full programme should show the complete timetable.

It is useful for organisers and senior leaders.

It may include:

- time
- session title
- type
- location
- activity
- participant group
- lead
- supporting staff
- risk assessment status
- notes

---

## Young Person Programme

The young person programme should be simpler.

It should avoid operational clutter.

It may include:

- time
- activity/session name
- group
- location
- simple notes

It should not include unnecessary internal planning information.

---

## Leader Programme

The leader programme should include more operational detail.

It may include:

- session lead
- supporting staff
- locations
- risk assessment status
- setup notes
- activity notes
- equipment notes
- warnings

---

## Activity Leader Schedule

An activity leader schedule should show what each activity lead is responsible for.

It should help answer:

- What am I leading?
- When?
- Where?
- Which group?
- Who is supporting me?

---

## Leader Board

The leader board should show where adults and helpers are expected to be.

This is useful during the camp for operational awareness.

Future improvements may include:

- staff allocation by time
- gaps in adult cover
- leader clashes
- first aider location
- floating support roles

---

## Risk Assessment Link

Programme sessions should show risk assessment status where relevant.

If a programme session links to an activity, the app should be able to show whether the activity risk assessment is:

- Not Started
- Draft
- Ready for Review
- Submitted
- Approved
- Needs Update

This does not replace official Scouts approval processes.

It helps the organiser see what still needs review.

---

## Equipment Link

Programme sessions should eventually connect to equipment needs.

For now, activity equipment notes can be used.

Future equipment links may include:

- activity equipment list
- group equipment
- setup equipment
- consumables
- who is bringing what
- where equipment should be during the programme

This is deferred until the equipment module exists.

---

## Food and Transport Sessions

Meals, travel, setup and pack down can appear in the programme even before full Food or Transport modules exist.

This allows the programme to show the real shape of the camp.

Future Food and Transport modules can build on these session types later.

---

## Current Limitations

Current Programme module limitations:

- editing is form-based rather than drag/drop
- rotation creation still needs more workflow polish
- clash detection is limited
- group filtering needs improvement
- section filtering needs improvement
- staff allocation warnings need improvement
- visual timeline layout could be better

These are acceptable for the early MVP but should improve before heavy real-world use.

---

## Near-Term Priorities

Programme is not the immediate next priority.

The next build focus remains People, Sections and OSM import safety.

After that, useful Programme improvements would be:

1. Improve programme warning logic
2. Improve rotation planner workflow
3. Add better group/section filtering
4. Improve print layouts
5. Add clash detection
6. Improve staff allocation view

---

## Deferred Ideas

Future Programme ideas:

- drag/drop timetable editing
- duplicate day/session tools
- reusable programme templates
- automatic rotation generation
- visual timeline
- export to calendar
- programme version history
- parent-friendly programme output
- leader operational programme output
- live camp running mode

These should wait until the core MVP is stable.

---

## Summary

The Programme Planner is already one of the useful working parts of the MVP.

It can create structured programme sessions and printable outputs.

The next improvements should focus on making it easier to build, review and safely run the programme, but only after the People, Sections and OSM workflows are safer.