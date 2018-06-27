from flask import Flask, request, render_template, redirect, session, send_file
from flaskext.mysql import MySQL
from flask_qrcode import QRcode
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

qrcode = QRcode(app)
mysql = MySQL()


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ppsi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>

    msg = Message('E-Ticket Evenet', sender = 'dianbagus96@gmail.com', recipients = ['heartworkscreative@gmail.com'])
    msg.body = ""
    msg.html = render_template('/mail.html')
    mail.send(msg)

    data = request.args.get('data', 'hai')
    print(data)
    return send_file(
        qrcode(data, mode='raw'),
        mimetype='image/png'
    )

@app.route('/', methods=['GET'])
def home():
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cur = cursor.execute(
        "SELECT id, category_name FROM tm_category WHERE status='00'")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about-us.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact-us.html')

@app.route('/event', methods=['POST', 'GET'])
def event():
    conn = mysql.connect()
    cursor = conn.cursor()

    data = request.form
    type_event = ""
    sel_gender = ""
    selected = ""
    sel_gen=""
    sel_mine=""
    mine=""
    participant=""

    if data.get('filters[sport_type_id]') is not None:
        selected = data.get('filters[sport_type_id]')
        if selected == '':
            type_event = ""
        else:
            type_event = " AND id_category = '" + data.get('filters[sport_type_id]') + "'"

    if data.get('filters[division]') is not None:
        sel_gen = data.get('filters[division]')
        if sel_gen == '':
            sel_gender = ""
        else:
            sel_gender = " AND gender = '" + data.get('filters[division]') + "'"

    if data.get('filters[sport_mine]') is not None:
        sel_mine = data.get('filters[sport_mine]')
        
        if sel_mine == 'participant':
            
            sql_participant = 'SELECT id_event FROM tx_participants WHERE email="'+session['username']+'"'
            cursor.execute(sql_participant) 
            idevent = cursor.fetchall()
            print('participant')
            a = "0"
            for row in idevent:
                a = a + ","+ str(row[0])

            participant=" AND A.id IN ("+a+") "
        elif sel_mine == 'event':
            mine = " AND id_user = '" + str(session['id']) + "'"
        else:
            mine = ""

    sql = "SELECT id, category_name FROM tm_category WHERE status = '00'"
    cursor.execute(sql)
    data = cursor.fetchall()

    sql_city = "SELECT province FROM tm_event GROUP BY province"
    cursor.execute(sql_city)
    city = cursor.fetchall()

    sql_event = "SELECT id_user, province, city, title, price, a.STATUS, gender, B.category_name, A.id FROM tm_event A LEFT JOIN tm_category B ON B.id = A.id_Category WHERE 1=1 " + type_event + sel_gender + mine + participant
    print(sql_event)
    cursor.execute(sql_event)
    event = cursor.fetchall()
    conn.close()

    return render_template('/partners/seassons.html', data=data, event=event, city=city, selecte=selected, select_gender=sel_gen, sel_mine=sel_mine)


@app.route('/login', methods=['GET'])
def signin():
    return render_template('/sign_in.html')

@app.route('/login', methods=['POST'])
def signin_post():
    conn = mysql.connect()
    cursor = conn.cursor()
    data = request.form
    
    user = data.get('identity[email]')
    pswd = data.get('identity[password]')

    sql_cek = "SELECT id FROM tm_user WHERE email='"+ user +"' AND password='"+ pswd +"' "
    print(sql_cek)
    cursor.execute(sql_cek)
    count = cursor.rowcount
    hasil = cursor.fetchall()
    
    conn.close()
    
    if count != 0:
        session['username'] = user
        session['passwrod'] = pswd
        session['id'] = hasil[0][0]    
        return redirect('/')
    else:
        return render_template('/sign_in.html')

@app.route('/register', methods=['GET'])
def signup():
    return render_template('/sign_up.html')


