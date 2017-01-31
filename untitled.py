
from flask import Flask, render_template, request
from flask import session as login_session
from model import * 


app = Flask(__name__)


@app.route("/")
@app.route('/meet/')



@app.route('/meet/<name>')
def hello(name=None):
    return render_template('meet.html', name=name)

def verify_password(email,password):
	member = session.query(Member).filter_by(email= email).first()
	if not member or not member.verify_password(password):
		return False
	else:
		return True
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email is None or password is None:
			flash('Missing Arguments')
			return redirect(url_for(login))
		if verify_password(email, password):
			member = session.query(Member).filter_by(email=email).one()
			flash('Login Successful, welcome, %s' % member.name)
			login_session['name'] = member.name
			login_session['email'] = member.email
			login_session['id'] = member.id
			return redirect(url_for('inventory'))
		else:
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))

@app.route('/newcustomer' methods = ['GET', 'POST'])
def newCustomer():
	if request.method == 'GET':
		





if __name__ == '__main__':
	app.run(debug=True)
