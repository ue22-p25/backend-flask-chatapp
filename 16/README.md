## step 16: pouring SocketIO into the mix

to make the app more reactive, we will use SocketIO, so the backend can notify
the frontend of incoming messages

in this first - admittedly quite limited - step, we just lay the groundwork for
adding SocketIO in the picture, even though it is not actually used for anything
useful yet

### SocketIO basics

SocketIO is a library that enables real-time, bidirectional communication between
clients and servers. It is built on top of WebSockets, which is a protocol that
allows for full-duplex communication channels over a single TCP connection.

SocketIO provides a higher-level abstraction over WebSockets, making it easier to
work with. It handles many of the complexities of WebSockets, such as
reconnection, event handling, and broadcasting messages to multiple clients.

It exposes the notion of **channels** (or **rooms**) that kind of like act as
multicast groups: a message sent to a channel reaches all clients subscribed to
that channel. Exactly what we need here then.

### SocketIO implementations

in our context, we actually need two SocketIO implementations:

- one for the backend - so, in Python, and more specifically for Flask
- and one for the frontend - so, in JS
- the backend will be responsible for sending messages to the frontend each time a message gets created
- and the frontend will be responsible for 
  - connecting the server in the first place
  - subscribing to the right channel (since our app has only DMs and no room, we will use one channel per user)
  - and reacting to incoming messages - typically by displaying them in the UI

So, what does all that take actually, in terms of code changes ?

### boilerplate

in `app.py`

- we need to import (and `pip install` if needed) the `flask-socketio` package
- and to create a `SocketIO` instance called `socketio` - it will in some context act as a replacement for the Flask `app`

### a socketIO callback (kind-of like an endpoint)

still in `app.py`

- we create a function called `connect_ack`
- the syntax for creating it looks a bit like the one for a regular Flask endpoint  
  except the decorator is `@socketio.on` instead of `@app.route`
- the name used for creating it - here `connect-ack` is the **name of a channel**

so what we're saying here is, each time a message occurs on the `connect-ack` channel, the backend will print a message about that  
we could have gone entirely without the `connect-ack` channel, but it is a good way to test that the connection is working

### in the HTML template

this is the place where we add the SocketIO client-side code into the mix; as always we use a `<script>` tag in `<head>` to do that; we picked a CDN for that

### the JS code

upon document loading, the JS code will 

- create a connection to the server using `socket = io()`
- and then define a callback function
- that will trigger upon a `connect` event (this time this is a builtin name, as
  opposed to the `connect-ack` channel we created earlier)
- and so this is how the frontend will send an acknowledgment to the backend
  upon successful connection

### expected behaviour

all this means that, when the web page is loaded:

- the frontend connects to the backend
- once connected it says so on the console
- and sends an acknowledgment to the backend
- which prints a message on the console as well

of course all this traffic is purely for educational purposes, and is not
required for the app to work properly
