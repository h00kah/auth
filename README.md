# User management application with authenticate module

Intened use of this application is hide one inside private
network and connect external frontend-extenssive application.

Any database management, session storing and exception handling
have been done here. Several routes could be used external, but
for security reasons they should be proxied.

* /api/v1/ (GET) will be used for listing available routes in future (not sure)
* /api/v1/oauth (GET/POST) will be used for set of routes for OAuth purposes
* /api/v1/manage/user/<email> (GET) show user info
* /api/v1/manage/user (POST) create user
* /api/v1/manage/user/<email> (POST) update user
* /api/v1/manage/user/<email> (DELETE) remove user