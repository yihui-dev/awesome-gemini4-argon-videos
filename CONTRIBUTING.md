# Contributing

Submit an original X post URL, creator credit, and any public prompt/source-code link. Do not invent prompts or attribute a repost to the reposting account as its creator.

For this collection, the original video post must be published strictly after 2026-10-13 16:00:00 UTC. Older prompts may be referenced if the new video's creator explicitly reused them. Older quoted media must not be imported as newly published video.

Verify the post timestamp against its X Snowflake ID; preserve the full original text and original-language prompt. Confirm Gemini 4 Argon attribution from the author or the author's thread. Exclude model comparisons, reviews, explainers, tutorials, production walkthroughs, and software feature presentations, even when short or popular. Finished animation, 3D scenes, and playable-game demonstrations are eligible. Deduplicate exact files and visual re-uploads, including cross-posts with different media IDs.

Screen candidates directly on X before downloading, considering finished-work quality, substantive comments, and visible engagement. Download only final selections, at most 50 per four-hour pass. New submissions must be at most 120 seconds; do not download a candidate merely to inspect its duration. Check the exclusion history to avoid re-adding removed entries.

Use content-hashed R2 object keys. Before publishing a catalog entry, verify the original file with ffprobe and a full decode, then confirm public HTTP status, byte count, SHA-256, and HTTP Range support. Keep credentials and downloaded videos out of Git.

Run `python3 scripts/build_readme.py` and `python3 scripts/validate.py` after updating the JSON catalog. The README and individual prompt pages are generated files.
