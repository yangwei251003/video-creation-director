# OpenFilm 2.1 integration lab

30-second editable test project: three different NASA shot segments, Chinese DOM titles, Kenney CC0 sound cues and an original synthetic harmonic bed. This verifies integration; it is not an aesthetically approved universal template.

Use official OpenFilm Desktop 0.2.6. Keep its bundled CLI at the same version; do not run `npx latest` over an existing desktop project. Node/Bun/Docker are not needed for the normal installer. Connect an existing supported coding agent, explicitly allow the director skill, and preserve its existing account and permissions.

Prepare a private project folder with `assets/source/` containing:

- NASA `GSFC_20140211_LDCM_m11481_Orbit.mp4` (Landsat Orbit Swath), using its official media collection.
- NASA `ARC-20190801-AAV3211-OCSD-OrbitalManeuver-NASAWeb.mp4` (OCSD maneuver animation), using its official media collection.
- [Kenney Interface Sounds](https://kenney.nl/assets/interface-sounds), with its included CC0 license. The author's [OpenGameArt upload](https://opengameart.org/content/interface-sounds) is an alternate distribution source.

Follow [NASA media usage guidelines](https://www.nasa.gov/nasa-brand-center/images-and-media/), credit NASA/Goddard and NASA/Ames, do not imply endorsement, and verify third-party exceptions. Original video audio is muted. Raw NASA media is not redistributed in this repository.

```sh
python examples/openfilm-lab/build.py <project> --fonts examples/design-lab/public/fonts --kenney <extracted-kenney-pack> --ffmpeg <ffmpeg>
python skill/scripts/audio_mix.py <project>/audio-cues.json --out <project>/audio --ffmpeg <ffmpeg>
```

The builder initializes a test project and overwrites its own generated film/pages: run only in a new test folder before manual edits. Do not run it again over user modifications. Open that folder in OpenFilm. After opening, use the application's bundled `openfilm render` to produce a file when needed.

The two voices of interaction are intentional: manually edit the opening title, then ask the agent to change only the closing subtitle color. Verify the `film.html` override remains. Check linked move/trim/delete, undo/reopen/versions separately. Preserve source files and unused valid alternatives even if the upstream manual suggests deleting intermediates.

PCM stems are float32 to preserve headroom; the final mix uses a limiter and PCM24. Scheduled cue alignment is not a measured listening result. Do not mark full viewing/listening or the 90-point rubric passed without actual evidence.
