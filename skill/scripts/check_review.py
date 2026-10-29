"""Validate review evidence records; this does not judge aesthetics or prove viewing."""
import argparse
import json
import math
import hashlib
from pathlib import Path

WEIGHTS = {'narrative': 20, 'pacing': 15, 'typography': 15, 'motion': 15, 'audio': 15, 'technical': 10, 'style': 10}
REQUIRED_GATES = ('brief', 'facts', 'rights', 'legibility', 'media_integrity', 'deliverables', 'visual_uniqueness')


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def valid_range(span, duration):
    return isinstance(span, list) and len(span) == 2 and all(number(v) for v in span) and 0 <= span[0] <= span[1] <= duration + 0.05


def full_coverage(spans, duration):
    end = 0.0
    for start, stop in sorted(spans):
        if stop <= start or start > end + 0.000001:
            return False
        end = max(end, stop)
    return end >= duration - 0.000001


def evaluate(review, base):
    errors, incomplete, failures = [], [], []
    if not isinstance(review, dict):
        return {'status': 'INVALID', 'total': None, 'errors': ['review must be an object']}
    duration = review.get('duration_seconds')
    if not number(duration) or duration <= 0:
        return {'status': 'INVALID', 'total': None, 'errors': ['positive duration_seconds required']}
    coverage = review.get('coverage', {})
    for key in ('coverage', 'gates', 'dimensions', 'scope'):
        if not isinstance(review.get(key), dict):
            errors.append(key + ' must be an object')
    for key in ('references', 'issues'):
        if not isinstance(review.get(key, []), list):
            errors.append(key + ' must be an array')
    if errors:
        return {'status': 'INVALID', 'total': None, 'errors': errors}
    for key in ('continuous_video_full', 'listened_full'):
        if key in coverage and not isinstance(coverage[key], bool):
            errors.append(key + ' must be boolean')
    scope = review['scope']
    if scope.get('kind') != 'full_film' or not valid_range(scope.get('time_range'), duration) or scope.get('time_range') != [0, duration]:
        incomplete.append('full-film scope; previews cannot receive a full-film total')
    for gate in REQUIRED_GATES:
        record = review.get('gates', {}).get(gate, {})
        if not isinstance(record, dict):
            errors.append('gate must be an object: ' + gate)
            continue
        if record.get('status') == 'fail':
            failures.append('gate:' + gate)
        elif record.get('status') != 'pass':
            incomplete.append('gate:' + gate)
        elif not nonempty(record.get('reason')):
            errors.append('gate reason missing: ' + gate)
    audio_required = review.get('audio_required')
    visual = review.get('gates', {}).get('visual_uniqueness', {})
    if isinstance(visual, dict) and visual.get('status') == 'pass':
        try:
            report = json.loads((base/visual['report']).read_text(encoding='utf-8-sig'))
            if report.get('status') != 'PASS_RECORD_ONLY' or len(report.get('inputs', [])) < 2 or report.get('timeline_audited') is not True:
                incomplete.append('visual uniqueness report not passed/bound to inputs')
            for item in report.get('inputs', []):
                if hashlib.sha256((base/item['file']).read_bytes()).hexdigest() != item['sha256']:
                    incomplete.append('visual uniqueness report stale')
        except (OSError, KeyError, TypeError, ValueError):
            incomplete.append('valid visual uniqueness report required')
    if not isinstance(audio_required, bool):
        errors.append('audio_required must be explicit boolean')
    if audio_required is False and review.get('audio_intent') not in ('user_requested_silence', 'silent_design_authorized'):
        incomplete.append('explicit silent intent')
    refs = review.get('references', [])
    if not refs or any(not isinstance(x, dict) or not all(nonempty(x.get(k)) for k in ('source', 'observed_scope', 'comparison')) for x in refs):
        incomplete.append('observed reference comparison')
    for ref in refs:
        methods = ref.get('observed_methods') if isinstance(ref, dict) else None
        if not isinstance(methods, list) or not all(m in ('page', 'source', 'frame', 'continuous_video', 'listened_audio', 'render') for m in methods) or not any(m in ('frame', 'continuous_video') for m in methods):
            incomplete.append('visual reference observation')
    total, denominator = 0.0, 0
    for key, weight in WEIGHTS.items():
        dim = review.get('dimensions', {}).get(key, {})
        if not isinstance(dim, dict):
            errors.append('dimension must be an object: ' + key)
            continue
        status = dim.get('status')
        if status == 'not_applicable':
            if key != 'audio' or audio_required is not False or not nonempty(dim.get('reason')):
                errors.append('invalid N/A: ' + key)
            continue
        denominator += weight
        if status != 'reviewed':
            incomplete.append(key)
            continue
        score = dim.get('score')
        if not number(score) or not 0 <= score <= 5:
            errors.append('invalid score: ' + key)
            continue
        if not nonempty(dim.get('reason')):
            errors.append('reason missing: ' + key)
        observations = dim.get('evidence', [])
        if not isinstance(observations, list):
            errors.append('evidence must be array: ' + key)
            continue
        if not observations:
            incomplete.append('evidence:' + key)
        spans = []
        kinds = []
        needed_kind = 'continuous_video' if key in ('pacing', 'motion') else 'listened_audio' if key == 'audio' else None
        for ev in observations:
            if not isinstance(ev, dict):
                errors.append('evidence must be object: ' + key)
                continue
            path = ev.get('file')
            if not isinstance(path, str) or not (base / path).is_file():
                errors.append('evidence file missing: ' + key)
            span = ev.get('time_range')
            if not valid_range(span, duration):
                errors.append('invalid time range: ' + key)
            elif needed_kind and ev.get('kind') == needed_kind:
                spans.append(span)
            if ev.get('kind') not in ('frame', 'continuous_video', 'listened_audio', 'media_report', 'source_check', 'project_open'):
                errors.append('invalid evidence kind: ' + key)
            else:
                kinds.append(ev['kind'])
            if not nonempty(ev.get('observation')):
                errors.append('evidence observation missing: ' + key)
        if needed_kind and not full_coverage(spans, duration):
            incomplete.append('full duration evidence:' + key)
        allowed = {'narrative': ('source_check', 'continuous_video'), 'typography': ('frame', 'continuous_video'), 'style': ('frame', 'continuous_video'), 'technical': ('media_report', 'project_open')}
        if key in allowed and not any(k in allowed[key] for k in kinds):
            incomplete.append('relevant evidence type:' + key)
        if key in ('pacing', 'motion') and coverage.get('continuous_video_full') is not True:
            incomplete.append('continuous full video review:' + key)
        if key == 'audio' and coverage.get('listened_full') is not True:
            incomplete.append('full audio listening')
        if score < 4:
            failures.append('below 4/5:' + key)
        total += score / 5 * weight
    for issue in review.get('issues', []):
        if not isinstance(issue, dict) or issue.get('severity') not in ('critical', 'major', 'minor') or issue.get('status') not in ('open', 'resolved', 'accepted_limit'):
            errors.append('invalid issue record')
            continue
        if 'affects_goal' in issue and not isinstance(issue['affects_goal'], bool):
            errors.append('affects_goal must be boolean')
        if issue.get('status') == 'resolved' and (not nonempty(issue.get('fix')) or not nonempty(issue.get('retest'))):
            errors.append('resolved issue needs fix and retest')
        if issue.get('status') != 'resolved' and (issue.get('severity') in ('critical', 'major') or issue.get('affects_goal') is True):
            failures.append('unresolved issue:' + str(issue.get('id', '?')))
    raw_total = total / denominator * 100 if denominator and not errors and not incomplete else None
    weighted = round(raw_total, 2) if raw_total is not None else None
    if raw_total is not None and raw_total < 90:
        failures.append('below 90/100')
    status = 'INVALID' if errors else 'INCOMPLETE' if incomplete else 'NEEDS_REVISION' if failures else 'PASS_RECORD_ONLY'
    return {'status': status, 'total': weighted, 'raw_total': raw_total, 'errors': errors, 'unverified': incomplete, 'failures': failures, 'notice': 'Record consistency only; does not prove aesthetic quality, watching or listening.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('review', type=Path)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    try:
        result = evaluate(json.loads(args.review.read_text(encoding='utf-8-sig')), args.review.resolve().parent)
    except (ValueError, OSError) as exc:
        result = {'status': 'INVALID', 'total': None, 'errors': [str(exc)]}
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text, encoding='utf-8')
    print(text)
    return 0 if result['status'] == 'PASS_RECORD_ONLY' else 2


if __name__ == '__main__':
    raise SystemExit(main())
