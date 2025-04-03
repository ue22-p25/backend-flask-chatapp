## the JS script

we just need to extend the JS script to handle the response from the API; for
that
- we improve on the sequence of `.then()` calls
- if the response is a success, we create a new row in the messages table
- and if not we use a `.catch()` to log the error in the console
