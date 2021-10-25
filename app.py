from flask import Flask
from flask_ngrok import run_with_ngrok
from flask import jsonify, request

from firebase_admin import credentials, firestore, initialize_app


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
run_with_ngrok(app)  # Start ngrok when app is run


cred = credentials.Certificate('./fs.json')
app_fs = initialize_app(cred)
db = firestore.client()

sensor = db.collection('sensor')

@app.route("/", methods=['GET'])
def index():
  return 'Welcome to FLASK'


# /create_sensor
@app.route("/create_sensor", methods=['POST'])
def create_sensor():
  try:
    print(request)

    sensor_id = request.form['id']
    sensor.document(sensor_id).set(request.form)
    return jsonify({
        "status": "CREATED",
        "data": request.form
    })
  except Exception as e:
    return jsonify({
        "status": "ERROR",
        "details": e
    })

@app.route("/get_sensor", methods=['GET'])
def get_sensor():
  try:
    sensor_id = request.args.get('id')
    print("sensor_id", sensor_id)

    if sensor_id:
      sensor_data = sensor.document(sensor_id).get()
      return jsonify({
          "status": "SUCCESS",
          "data": sensor_data.to_dict()
      })
    else:
      all_sensor = [doc.to_dict() for doc in sensor.stream()]
      return jsonify({
          "status": "SUCCESS",
          "data": all_sensor
      })
  except Exception as e:
    return jsonify({
        "status": "ERROR",
        "details": e
    })

# /update_sensor
@app.route("/update_sensor", methods=['POST', 'PUT'])
def update_sensor():
  try:
    sensor_id = request.form['id']
    sensor.document(sensor_id).update(request.form)
    sensor_data = sensor.document(sensor_id).get()
    return jsonify({
          "status": "UPDATED",
          "data": sensor_data.to_dict()
    })
  except Exception as e:
    return jsonify({
        "status": "ERROR",
        "details": e
    })


@app.route("/delete_sensor", methods=['GET', 'DELETE'])
def delete_sensor():
  try:
    sensor_id = request.args.get('id')
    sensor_data = sensor.document(sensor_id).delete()
    return jsonify({
          "status": "DELETED",
          "id": sensor_id
      })
  except Exception as e:
    return jsonify({
        "status": "ERROR",
        "details": e
    })


if __name__ == '__main__':
    app.run()
