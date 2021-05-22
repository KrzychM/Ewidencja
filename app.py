from flask import Flask, request, url_for, redirect, render_template, g, flash
import sqlite3

app = Flask(__name__)

SECRET_KEY = 'UHl0aG9uIERldmVsb3Blcg'

def get_db():
    
    if not hasattr(g, 'sqlite_db'):
        connection = sqlite3.connect('ewidencja.db')
        connection.row_factory = sqlite3.Row
        g.sqlite_db = connection
    return g.sqlite_db


@app.route('/')
def index():

    
    db = get_db()
    rec = db.execute('select * from ewidencja where czyus=0')    
    db.commit()    

    rows = rec.fetchall()

    ilosc = len(rows)  
    db.close()  
   
    return render_template('index.html',rows=rows,ilosc=ilosc) 

@app.route('/new')
def new():
    return render_template('new.html')
    

@app.route('/addnew',methods = ['POST','GET'])
def addnew():
        if request.method == 'POST':
            f_nazwa = request.form['nazwa']
            f_nrew = request.form['nrew']
            f_nrser = request.form['nrser']
            f_zdalna = request.form['zdalna']
            f_wyposazenie = request.form.getlist('wyposazenie')
            f_d_wydania = request.form['d_wydania']
            f_IT_wydal = request.form['IT_wydal']
            f_odb = request.form['odb']
            f_pok = request.form['pok']
            f_stanowisko = request.form['stanowisko']
            f_dzial = request.form['dzial']
            f_w_uwagi = request.form['w_uwagi']
            
            
            f_wyp = ','.join(f_wyposazenie)

            db = get_db()
            try:
                sql_command = '''INSERT into ewidencja 
                                    (nazwa,
                                    nrew,
                                    nrser,
                                    zdalna,
                                    wyposazenie,
                                    d_wydania,
                                    IT_wydal,
                                    odb,
                                    pok,
                                    Stanowisko,
                                    dzial,
                                    wyd_uwagi) values (?,?,?,?,?,?,?,?,?,?,?,?)'''
                
                new_rec = db.execute(sql_command,(f_nazwa,f_nrew,f_nrser,f_zdalna,f_wyp,f_d_wydania,f_IT_wydal,f_odb,f_pok,f_stanowisko,f_dzial,f_w_uwagi))
                db.commit()
            except:    
                db.close() 
     
        return redirect('/') 
                 

@app.route('/edit/<id>',methods = ['POST','GET'])
def edit(id):
    if request.method == 'POST':
    
            f_nazwa = request.form['nazwa']
            f_nrew = request.form['nrew']
            f_nrser = request.form['nrser']
            f_zdalna = request.form['zdalna']
            f_wyposazenie = request.form['wyp']
            f_d_wydania = request.form['d_wydania']
            f_IT_wydal = request.form['IT_wydal']
            f_odb = request.form['odb']
            f_pok = request.form['pok']
            f_stanowisko = request.form['stanowisko']
            f_dzial = request.form['dzial']
            f_w_uwagi = request.form['w_uwagi']
            f_d_zwrotu = request.form['d_zwrotu']
            f_IT_zwrot = request.form['IT_zwrot']
            f_z_uwagi = request.form['z_uwagi']
            db = get_db() 

            # zamiana listy na string
            # f_wyp = ','.join(f_wyposazenie)   
            
            try:   
                sql_command = '''update ewidencja 
                                 set nazwa = ?,
                                 nrew = ?, 
                                 nrser = ?,
                                 zdalna = ?,
                                 d_wydania = ?,
                                 odb = ?,
                                 pok =?,
                                 Stanowisko = ?,
                                 dzial = ?,
                                 wyd_uwagi = ?,
                                 d_zwrotu = ?,
                                 IT_zwrot = ?,
                                 zw_uwagi = ?,
                                 wyposazenie =?,
                                 IT_wydal = ?
                            

                                 where ewidencja.id=?'''
                e_rec = db.execute(sql_command,(f_nazwa,f_nrew,f_nrser,f_zdalna,f_d_wydania,f_odb,f_pok,f_stanowisko,f_dzial,f_w_uwagi,f_d_zwrotu,f_IT_zwrot,f_z_uwagi,f_wyposazenie,f_IT_wydal,id))    
                db.commit()
            except:    
                db.close()
            return redirect('/')

    else:
        db = get_db()

        sql_command = 'select * from ewidencja where ewidencja.id=?'

        e_rec = db.execute(sql_command,(id,))
        e_rows = e_rec.fetchone()
        
        
        return render_template('edit.html',id=id,e_rows=e_rows)

@app.route('/zwrot/<id>')
def zwrot(id):
    db = get_db()

    sql_command = 'select * from ewidencja where ewidencja.id=?'

    zw_rec = db.execute(sql_command,(id,))

    db.commit()
    zw_rows = zw_rec.fetchall()
   
    db.close()

    return render_template('zwrot.html',id=id,zw_rows=zw_rows)



@app.route('/rodo/<id>')
def rodo(id):
         
    db = get_db()

    sql_command = 'select * from ewidencja where ewidencja.id=?'
    
    r_rec = db.execute(sql_command,(id,))

    db.commit()
    r_rows = r_rec.fetchall()

    db.close()
    
    return render_template('rodo.html',id=id,r_rows=r_rows)

@app.route('/protokol/<id>')
def protokol(id):
       
    
    db = get_db()
    
    sql_command = 'select * from ewidencja where ewidencja.id=?'
    
    pr_rec = db.execute(sql_command,(id,))

    db.commit()
    
    pr_rows = pr_rec.fetchall()
    
    db.close()
    
    return render_template('protokol.html',id=id,pr_rows=pr_rows)


@app.route('/oswiadczenie/<id>')
def oswiadczenie(id):

    db = get_db()
    
    sql_command = 'select * from ewidencja where ewidencja.id=?'

    os_rec = db.execute(sql_command,(id,))

    db.commit()
    
    os_rows = os_rec.fetchall()
    
    db.close()


    return render_template('oswiadczenie.html',id=id,os_rows=os_rows)    

@app.route('/usun/<id>')
def usun(id):
    db = get_db()
    
    sql_command = 'update ewidencja set czyus=1 where ewidencja.id=?'
    
    del_rec = db.execute(sql_command,(id,))

    db.commit()
    
    db.close()
    
    return redirect('/')



if __name__ == '__main__':
    app.run()


