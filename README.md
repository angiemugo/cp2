# API Bucketlist
This is an app built on python running on the flask framework. It supports creating, editing, viewing and deleting both bucket lists and bucketlist items.


|  ENDPOINT                             |  METHOD         | FUNCTIONALITY                              | PUBLIC ACCESS  |
|---------------------------------------|:----------------|:-------------------------------------------|----------------|
|`/auth/register`                       |POST             |Signs up a user                             |FALSE           |
|`/auth/login`                          |POST             |Logins in a user                            |FALSE           |
|`/bucketlists/`                         |GET              |Lists all bucketlists                       |FALSE           |
|`/bucketlists/`                         |POST             |Creates a bucketlist                        |FALSE           |
|`/bucketlists/<id>`                    |UPDATE           |Updates bucketlist with given id            |FALSE           |
|`/bucketlists/<id>`                    |DELETE           |Updates bucketlist with given id            |FALSE           |
|`/api/bucketlists/<id>/items`          |POST             |Creates an item in a bucketlist             |FALSE           |
|`/api/bucketlists/<id>/items/<id>`     |GET              |Get a specific item                         |FALSE           |
|`/api/bucketlists/<id>/items/<id>`     |UPDATE           |Update an item matching the id              |FALSE           |
|`/api/bucketlists/<id>/items/<id>`     |DELETE           |Delete an item matching the id              |FALSE           |

## Get Up and running
1. Git clone the repo
2. Create a virtualenv `mk virtualenv venv`
3. Activate the environment `workon venv`
4. Pip install requirements by running `pip install -r requirements.txt`
5. Run the server `python manage.py runserver`

## Sending and Receiving requests
For this API, use curl or postman. This app was tested using postman and the screenshots and video are from postman.

### Registration
To register, a username and password is required.
![Imgur](http://i.imgur.com/fviidvi.png)

### Login
To register, a username and password is required. This method returns a token that is used as authorization.
![Imgur](http://i.imgur.com/bGXjGvN.png)

### Bucketlist POST
This method creates a password. A bucketlist name is required as well as authorization in the form of a token.
![Imgur](http://i.imgur.com/ENwjcUc.png)

### Bucketlist GET  
This method returns all the bucketlists when an ID is not specified. When specified, it returns the specific bucketlist.
![Imgur](http://i.imgur.com/UQOHE99.png)

### Bucketlist GET with <ID>
This method returns the specific bucketlist that matches the given id while displaying the items it contains.
![Imgur](http://i.imgur.com/9HlSp5p.png)

### Bucketlist PUT
An ID is required to edit a specific bucketlist. The body has the new name of the bucketlist.
![Imgur](http://i.imgur.com/ENwjcUc.png)

### Bucketlist DELETE
An ID is required to delete a specific bucketlist.
![Imgur](http://i.imgur.com/wlecKBS.png)

### Item POST
In a specific id, an item is created. The body contains the item name and the done status.
![Imgur](http://i.imgur.com/f3UgpxD.png)

### Item PUT
This method edits a specific  item thus an id has to be specified. An item name is required as well as the done status.
![Imgur](http://i.imgur.com/7fgRxFb.png)

### Item DELETE
This method deletes the item that is specified.
![Imgur](http://i.imgur.com/VCDFhtV.png)

##Dependencies
- flask_restful
- Postgres
- flask_sqlalchemy
- Nosetests
