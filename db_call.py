import MySQLdb
import pandas as pd
import csv
import sys
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import shutil
#import subprocess

# Connect
dbConnect = MySQLdb.connect('localhost','username','password','my_db')
cursor = dbConnect.cursor()

# Query
sql = """ SELECT * FROM  my_db.books """

cursor.execute(sql)
rows = cursor.fetchall()
data = cursor.fetchall()

# save file
csv_path = datetime.now().strftime("example.csv")

dbConnect.close()

if rows:
    # New empty list called 'result'. This will be written to a file.
    result = list()

    # The row name is the first entry for each entity in the description tuple.
    column_names = list()
    for i in cursor.description:
        column_names.append(i[0])

    result.append(column_names)
    for row in rows:
        result.append(row)

    # Write result to file.
    with open(csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in result:
            csvwriter.writerow(row)
else:
    sys.exit("No rows found for query: {}".format(sql))

# Calling newly created variable
df = pd.read_csv(csv_path)   

graph = sns.catplot(x="released_year", y="pages", hue="title", data=df,
                height=10, kind="bar")
graph.despine(left=True)
graph.set_ylabels("pages")

graph.savefig('author_info', dpi=200)

#plt.show()

# Move newly created files to new folder
shutil.move('/Users/Mike_F/Documents/GitHub/scheduled_report-1/example.csv', 'C:/Users/Mike_F/Desktop/test_folder/example.csv')
shutil.move('/Users/Mike_F/Documents/GitHub/scheduled_report-1/author_info.png', 'C:/Users/Mike_F/Desktop/test_folder/author_info.png')


#subprocess.call(['cscript.exe', 'C:\\Users\\Mike_F\\Desktop\\outfile.vbs'])
