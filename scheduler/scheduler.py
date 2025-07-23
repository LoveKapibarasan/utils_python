import csv
from datetime import datetime, timedelta

class Task:
    def __init__(self, task_id, name, deadline, duration, progress=0, priority=1):
        self.task_id = task_id
        self.name = name
        self.deadline = deadline
        self.duration = timedelta(minutes=duration)
        self.progress = progress
        self.priority = priority

    def remaining_time(self):
        ratio = max(0, 1 - self.progress / 100)
        return self.duration * ratio

    def __repr__(self):
        return (f"[{self.task_id}] {self.name} "
                f"- Deadline: {self.deadline} "
                f"- Total Duration: {self.duration} "
                f"- Progress: {self.progress}% "
                f"- Remaining: {self.remaining_time()} "
                f"- Priority: {self.priority}")

    def update_progress(self, new_progress):
        self.progress = max(0, min(new_progress, 100))

def read_tasks(file_path):
    tasks = []
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = row["task_id"].strip()
            name = row["name"].strip()
            deadline = datetime.strptime(row["deadline"].strip(), "%Y-%m-%d %H:%M")
            duration = int(row["duration"].strip())
            progress = int(row["progress"].strip())
            priority = int(row["priority"].strip())
            tasks.append(Task(tid, name, deadline, duration, progress, priority))
    return tasks

def write_tasks(file_path, tasks):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["task_id", "name", "deadline", "duration", "progress", "priority"])
        for t in tasks:
            writer.writerow([
                t.task_id, t.name,
                t.deadline.strftime("%Y-%m-%d %H:%M"),
                int(t.duration.total_seconds() / 60),
                t.progress,
                t.priority
            ])

def main():
    file_path = "tasks.csv"
    tasks = read_tasks(file_path)

    print("=== Progress Update ===")
    raw = input("Example: 1:20,3:50 → Task 1 to 20%, Task 3 to 50%: ").strip()
    if raw:
        updates = raw.split(",")
        for upd in updates:
            if ":" in upd:
                tid, perc = upd.split(":")
                for t in tasks:
                    if t.task_id == tid.strip():
                        t.update_progress(int(perc.strip()))

    print("\n=== Today's Available Time ===")
    available_min = float(input("Example: 120 → Available time today (minutes): ").strip())
    available = timedelta(minutes=available_min)

    # Allocate 50% to TODO work
    plan_time = available * 0.5

    # Allocation ratio by priority
    ratio_map = {
        5: 5/15,
        4: 4/15,
        3: 3/15,
        2: 2/15,
        1: 1/15
    }

    # Redistribute quota from missing priorities to Priority 5
    absorbed = timedelta()
    for p in [4, 3, 2, 1]:
        relevant = [t for t in tasks if t.priority == p]
        if not relevant:
            absorbed += plan_time * ratio_map[p]
            ratio_map[p] = 0

    ratio_map[5] += absorbed.total_seconds() / plan_time.total_seconds()

    print("\n=== Remaining Tasks ===")
    for t in tasks:
        print(t)

    print(f"\nToday's available time: {available} / 50% allocated: {plan_time}")
    print(f"Redistributed (no task in some priorities) → to Priority 5: {absorbed}")

    print("\n=== Today's TODO Allocation (By Priority) ===")
    for p in range(5, 0, -1):
        quota = plan_time * ratio_map[p]
        relevant = [t for t in tasks if t.priority == p]
        relevant.sort(key=lambda t: t.deadline)

        assigned = timedelta()
        for t in relevant:
            if assigned >= quota:
                break
            rem = t.remaining_time()
            if rem <= timedelta(0):
                continue
            alloc = min(quota - assigned, rem)
            print(f"→ Priority[{p}] Task[{t.task_id}] {t.name}: {alloc}")
            assigned += alloc

    # Save updated progress
    write_tasks(file_path, tasks)
    print(f"\n=== Saved === Please check {file_path}")

if __name__ == "__main__":
    main()

