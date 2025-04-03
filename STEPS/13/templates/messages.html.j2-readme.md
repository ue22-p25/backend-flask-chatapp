## the template

- injects the new JS script
- adds a new form area to send messages, that has as many `<input>` fields as there are fields in a message, namely
  - a `hidden` input with the `author_id` (the user id) - that won't change, but is required as part of the newly created message
  - a `<select>` tag for the recipient
  - a `<input>` tag for the content, typed as `text`
