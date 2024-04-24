# Politricks App
> Link: http://politricks.me/

This application is entirely about politics. Here people can talk about their reviews and suggestions on each party available in a particular country. I'm planning to add hierarchy of users, like Admin and User.
There will be a home page showing the latest post of users about political parties, and other users can support/not support the post. Also, they can add comments/Suggestions underneath. 
User registration and login features will be included. Each user will have their profile pages. User profile page includes their details and interests. Also, Tags which users are interested in and post related to that tags will be shown first on the homepage. 
Landing page for each post, there are more options will be available for users. Possibilities include, each user can edit/delete/add their reviews.


# Server-Side rendering
The first rendering of a web page is performed on server in server rendered applications. The user receives a pre-rendered document, which can be viewed without any JavaScript being run. This allows for better SEO visibility, as JavaScript can not be run by many web crawlers, and page load times perceived faster.

> How it works

![Server-side Rendering](https://github.com/amal-ideas/amal-python-react-project/blob/main/images/server-side-rendering.jpeg)

Since our primary application server is a Django application which can not understand JavaScript, we need a runtime of JavaScript to make our React frontend. We can use a Node Server for this. When our primary Django server is hit by a message, we will check our database to get the details we need. Next we must send the info to our Node server in an HTTP POST request the returns our markup, plus the final state of our Redux store. Finally we must incorporate this information into our Django app's HTML response and send it to the customer.(*Setting Up Server Side Rendering with React, Redux, and Django, Alexander Richey*)

# ERD for my Web Application

I created this ERD with Visual Paradigm destop application.

![Database Entity-Relationship Diagrams](https://github.com/amal-ideas/amal-python-react-project/blob/main/images/ERD.png)
