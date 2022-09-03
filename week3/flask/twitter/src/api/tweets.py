from flask import Blueprint, jsonify, abort, request
from ..models import Tweet, User, db

bp = Blueprint('tweets', __name__, url_prefix='/tweets')


@bp.route('', methods=['GET'])  # decorator, denoted by @, takes path and list of HTTP verbs
# Since bp has a url_prefix of /tweets as defined in tweets.py, we pass an empty string to the URL path argument of the decorator
# Second parameter is the GET method name.
def index():
    tweets = Tweet.query.all()  # ORM performs SELECT query (Under the hood, this means that the SQLAlchemy ORM will execute an SQL function akin to SELECT * FROM tweets;. )
    # The query result objects turn into Tweet objects.
    result = []
    # We then iterate over these Tweet objects:
    for t in tweets:
        result.append(t.serialize())  # build list of Tweets as dictionaries
    # return JSON response (This is Flask's jsonify() function, which will issue an HTTP response containing the list of tweets with a Content-Type header of application/json.)
    return jsonify(result)


# The first argument '/<int:id>' is Flask syntax that defines a route parameter. Specifically, it says that an integer value will be passed into the URL following the URL prefix, resulting in a URL such as: http://localhost:5000/tweets/1, http://localhost:5000/tweets/23, etc.
# 	This integer value will be stored in a variable named id and made available to the immediately following endpoint function, which in this case is show().
@bp.route('/<int:id>', methods=['GET'])
# In the show() function, we take that id from the route 
def show(id: int):
# use the superclass db.Model method that the Tweet model inherited, get_or_404(), to try to GET a record for the given id from the tweets table in our database. The ORM transforms this request into a SELECT query and sends the raw SQL to the database server. 
# If no match is found, the get_or_404() method will send a HTTP response to the client with a 404 status code.
    t = Tweet.query.get_or_404(id)
# If a match is found, then we serialize and jsonify the matching record and send it back to the client.
    return jsonify(t.serialize())


@bp.route('', methods=['POST'])
# When the POST method comes in, create() will handle it:
def create():
    # req body must contain user_id and content
    if 'user_id' not in request.json or 'content' not in request.json:
        # If the checks don't pass, then Flask's abort() method is called to respond to the client with a 400 status code (meaning "Bad Request").
        return abort(400)
    # user with id of user_id must exist (If not, 404 will be returned.)
    User.query.get_or_404(request.json['user_id'])
    # construct Tweet
    t = Tweet(
        user_id=request.json['user_id'],
        content=request.json['content']
    )
    # SQLAlchemy's add and commit  methods:
    db.session.add(t)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement
    return jsonify(t.serialize())

# watching out for HTTP DELETE requests to URLs with a pattern such as http://localhost:5000/tweets/1
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    # get_or_404 to confirm whether a tweet with this id exists or not
    t = Tweet.query.get_or_404(id)
    try:
# If the tweet to delete exists, we prepare and execute the DELETE statement on the server, and return a JSONified response of True if this succeeds.
        db.session.delete(t)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
# If the code in the try block causes an error, then instead of the application failing, it will default to the code in the catch block beneath it. In this case, if the prepare and commit of the DELETE query fails for some reason, we will return a JSONified response of False to the client, so that it knows that an error occurred and can handle it appropriately on its end.
        return jsonify(False)


@bp.route('/<int:id>/liking_users', methods=['GET'])
def liking_users(id: int):
    t = Tweet.query.get_or_404(id)
    result = []
    for u in t.liking_users:
        result.append(u.serialize())
    return jsonify(result)

