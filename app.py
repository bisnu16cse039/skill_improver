from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from data import Catagories
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
Catagories = Catagories()

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'skill_improver_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/about")
def about():
   return render_template("about.html")


@app.route('/catagories')
def catagories():
    cur = mysql.connection.cursor()

    # Get Catagories
    result = cur.execute("SELECT * FROM catagories")

    catagories = cur.fetchall()

    if result > 0:
        return render_template('catagories.html', catagories=catagories)
    else:
        msg = 'No Catagories Found'
        return render_template('catagories.html', msg=msg)

    cur.close()


#Single Catagory
@app.route('/catagory/<string:id>/')
def catagory(id):
    cur = mysql.connection.cursor()

    # Get catagory
    result = cur.execute("SELECT * FROM catagories WHERE id = %s", [id])

    catagory = cur.fetchone()

    return render_template('catagory.html', catagory=catagory)

class RegisterForm(Form):
    name=StringField('name', [validators.length(min=1,max=50)])
    username=StringField('username', [validators.length(min=4,max=25)])
    email=StringField('email', [validators.length(min=6,max=50)])
    password = PasswordField('password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message="password do not match")
    ])
    confirm=PasswordField('confirm password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, user_name, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE user_name = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    # Show catagories only from the user logged in
    result = cur.execute("SELECT * FROM catagories WHERE author = %s", [session['username']])

    catagories = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', catagories=catagories)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)

    cur.close()


class CatagoryForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


@app.route('/add_catagories', methods=['GET', 'POST'])
@is_logged_in
def add_catagories():
    form = CatagoryForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO catagories(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        mysql.connection.commit()

        cur.close()

        flash('Catagory Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_catagories.html', form=form)

@app.route('/edit_catagory/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_catagory(id):
    cur = mysql.connection.cursor()

    # Get catagory by id
    result = cur.execute("SELECT * FROM catagories WHERE id = %s", [id])

    catagory = cur.fetchone()
    cur.close()
    # Get form
    form = CatagoryForm(request.form)

    # Populate catagory form fields
    form.title.data = catagory['title']
    form.body.data = catagory['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)

        cur.execute ("UPDATE catagories SET title=%s, body=%s WHERE id=%s",(title, body, id))

        mysql.connection.commit()

        cur.close()

        flash('Catagory Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_catagory.html', form=form)

@app.route('/delete_catagory/<string:id>', methods=['POST'])
@is_logged_in
def delete_catagory(id):
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM catagories WHERE id = %s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Catagory Deleted', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)



