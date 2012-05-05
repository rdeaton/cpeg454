from wifimap import app, db, database
from flaskext.sqlalchemy import SQLAlchemy
from wifimap.database import *
from flask import Flask, request, flash, redirect, url_for, render_template
from flask import jsonify, session
from flaskext.wtf import Form, PasswordField, validators

class NewPassOnlyForm(Form):
    new_pass = PasswordField('Password', 
                        validators = [validators.Length(min=8, max=50, message='Password length must be between 8 and 50'),
                            validators.CrackLib()])

@app.route('/api/reset_password/', methods=['GET', 'POST'])
def api_reset_password():
    username = request.form.get('username', None)
    old_pass = request.form.get('old_password', None)
    new_pass = request.form.get('new_password', None)
    if username is None or old_pass is None:
        return jsonify(error=True)
    user = User.query.get(username)
    if user is None:
        return jsonify(error=True)
    if new_pass is None:
        if user.verify_password(old_pass):
            return jsonify(password_okay = True)
        return jsonify(password_okay = False)
    
    # Need to run new password validation here. Should use the same WTForms validators?
    f = NewPassOnlyForm()
    f.new_pass.data = new_pass
    if f.new_pass.validate(f):
        user.password = new_pass
        user.add_flag('update_password')
        return jsonify(password_reset = True)
    return jsonify(password_reset = False, message = str(f.new_pass.errors[0]))
