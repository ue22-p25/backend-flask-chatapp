## step 12: a frontend to display messages

just like we did earlier for users, it's time to build a frontend to display messages  
this comes in two parts:
- a new frontend endpoint `/front/messages/<id>` that will be the main page for one user
- an html template that will display the messages relevant for a given user

### accessing the DB

like for the earlier step, we refrain from accessing the DB directly, and use
the `/api/messages/with/<id>` endpoint  
the arguments we had for users - the fact that we want the app to remain modular - still holds as well of course  
plus, on top of that, the approach here makes even more sense, in that the logic for
retrieval this time is a little more complex, and **should not be duplicated**

### other caveats

at this point, the main default is, we don't see incoming messages as they are
posted; the user needs to refresh the page to see new messages; a bit of
patience...
