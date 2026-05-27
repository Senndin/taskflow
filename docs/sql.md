# SQL Exercises

Practice queries based on simplified tables:

- `tasks (id, name, status, project_id)`
- `projects (id, name)`

---

## Query 1 — All statuses, no duplicates, alphabetically ordered

```sql
SELECT DISTINCT status
FROM tasks
ORDER BY status;
```

`DISTINCT` removes duplicate values. `ORDER BY status` sorts A→Z.

---

## Query 2 — Count of tasks in each project, ordered by count descending

```sql
SELECT p.name,
       COUNT(t.id) AS task_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY task_count DESC;
```

`LEFT JOIN` ensures projects with zero tasks still appear. `COUNT(t.id)` counts only non-NULL task ids.

---

## Query 3 — Count of tasks in each project, ordered by project name

```sql
SELECT p.name,
       COUNT(t.id) AS task_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY p.name;
```

Same as Query 2 but sorted by `p.name` instead of `task_count`.

---

## Query 4 — Tasks from projects whose name starts with "N"

```sql
SELECT t.*
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name LIKE 'N%';
```

`LIKE 'N%'` matches any string starting with "N". `INNER JOIN` is intentional — orphan tasks with no matching project are excluded.

---

## Query 5 — Projects with "a" in the middle of the name + task count

> "Middle" means not the first and not the last character.

```sql
SELECT p.name,
       COUNT(t.id) AS task_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
WHERE p.name LIKE '%_a_%'
GROUP BY p.id, p.name;
```

`LIKE '%_a_%'` — each `_` matches exactly one character, requiring at least one character before and after "a". `LEFT JOIN` includes projects with zero tasks.

---

## Query 6 — Tasks with duplicate names, ordered alphabetically

```sql
SELECT name
FROM tasks
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY name;
```

`GROUP BY name` + `HAVING COUNT(*) > 1` finds names that appear more than once.

To get full task rows instead of just names:

```sql
SELECT *
FROM tasks
WHERE name IN (
    SELECT name
    FROM tasks
    GROUP BY name
    HAVING COUNT(*) > 1
)
ORDER BY name;
```

---

## Query 7 — Duplicate (name + status) pairs from project "Delivery", ordered by match count

```sql
SELECT t.name,
       t.status,
       COUNT(*) AS matches_count
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY matches_count DESC;
```

`GROUP BY t.name, t.status` groups by the exact combination of both fields. `HAVING COUNT(*) > 1` keeps only duplicate pairs.

---

## Query 8 — Projects with more than 10 completed tasks, ordered by project_id

```sql
SELECT p.name
FROM projects p
JOIN tasks t ON t.project_id = p.id
WHERE t.status = 'completed'
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id;
```

`WHERE t.status = 'completed'` filters before grouping — more efficient than filtering in `HAVING`. `HAVING COUNT(t.id) > 10` keeps only projects above the threshold.
