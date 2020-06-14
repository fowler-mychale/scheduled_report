import MySQLdb
import pandas as pd
import csv
import sys
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Connect
dbConnect = MySQLdb.connect('localhost','username','password','my_db')
cursor = dbConnect.cursor()

# Query
sql = """ SELECT * FROM  my_db.books """

cursor.execute(sql)
rows = cursor.fetchall()
data = cursor.fetchall()

# save file
csv_path = datetime.now().strftime("%Y-%m-%d.csv")

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

plt.show()

