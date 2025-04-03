## the JS code

upon document loading, the JS code will 

- create a connection to the server using `socket = io()`
- and then define a callback function
- that will trigger upon a `connect` event (this time this is a builtin name, as
  opposed to the `connect-ack` channel we created earlier)
- and so this is how the frontend will send an acknowledgment to the backend
  upon successful connection
