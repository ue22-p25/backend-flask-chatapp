## step 14: also display newly created message

upon successful creation of a message, the API returns the message details so,
we can use that to display the message in the frontend

in the mix, we can also take care of any error that may occur, and inform the
user (actually in this rustic app we just log in the console)

### the JS script

we just need to extend the JS script to handle the response from the API; for
that
- we improve on the sequence of `.then()` calls
- if the response is a success, we create a new row in the messages table
- and if not we use a `.catch()` to log the error in the console

### the caveats

at this point in time, the data returned by the API about the newly created
message only contains user ids, not the user names
