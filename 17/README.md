## step 17: subscribe to the nickname channel

our next move is to subscribe to the nickname channel  
but wait, the JS code currently is static, and has no access to the nickname

we have 2 options here:

1. make the JS code a template, and instantiate it with the nickname
1. pass the nickname to the JS code **through the HTML tree**

### change in the template

actually, the first option is a little awkward, there is no need to make the JS
code a template;

instead we can simply attach the nickname in the HTML tree; and there is a
standard practice for that, which is to add a **data attribute** to the HTML
element; and since this is of interest to the whole tree, we pick the `<body>`
element for that purpose

hence this line in the HTML template:

```html
<body data-nickname="{{ user.nickname }}">
```

### change in the JS code

from then on, the nickname becomes accessible in the JS code, thanks to this
line

```javascript
    const nickname = document.body.dataset.nickname
```

and from there, we can simply subscribe to the nickname channel, using the
`socket.on()` method like before

### what's left then ?

but of course this version is not functional yet, as nobody writes on that
channel yet...
