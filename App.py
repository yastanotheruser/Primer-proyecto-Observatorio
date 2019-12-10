"""Reading and data display program
   .. moduleauthor:: Alejandro Burgos

"""
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
"""Creates the Flask instance.

:param __name__: Is the name of the current Python module.
"""
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
mysql = MySQL(app)

@app.route('/')
def Index():
    """This function returns all the information from the database through render_template function 
    
    :return: index.html 
    :rtype: html file
    :return: contacts --  list with the all the database objetcs 
    :rtype: list
    :return: list_name -- list with the variable´s name
    :rtype: list
    :return: list_fvar -- list with the first variable
    :rtype: list
    :return: list_svar -- list with the second variable
    :rtype: list
    """    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    f = open ('piopio.txt','r')
    f.close()
 
    list_name = []
    list_fvar = []
    list_svar = []

    for i in range(len(data)):
        """Cycle used to extract from the database the name, var1 and var2 of each point
        """        
        list_name.append(data[i][1])
        list_fvar.append(data[i][2])
        list_svar.append(data[i][3])

    graphdata = [
                        ['1', '10', '100'],
                        ['2', '20', '80'],
                        ['3', '50', '60'],
                        ['4', '70', '80']
                      ]

    return render_template('index.html', contacts = data, Result = list_name, Result2 = list_fvar, Result3 = list_svar, Graphdata = graphdata)
       
app.secret_key = 'YLGd*L-b4NS864Z[X~lC'

@app.route('/add_contact', methods=['POST'])
def add_contact():
    """Creates new points to plot, and add the points to the database
    
    :return: redirect
    :rtype: function
    """    
    if request.method == 'POST':
        name = request.form['name']
        var1 = request.form['var1']
        var2 = request.form['var2']
        f = open ('holamundo.txt','w')
        f.write(name+var1)       
        f.close()
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (name, var1, var2) VALUES (%s, %s, %s)', 
        (name, var1, var2))
        mysql.connection.commit() 
        f = open ('piopio.txt','r')
        mensaje = f.read()
        f.close()
        flash(mensaje)
        return redirect(url_for('get_forum'))                

@app.route('/edit/', methods = ['POST', 'GET'])
def get_contact():
    """Edit the name, var1 and var2 of the points to plot
    
    :param id: id of the points to edit
    :type id: int
    :return: render_template('edit-contact.html', contact = data[0])
    :rtype: function
    """ 
    id =1   
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id={0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/descargar/', methods = ['POST', 'GET'])
def get_download():
    """Edit the name, var1 and var2 of the points to plot
    
    :param id: id of the points to edit
    :type id: int
    :return: render_template('edit-contact.html', contact = data[0])
    :rtype: function
    """ 
    id =1   
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id={0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('descargar.html', contact = data)

@app.route('/versiones/', methods = ['POST', 'GET'])
def get_versiones():
    """Edit the name, var1 and var2 of the points to plot
    
    :param id: id of the points to edit
    :type id: int
    :return: render_template('edit-contact.html', contact = data[0])
    :rtype: function
    """ 
    id =1   
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id={0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('versiones.html', contact = data)

@app.route('/software/', methods = ['POST', 'GET'])
def get_software():
    """Edit the name, var1 and var2 of the points to plot
    
    :param id: id of the points to edit
    :type id: int
    :return: render_template('edit-contact.html', contact = data[0])
    :rtype: function
    """ 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('software.html', contact = data)

@app.route('/foro/', methods = ['POST', 'GET'])
def get_forum():
    """Edit the name, var1 and var2 of the points to plot
    
    :param id: id of the points to edit
    :type id: int
    :return: render_template('edit-contact.html', contact = data[0])
    :rtype: function
    """ 
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('foro.html', contacts = data)

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    """Update the points to plot
    
    :param id: id of the points to update
    :type id: int
    :return: redirect
    :rtype: function
    """    
    if request.method == 'POST':
        name = request.form['name']
        var1 = request.form['var1']
        var2 = request.form['var2']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET name = %s,
                var2 = %s,
                var1 = %s
            WHERE id = %s
        """, (name, var2, var1, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('get_forum'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    """It allows to delete points that the user no longer wants to plot
    
    :param id: id of the point to delete
    :type id: int
    :return: redirect
    :rtype: function
    """    
    cur =  mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash('Contact removed')
    return redirect(url_for('Index'))

@app.route('/add_file', methods=['POST'])
def add_file():

    
    """It allows to plot points by loading them from a plain text file
    
    :return: redirect
    :rtype: function
    """    
    if request.method == 'POST':        
        contenido = request.form['contenido-archivo']
        contenido = contenido.split()
        list_nam = []
        list_val1 =[]
        list_val2 =[]

        for i in range(len(contenido)):
           """Cycle used to extract from the plain text file the name, var1 and var2 of each point
           """            
           if i%3 == 0:
               list_nam.append(contenido[i])
           elif i%3 ==1:
               list_val1.append(contenido[i])
           elif i%3 ==2:
               list_val2.append(contenido[i])

        cur = mysql.connection.cursor()
        for i in range(len(list_nam)):
            """Cycle used to upload each point to the database
            """            
            cur.execute('INSERT INTO contacts (name, var1, var2) VALUES (%s, %s, %s)', 
            (list_nam[i], list_val1[i], list_val2[i]))

        mysql.connection.commit() 
        return redirect(url_for('Index'))      

if __name__ == '__main__':
    app.run(port = 3000, debug=True)
