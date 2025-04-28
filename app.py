from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['dietplanner']
collection = db['recommendations']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    age = request.form['age']
    gender = request.form['gender']
    weight = request.form['weight']
    height = request.form['height']
    veg_or_nonveg = request.form['veg_or_nonveg']
    disease = request.form['disease']
    region = request.form['region']
    allergics = request.form['allergics']
    foodtype = request.form['foodtype']

    query = {
        "gender": gender,
        "veg_or_nonveg": veg_or_nonveg,
        "region": region,
        "foodtype": foodtype
    }

    data = collection.find_one(query)

    if data:
        restaurant_names = data.get('restaurants', [])
        breakfast_names = data.get('breakfasts', [])
        dinner_names = data.get('dinners', [])
        workout_names = data.get('workouts', [])
    else:
        restaurant_names = breakfast_names = dinner_names = workout_names = []

    return render_template('result.html',
                           restaurant_names=restaurant_names,
                           breakfast_names=breakfast_names,
                           dinner_names=dinner_names,
                           workout_names=workout_names)

if __name__ == '__main__':
    app.run(debug=True)
