# Learn: Tutor

Learn: Tutor is a Grok bot that teaches the owner one item at a time from a Notion "To Learn" database. Learn: Scout keeps the database. A topic is finished when the owner says it is done and the transfer check and recap were solid.

This folder is the whole bot. It does not depend on the other folders in this repo, so it can move to another repo later. The socratic files it uses stay on main here. The skill fetches them by the URLs in `SKILL.md`.

## In this folder

- `PROFILE.md`: the profile to paste into the bot. It names the owner and points at the skill.
- `SKILL.md`: the `learn-tutor` skill. The workflow lives here.
- `ROUTINES.md`: the one routine, a daily poke. Reconstructed from the profile, not exported from the live routine.

## Recreate it

1. Create the bot and paste in `PROFILE.md`.
2. Install the skill from `SKILL.md`.
3. Add the routine in `ROUTINES.md`.
4. Connect Notion, so the bot can read and update the To Learn database.

## What cannot live in a repo

Memory, secrets, connector logins, and the Notion data itself. Those stay in the app and in Notion.
