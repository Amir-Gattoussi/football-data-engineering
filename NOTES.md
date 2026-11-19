# Notes

This is a log file, representing the work I did after each session, with notes about decisions I took (variable names, field handling, ...). These are working notes -> Rough on purpose.

## Plan (skills only)
 
 
- [ ] **Loaders (PR 4 event details, PR 5 matches).** Manual loaders, hand-written, generally no libraries or automation to get into the nitty-gritty of how loading works. Tested on samples whilst creating tests at the same time.
- [ ] **kloppy and Parquet.** Compare kloppy's output with my loader. Write Parquet partitioned by competition and match before switching to files.
- [ ] **Coordinate normalisation.** One pitch system and attacking direction for `x`, `y`, `end_x`, `end_y`. 
- [ ] **DuckDB SQL, `MERGE` and idempotent loads.** Load the data into a database and play with idempotent loading.
- [ ] **Data checks in the pipeline.** Checking if I can plant a bad row and watch a check catch it.
- [ ] **Docker and GitHub Actions CI.** Containarizing the work.
- [ ] **Phase 2 (WIP):** dbt on DuckDB, an orchestrator, object storage, star-schema modelling, matching players across StatsBomb and Wyscout.
- [ ] **Phase 3 (WIP):** tracking data at scale, a simulated live stream with idempotent writes, optional PySpark.


## Data notes: StatsBomb events
 
Explored with match 8658 (2018 World Cup final, France 4, Croatia 2). The 2018 World Cup has 64 matches in `matches/43/3.json`.
 
- Nested objects follow one pattern: `{"id": ..., "name": ...}`. This applies to `type`, `team`, `player`, `recipient`, `height`, `body_part`, `outcome` and `technique`.
- In the matches file the prefix repeats inside the object: `home_team` contains `home_team_name`.
- Type-specific data lives in an object named after the event type (`pass`, `shot`). Those keys exist only on their own event types, so the loader must treat them as optional.
- `pass.end_location` is `[x, y]`. `shot.end_location` is `[x, y, z]`, where `z` is the height at which the ball reaches the goal.
- `shot.statsbomb_xg` is the chance quality as a probability.
- `shot.freeze_frame` is a list of 16 player positions at the moment of the shot. It is one-to-many data, so it needs its own table later, not a column.
- In `freeze_frame`, `teammate` is relative to the shooter. It is not a team flag. The goalkeeper of the defending side shows `teammate: False`.
- Some events have no player. Half start and end markers are examples. Reading `event["player"]["name"]` would crash on them.
- The first pass in the file has `pass.type` of `Kick Off`. For ordinary passes the `pass.type` key is usually absent.
- Source quirk: `"N''Golo Kanté"` has a doubled apostrophe. The loader leaves it as it is. This is the kind of mismatch that makes player matching across providers hard.
## Decisions
 
1. **Mandatory fields use `[...]`, optional fields use `.get(...)`.** A missing mandatory field means something is really wrong, and I want the crash. A missing optional field is normal and becomes `None`.
2. **Missing means `None`, never `0`.** A shot with xG of 0 and an event with no xG are different things.
3. **`end_x` and `end_y` come from passes only.** Shot end locations have three values and belong in their own change (with an `end_z` column).
4. **`freeze_frame` is left out of the flat record.** It becomes a separate table keyed by event ID.
5. **Source quirks are left as they are.** Cleaning belongs in a later, deliberate step, not in the loader.
6. **Test fixtures are hand-written, and new events are added at the end.** That way the record positions the existing tests use do not shift.
## Concepts, in my own words
 
- **Loader:** reads a provider's nested format and converts it to a flat, predictable schema I control. It is the ingestion step of a pipeline.
- **Code tests vs data checks:** code tests ask whether my loader behaves correctly on inputs I designed. Data checks ask whether today's real data is sane. I need both, and they catch different problems.
- **Fixtures guard the logic, real-data checks guard my assumptions.** For example, 64 matches in the World Cup file, and xG totals of roughly 1 to 3 per team in a final.
- **Idempotent:** running a step twice gives the same result as running it once.
## Session log
 
### PR 3: `chore/pre-commit-cleanup`
- Date:
- Changes: renamed the lint hook from `ruff` to `ruff-check` (the old name is a legacy alias), and replaced the placeholder README.
- Learned: what ruff does exactly (had a rough (no pun intended) idea before)
- Confused me: what the difference between `ruff` and `ruff-check` was.
### PR 4: `feature/event-details`
- Date:
- Changes: `end_x`, `end_y` and `xg` in the loader, two new fixture events (`evt-004` pass, `evt-005` shot), three new tests, count test now expects 5.
- Real-data check (xG total per team for match 8658):
- Learned:
- Confused me:
### PR 5: `feature/matches-loader`
- Date: 19/11
- Changes: created a matches loader for matches metadata 
- Real-data check (expect 64 matches, final is France 4, Croatia 2):
- Learned: In this example, we took the world cup matches, which is recent data, meaning all of the fields are always full. This may not be the case for older matches, which might be missing dates, kickoff times, referees, managers,...
- Confused me:.
## Open questions
 
- Shot end locations and `end_z`: add later as their own change?
- How should the `freeze_frame` table be keyed and partitioned?
- What does kloppy handle that my loader does not?