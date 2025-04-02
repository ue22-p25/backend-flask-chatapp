## step 19: finish it off

the last ring of changes is concentrated in the JS code

we need to do 2 things:

- the code that used to add a newly sent message to the table is no longer relevant (we will receive this information through the channel)
- but on the other hand we need to add messages to the table when we receive them through the channel

so the changes are 

- to factor out a function that we call `display_new_message()` - based on the previous code
- and to call this function when we receive a message through the channel, like so

```javascript
    socket.on(nickname, (str) => display_new_message(JSON.parse(str)))
```

and this time the app is totally functional !
