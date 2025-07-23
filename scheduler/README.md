# 📝 Task Progress Manager & Daily Allocation Tool

This script helps you manage your tasks, track their progress, and allocate your available daily time efficiently based on priority and deadlines.

---

## 📋 Features

- Reads tasks from a CSV file (`tasks.csv`)
- Allows interactive progress updates (e.g., "1:30,2:100")
- Prompts for today's available time and allocates 50% of it to unfinished tasks
- Distributes time based on priority (5 levels)
- Handles redistribution if no tasks exist in a given priority
- Outputs detailed allocation suggestions
- Saves updated task progress back to CSV

---

## 📂 Input Format (`tasks.csv`)

```csv
task_id,name,deadline,duration,progress,priority
1,Write report,2025-07-25 17:00,120,30,5
2,Prepare slides,2025-07-26 10:00,90,0,4
3,Review paper,2025-07-24 18:00,60,80,3
```

### Column Explanation:

| Column     | Description                                 |
|------------|---------------------------------------------|
| `task_id`  | Unique identifier for the task              |
| `name`     | Task description                            |
| `deadline` | Deadline in `YYYY-MM-DD HH:MM` format       |
| `duration` | Total expected minutes                      |
| `progress` | Completion percentage (0–100)               |
| `priority` | Priority level (1 = lowest, 5 = highest)    |

---

## 🚀 How to Use

1. Prepare your `tasks.csv` file as shown above.
2. Run the script:

```bash
python task_manager.py
```

3. Follow the prompts:

- Example for progress update:

  ```
  1:50,3:100
  ```

- Example for available time input:

  ```
  120
  ```

4. The script will:

- Recalculate remaining time for each task
- Allocate 50% of available time to TODOs
- Distribute that time according to task priority
- Print out allocation suggestions
- Save updated progress back to `tasks.csv`

---

## ⚙️ Allocation Logic

- 50% of your available time is reserved for remaining tasks.
- Time is distributed using fixed priority ratios:

| Priority | Ratio   |
|----------|---------|
| 5        | 5 / 15  |
| 4        | 4 / 15  |
| 3        | 3 / 15  |
| 2        | 2 / 15  |
| 1        | 1 / 15  |

- If no task exists in a priority level, its share is reallocated to priority 5.

---

## ✅ Example Output

```
Today's available time: 2:00:00 / 50% allocated: 1:00:00
Redistributed → to Priority 5: 0:20:00

=== Today's TODO Allocation (By Priority) ===
→ Priority[5] Task[1] Write report: 0:40:00
→ Priority[4] Task[2] Prepare slides: 0:20:00

=== Saved === Please check tasks.csv
```

---

## 📦 Requirements

- Python 3.7+

---

## 📄 License

MIT License

