from flask import Flask, redirect, url_for, render_template, request, session
from Connection import connectToSQLServer


app = Flask(__name__)
app.secret_key = 'Hello'

@app.route('/home', methods = ['POST', 'GET'])
def home():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['message']

         #Database connection
        conn = connectToSQLServer()
        cursor = conn.cursor()
        cursor.execute("INSERT into dbo.User_Query values ('%s', '%s', '%s', '%s')" % (name, email, subject, msg))
        conn.commit()
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        subject = "Contacting address details"
        body = "Dear Admin,  This is the mail regarding the questions asked for the details"
        sender_email = "smtp@noreply.com"
        receiver_email = "sugreev1996@gmail.com"
        password = "Suggi@218"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

         # Add body to email
        regards = 'Thank you ' \
                   'Noreply.com'
        message.attach(MIMEText(body, "plain"))
        message.attach(MIMEText(msg, "plain"))
        message.attach(MIMEText(email, 'plain'))
        message.attach(MIMEText(regards, 'plain'))
        text = message.as_string()
        with smtplib.SMTP("localhost", 25) as server:

            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)


        return redirect(url_for("user"))
    else:
        return render_template("Home.html")

@app.route('/Login', methods = ['POST','GET'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['pass']
            conn = connectToSQLServer()
            cursor = conn.cursor()
            cursor.execute("select * from dbo.Form_Login where Username = '%s' and pass = '%s'" % (username,password))
            for row in cursor:
                session['user'] = row[0]
                if str(row[0]) == '1':
                    return redirect(url_for("admin"))
                elif str(row[0]) == '2':
                    return redirect(url_for("user"))
                elif str(row[0] == ''):
                    print("<script>You Have entered wrong Username or Password</script>")
                    return render_template("Login.html")
                else:
                    return render_template("Login.html")
        else:
            return render_template("Login.html")
    except TypeError:
        return render_template("Login.html")


@app.route('/admin')
def admin():
    for usr in session:
        u = session[usr]
        if str(u) == '1':
            print('In the admin block')

            return render_template('admin.html')
        else:
            print('In the login block')
            return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/user')
def user():
    for username in session:
        usr = session[username]
        if str(usr) == '2':
            return render_template('user.html')
        else:
            return redirect(url_for('login'))

    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug='true')