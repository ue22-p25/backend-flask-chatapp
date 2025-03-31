function list-users() {
    http :5001/api/users
}

function create-users() {
    http :5001/api/users name="Alice Caroll" email="alice@foo.com" nickname="alice"
    http :5001/api/users name="Bob Morane" email="bob@foo.com" nickname="bob"
    http :5001/api/users name="Charlie Chaplin" email="charlie@foo.com" nickname="charlie"
}

function create-messages() {
    http :5001/api/messages author_id=1 recipient_id=2 content="trois petits chats"
    http :5001/api/messages author_id=2 recipient_id=1 content="chapeau de paille"
    http :5001/api/messages author_id=2 recipient_id=3 content="not visible by 1"
}

function create-all() {
    create_users
    create_messages
}

function message-to-alice() {
    http :5001/api/messages author_id=3 recipient_id=1 content="from the API"
}
