# ShinarNews

> *Shinar*
>
> the place where the Babel Tower was built

## Installing

```
pip install -e git+https://github.com/ruipgil/unbabel-py/#egg=unbabel_py
```

```
pip install -e .
```

## Running

```
flask run
```

The app requires some environment variables to be set:
+ `` FLASK_APP ``: which should be set to ``` shinarnews ```
+ `` UNBABEL_USERNAME ``: refers to the username of the unbabel sanbox API
+ `` UNBABEL_API_KEY ``: must be set to the required API key
+ `` MONGO_PORT ``: optional, mongodb port. Defaults to 27017
+ `` MONGO_HOST ``: optional, mongodb host. Defaults to localhost

The app can be tested by running:
```
python -m unittest
```

## Remarks

+ Stories are fetched from the HN api regularly and stored in a collection within mongodb.
+ The fetching process executes in a separate thread to the flask server
+ The client will ask for the stories using an AJAX request (using fetch), and update the DOM without the need to reload the page.
+ The (little) javascript code uses some of the features of the ES6 specification, and there is no bundling and transcompilation. This means that a modern and updated browser is needed to run the code.
+ Translations are requested whenever a new story is found. The target languages to translate (portuguese and italian) are hard coded, but could be changed easily.
+ In the same thread as the polling of new stories, the translations are checked.
+ In the client side, stories that have just been discovered will appear without translations, as they become available they will appear on the screen.
+ ShinarNews is tested and developed with python 3 in mind. It also uses a [tweaked version of the unbabel sdk](//github.com/ruipgil/unbabel-py).
