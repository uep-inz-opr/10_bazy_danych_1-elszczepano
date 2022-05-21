import csv
import sqlite3
class ReportGenerator:
  def __init__(self, connection, escape_string="(%s)"):
    self.connection = connection
    self.report_text = None
    self.escape_string = escape_string

  def generate_report(self):
    cursor = self.connection.cursor()
    sql_query = f"SELECT SUM(duration) FROM polaczenia"
    cursor.execute(sql_query)
    result = cursor.fetchone()[0]
    self.report_text = result

  def get_report(self):
    return self.report_text

if __name__ == "__main__":
    file = input()

    sqlite_con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES |
                                 sqlite3.PARSE_COLNAMES)  # change to 'sqlite:///your_filename.db'
    # This little bugger above https://stackoverflow.com/questions/1829872/how-to-read-datetime-back-from-sqlite-as-a-datetime-instead-of-string-in-python
    cur = sqlite_con.cursor()

    #Tworzymy pusta tabele polaczenia
    cur.execute('''CREATE TABLE polaczenia (from_subscriber data_type INTEGER, 
                  to_subscriber data_type INTEGER, 
                  datetime data_type timestamp, 
                  duration data_type INTEGER , 
                  celltower data_type INTEGER);''')  # use your column names here

    #Otwieramy plik.csv i przerzucamy go w najprostszy sposób do naszej nowo utworzonej bazy sqlite
    with open(file, 'r') as fin:
        # csv.DictReader uses first line in file for column headings by default
        reader = csv.reader(fin, delimiter=";")  # comma is default delimiter
        next(reader, None)  # skip the headers
        rows = [x for x in reader]
        cur.executemany(
            "INSERT INTO polaczenia (from_subscriber, to_subscriber, datetime, duration , celltower) VALUES (?, ?, ?, ?, ?);", rows)
        sqlite_con.commit()

        rg = ReportGenerator(sqlite_con, escape_string="?")
        rg.generate_report()
        print(rg.get_report())
