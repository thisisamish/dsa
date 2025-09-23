| Folder | Commit Type | Commit Format |
| ------ | ------ | ------- |
|  | logically related files spread across folders | `add: <lowest_ancestor_folder_name>/(<logical_name>)`. follow the same for updates/deletes. |
|  | restructure | `restructure` |
| `leetcode-daily` | basic commit | `lc-daily: <date>` e.g. `lc-daily: april 1, 2025` |
| `leetcode-daily` | content correction | `errata::` prefix to the basic commit message |
| `leetcode-daily` | content addition | `addenda::` prefix to the basic commit message |
|  | config/guides addition | `add: <folder_name>/<file_name>` e.g. `add: utils/create_problem.py`. if there are multiple files in a folder, write `add: utils/`. if the file is in the root, write `add: README.md`. if multiple files are in the root, add each one of them individually. |
|  | config/guides updation | `update: <folder_name>/<file_name>`. follow rest of the guidelines as the addition one. |
|  | config/guides deletion | `delete: <folder_name>/<file_name>`. follow rest of the guidelines as the addition one. |