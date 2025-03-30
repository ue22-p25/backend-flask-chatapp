## step 07: how to create messages

In this very rustic app, a message is simply a text sent from one user (the author) to another one (the recipient)

Nothing exactly new here; we use the same approach as for the users, but this time we deal with messages

- we create a new class `Message` that will represent the messages
- we create a new endpoint `/api/messages` that will allow us to create messages

### using primary keys to model relationships

Worth being noted though, in the `Message` class we need to refer to the `User`
class (for the author and recipient)  
the standard approach here is **to use the primary keys** in the `messages` table

hence the `author_id` and `recipient_id` columns, that are both `Integer`, and
declares as `ForeignKey` to the `id` column of the `users` table

This is an intermediary step, and in a future step down the road we will improve
this a bit, but it's helpful to understand how to deal with foreign keys in
SQLAlchemy;

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
