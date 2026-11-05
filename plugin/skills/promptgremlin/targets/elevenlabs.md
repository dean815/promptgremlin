---
family: elevenlabs
kind: tool
last_verified: 2026-10-01
sources: [tts, music]
---
## All models
- Decide first: speech (a script to be spoken) or music (a style description). They are separate prompts. Speech text is read aloud verbatim; music text is a brief, never a script, unless it contains lyrics. Voice, model id, and speed are settings, not text: speed is 0.7 to 1.2 (default 1.0). Output them on a separate settings line. (tts#Pace, music#How the Model Reads a Prompt)
- Syntax depends on the model. Square-bracket audio tags work on v4 and v3 only; `<break>` and phoneme tags are for the v2 and Flash models. Never mix them: use only the syntax of the chosen model. (tts#Pauses, #Prompting Eleven v4)
- Normalize before synthesis: write numbers, dates, currencies, units, abbreviations, URLs, and shortcuts the way they should be spoken. Where the format is ambiguous (day/month order, 24-hour time), choose one explicitly. (tts#Text normalization)
- Emotion comes from narrative context or explicit dialogue tags, which are more predictable than context alone. The model also speaks narrated cues aloud, so mention that those lines need trimming in editing. (tts#Emotion)
- Pace: narrative phrasing and punctuation (ellipses, dashes) shape rhythm; the speed setting changes overall rate. Extreme speeds hurt quality. (tts#Pace)
- Many `<break>` tags in one generation cause instability; use them sparingly where supported. Dashes and ellipses are a weaker alternative. (tts#Pauses)
- Multi-speaker scripts: one labelled line per speaker ("Speaker 1:") with a distinct voice assigned to each, on v4 and v3. (tts#Multi-speaker dialogue)
- Music prompt: settle genre, mood, instrumentation, tempo, and production era; any left open gets the most average answer. Add BPM and key, studio words for the sound (dry, close-miked, tape-saturated), and a description of the room when the vocabulary fails. (music#How the Model Reads a Prompt, #Production Vocabulary, #Musical Control)
- Music structure: narrate the arrangement in time order with words like "start with just", "then add"; say "instrumental only" for no vocals; give a length; time the vocals ("vocals begin at 0:15"); for stems prefix "solo" or "a cappella". For loops, state bars, BPM, key, and list what is excluded. (music#Arrangement, #Structural Timing & Lyrics, #Instrument & Vocal Isolation, #Loops)
- Detailed song-section control uses a composition plan, not a text prompt; that is an API structure, so flag it when the user needs exact sections. (music#Advanced: Composition plans)
- For complex sound effects, split the request into smaller sequential pieces and combine them afterward. (tts#Tips, #Layered outputs)

## eleven-v4
- Recommended default. Put delivery in brackets before the line ([whispers], [laughs], [sighs], [excited]); describe a voice quality ("low, gravelly") instead of a word that could read as a sound effect. (tts#Audio tags, #Prompting Eleven v4)
- Punctuation and capitals steer delivery: ellipses add weight, capitals add emphasis. (tts#Punctuation)
- Pronunciation: wrap the IPA in forward slashes inside double quotes, with stress marks, only on words that need it. (tts#IPA with Eleven v4)
- No `<break>`. Match each tag to what the chosen voice can plausibly do; test the important ones. (tts#Pauses, #Tips)

## eleven-v3
- Same bracketed audio tags, punctuation, and multi-speaker format as v4; no `<break>`. (tts#Prompting Eleven v3, #Pauses)
- Professional voice clones are not fully optimized here; if the user has one, say v4 is likely better. (tts#Prompting Eleven v3)

## eleven-flash-v2
- Audio tags are a v4/v3 feature; leave them out. Pause with `<break time="1.5s" />` (up to 3 seconds). (tts#Pauses, hand-written: no tags for v2)
- The only model the guide lists for phoneme tags: `<phoneme alphabet="cmu-arpabet" ph="...">word</phoneme>`, one tag per word, stress marked; CMU Arpabet is steadier than IPA. (tts#Phoneme tags for v2 models)

## eleven-multilingual-v2
- No phoneme tags (the guide names this model as lacking them). Audio tags are v4/v3 only. Pause with `<break>`; fix pronunciation by respelling or an alias in a pronunciation dictionary. (tts#Pauses, #Alias Tags, hand-written: no tags for v2)
- Reads currency and numbers more naturally than the small models, so less pre-normalizing is needed. (tts#Why do models read out inputs differently?)

## eleven-flash-v2-5
- Small and fast: it misreads big numbers and symbols, so normalize all of them in the text. (tts#Why do models read out inputs differently?)
- Audio tags are v4/v3 only. Phoneme tags are listed for eleven-flash-v2 only, so respell hard words. (tts#Phoneme tags for v2 models, #Alias Tags, hand-written: no tags for v2)
