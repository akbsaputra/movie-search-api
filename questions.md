# Problem 2 Questions

## Which library did you choose?
I choose Flask library

## Did you encounter any difficulties while going through the tutorial/quickstart?  How did you resolve them?
Yes. Flask contains many other libraries. One of the most important libraries included is jinja2 that enables you to create HTML template containing Python variables and functions. Thus, while learning about Flask, I have to go through jinja2's documentation as well. To be honest, although comprehensive, both Flask and jinja2's documentation might be a little complicated to follow, especially for beginners. The tutorial project is also not simple and requires extensive effort to follow. To resolve this, I did some browsing and saw other people's projects and read their experience in using Flask and jinja2. Many of them have a more simplified take on how to implement Flask into their own web-app Python projects. With the help of these stranger's project showcased on the internet, I got inspired on how to implement Flask and jinja2 in a more straightforward way. 

## Referencing the documentation, what is an important class that the library provides? Explain (in your own words) what it does.
The most important class in flask is the "Flask" class. In my app, I use it at the very beginning, before defining any methods (ie., web = flask.Flask(__name__)). The "Flask" class is important because it defines a flask app out of our Python file, and is also responsible in managing and handling requests/routing of the app. You can't build and customize your flask app without using the "Flask" class at the first place.

## Referencing the documentation, what is an important function that the library provides? Explain (in your own words) what it does.
The most important function in flask is the "route" function. In my app, I use it to define every endpoint (i.e., @web.route("/trending", methods=("GET",))). The "route" function is important because it defines the route or path of your web program, and associate each path with functions in your Python file. When a user tries to access a URL that matches a route in your web app, flask calls the associated function to handle the request using "route" function.