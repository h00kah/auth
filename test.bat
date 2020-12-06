curl -X POST -d "username=John&pswd=qwery&email=john@example.com" http://localhost:5050/api/v1/manage/user
curl -X GET http://localhost:5050/api/v1/manage/user/john@example.com
curl -X DELETE http://localhost:5050/api/v1/manage/user/john@example.com
curl -X GET http://localhost:5050/api/v1/manage/user/john@example.com