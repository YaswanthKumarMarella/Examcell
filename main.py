from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pandas

app = Flask(__name__)


@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/assignDuties")
def assignDuties():
    return render_template("assignDuties.html")

@app.route("/assignDuties", methods= ["POST"])
def postAssignDuties():
    print(request.form)
    form = request.form
    col_names = ['name', 'day', '1','2','3','4']
    df = pandas.read_csv('faculty.csv', names =col_names, header= None)
    x = df[(df['day'] == form['day'])& (df['1'] == 0)]
    return render_template("assignDuties.html", data = x.values.tolist())


@app.route("/updateTimeTable")
def updateTimeTables():
    return render_template("updateTimeTable.html")

@app.route("/updateTimeTable", methods = ["POST"])
def setUpdateTimeTables():
    try :
        f = request.files['faculty']
        f.save('faculty.csv')
        return render_template("updateTimeTable.html", message = "updated successfully")
    except Exception as e:
        print("error is ", e)
        return render_template("updateTimeTable.html", message = "update failed !!!!")


@app.route("/get-fac")
def get_fac():
    try:
        dt = pandas.read_csv("faculty.csv")
        return render_template("fac-list.html", data = dt.values.tolist())
    except:
        return render_template("fac-list.html", data = "not found")

if __name__ == '__main__':
    app.run(debug=True)