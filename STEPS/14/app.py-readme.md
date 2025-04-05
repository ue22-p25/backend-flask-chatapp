## also display newly created message

upon successful creation of a message, the API returns the message details so,
we can use that to display the message in the frontend

in the mix, we can also take care of any error that may occur, and inform the
user (actually in this rustic app we just log in the console)

### the caveats

at this point in time, the data returned by the API about the newly created
message only contains user ids, not the user names
