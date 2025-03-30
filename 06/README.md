## Step 06: add a `/api/users/<id>` endpoint

A new endpoint to get the details of one specific user from their ID

Nothing new indeed, very similar to the `/api/users` endpoint, except that we
use the `get()` method to retrieve the user by its primary key

(and we still need to convert the `User` object to a regular Python dictionary)
