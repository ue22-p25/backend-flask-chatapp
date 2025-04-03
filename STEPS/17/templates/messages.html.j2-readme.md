## change in the template

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
