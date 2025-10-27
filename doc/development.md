## 🧱 Conventional Commits — Standard for Clear and Consistent Git History

### **Overview**

The **Conventional Commits** specification provides a structured format for writing Git commit messages.
It helps teams maintain **readable**, **automatable**, and **semantic** commit histories that can be used to generate changelogs, version numbers, and release notes automatically.

---

### **Commit Message Structure**

Each commit message follows this pattern:

```
<type>(<scope>): <short summary>
```

#### **Parts explained**

* **`type`** → describes the category or purpose of the change.
* **`scope`** (optional) → specifies the part of the project affected.
* **`summary`** → a brief, imperative description of what the commit does.

Example:

```bash
feat(api): add endpoint for meal tracking
```

---

### **Common Commit Types**

| Type         | Description                                  | Example                                               |
| ------------ | -------------------------------------------- | ----------------------------------------------------- |
| **feat**     | A new feature                                | `feat(user): add endpoint to fetch daily nutrients`   |
| **fix**      | A bug fix                                    | `fix(calorie): correct total calories rounding issue` |
| **docs**     | Documentation-only changes                   | `docs(readme): update API usage section`              |
| **style**    | Code style or formatting (no logic change)   | `style(pep8): reformat utils.py to comply with PEP8`  |
| **refactor** | Code restructuring without changing behavior | `refactor(services): simplify nutrient calculation`   |
| **test**     | Adding or improving tests                    | `test(api): add tests for /meals endpoint`            |
| **chore**    | Maintenance tasks (deps, configs, CI/CD)     | `chore(deps): upgrade fastapi to 0.110`               |
| **perf**     | Performance improvement                      | `perf(database): optimize food search query`          |
| **build**    | Changes affecting build system               | `build(docker): add production Dockerfile`            |
| **ci**       | CI/CD configuration                          | `ci(github): add test workflow for pull requests`     |

---

### **Best Practices**

✅ **Write in the imperative mood**
Think “*this commit will…*”.
Example:

* ✅ `fix(route): handle missing meal_id gracefully`
* ❌ `fixed missing meal_id bug`

✅ **Keep the summary short**
Aim for ≤ 72 characters. Put details in the body if needed:

```bash
feat(api): add endpoint to list meals

This new endpoint supports pagination and filtering by date range.
```

✅ **Include a scope when possible**
Helps identify which part of the app was affected.
Example:
`refactor(models): rename NutritionFact to Nutrient`

✅ **Group atomic changes**
One logical change per commit → easier to revert and understand later.

✅ **Avoid generic messages**
Don’t use “update stuff” or “fix things.” Be specific about *what* and *why*.

---

### **Extended Examples**

**Good:**

```bash
feat(api): implement /nutrients endpoint for daily summary
fix(auth): validate token before saving meal data
refactor(models): merge Food and Ingredient models
test(api): add pytest fixtures for nutrition service
```

**Bad:**

```bash
update api
fix bug
stuff works now
```

---

### **Automation Benefits**

When following Conventional Commits, you can:

* **Generate changelogs** automatically (e.g., using `semantic-release`).
* **Auto-bump versions** (`feat` = minor version, `fix` = patch).
* **Improve code review clarity** — reviewers can filter by type.

---

### **Quick Reference Template**

```bash
<type>(<scope>): <short summary>

[optional body with details or reasoning]

[optional footer for breaking changes or issue refs]
```

Example with all parts:

```bash
feat(api): add endpoint for nutrition summary

Implements /summary endpoint that aggregates daily meal data.
BREAKING CHANGE: renamed /stats to /summary for consistency.
```

---