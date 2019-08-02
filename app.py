from flask import Flask,request,render_template
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('teachers/list.html')
@app.route('/s')
def stud():
   return render_template('students/assignment_list.html')
if __name__ == '__main__':
   app.run(debug = True)
