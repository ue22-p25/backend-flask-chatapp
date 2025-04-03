## step 05: how to redirect

Nothing crucial here, but an opportunity to show how to redirect HTTP traffic

### what is a redirect ?

There are many reasons why you would want to redirect a request to another URL:

- the URL has changed
- the resource is now located on another server
- ...

### how to redirect

In Flask you can use the `redirect()` function to redirect a request to another URL; it's dead simple;
in our case we just redirect the `/' URL to the `/front/users` URL:

### see also

in particular about the HTTP codes, see:

https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections
