# Douyin public video reader: independent bounded validation

Validated on 2026-10-28 against `skill/scripts/read_douyin.py`. Only that script was changed. No dependencies were installed, no new video was downloaded, no external service was called and no third-party screenshot/transcript was published by this validation.

## Result

- **20/20 offline contract tests pass** after the repair. Before the repair, 7 passed; 9 assertions failed and 4 cache/budget cases reached a deliberately blocked network fixture.
- **One real local OCR frame succeeds**, using the existing private xiaofeng sample and the already-installed RapidOCR models. The test disabled socket connections. It sampled only 12.0 seconds / frame 360, detected 32 text blocks, and verified matching text/confidence array lengths.
- The source video's SHA-256 was identical before and after. The output remained `type=sampled_frames`, `continuous_video_review=false`, with the sampling/OCR warning present.
- No full video viewing, listening, ASR transcript generation or OCR accuracy certification was performed. This test does not revalidate the live public feed or downloadable URLs; those were deliberately mocked.

Script SHA-256 at final validation: `bcf763ddd05fb5ab2936f94a13471432b86403fde67d55cfd2770c88b721d838`.

## Confirmed defects and repairs

| Boundary | Before | Final behavior / evidence |
|---|---|---|
| Exact ID extraction | Regex scanned the entire URL, accepting `/video/123` inside a query or the prefix of `/video/123abc` | Only a complete canonical `/video/ID`, `/note/ID` or `/share/video/ID` path yields an ID; query strings are separate |
| Share entry domains | All media/CDN hosts could also act as share-page inputs | Share entries and resolved share-page targets are restricted to douyin.com / iesdouyin.com and their subdomains; the existing platform CDN list remains for actual media |
| URL credentials | An empty username with a password passed the check | Any username/password field is rejected, including an empty username |
| Redirect defense | HTTPRedirectHandler already rejected foreign hosts; final response identity was not independently rechecked | Redirect handler control remains; request/media response domains and resolved share-page domains are also checked. Final-response fixture tests are defense-in-depth checks, not a claim of an observed live redirect escape |
| Cached media | Feed request ran before the local identity/hash check, so network failure prevented offline reuse/refusal | ID plus SHA-256 are verified first; valid cache reuses without a request, mismatch fails without modifying the existing bytes |
| Download budget | Invalid values were not validated before acquiring the feed | `acquire` rejects nonpositive, noninteger, nonfinite and boolean budgets before its network/cache work |
| Sampling limit | 120 uniform samples plus 120 added times could produce 240 samples | The merged, deduplicated selection is capped at 120 |
| Sample filenames | Times 1.0001 and 1.0002 both mapped to the same millisecond filename and overwrote one output | Files use an ordinal and six-decimal requested time; each recorded path is distinct |
| Evidence timing | Only requested seek time was recorded | Requested time remains, alongside decoder-reported time and frame index; callers must not infer an exact visual state only from a requested seek |
| Decoder cleanup | Validation/extraction exceptions could bypass release | VideoCapture is released in `finally`, including invalid-time failure |

The existing feed filter already compared the complete requested ID. Positive and negative controls confirmed that a recommended item or prefix ID cannot be substituted for the requested item.

## Evidence files and reproduction

- `test_read_douyin.py`: 20 offline fixtures for parser/domain/cache/budget/sampling behavior. Network access is replaced with explicit fixture functions.
- `results-before.json`: original outcomes, retained to show the observed defects.
- `results-after.json`: 20 passed, zero failures/errors.
- `run_local_ocr_check.py`: one-frame smoke test using the already-existing private sample and models, with socket connections blocked.
- `local-ocr-check.json`: content-free OCR structure summary, confidence range, hashes and 12 boolean checks, all true.

Run with the already-provisioned video-reader Python environment; do not install or download as part of this test:

```text
python -B validation/video-reader/test_read_douyin.py after
python -B validation/video-reader/run_local_ocr_check.py
```

The second command requires the private sample already present at `.research-sources/tutorials/xiaofeng/source.mp4`. It cannot be reproduced from a public source-only archive without separately supplying authorized local media.

## Private evidence boundary

The actual one-frame JPEG and its OCR text remain only in `private-ocr/`. The local `.gitignore` excludes that directory and generated fixture files. This workspace was not a Git repository at validation time, so `git check-ignore` could not verify future staging behavior; the publishing agent must still inspect the final archive/staging list. Do not publish the private frame, OCR text or full third-party media/transcript.

The confidence range was approximately 0.516–1.000. Those are recognition-model confidence values, not a verified accuracy percentage. No third-party recognized text is quoted in this report.
