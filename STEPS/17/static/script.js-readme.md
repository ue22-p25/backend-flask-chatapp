## change in the JS code

from then on, the nickname becomes accessible in the JS code, thanks to this
line

```javascript
    const nickname = document.body.dataset.nickname
```

and from there, we can simply subscribe to the nickname channel, using the
`socket.on()` method like before
