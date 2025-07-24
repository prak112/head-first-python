from flask import Flask, session, render_template, request
import os
import swimclub
from dotenv import load_dotenv

load_dotenv()
APP_SECRET = os.getenv('APP_SECRET_KEY')

app = Flask(__name__)
app.secret_key = APP_SECRET

@app.get("/")
def home():
  return render_template(
    "index.html",
    title="Kuopio Swimmers Club",
    )

def populate_data():
  """
  Populates dictionary of swimmer names (keys) and files related to their swimming sessions (values) in a list.
  Makes it available for the session in "swimmers" variable.
  """
  if "swimmers" not in session:
    files_list = os.listdir(swimclub.DataFile.DATA_DIR.value)
    if ".DS_Store" in files_list:
      files_list.remove(".DS_Store")
    session["swimmers"] = {}
    for file in files_list:
      name, *_ = swimclub.process_swim_data(file)
      if name not in session["swimmers"]:
        session["swimmers"][name] = []
      session["swimmers"][name].append(file)

@app.get("/swimmers")
def display_swimmers():
  """HTTP GET Method displays a dropdown list of swimmers.
  Uses session variable, session["swimmers"] in select.html to populate list.
  """
  populate_data()
  return render_template(
    "select.html",
    title="Select a Swimmer", 
    url="/showfiles",
    select_id="swimmer",
    data=sorted(session["swimmers"]),
  )

@app.post("/showfiles")
def display_swimmer_files():
  """HTTP POST Method retrieves Form data using request module.
  Uses form data to list files related to swimmer available from session variable, session["swimmers"].
  """
  populate_data()
  session["name"] = request.form["swimmer"]
  if session["name"] not in session["swimmers"]:
    return "Oops! Swimmer not listed as member of the Kuopio Swimmers Club!"
  return render_template(
    "select.html",
    title="Select a swimmer session",
    url="/showchart",
    select_id="file",
    data=session["swimmers"][session["name"]]
  )

@app.post("/showchart")
def display_swimmer_chart():
  """HTTP POST Method retrieves Form data using request module.
  Displays generated HTML-SVG file in browser.
  """
  file_id = request.form["file"]
  html_path = swimclub.generate_bar_chart(file_id)
  return render_template(html_path.split("/")[-1]) 


if __name__ == "__main__":
  app.run(debug=True)