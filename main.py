
from flask import flash, redirect, Flask, render_template, request, url_for
from flask import session as login_session
from model import * 



app = Flask(__name__)

app.secret_key='this is my password'

#email serever:
"""MAIL_SERVER =  'smtp.googlemail.com'
MAL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

#admin list:
ADMINS = ['gidonschreiber@gmail.com']"""
@app.route("/")
def main():
    return render_template('meet.html')

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
			return redirect(url_for('myProfile'))
		else:
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))

@app.route('/newcustomer', methods = ['GET', 'POST'])
def newMember():
	if request.method == 'GET':
		return render_template('newMember.html')
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		verify = request.form['verify']
		if name == "" or email == "" or password == "":
			flash("Your form is missing arguments")
			return redirect(url_for('newMember'))
        if session.query(Member).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newMember'))
        if verify != password:
        	flash("Your two passwords do not match!")
        	return redirect(url_for('newMember'))
        member = Member(name = name, email=email)
        member.hash_password(password)
        session.add(member)
        session.commit()
        return redirect(url_for('login'))

@app.route('/myprofile', methods  = ['GET', 'POST'] )
def myProfile():
	if "id" not in login_session:
		flash("You must be logged in to view this page")
		return redirect(url_for("login"))
	else:
		members = session.query(Member).filter_by(email= login_session["email"]).first()
		myEvents = session.query(Event).filter_by(owner_id = login_session["id"]).all()
		return render_template("myProfile.html", myEvents = myEvents, members = members)
		

@app.route('/addEvent', methods = ['GET', 'POST'])
def addEvent():
	if request.method == 'GET':
		members = session.query(Member).all()
		return render_template("addEvent.html", members = members)
	else:
		name = request.form['name']
		location = request.form['location']
		date = request.form['date']
		invitees = request.form.getlist('memberNames')
		newEvent = Event(name = name, date = date, owner_id = login_session['id'])
		session.add(newEvent)
		for invitee in invitees:
			assoc = InvitesAssociation(member_id = invitee, event_id = newEvent.id , attending = False)
			session.add(assoc)
		session.commit()
		flash('succesfully created event!')
		return redirect(url_for('myProfile'))

		
if __name__ == '__main__':
	app.run(debug=True)
