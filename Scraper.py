#setting up library
import mysql.connector
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
#url to search
url=input("Hi henlo fren this is a simple Guitar Center web scraper. Please put in the url of the page you want to scrape for prices: ")
print("\n")

#Getting the page
uClient = uReq(url)
pghtml = uClient.read()
uClient.close()

#Loading the parser
pgsoup=soup(pghtml, "html.parser")

#this parses through html code

#grabs each product and throws it into an array
containers = pgsoup.findAll("li",{"class":"product-container"})
container=containers[0]

#print(container)

#Making a csv in order to populate a DB
filename = "Controllers.csv"
file = open(filename,"w")
headers = "Product Name, Price\n"

file.write(headers)

counter=1
for container in containers:

#going into the <img> tag and finding what "alt" is equal to.
    print("Product #", counter)
    prodname = container.img["alt"]
#In every iteration, print product name and find it's price.
    print(prodname)
    price = container.findAll("span", {"class":"productPrice"})

#print product's price.
    print(price[0].text.strip())
    print("\n")
    counter+=1


    file.write(price[0].text.replace(",", "") + "," + prodname + "," + "\n")

file.close()


cnx = mysql.connector.connect(user='root', password='mypass',
                              host='127.0.0.1',
                              database='scraper')


if cnx:
    print("Connection made! ")
    cursor=cnx.cursor()
#Use mydb
    cursor.execute("use scraper;")
#Do these commands
    cursor.execute(" create table controllers(id int not null primary key auto_increment, prodname varchar(50), price varchar(50));")


else:
    print("No connection made. ")
    quit()

#cursor.execute("load data local infile 'controllers.csv' into table controllers fields terminated by ',' lines terminated by '\n' (id, prodname, price);")
cnx.close()

print("Table successfully made!")
