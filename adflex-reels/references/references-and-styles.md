# References and motion styles

## Rules

- Reuse the **idea, structure and motion style**, never the story, characters, footage, music or logos.
- Links die, so the written breakdown is what matters.
- Before searching outside, check the existing reference lists, `motion-styles/` and past videos' `production.md`.

## Where to look

Start with the content repo's `references/<type>/README.md`: each has a "Where to search" table, a list of curated libraries with sizes and access notes, and the references already used. The short version:

| Type | Places | Search words |
|---|---|---|
| `ad` | Meta Ad Library (search advertisers of nearby AI tools, filter to active video ads; send the exact ad ID), TikTok Creative Center top ads, YouTube, sponsored Reels, competitor launch pages. Libraries: UGC Agent's winning UGC ads (ugcagent.app/ugc-ads/examples), AdSwipeFile (adswipefile.com), Swipekit, Starpop | AI ad generator, UGC AI, AI marketing agent, "one prompt" campaign, إعلان بالذكاء الاصطناعي |
| `social` | Instagram Reels from AI-video creators, YouTube Shorts, Reddit r/aivideo, X. Libraries: Graynote Virals (graynote.ai/virals, daily view counts), Jump on the Trend, Reveo, Comotion | AI grandma, AI comedy reel, anachronism, AI animal, Khaleeji AI reel |
| `hero` | AI product launch videos, product landing-page heroes, motion design galleries. Libraries: What Ships (whatships.com), Launchscene (launchscene.app), Refs (refs.video), Motion Index, Comotion | product launch video, feature launch, motion graphics promo, "now available" |

- What Ships, Launchscene, Refs and Comotion have MCP servers. They can be searched directly once connected; ask before adding one, some have paid tiers.
- Launchscene tags scenes by technique (kinetic type, UI zoom, split screen), which maps straight onto motion styles.
- Launch-video libraries help with ads too: their hook, demo and CTA scenes apply.
- General web research uses whatever search tool the session has. The content repo's `SETUP.md` lists the team's research setup.

What makes a reference good differs by type; see `video-types.md`.

## What works

- **Exact links:** an Instagram Reel, YouTube video or Short, or a direct `.mp4` can be imported and inspected with `import_web_video` for 0 credits.
- **Feeds don't:** Instagram and TikTok can't be scrolled, and the Meta Ad Library search page is unreliable without an exact ad ID. Ask the team for the link.
- **TikTok links can't be imported.** Ask for the downloaded file and upload it.

## Breaking down a reference

1. `import_web_video` with `purpose=inspect`.
2. `inspect_video`: shot-by-shot time, picture, camera move, cut, on-screen text.
3. `inspect_audio` only if the hook depends on voice or music.
4. Write it up: shot list, why it works, what we keep, what we change. Use the reference template in `templates.md`.
5. Add the row to `references/<type>/README.md` with the exact link or ad ID. If the team sent a file, say so, since there is no link to recover.

A good "what we took" line names structure, not story: "result first → 'I only explained the idea' → live prompt → numbered step cards → recap → creator on camera".

## Motion styles

A motion style is one reusable file describing camera, cuts, transitions, text/graphics animation, grade and sound cues.

| Type | Covers | Example |
|---|---|---|
| `camera` | How the camera moves and frames | handheld selfie, drone push-in, locked-off wide |
| `transition` | How one shot becomes the next | white bloom → color flood, whip pan, match cut |
| `edit` | Cut rhythm and pacing | 1.2 s hard cuts on the beat, multi-shot gag montage |
| `graphics` | Text, UI and card animation | typed prompt, numbered step cards, popping ad cards, PiP screens |
| `look` | Grade and texture | faded 1990s 35 mm film with grain, neon gradient |

Each style lists the video types it `fits` (`ad`, `social`, `hero`).

**Copy freely:** camera moves, shot lengths and rhythm, transitions, text animation, grade, sound-design cues.
**Never copy:** story, characters, footage, licensed music, logos.

To add one, use the motion-style template in `templates.md`, add it to the index, and link it from the videos that use it.
