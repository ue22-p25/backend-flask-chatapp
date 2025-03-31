PEERREPO=../../ue22-p24-backend-flask-chatapp-hike

function redo-1() {
    local out=$PEERREPO/app/singlecolumn/AUTO
    python tocodehike.py chain-dirs ../?? > $out
    echo single column output written in $out
}

function redo-2() {
    local out=$PEERREPO/app/scrollycoding/AUTO
    python tocodehike.py chain-dirs -s ../?? > $out
    echo double column output written in $out
}

function redo() {
    redo-1
    redo-2
}

# create 2 symlinks inside to the -hike repo
function fill() {
    python fillauto.py scrollycoding singlecolumn
}

function all() {
    redo
    fill
}
