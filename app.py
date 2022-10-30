
# #from flask import uuid
 from flask import Flask, render_template, redirect, url_for,request
 from random import randint


 from flask_mysqldb import MySQLs
 import MySQLdb.cursors


 app = Flask(__name__, template_folder="templates")

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "12345"
app.config["MYSQL_DB"] = "patient1"

mysql = MySQL(app)


def proj(ema):
    global email
    email = ema


from flask import Flask, render_template, redirect, request




@app.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("registration.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    firstname = " "
    middlename = ""
    lastname = " "
    gender = " "
    email = ""
    birthday = " "
    pin= " "
    score = " "
    remarks = ""
    patient_id =""
   
    if request.method == "POST":
        firstname = request.form["firstname"]
        middlename = request.form["middlename"]
        lastname = request.form["lastname"]
        gender = request.form["gender"]
        email = request.form["email"]
        birthday = request.form["birthday"]
        pin = request.form["pin"]
        proj(email)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT patient_id from project')
        pid=cursor.fetchall()
         
        if(len(pid)>0):
            for i in pid:
                id=random_n_digits(14)
                if(id!=i):
                    cursor.execute(' INSERT INTO project VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(firstname,middlename,lastname,gender,email,birthday,pin,score,remarks,id))

                    mysql.connection.commit()
                    msg='You have successfully registered !'
                    break
                else:
                    continue
                
    else:
        id=random_n_digits(14) 
        cursor.execute(
            " INSERT INTO project VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                firstname,
                middlename,
                lastname,
                gender,
                email,
                birthday,
                pin,
                score,
                remarks,
                id,
            ),
        )
        mysql.connection.commit()
        #uuidOne = uuid.uuid1()
        ##print ("Printing my First UUID of version 1")
        #print(uuidOne)
    cursor.execute('SELECT patient_id from project WHERE email=%s',[email])
    patient_id= cursor.fetchone()
    return render_template('index.html',id=id)
def random_n_digits(s):
    range_start = 10**(s-1)
    range_end = (10**s)-1
    return randint(range_start, range_end)
   # return render_template("index.html")


@app.route("/index", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        num3 = request.form.get("num3")
        num4 = request.form.get("num4")
        num5 = request.form.get("num5")
        num6 = request.form.get("num6")
        score = int(num1) + int(num2)+int(num3)+int(num4) + int(num5)+int(num6)
        # global add
        add=score  
        # global res
        res=" "
        if score>4:
            res="screening needed"
            
        else:
            res="no need to screen"

        cursor = mysql.connection.cursor()
        #cursor.execute(''' INSERT INTO user VALUES(%f)''',(add))
        cursor.execute('UPDATE project SET score = %s, remarks =%s  WHERE email=%s',(score,res,email))
        #cursor.execute('UPDATE user SET  username =% s, password =% s, email =% s,  WHERE id =% s', (username, password, email(session['id'], ), ))
        mysql.connection.commit()
        return render_template('result.html', add1=add,res=res,em=email)
    return render_template('index.html')



@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('registration.html')


if __name__ == "__main__":
   
     app.run(debug=True)
