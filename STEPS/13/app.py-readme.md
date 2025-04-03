## step 13: the frontend can send messages too

it's nice to see the messages; but better still, we'd need to be able to send messages as well

in order to achieve this, we need:

- more information made available in the frontend page: the list of users, so that the user can select a recipient
- in the frontend as well, a new form area to send messages
- a new frontend script - stored in `static/script.js` - that will actually send the message - by talking back to the API

### the /front/ endpoint

- simply makes a 3rd request to the API, to get the list of users

### still missing

and fixed in the next step:

the page does not refresh after sending a message; i.e. the new message is not
displayed in the list of messages
