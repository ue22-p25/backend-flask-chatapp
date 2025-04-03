## the new JS script

- as we've learned in the frontend courses, the script arranges to execute itself when the page is loaded
- at that time it binds the 'submit' event of the form to a function that will
  - prevent the default behavior of the form (which would be to reload the page)
  - get the values of the fields in the form
  - and send them to the API, using a `POST` request

**Note**: there actually is a default behaviour for a form submission event,
which uses the `action` and `method` attributes of the form to determine where
to send the data. However that default behaviour does not support JSON encoding,
this is the only reason why we need to bother with the JS script at that point.  
(we will take advantage of our custom script in the next steps anyway, so it's
no regret)
