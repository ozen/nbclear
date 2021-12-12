nbclear
=========

A tool (and pre-commit hook) to automatically remove the output from all code cells in all Jupyter notebooks.

## Installation

`pip install nbclear`

## As a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/ozen/nbclear
    rev: v0.1.0
    hooks:
    -   id: nbclear
```

## Behavior

The tool opens the notebook and clears the outputs of cells in the memory.  
If there are no changes in the notebook, it quits without further action.  
If there are changes, it moves the original file `notebook.ipynb` to `notebook.ipynb~` and saves the cleared notebook to `notebook.ipynb`.  
If the backup cannot be created, it prints the error and quits. 