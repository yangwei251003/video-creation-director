# Shared video resource library

The exact machine-readable catalog is generated from `source-libraries.json`, the earlier Adu/Vincent research inventories, `upstream-index.json`, `kenney-index.json`, and the original starter-pack index. It distinguishes source libraries, independent shots, child variants, demonstrations and individual assets.

```sh
python resources/build_starter.py
python resources/build_catalog.py
```

The first command rebuilds the original 27 HTML bundles only; do not run it on an edited user project. `saved.json` follows the reviewed OpenFilm v0.2.6 Saved bundle format. The pages expose deterministic `window.film.frame(t)` and `ready`; no wall-clock animation is needed for rendering. The optional time-only message handler supports the catalog preview player, including a locally opened catalog.

Generated previews and original pages are included under `docs/`. `resources/install_native.py` compares resource files and backs up differences in the chosen Saved root; it never deletes user content. Third-party raw media are not shipped here: follow each record's source, licence and acquisition method, or use existing locally verified files. The published catalog's local-file status describes the 2026-10-30 validation machine, not every reader's installation.

See [the director's acquisition and integration guide](../skill/references/resource-library.md) and [verification scope](../validation/director21/README.md). All original HTML/SVG pages and generators are MIT. Third-party records retain their individual rights; full upstream Skill/research video content is not redistributed.
