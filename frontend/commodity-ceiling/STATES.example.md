# STATES.md: Session quota card

Feature: a card on an account page showing how many coaching sessions a user has used this month and when the quota refreshes. Based on the Undertone example in Tim Gabe's "The Psychology of Premium Apps" (one pattern for both out-of-sessions screens: a "2 of 2 sessions used" badge, one sentence, the exact refresh date).

Rows = screens (one here). Columns = the nine states. Each cell = designed copy or behaviour, or "n/a" with a reason. Cells drafted by the coder, approved by the orchestrator.

| Screen | loading | empty | partial | success feedback | error | offline | permission denied | undo | next step |
|---|---|---|---|---|---|---|---|---|---|
| Quota card | Skeleton blocks in the final shape (badge, sentence, date, button); no text, no spinner (CSS shimmer, off under reduced motion) | Sentence "No plan yet. Pick one to start booking sessions."; button "See plans" | Badge "2 of 2 sessions used"; date line "Refresh date unavailable"; button "Retry" (reloads for 600 ms, then next step) | Sentence "Upgraded to 4 sessions a month. 2 of 4 used. Refreshes on 1 November 2026." (settled state, no undo control) | Sentence "Couldn't load your session count. Check your connection and try again."; badge "2 of 2 sessions used" kept as last known; button "Retry" (reloads for 600 ms, then next step); link "Contact support" | Line "You're offline. Showing the last saved count; it refreshes when you're back online."; last known badge "2 of 2 sessions used", sentence "You've used both sessions this month", date "Refreshes on 1 November 2026" (auto on the browser offline event, back to the previous state on online) | Sentence "Only the account owner can see session usage."; button "Ask the owner", which becomes the text "Request sent to the owner" (no network) | Success sentence as in success feedback plus button "Undo upgrade (10 s)" with a live countdown (10 s down to 1 s, then success feedback); press returns to next step; at 0 the button disappears and success feedback stays | Badge "2 of 2 sessions used"; sentence "You've used both sessions this month"; date "Refreshes on 1 November 2026"; primary button "Upgrade plan" (goes to undo); quiet link "Remind me on 1 November" (becomes the text "Reminder set for 1 November") |

Rules for every cell:
- Loading: a skeleton with the card's final shape, no spinner, no text.
- Empty: the user has no plan. Say so in one sentence and offer one action.
- Partial: the count is known but the refresh date failed to load. Show the count, say the date is unavailable, offer retry.
- Success feedback: after an upgrade, confirm in one sentence what changed (the new quota and the date).
- Error: the fetch failed. Say what happened, what to do, and how to reach support. Keep the last known count if any.
- Offline: say the data may be stale, show the last known values, say it will refresh when back online.
- Permission denied: a non-owner viewing a team account. Say who can see this and offer to ask the owner.
- Undo: after an upgrade, offer undo for a short window with a visible countdown.
- Next step: when all sessions are used, the badge reads "N of N sessions used", the sentence says "You've used both sessions this month", and the exact refresh date is shown with one CTA (Upgrade plan) and one quiet secondary action (Remind me on the refresh date).
