## an endpoint to create messages

nothing new here as compared to users; except the minor point that the `date`
column is not provided by the caller, but computed by the API at creation time

### try it out

Here's a trick that can help you populate the DB with some users and messages, from scratch;
especially as we might have to do this over and over again

#### create a bash file

copy and paste the following in a file named `aliases.sh` (or whatever you want)

```bash
# put this in aliases.sh
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
```

#### load the file

By running the following, you will load the file in your current shell session

```bash
source aliases.sh
```

#### run the commands

After you've source'd `aliases.sh` your shell knows about
the functions defined in the file; so you can do

```bash
create-users
create-messages
list-users
```
