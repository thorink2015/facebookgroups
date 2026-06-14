# Tank Mix Keyword Opt-In Mechanic v1

The play: Facebook kills posts that contain external links. So you don't put the link in the post. You ask people to comment a keyword, then you DM them the link. The comment boosts your reach. The DM is the conversion.

This file is the full system. Scripts, templates, workflow, edge cases.

---

## 1. Keyword-to-post mapping

Match the keyword to the topic so the reply feels natural, not robotic. Rotate so any one keyword doesn't get pattern-flagged by Facebook.

| Post topic | Keyword to use | Example post-end line |
|---|---|---|
| Rates / $/acre | RATES | "Drop RATES below and I'll send the breakdown" |
| Regulation / FAA / state | REG | "Comment REG and I'll send the plain-English version" |
| Equipment / gear | GEAR | "Comment GEAR for the full teardown" |
| DJI ban / China policy | DJI | "Comment DJI and I'll send the running tracker" |
| Job leads / open acres | ACRES | "Reply ACRES and I'll add you to the list" |
| General Tank Mix interest | TANK | "Comment TANK for the link" |
| Specific issue request | SEND | "Comment SEND and I'll get it to you" |
| Beginner / how-to | HOW | "Comment HOW and I'll send the starter guide" |
| Yes / soft commitment | YES | "Comment YES and I'll send it over" |

Rule of thumb: never use the same keyword twice in the same week. Rotate.

## 2. The public comment reply (what you write back in the thread)

This is what other people in the group see. Keep it warm, low-key, and short. Three variations to rotate:

**Variation A (most common):**
> Sent it your way [Name]. Anyone else who wants it, drop [KEYWORD] below.

**Variation B (when 5+ people have already commented):**
> Sending these out now. Bear with me, I do them by hand so it's not spam.

**Variation C (when someone asks a real question alongside the keyword):**
> Sent. The short answer is [one-line take]. Full breakdown is in the link I DM'd you.

Don't post the link in the public comment. Always DM. Two reasons: keeps Facebook's algorithm friendly, and gives you a direct line to the person for follow-up.

## 3. The DM template (the real conversion moment)

This is what they get privately. It's the only place the link appears. Make it good.

**Template:**

> Hey [Name], thanks for asking.
> 
> Here's the link to Tank Mix: tankmix.[domain]
> 
> Free weekly. Drops Thursdays. Covers the US ag drone spray industry the way you actually need to read about it. Rates, regs, gear, what's working in the field.
> 
> I'm Eugen. I run it. If you've got a question or a story I should cover, hit me back here anytime.

**Length matters:** 4 short paragraphs. Anything longer feels like a sales pitch and people bounce.

**Personalization:** Always use their first name (Facebook shows it). Pull one detail from their profile if obvious ("Saw you're in Iowa, big drone season there right now"), but don't fake it. If you can't add one real detail, skip it.

**Soft follow-up (24 hours later, only if they read it but didn't reply):**

> Just checking the link came through OK. What kind of operation are you running? Always curious what brings folks to ag drones.

That second message starts a real conversation. About 1 in 4 will reply. Those replies turn into the relationships that drive long-term subscribers, referrals, and eventually paid sponsorship leads.

## 4. The workflow (one solo operator, 15 minutes a day)

**Twice a day, 7 minutes each session:**

**Morning check (9 AM):**
1. Open Facebook notifications
2. Filter for "comments on your posts"
3. For each keyword comment from last 12 hours: send the DM (4 minutes)
4. Reply in the comment thread with Variation A (2 minutes)
5. Log in tracking sheet: date, group, keyword, name (1 minute)

**Evening check (8 PM):**
1. Same drill for comments since morning
2. Check DMs for replies to your DMs from yesterday
3. Reply to any real conversations (don't ignore, even short replies build the relationship)

**24-hour rule:** Every keyword comment must get a DM within 24 hours. Slower than that, you lose 40% of the conversion. People forget.

**48-hour follow-up:** Anyone who read the DM but didn't subscribe gets the soft follow-up message.

## 5. Automation options (when manual gets too slow)

You can run this all by hand up to about 30 keyword comments a day. Past that, automate. Three tools, ranked by fit:

**1. Meta's built-in keyword automation (free, but pages only):**
Facebook Pages have a built-in "Comment to message" feature. Set a keyword, automated DM, done. Catch: only works on Pages, not personal profiles. If you ever convert Tank Mix to a Page (you shouldn't yet, organic reach is worse), you get this.

**2. ManyChat (paid, ~$15/month):**
Works on personal profiles via the Messenger API. You set keyword triggers and DM templates. Auto-sends the link, then routes any reply to your inbox. The standard tool for this play. Best fit when volume crosses 20 keyword comments a day.

**3. Sprout Social or Zapier + Messenger (paid, more enterprise):**
Overkill until you're processing 100+ comments a day. Skip.

**Recommendation:** Run manual for 30 days. You'll learn what people actually ask, you'll spot which keywords are converting, and you'll catch the conversational replies that automation misses. Switch to ManyChat in month 2 if volume warrants.

## 6. Edge cases

**They comment the keyword but their DMs are off:**
Reply in the thread: "Couldn't DM you, your inbox is locked. Send me a quick hi here: [your email] and I'll get the link to you."

**They comment something rude or skeptical:**
Reply once, brief, no defensiveness: "Fair point. Tank Mix is free, no obligation. If it's useful, great. If not, no worries." Then drop it. Don't argue.

**Group admin removes your keyword post:**
Don't repost. Don't argue. Note that group in your tracking sheet as "link-hostile" and skip future posts there. Try a different angle next time (ISO post, peer question, photo story without a CTA).

**Facebook sends you a "you can't message non-friends" warning:**
You hit a rate limit. Slow down to 5 to 10 DMs an hour for a week. Volume comes back.

**Someone in the comments tries to "steal" the conversion (drops their own link):**
Ignore it. Don't engage. Send your DM to the original commenter and move on.

## 7. Tracking sheet (10 columns, Google Sheets, build today)

| Date | Group Name | Post Topic | Keyword | Commenter Name | DM Sent (Y/N) | DM Read (Y/N) | Subscribed (Y/N) | Replied to DM (Y/N) | Notes |

Fill it after every batch. After 30 days you'll see which post types and which keywords are pulling. Kill the bottom third.

## 8. Quick start (today, 20 minutes)

- [ ] Build the tracking sheet in Google Sheets (5 min)
- [ ] Save the DM template as a draft in Facebook Messenger so you can copy-paste fast (3 min)
- [ ] Save the 3 comment reply variations in a notes app on your phone (3 min)
- [ ] Test the full loop: post one of your 10 starter posts in ONE group with "Comment RATES below for the breakdown" at the end. Wait. When the first keyword comment comes in, run the full workflow. Time yourself. (rest of the time)

That's it. The mechanic is the difference between Facebook posts that just get likes and Facebook posts that grow your list.
