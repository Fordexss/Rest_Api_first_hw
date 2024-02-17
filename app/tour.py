from flask import Flask, jsonify
from flask import render_template, request, redirect, url_for
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tours.db'
db = SQLAlchemy(app)


class TourApi(Resource):
    def get(self):
        tours = Tour.query.all()
        tours_data = [{
            'title': tour.title,
            'description': tour.description
        } for tour in tours]
        return jsonify(tours_data)


class OrderApi(Resource):
    def get(self):
        orders = Order.query.all()
        booked_tours_data = [{
            'tour_title': order.tour_title,
            'surname': order.surname,
            'name': order.name,
            'date': order.date
        } for order in orders]
        return jsonify(booked_tours_data)


class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    tour_title = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(10), nullable=False)

    tour = db.relationship('Tour', backref=db.backref('orders', lazy=True))


with app.app_context():
    db.create_all()


@app.route('/api/booked_tours', methods=['GET'])
def api_booked_tours():
    orders = Order.query.all()
    booked_tours_data = []

    for order in orders:
        booked_tours_data.append({
            'tour_title': order.tour_title,
            'surname': order.surname,
            'name': order.name,
            'date': order.date
        })

    return jsonify(booked_tours_data)


@app.route('/api/tours_summary', methods=['GET'])
def api_tours_summary():
    tours = Tour.query.all()
    tours_summary_data = [{
        'title': tour.title,
        'description': tour.description
    } for tour in tours]
    return jsonify(tours_summary_data)


# тест
@app.route('/api/data1', methods=['GET'])
def api_page1():
    data = {"message": "Це дані для першої сторінки API."}
    return jsonify(data)


# тест
@app.route('/api/data2', methods=['GET'])
def api_page2():
    data = {"message": "Це дані для другої сторінки API."}
    return jsonify(data)


@app.route('/')
def index():
    tours = Tour.query.all()
    return render_template('index.html', tours=tours)


@app.route('/booked_tours')
def booked_tours():
    orders = Order.query.all()
    return render_template('booked_tours.html', booked_tours=orders)


@app.route('/add_tour', methods=['GET', 'POST'])
def add_tour():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image = request.form.get('image')

        new_tour = Tour(title=title, description=description, image=image)
        db.session.add(new_tour)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_tour.html')


@app.route('/tour/<int:tour_id>', methods=['GET', 'POST'])
def view_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)

    if request.method == 'POST':
        surname = request.form.get('surname')
        name = request.form.get('name')
        date = request.form.get('date')
        tour_title = request.form.get('tour_title')

        order = Order(tour_id=tour_id, surname=surname, name=name, date=date, tour_title=tour_title)
        db.session.add(order)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('view_tour.html', tour=tour)


if __name__ == '__main__':
    app.run(debug=True)
