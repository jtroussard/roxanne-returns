import os
import psycopg2
import psycopg2.extras

from lib.config import *
from lib import data_postgresql as pg

from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')

members = [{}]
logged = False;
user = ['','']


@app.route('/', methods=['GET', 'POST'])
def mainIndex():
    # user attempts login
    # send/rec data to db
    if request.method == 'POST':
        login_result = pg.login_member(request.form['fn'], request.form['pass']);
        # if successful set session variables, modify user variable
        # finally render bdashboard
        if (login_result):
            session['username'] = login_result[0][1]
            session['userlast'] = login_result[0][2]
            session['userlocation'] = login_result[0][4]
            user = [session['username'], session['userlast']]
            logged = True;
            return render_template('dashboard.html', selected='', error=False, user=user, logged=logged)
        # if failure set user and logged to defaults, flip error bool 
        # finally render login and send error bool to notifiy user of failure
        else:
            user = ['', '']
            logged = False;
            return render_template('login.html', selected='', error=True, user=user)
    
    # default render        
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False
    return render_template('index.html', selected='home', user=user, logged=logged)

@app.route('/error')
def mainError():
    print ("==========\nStart - mainError:")
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False
    return render_template('error.html', user=user, logged=logged)
    
@app.route('/about')
def mainAbout():
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False

    return render_template('about.html', selected='about', user=user, logged=logged)

@app.route('/blog')
def mainBlog():
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False

    return render_template('blog.html', selected='blog', user=user, logged=logged)

@app.route('/meet')
def mainMeet():
    print ("==========\nStart - mainMeet:")
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False
    showMonth = "April"
    isPresent = False
    shows = {'date': 'April 6-9', 'location': 'The Charlotte Motor Speedway', 'address': '5555 Concord Pkwy S, Concord, NC 28027', 'name': 'Charlotte AutoFair',
             'description': 'These events provide collector car Flea Market Vendor spaces to buy and sell restoration parts and supplies for almost any vehicle ever produced - in addition to Car Corral vehicle spaces on the track oval for buying and selling collector vehicles of all descriptions! The collector car Flea Market includes everything automotive, including memorabilia, vintage signs, tires, wheels, automotive toys, restoration supplies, tools, and classic cars for sale!'}
    if 'username' in session:
        user = [session['username'], session['userlast']]
    else:
        user = ['', '']
    return render_template('meet.html', selected='meet', showMonth=showMonth, show=shows, isPres=isPresent, user=user, logged=logged)

@app.route('/form', methods=['GET', 'POST'])
def mainForm():
    if request.method == 'POST':
        members.append({'first': request.form['first'], 'last': request.form[
                       'last'], 'year': request.form['year'], 'model': request.form['model']})
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
        return render_template('form2.html', selected='form', members=members, user=user, logged=logged)
    else:
        user = ['', '']
        logged = False
        return render_template('form.html', selected='form', members=members, user=user, logged=logged)

@app.route('/form2', methods=['POST', 'GET'])
def reply():
    thename = request.form['first']
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False
    print(request.form)
    insert_result = pg.add_member(request.form['first'], request.form[
                                  'last'], request.form['email'], request.form['zip'], request.form['year'], request.form['model'], request.form['pass'])
    if insert_result == None:
        print("There was an error executing insert command")
        return render_template('error.html', user=user, logged=logged)
    else:
        print("Member add to database SUCCESSFUL")
        select_results = pg.get_member_list()
    if select_results != None:
        print("Member list return SUCCESSFUL")
        return render_template('form2.html', name=thename, members_list=select_results, user=user, logged=logged)
    else:
        print("There was an error executing select command")
        return render_template('error.html', user=user, logged=logged)
    if logged:
        select_results = pg.get_member_list()
        print("Member list return SUCCESSFUL")
        return render_template('form2.html', name=thename, members_list=select_results, user=user, logged=logged)

@app.route('/vids')
def mainVids():
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False
    videos = [{'title': 'Famous GTOs: Walking Dead', 'link': 'hYHYW-vcIMw?start=107&end=155'},
              {'title': 'Quarter Mile Action', 'link': 'kEVJV8BFnpw?start=21'},
              {'title': 'Nice Example of Restored GTO',
               'link': 'HT7bKCTxUhM?start=9'},
              {'title': 'Paul Cangialosi explains Gear Ratios', 'link': 'RyOWKW21I0c'}]

    return render_template('vids.html', selected='vids', vids=videos, user=user, logged=logged)
    
@app.route('/login')
def mainLogin():
    error = False
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False

    return render_template('login.html', selected='form', user=user, logged=logged)
    
@app.route('/dashboard', methods=['POST'])
def mainDash():
    print ("==========\nStart - mainDash:")
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False
        
    # checking logged status
    if logged:
        selection = request.form["dash_option"]
        print ("\n\tmainDash-> if logged True\n\tvar logged = {}".format(logged))
        if selection == "search":
            print ("\n\t\tmainDash-> if selection == search\n\t\tvar selection = {}".format(selection))
            print ("\n\t\tmainDash-> return render_template('market.html', user=user)\n\t\tvar user = {}\nEND mainDash".format(user))
            return render_template('market.html', user=user, logged=logged)
        else:
            print ("\n\t\tmainDash-> else selection == search\n\t\tvar selection = {}".format(selection))
            print ("\n\t\tmainDash-> return render_template('market.html', user=user)\n\t\tvar user = {}\nEND mainDash".format(user))
            return render_template('market_post.html', user=user, logged=logged)
    else:
        print ("\n\tmainDash-> else logged True\n\tvar logged = {}".format(logged))
        print ("\n\tmainDash-> return render_template('login.html', user=user)\n\t\tvar user = {}\nEND mainDash".format(user))
        return render_template('login.html', user=user, logged=logged)
    
    # default render
    print ("\nmainDash-> (default render)\nEND mainDash")
    return render_template('dashboard.html', user=user, logged=logged)

@app.route('/market', methods=['GET', 'POST'])
def mainMarket():
    print ("==========\nStart - mainMarket:")
    if 'username' in session:
        user = [session['username'], session['userlast']]
        logged = True
    else:
        user = ['', '']
        logged = False
    config_values = {}
    if request.method == 'POST':
        search_term = request.form['search']
        loc_search = request.form['location_switch']
        results = pg.search_market(search_term, loc_search, session['userlocation'])
        config_values['header_01'] = "Description";
        config_values['header_02'] = "Price";
        config_values['header_03'] = "Location";
        print ("\n\tmainDash-> if POST\n\tvar search_term = {}\n\tvar config_v['header_01'] = {}\n\tvar config_v['header_02'] = {}".format(search_term,config_values['header_01'],config_values['header_02']))
        return render_template('/market.html', user=user, logged=logged, config=config_values, test_return=search_term, results=results)
    return render_template('/market.html', user=user, config=config_values, logged=logged)

# start the server
if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)
