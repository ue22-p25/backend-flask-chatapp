# the dir where this script is located
BIN=$(dirname $(realpath $0))
# the repo root
ROOT=$(dirname $BIN)
# the js main dir
APP=${ROOT}/app

# where to get the steps
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

# compute the steps folder from the git repo
function tofolders() {
    $BIN/steps.py tofolders $STEPS
}

# create a new branch in the steps repo from the current folders
function togit() {
    $BIN/steps.py togit $STEPS
}

# compute AUTO in singlecolumn
function toauto-1() {
    local out=$APP/singlecolumn/AUTO
    python $BIN/tocodehike.py chain-dirs --all-files ${STEPS}/.steps/* > $out
    echo single column output written in $out
}
# compute AUTO in scrollycoding
function toauto-2() {
    local out=$APP/scrollycoding/AUTO
    python $BIN/tocodehike.py chain-dirs --all-files --scrolly ${STEPS}/.steps/* > $out
    echo double column output written in $out
}
# both
function toauto() {
    toauto-1
    toauto-2
}
# use the .je template and the AUTO files to create the final output
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

###########
# compute the output, using the folders as reference
function from-folders() {
    toauto
    fill
}

# compute the output, using the steps repo as reference
function from-git() {
    tofolders
    toauto
    fill
}

# display the recipe to adopt the latest created branch as main in the steps repo
function save-steps() {
    echo "===== the recipe:"
    echo "cd $STEPS"
    echo "git branch -f main HEAD"
    echo "git push -f origin main:main"
    echo "cd -"
    echo "===== end recipe"
}

# tests: shorter outputs, because the dev server is so slow..
TESTSTEPS=${STEPS}/.steps/0[0-4]*
function testauto-1() {
    local out=$APP/singlecolumn/AUTO
    python $BIN/tocodehike.py chain-dirs --all-files $TESTSTEPS > $out
    echo single column output written in $out
}
function testauto-2() {
    local out=$APP/scrollycoding/AUTO
    python $BIN/tocodehike.py chain-dirs --all-files --scrolly $TESTSTEPS > $out
    echo double column output written in $out
}
function testauto() {
    testauto-1
    testauto-2
}
function test() {
    testauto
    fill
}

"$@"
