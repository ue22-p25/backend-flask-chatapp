## step 15: display nicknames in newly created messages

to be able to display the nicknames of the users in the newly created messages,
we need to slightly tweak our `/api/messages` endpoint  
instead of returning a `author_id` and a `recipient_id`, we will return the
`author` and `recipient` objects with full details

for that the endpoint does 2 requests to the DB

**Note** in real life, one tends to optimize the number of requests to the DB;  
it would be possible to get the `author` and `recipient` objects in one go, but
here we are not in a performance context, and we want to keep things simple

### caveats

now the app works reasonably fine as far as sending messages is concerned  
but it still sucks in terms of receiving messages; we have no simple way to be
made aware of incoming messages
