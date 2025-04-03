## step 13: the frontend can send messages too

it's nice to see the messages; but better still, we'd need to be able to send messages as well

in order to achieve this, we need:

- more information made available in the frontend page: the list of users, so that the user can select a recipient
- in the frontend as well, a new form area to send messages
- a new frontend script - stored in `static/script.js` - that will actually send the message - by talking back to the API

### the /front/ endpoint

- simply makes a 3rd request to the API, to get the list of users

### the template

- injects the new JS script
- adds a new form area to send messages, that has as many `<input>` fields as there are fields in a message, namely
  - a `hidden` input with the `author_id` (the user id) - that won't change, but is required as part of the newly created message
  - a `<select>` tag for the recipient
  - a `<input>` tag for the content, typed as `text`

### the new JS script

- as we've learned in the frontend courses, the script arranges to execute itself when the page is loaded
- at that time it binds the 'submit' event of the form to a function that will
  - prevent the default behavior of the form (which would be to reload the page)
  - get the values of the fields in the form
  - and send them to the API, using a `POST` request

**Note**: there actually is a default behaviour for a form submission event,
which uses the `action` and `method` attributes of the form to determine where
to send the data. However that default behaviour does not support JSON encoding,
this is the only reason why we need to bother with the JS script at that point.  
(we will take advantage of our custom script in the next steps anyway, so it's
no regret)

### still missing

and fixed in the next step:

the page does not refresh after sending a message; i.e. the new message is not
displayed in the list of messages
