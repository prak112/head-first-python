# Optional: constants declaration using enum class syntax
from enum import Enum
class DataFile(Enum):
# for development - "app/<dir_name>"
# for production - "<dir_name>"
  DATA_DIR = "app/data/"
  RECORDS_DIR = "app/records.json"
  CHARTS_DIR = "app/templates/"



def process_swim_data(textfile):
  """Return swimmer data and stats from a file.

  Given name of a swimmer's file (textfile) and return swimmer profile data and average lap time in a tuple.
  """
  import statistics

  # sub-tasks 2a, 2b, 2c: Read file and split data for a list of items
  read_from = f"{DataFile.DATA_DIR.value}{textfile}"
  with open(read_from, mode="r") as file:
    times = file.readline().strip('\n').split(',')

  # sub-task 2f: unpacking data from textfile using string object methods into variables
  swimmer, age_group, distance, stroke = textfile.removesuffix(".txt").split("-")

  # sub-tasks 2d: Convert each of the times in times to number, preferably milliseconds, from string in 'min:sec:msec' format
  # sub-task 2e: Calculate average time from the times and represent average in 'min:sec:msec' format
  # Tip: always best to convert numerical times to smallest unit for ease of calculations
  times_in_msec = []

  for t in times:
    if ":" in t:
      minutes, rest = t.split(":")
      seconds, millisecs = rest.split(".")
    else:
      minutes = 0
      seconds, millisecs = t.split(".")
    times_in_msec.append((int(minutes) * 60 * 100) + (int(seconds) * 100) + int(millisecs))
  
  avg_in_msec = statistics.mean(times_in_msec) / 100
  mins_secs, millisecs = f"{avg_in_msec:.2f}".split(".") # data representation is unclear when using round, hence string format specifier, 2f

  mins = int(mins_secs) // 60
  secs = int(mins_secs) - (mins * 60) # subtract acquired minutes (in seconds) from total seconds for actual representation of seconds, i.e., between 0 to 60

  avg_in_timerformat = f"{mins}:{secs:0>2}.{millisecs}"   # 0>2 format specifier adds left-padding to seconds < 10

  # Reverse data order to accomodate bar chart generation as per requirements: oldest swim at bottom, latest swim at top.
  times.reverse()
  times_in_msec.reverse()

  return swimmer, age_group, distance, stroke, times, times_in_msec, avg_in_timerformat



def get_worldrecords(fname):
  """Given filename of the swimmer, returns relevant world records in that particular course, distance and stroke.

  Generates lookup value from filename and conversions dictionary.
  Reads data stored in RECORDS_DIR.
  Returns list with world record in each course. 
  List data format - [LC Men, LC Women, SC Men, SC Women]
  """

  import json 

  *_, distance, stroke = str(fname).removesuffix(".txt").split("-")
  COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
  conversions = {
    "Free": "freestyle",
    "Back": "backstroke",
    "Fly":  "butterfly",
    "Breast": "breaststroke",
    "IM": "individual medley"
  }
  lookup = f"{distance} {conversions[stroke]}"

  records_path = DataFile.RECORDS_DIR.value
  with open(records_path, mode="r") as df:
    records = json.load(fp=df)
  
  course_records = []
  for course in COURSES:
    course_record = records[course][lookup]
    course_records.append(course_record)
  
  return course_records



def generate_bar_chart(fname):
  """Given the name of a swimmer's file, generates a HTML/SVG-based bar chart.
  
  Save generated bar chart to 'charts/' directory.
  Return path of generated bar chart file.
  """
  import hfp_utils

  swimmer, age_group, distance, stroke, times, times_in_msec, avg_in_timerformat = process_swim_data(fname)
  course_records = get_worldrecords(fname)

  # setup HTML with SVG barchart
  html = ""
  title = f"{swimmer}(Under {age_group}) {distance} - {stroke}"
  header = f"""
  <!DOCTYPE html>
  <html>
      <head>
          <title>
              {title}
          </title>
          <link rel="stylesheet" href="/static/index.css"/>
      </head>
      <body>
          <h3>{title}</h3>
  """
  html += header

  time_min = 0
  time_max = max(times_in_msec)
  svg_min = 0
  svg_max = 400
  for t in times_in_msec:
    bar_width = hfp_utils.normalize(t, time_min, time_max, svg_min, svg_max)
    body = f"""
          <svg height="30" width="450">
            <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
          </svg>{times[times_in_msec.index(t)]}<br />
    """
    html += body

  footer = f"""
          <p>Average time: {avg_in_timerformat}</p>
          <p>Men: {course_records[0]} ({course_records[2]})</p>
          <p>Women: {course_records[1]} ({course_records[3]})</p>
          <p>
            <a href="/">Home</a> | <a href="/swimmers">All Swimmers</a>
          </p>
      </body>
  </html>
  """
  html += footer
  
  # write generated html string to file
  save_to = f"{DataFile.CHARTS_DIR.value}{fname.removesuffix('.txt')}.html"
  with open(save_to, mode="w") as hf:
    print(html, file=hf) # file argument sends print data through hf file
  
  return save_to


