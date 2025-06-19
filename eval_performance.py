import json
import argparse
from datetime import datetime

def load_selection_logs(path="selection_log.json"):
    """Load the user-feedback log."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {path} contains invalid JSON.")
        return []

def filter_by_date(logs, date_str):
    """Keep only log entries whose timestamp date matches `date_str`."""
    filtered = []
    for entry in logs:
        ts = entry.get("timestamp", "")
        try:
            entry_date = ts.split(" ")[0]  # "YYYY-MM-DD"
        except Exception:
            continue
        if entry_date == date_str:
            filtered.append(entry)
    return filtered

def compute_accuracy(logs):
    """Compute overall accuracy from the 'correct' field."""
    total = len(logs)
    if total == 0:
        return total, 0, 0
    correct = sum(1 for entry in logs if entry.get("correct", False))
    return total, correct, correct / total

def breakdown_by_camera(logs):
    """Return per-camera accuracy breakdown."""
    stats = {}
    for entry in logs:
        cam = entry.get("camera_id", "unknown")
        stats.setdefault(cam, {"total": 0, "correct": 0})
        stats[cam]["total"] += 1
        if entry.get("correct"):
            stats[cam]["correct"] += 1
    # compute percentages
    for cam, s in stats.items():
        s["accuracy"] = s["correct"] / s["total"] if s["total"] else 0
    return stats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate face-recognition performance from selection_log.json"
    )
    parser.add_argument(
        "--date",
        help="Only include entries from this date (YYYY-MM-DD)",
        required=False
    )
    args = parser.parse_args()

    logs = load_selection_logs()

    # If no --date flag provided, ask interactively
    if not args.date:
        date_str = input("Enter a date to filter (YYYY-MM-DD), or press Enter to skip: ").strip()
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print(f"Error: `{date_str}` is not a valid YYYY-MM-DD date.")
                exit(1)
            logs = filter_by_date(logs, date_str)
            print(f"\nEvaluating only entries from {date_str!r} ({len(logs)} entries)\n")
    else:
        # already validated by argparse, but double-check format
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print(f"Error: `{args.date}` is not a valid YYYY-MM-DD date.")
            exit(1)
        logs = filter_by_date(logs, args.date)
        print(f"\nEvaluating only entries from {args.date!r} ({len(logs)} entries)\n")

    total, correct, acc = compute_accuracy(logs)
    print(f"Overall selections: {total}")
    print(f"Overall correct:    {correct}")
    print(f"Overall accuracy:   {acc:.2%}\n")

    per_cam = breakdown_by_camera(logs)
    print("Per-camera performance:")
    for cam, s in per_cam.items():
        print(f"  • {cam}: {s['correct']}/{s['total']} correct ({s['accuracy']:.2%})")
