import random

from flask import Flask, request, jsonify, render_template, abort
from mongoengine import connect
from mongoengine.base import ValidationError

from models import Topic

app = Flask(__name__)
app.config.from_object('settings')

connect(app.config['DATABASE_NAME'])

@app.route('/')
def main():
    return render_template('base.html', data='screw this')


@app.route('/api/1/topics/', methods=['GET', 'POST'])
def get_or_create_topic():
    if request.method == 'POST':
        topic = request.form.get('topic', None)
        try:
            t, created = Topic.objects.get_or_create(topic=topic)
        except ValidationError:
            return jsonify(success = False,
                data = {},
                error = '[ValidationError] Could not validate your data. \
                Please refer to the API-documentation.')

        return jsonify(success = created,
            data = [{'id': str(t.id), 'topic': t.topic}])

    elif request.method == 'GET':
        count = request.args.get('count') or 1
        count = int(count)
        total = int(Topic.objects.count())

        if total <= count and total != 0:
            t = Topic.objects.all()
        else:
            t = []
            for l in xrange(0, count):
                if total <= 1:
                    rand = 0
                else:
                    rand = random.randint(0, total-1)
                t.append(Topic.objects.all().skip(rand).next())
            if len(t) == 0:
                return jsonify(success = False, data = [], 
                        error = 'No topics found.1')
        if not t:
            return jsonify(success = False, data = [], error = 'No topics \
                    found.')
        data = [{'id': str(x.id), 'topic': x.topic} for x in t]
        return jsonify(success = True, data = data)

    abort(400)


@app.route('/api/1/topics/<topic_id>/votes/', methods=['POST'])
def vote_on_topic(topic_id):
    pass
