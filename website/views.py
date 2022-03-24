from unicodedata import category
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

# Initialize blueprint called names
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/account')
@login_required
def account():
    return render_template("account.html", user=current_user)
