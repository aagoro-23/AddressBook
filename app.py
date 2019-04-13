#importing modules from flask to create an interface; MySQL to access database; wtforms to create form class; and yaml to store sensitive database info
from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
import yaml

#initiating flask app
app = Flask(__name__)

#yaml file storing database delicate information
db = yaml.load(open('db.yaml'))

#database configuration
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

#initiating MySQL
mysql = MySQL(app)
	
#contact form class
class contactForm(Form):
	organisation = StringField('organisation', [validators.Length(min=1,max=50)])
	name = StringField('name', [validators.Length(min=1,max=50)])
	email = StringField('email', [validators.Length(min=1,max=50)])
	phonenumber = StringField('phonenumberhone', [validators.Length(min=1,max=50)])
	
	
#creating add method to add items to the address book
@app.route("/add", methods=['GET','POST'])
def add():
	form = contactForm(request.form)
	if request.method == 'POST' and form.validate():
		organisation = form.organisation.data
		name = form.name.data
		email = form.email.data
		phonenumber = form.phonenumber.data
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO contacts(organisation,name,email,phonenumber) VALUES(%s,%s,%s,%s)",(organisation,name,email,phonenumber))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('index'))
	return render_template('add.html')

#search method to look for Contacts in data base and display them in a table.
@app.route('/search', methods=['POST', 'GET'])
def search():	
	try:
		if request.method =='POST':
			searchRequest = request.form
			result = searchRequest['result']
			cur = mysql.connection.cursor()	
			cur.execute("""SELECT * FROM contacts WHERE organisation =%s OR name =%s or email =%s or phonenumber =%s""", (request.form['result'],request.form['result'],request.form['result'],request.form['result']))
			data = cur.fetchall()
			mysql.connection.commit()
			cur.close()
			return render_template('index.html', data=data)
	except Exception as e:
		print(e)
	return render_template('index.html')

#creating an edit method to edit entries
@app.route('/edit/<string:id>', methods=['POST','GET'])
def edit(id):
	form = contactForm(request.form)
	if request.method == 'POST':
		organisation = request.form['organisation']
		name = request.form['name']
		email = request.form['email']
		phonenumber = request.form['phonenumber']
		cur = mysql.connection.cursor()
		app.logger.info(organisation)
		cur.execute("UPDATE contacts SET organisation=%s, name=%s, email=%s,phonenumber=%s WHERE id =%s",(organisation,name,email,phonenumber,id))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('index'))
		
	return render_template('edit.html', form=form)
	
#Delete method to delete entries
@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
	cur=mysql.connection.cursor()
	cur.execute("DELETE FROM contacts WHERE id=%s", [id])
	mysql.connection.commit()
	cur.close()
	return redirect(url_for('index'))

#index showing all Contacts in database.
@app.route("/", methods=['GET', 'POST'])
def index():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM contacts")
	data = cur.fetchall()
	mysql.connection.commit()
	cur.close()
	return render_template('index.html', data=data)



if __name__=="__main__":
	app.run(debug=True)