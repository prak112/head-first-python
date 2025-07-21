from enum import Enum
import statistics

# Optional: constants declaration using enum class syntax
class DataFile(Enum):
  DIRNAME = "swimdata/"

def process_swim_data(filename):
  """Retrun swimmer data and stats from a file.

  Given name of a swimmer's file (filename) and return swimmer profile data and average lap time in a tuple.
  """
  # sub-tasks 2a, 2b, 2c: Read file and split data for a list of items
  with open(DataFile.DIRNAME.value + filename, mode='r') as file:
    times = file.readline().strip('\n').split(',')

  # sub-task 2f: unpacking data from filename using string object methods into variables
  swimmer, age_group, distance, stroke = filename.removesuffix(".txt").split("-")

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
  
  avg_in_msec = round(statistics.mean(times_in_msec) / 100, 2)
  mins_secs, millisecs = str(avg_in_msec).split(".")
  mins = int(mins_secs) // 60
  secs = int(mins_secs) - (mins * 60) # subtract acquired minutes (in seconds) from total seconds for actual representation of seconds, i.e., between 0 to 60
  avg_in_timerformat = f"{mins}:{secs}.{millisecs}"

  return swimmer, age_group, distance, stroke, times, times_in_msec, avg_in_timerformat


# if __name__ == "__main__":
#     abi_file = "Abi-10-50m-Back.txt"
#     process_swim_data(filename=abi_file)