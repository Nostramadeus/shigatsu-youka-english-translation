"""Fail-closed reference coverage check against the actual candidate ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

STATUSES = {"existing_overlay", "repaired_overlay", "textless_art", "intentional_puzzle_japanese",
            "thumbnail_original", "animation_descriptor", "unused_source", "decorative_art"}
PREFIX = "グラフィック/リファレンス/"


def indexed(records, field, label, errors):
    result = {}
    for record in records:
        path = record.get(field)
        if not isinstance(path, str) or not path or "\\" in path or path.startswith("/") or ":" in path or ".." in path.split("/"):
            errors.append("%s has an invalid path: %r" % (label, path))
            continue
        if path in result:
            errors.append("%s has a duplicate path: %s" % (label, path))
        result[path] = record
    return result


def check(inventory, classification, patch):
    errors = []
    originals = indexed(inventory.get("assets", []), "original_path", "inventory", errors)
    decisions = indexed(classification.get("assets", []), "original_path", "classification", errors)
    extras = indexed(classification.get("extra_overlays", []), "path", "extra overlays", errors)
    if not originals:
        errors.append("Original archive inventory is empty")
    if set(originals) != set(decisions):
        for path in sorted(set(originals) - set(decisions)):
            errors.append("Unclassified original asset: " + path)
        for path in sorted(set(decisions) - set(originals)):
            errors.append("Classification has no original archive asset: " + path)
    if set(extras) & set(originals):
        errors.append("Extra overlay paths overlap original classifications")
    required = {}
    forbidden_changes = {}
    for path, original in originals.items():
        decision = decisions.get(path, {})
        status = decision.get("status")
        if status not in STATUSES:
            errors.append("Unknown or pending status for %s: %r" % (path, status))
        if decision.get("original_sha256") != original.get("original_sha256"):
            errors.append("Original hash binding mismatch: " + path)
        if not decision.get("evidence"):
            errors.append("Missing review/ruling evidence: " + path)
        expected = decision.get("expected_overlay_sha256")
        baseline = original.get("shipped_overlay_sha256") if original.get("shipped_overlay_present") else None
        if status in ("existing_overlay", "repaired_overlay"):
            if not isinstance(expected, str) or len(expected) != 64:
                errors.append("Missing expected overlay SHA256: " + path)
            else:
                required[path] = expected.lower()
            if status == "existing_overlay" and expected != baseline:
                errors.append("Existing overlay does not match the protected baseline: " + path)
        elif baseline:
            required[path] = baseline
            if expected and expected != baseline:
                errors.append("Baseline change is not explicitly classified repaired_overlay: " + path)
        elif status in STATUSES:
            forbidden_changes[path] = original["original_sha256"]
    for path, extra in extras.items():
        expected = extra.get("sha256")
        if not isinstance(expected, str) or len(expected) != 64 or not extra.get("evidence"):
            errors.append("Extra overlay lacks exact hash/evidence: " + path)
        else:
            required[path] = expected.lower()
    actual = {}
    with zipfile.ZipFile(patch) as archive:
        members = indexed([dict(path=item.filename, info=item) for item in archive.infolist() if not item.is_dir()],
                          "path", "ZIP", errors)
        for path in sorted(set(required) - set(members)):
            errors.append("Required English overlay missing from actual ZIP: " + path)
        unexpected = {path for path in members if path.startswith(PREFIX)} - set(originals) - set(extras)
        for path in sorted(unexpected):
            errors.append("Unregistered reference overlay in actual ZIP: " + path)
        for path in sorted((set(required) | set(forbidden_changes)) & set(members)):
            try:
                actual[path] = hashlib.sha256(archive.read(members[path]["info"])).hexdigest()
            except (RuntimeError, zipfile.BadZipFile) as error:
                errors.append("ZIP read/CRC failed for %s: %s" % (path, error))
                continue
            expected = required.get(path, forbidden_changes.get(path))
            if actual[path] != expected:
                errors.append("Actual ZIP hash mismatch: " + path)
    return dict(passed=not errors, original_assets=len(originals), classifications=len(decisions),
                required_overlays=len(required), checked_zip_hashes=len(actual),
                limitations=classification.get("limitations", []), errors=errors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--classification", required=True, type=Path)
    parser.add_argument("--patch", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = check(json.loads(args.inventory.read_text(encoding="utf-8")),
                       json.loads(args.classification.read_text(encoding="utf-8")), args.patch)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        result = dict(passed=False, errors=[str(error)])
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
