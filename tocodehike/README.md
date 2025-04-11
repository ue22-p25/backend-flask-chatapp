# managing a step by step rollout (steps.py)

## 2 representations

- as a git repo (the reference)
  - one commit per step
  - each commit is expected to have a commit message with a first line that looks like
    ```text
    step <step_number> - <step_description>
    ```
- optionally, as a folder with as many subfolders as steps
  - the subfolder name corresponds to <step_number>
  - the <step_description> is taken from the file `readme.md` whose first line should look like
    ```text
    # <step_description>
    ```

**as of now**, the tool that converts all this to a nextjs/markdown/codehike input uses **the folder structure as input**;  
and so it refreshes it from the git repo as a first processing phase

## locations

default layout is:

- both representations are expected to be in the **same folder**
- with the folder structure - when present - is in `./steps`

**for convenience only** (mostly development)  
the commands allow to specify a different input or output folder (the -i and -o options)  
this is hopefully only needed when bootstrapping, and not in production

## tooling

### from git to folders

```bash
# the default is for steps_folder to be in <git_repo>/.steps
steps.py tofolders <git_repo> [-o <steps_folder>]
```

this will
- create a new folder if needed
- clean it up if needed
- create a subfolder for each step in the git repo
- note that only the steps whose log message match the convention above are taken into account

### conversely

```bash
# likewise, the steps folder is expected to be found
# in <git_repo>/.steps
steps.py togit [-b branch] [-i steps_folder] <git_repo>
```

- if the provided repo is not yet a git repo, it will be created and initialized
- it will create an orphan branch whose name is `branch` or `branch-1` etc...  
- the branch will contain the various steps found in `.steps` - in alphabetcal
  order - as successive commits
- again wrt our first usecase, this applies the `strip-docstring` filter on
  `app.py` - that was a one-shot thing and we can now ignore it
- the default for `branch` is `steps`

- when bootstrapping from a steps-folder that is under git itself
  - if `git ls-files` returns something when run in the steps folder
  - in that case only the files known to git are inserted in the new git repo

### comparing branches

when doing back and forth between the two representations, we keep a history of
the changes by incrementing the branch name; typically you start with `steps`,
then `steps-1`, `steps-2` etc...

you can compare two branches with

```bash
steps.py diff-branches <git_repo> <branch1> <branch2>
```

as of now this is relevant only if both branches have the same steps (no
re-syncing yet

## from folders to codehike (tocodehike,py)

```
./tocodehike.py chain-dirs [--scolly] steps-repo/.steps/*
```

will write on stdout the codehike input  
see `--help` to see the other lower-level subcommands

# producing the codehike input

## redo.sh

```
redo.sh all
```

will
- clone the upstream repo `ue22-p24/flask-chatapp-steps` under `tocodehike/steps-repo`
- run the `tofolders` command above to explode this repo into a folder
- invoke `tocodehike.py` to produce the codehike input
- run `fillauto.py` to fill the .j2 templates and produce the final `.mdx` input to codehike
