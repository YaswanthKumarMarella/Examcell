from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file, Response
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
    pd = pandas.read_csv('faculty.csv', names =col_names, header= None)
    x = pd[(pd['day'] == form['day'])&(pd['2'].isin([form['year'], '0'])) &(pd['1'].isin(['0', form['year']]))]
    return render_template("free.html", data = x.values.tolist())


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
        return render_template("updateTimeTable.html", message = "update failed check columns or file data !!!!")


@app.route("/get-fac")
def get_fac():
    try:
        dt = pandas.read_csv("faculty.csv")
        return render_template("fac-list.html", data = dt.values.tolist())
    except:
        return render_template("fac-list.html", data = "not found")
    
@app.route("/download")
def downloadFile():
    dt = pandas.read_csv("faculty.csv")
    resp = Response(dt.to_csv(), mimetype='text/csv')
    resp.headers.set("Content-Disposition", "attachment", filename="data.csv")
    return render_template("ex.html", link = resp)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)