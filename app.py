from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
  return render_template('home.html')

@app.route('/upload', methods = ['POST'])
def uploadFile():
  if request.method == 'POST':
    print("THE DATA STARTS HERE ")
    print(request.data)
    return 'success'
if __name__ == '__main__':
  app.run(debug=True)