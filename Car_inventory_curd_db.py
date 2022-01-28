from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sidd@localhost/Showroom'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Manageinfo(db.Model):
    __tablename__ = "Manageinfo"
    TagID = db.Column(db.Integer(), primary_key=True)
    Car_name = db.Column(db.String(255), nullable=False)
    Color = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.String(255), nullable=False)

    def json(self):
        return {'Tagid': self.TagID, 'Car_name': self.Car_name,
                'Color': self.Color, 'Price': self.Price}

    # def updateinfo(self, tagid, carname):
    #     updatec = Manageinfo.query.filter_by(TagID=tagid).first()
    #     updatec.Car_name = carname
    #     db.session.commit()


@app.route("/carinfo", methods=['GET', 'POST'])
def caraddpg():
    if request.method == 'POST':
        TagID = request.form.get("TagID")
        Car_name = request.form.get("Car_name")
        Color = request.form.get("Color")
        Price = request.form.get("Price")

        entry = Manageinfo(TagID=TagID, Car_name=Car_name, Color=Color, Price=Price)
        db.session.add(entry)
        db.session.commit()
    return render_template("addinfo.html")


@app.route('/showcars', methods=['GET'])
def showcarall():
    allcar = [Manageinfo.json(data_items) for data_items in Manageinfo.query.all()]
    return jsonify(allcar)


@app.route('/getcar/<int:tagid>', methods=['GET'])
def get_car(tagid):
    getcar1 = Manageinfo.json(Manageinfo.query.filter_by(TagID=tagid).first())
    return jsonify(getcar1)


@app.route('/updatecar/<int:tagid>/<carname>', methods=['GET', 'POST'])
def updatecar(tagid, carname):
    updatec = Manageinfo.query.filter_by(TagID=tagid).first()
    updatec.Car_name = carname
    db.session.commit()
    updateinfo = Manageinfo.json(Manageinfo.query.filter_by(TagID=tagid).first())
    return jsonify(updateinfo)


@app.route('/deletecar/<int:tagid>', methods=['GET', 'POST'])
def delete_car(tagid):
    dele_car = Manageinfo.query.filter_by(TagID=tagid).first()
    db.session.delete(dele_car)
    db.session.commit()
    return "data deleted"


@app.route('/Editinfo/<int:tagid>/<carname>/<color>/<price>', methods=['GET', 'POST'])
def editpg(tagid, carname, color, price):
    edit_car = Manageinfo(TagID=tagid, Car_name=carname, Color=color, Price=price)
    db.session.add(edit_car)
    db.session.commit()
    return 'Car info added successfully in database'


if __name__ == "__main__":
    app.run(debug=True)
