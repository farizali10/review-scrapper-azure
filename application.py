# Whenever creating a professional grade code do not import each lib onebyone refer them to 'pip install -r requirements.txt' in terminal 
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs # Will beautify HTML code
from urllib.request import urlopen as uReq
from flask import Flask
import logging
logging.basicConfig(filename = "scrapper.log", level = logging.INFO)


application = Flask(__name__) # Creating a object for flask
app = application # Using application as it is a convention from beanstalk

@app.route("/", methods = ["GET"]) 
def homepage():
    return render_template("index.html") 

# Calling a method which will accept data from search and give output
@app.route("/review",methods = ["POST", "GET"]) # Whenver we will hit review in HTML this function will work

def index():
    if request.method == 'POST': 
        try: 
            searchString = request.form['content'].replace(" ","") # Sending data through form(request.form). # Getting data from content tab in HTML form. # If there is a blank in searchbox replace it with none [.replace(" ","")]
            # Thru above function we will be able to get a searchstring from the form to the
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            # Storing search results into a .csv
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    logging.info("Name")

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'
                    logging.info("Rating")

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    logging.info(e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            logging.info("Log my final result {}".format(reviews))
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
