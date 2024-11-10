from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file, Response
import pandas

app = Flask(__name__)

#constants
COL_NAMES = ['id', 'name', 'day','1','2','3','4', '5', '6', '7']


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
    pd = pandas.read_csv('faculty.csv', names =COL_NAMES, header= None)
    x = pd[(pd['day'] == form['day'])&(pd['2'].isin([form['year'], '0'])) &(pd['1'].isin(['0', form['year']]))]
    if x.empty:
        return render_template("assignDuties.html", message = "no data found")
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
        return render_template("updateTimeTable.html", message = "update failed check columns or file data !!!!")


@app.route("/get-fac")
def get_fac():
    try:
        dt = pandas.read_csv("faculty.csv", names = COL_NAMES)
        return render_template("fac-list.html", data = dt.values.tolist())
    except Exception as e:
        print(e)
        return render_template("fac-list.html", data = "not found")
    
@app.route("/download")
def downloadFile():
    dt = pandas.read_csv("faculty.csv")
    resp = Response(dt.to_csv(), mimetype='text/csv')
    resp.headers.set("Content-Disposition", "attachment", filename="data.csv")
    return render_template("ex.html", link = resp)

@app.route("/select-fac", methods = ['post'])
def select_fac():
    fac_list = request.form.getlist('fac-id')
    df = pandas.read_csv('faculty.csv', names=COL_NAMES)
    data = df.loc[df['id'].isin(fac_list), ['id', 'name']].drop_duplicates().values.tolist()
    return render_template("free.html", data = data)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)