@app.route('/register', methods=['POST'])
def signup_post():
    data = request.form

    gender = data.get('identity[gender]')
    f_name = data.get('identity[first_name]')
    l_name = data.get('identity[last_name]')
    email = data.get('identity[email]')
    phone = data.get('identity[phone]')
    pswd = data.get('identity[password]')

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tm_user(id, gender, first_name, last_name, email, mobile, password, status) VALUES ('',%s,%s,%s,%s,%s,%s, %s)""", (gender, f_name, l_name, email, phone, pswd, '00'))
    conn.commit()

    return render_template('/sign_in.html')


@app.route('/detail/<id>', methods=['GET'])
def detail(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql_event = "SELECT id_user, province, city, title, price, a.STATUS, gender, B.category_name, A.id, max_join, DATE_FORMAT(date_from, '%W, %M %e %Y') , DATE_FORMAT(date_to, '%W, %M %e %Y'), price_before, register_needed,  A.id, time_from,time_to FROM tm_event A LEFT JOIN tm_category B ON B.id = A.id_Category WHERE A.id='" + id + "' "
    cursor.execute(sql_event)
    event = cursor.fetchall()

    sql_comment = "SELECT B.image_uri, A.comment, DATE_FORMAT(date_time, '%W, %M %e %Y'), CONCAT(B.first_name, ' ', B.last_name)  FROM th_review A LEFT JOIN tm_user B ON B.id = A.id_user WHERE A.id_event='"+id+"' ORDER BY date_time LIMIT 1"
    cursor.execute(sql_comment)
    comment = cursor.fetchall()
    
    conn.close()
    return render_template('/leagues/2130.html', data=event, comment=comment)

@app.route('/news', methods=['GET'])
def news():
    return render_template('/leagues/new.html')

@app.route('/news/<id>', methods=['GET'])
def news_edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql_event = "SELECT B.category_name, A.province, A.city, A.title, A.max_join, A.date_from, A.date_to,time_from,time_to, A.gender, register_needed, A.price, A.price_before, A.id  FROM tm_event A LEFT JOIN tm_category B ON B.id = A.id_Category WHERE A.id='" + id + "' "
    cursor.execute(sql_event)
    event = cursor.fetchall()
    
    conn.close()
    return render_template('/leagues/edit.html', event=event)


@app.route('/news/<id>', methods=['POST'])
def news_edit_post(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    data = request.form
    
    province = data.get('location')
    title = data.get('title')
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    time_from = data.get('time_start')
    time_to = data.get('time_end')
    price_before = data.get('price_before')
    price = data.get('price')
    gender = data.get('gender')
    #id_category = data.get('id_category')
    id_category = '1'
    max_join = data.get('player')
    register_needed = data.get('isregister')
    iduser = session['id']
    city = data.get('city')

    sql_update = "UPDATE tm_event SET id_category='"+id_category+"', province='"+province+"', city='"+city+"', title='"+title+"', max_join='"+max_join+"', date_from='"+date_from+"', date_to='"+date_to+"', time_from='"+time_from+"', time_to='"+time_to+"', gender='"+gender+"', register_needed='"+register_needed+"', price='"+price+"', price_before='"+price_before+"' WHERE id = '"+id+"'"
    print(sql_update)
    cursor.execute(sql_update)
    conn.commit()

    conn.close()
    return redirect('/detail/'+id)


@app.route('/news', methods=['POST'])
def news_post():
    data = request.form
    
    conn = mysql.connect()
    cursor = conn.cursor()

    sql_select = 'SELECT id FROM tm_user WHERE email = "'+ session['username']+'"'
    cursor.execute(sql_select)
    user = cursor.fetchall()
    
    print(data)

    province = data.get('location')
    title = data.get('title')
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    time_from = data.get('time_start')
    time_to = data.get('time_end')
    price_before = data.get('price_before')
    price = data.get('price')
    gender = data.get('gender')
    #id_category = data.get('id_category')
    id_category = '1'
    max_join = data.get('player')
    register_needed = data.get('isregister')
    status = '00'
    iduser = user[0][0]
    city = data.get('city')

    print( province, title, date_from, date_to, time_from, time_to, price_before, price, gender, id_category, max_join, register_needed, status)

    sql_insert="INSERT INTO tm_event(id_user, province, title, date_from, date_to, time_from, time_to, price_before, price, gender, id_category, max_join, register_needed, status, city) VALUES('"+str(iduser)+"', '"+province+"', '"+title+"', '"+date_from+"', '"+date_to+"', '"+time_from+"', '"+time_to+"', '"+price_before+"', '"+price+"', '"+gender+"', '"+id_category+"', '"+max_join+"', '"+register_needed+"', '"+status+"', '"+city+"')"
    print(sql_insert)
    cursor.execute(sql_insert)
    conn.commit()

    conn.close()
    return redirect('/event')


@app.route('/rsvp/<id>', defaults={'err': None})
@app.route('/rsvp/<id>/<err>', methods=['GET'])
def rsvp(id, err):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql_event = "SELECT id_user, province, city, title, price, a.STATUS, gender, B.category_name, A.id, max_join, DATE_FORMAT(date_from, '%W, %M %e %Y') , DATE_FORMAT(date_to, '%W, %M %e %Y'), price_before, register_needed,  A.id FROM tm_event A LEFT JOIN tm_category B ON B.id = A.id_Category WHERE A.id='" + id + "' "
    cursor.execute(sql_event)
    event = cursor.fetchall()

    sql_comment = "SELECT B.image_uri, A.comment, DATE_FORMAT(date_time, '%W, %M %e %Y'), CONCAT(B.first_name, ' ', B.last_name)  FROM th_review A LEFT JOIN tm_user B ON B.id = A.id_user WHERE A.id_event='"+id+"' ORDER BY date_time LIMIT 1"
    cursor.execute(sql_comment)
    comment = cursor.fetchall()
    
    conn.close()

    data = request.args.get('data', 'hai')

    return render_template('/leagues/rsvp.html', data=event, comment=comment, err=err)

@app.route('/rsvp/<id>', methods=['POST'])
def rsvp_post(id):
    data = request.form
    
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql_cek = "SELECT id FROM tx_participants WHERE (email='"+data.get('identity[email]')+"' OR mobile = '"+data.get('identity[last_name]')+"') AND status = '00' AND id_event='"+id+"'"
    cursor.execute(sql_cek)
    
    if cursor.rowcount != 0:
        conn.close()
        return redirect('/rsvp/'+id+'/1')
    else:
        sql_insert = "INSERT INTO tx_participants(id_event, first_name, last_name, email, mobile, status) VALUES('"+id+"', '"+data.get('identity[first_name]')+"', '"+data.get('identity[last_name]')+"', '"+data.get('identity[email]')+"', '"+data.get('identity[phone]')+"', '00')"        
        cursor.execute(sql_insert)
        conn.commit()

        conn.close()
        return redirect('/qrcode')

@app.route('/del/<id>')
def desl(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql_delete = "DELETE FROM tm_event WHERE id= '"+str(id)+"'"
    cursor.execute(sql_delete)
    conn.commit()
    return redirect('/event')

if __name__ == "__main__":
    createBarCodes()
    app.run(debug=True)
