## the HTML template

this new file is a Jinja2 template, which is a templating engine for Python; it
allows you to create HTML pages dynamically by embedding Python code within the
HTML.

the basics for Jinja2 templating is:

- you compute one or several variables on the Python side - here e.g. we have
  `users` and `VERSION`
- you pass them to the template with `render_template()`
  ```python
  render_template('users.html.j2', users=users, version=VERSION)
  ```
- and from then on you can access the variables in the template with the
  corresponding names - here `users` and `version`
- for example, to display the version in the template, we use:
  ```html
  <h1>Welcome to the chat app (version {{ version }})</h1>
  ```
- Jinja also offers more advanced features, like loops and conditionals; observe
  how the template iterates over the `users` variable to create one HTML element
  per user
  ```html
    {% for user in users %}
        <div class="user">
        <h2>{{ user.name }}</h2>
        <p>{{ user.email }}</p>
        <p>{{ user.nickname }}</p>
        </div>
    {% endfor %}
    ```

