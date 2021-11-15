from flask import Flask,render_template,redirect,url_for,request,session,g,url_for
import os
cap1=os.path.join('static', 'images')
cap2=os.path.join('static', 'images')
cap3=os.path.join('static', 'images')
cap4=os.path.join('static', 'images')
cap5=os.path.join('static', 'images')
app = Flask(__name__)
app.config['upload1']=cap1
app.config['upload2']=cap2
app.config['upload3']=cap3
app.config['upload4']=cap4
app.config['upload5']=cap5
@app.route("/")
def po():
    return render_template('loginn.html')
@app.route("/iotpoc")
def home1():
    filename1=os.path.join(app.config['upload1'], 'sam.jpg')
    filename2=os.path.join(app.config['upload2'], 'track.jpg')
    filename3=os.path.join(app.config['upload3'], 'stock.jpg')
    filename4=os.path.join(app.config['upload4'], 'pass.jpg')
    filename5=os.path.join(app.config['upload5'], 'pass1.jpg')
    return render_template("style.html",user_image1=filename1,user_image2=filename2,user_image3=filename3,user_image4=filename4,user_image5=filename5)



    



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')



