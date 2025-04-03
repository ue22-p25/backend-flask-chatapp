## the template

the template is created with 2 variables:

- `user`: the details about the user, that we get .. wait for it .. from the
  `/api/users/<id>` endpoint
- `messages`: the messages for the user, that we get from the
  `/api/messages/with/<id>` endpoint

in this first version we just display the messages, we'll add a prompt area later on
