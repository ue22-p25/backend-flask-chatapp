# the dir where this script is located
BIN=$(dirname $(realpath $0))
# the repo root
ROOT=$(dirname $BIN)
# the js main dir
APP=${ROOT}/app

# wher to get the steps
STEPS_REPO=git@github.com:ue22-p24/backend-flask-chatapp-steps.git
# where we graft it here
STEPS=${BIN}/steps-repo

function clone() {
    if [ ! -d $STEPS ]; then
        git clone $STEPS_REPO $STEPS
    else
        echo "Directory $STEPS already exists. Skipping clone."
        git -C $STEPS remote get-url origin
    fi
}

function need-pull() {
    local localtip=$(git -C $STEPS rev-parse HEAD)
    local remotetip=$(git -C $STEPS rev-parse origin/main)
    if [ "$localtip" != "$remotetip" ]; then
        echo "WARNING -- double check $STEPS"
        echo "we have    HEAD=$localtip"
        echo "remote has HEAD=$remotetip"
    fi
}

function tofolders() {
    $BIN/steps.py tofolders $STEPS
}

function toauto-1() {
    local out=$APP/singlecolumn/AUTO
    python $BIN/tocodehike.py chain-dirs --all-files ${STEPS}/.steps/* > $out
    echo single column output written in $out
}

function toauto-2() {
    local out=$APP/scrollycoding/AUTO
    python $BIN/tocodehike.py chain-dirs --all-files --scrolly ${STEPS}/.steps/* > $out
    echo double column output written in $out
}

function toauto() {
    toauto-1
    toauto-2
}

# create 2 symlinks inside to the -hike repo
function fill() {
    python $BIN/fillauto.py $APP/scrollycoding $APP/singlecolumn
}

# the full monty
function all() {
    clone
    need-pull
    tofolders
    toauto
    fill
}

# using the folders as reference
function from-folders() {
    toauto
    fill
}

function from-git() {
    tofolders
    toauto
    fill
}

function save-steps() {
    echo "the recipe:"
    echo "cd $STEPS_REPO"
    echo "git branch -f main HEAD"
    echo "git push -f origin main:main"
}

"$@"
