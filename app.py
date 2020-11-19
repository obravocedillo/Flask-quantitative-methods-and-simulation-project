from flask import Flask, request, jsonify
from flask_cors import CORS
import markovify
from mbot import MBot
import time

app = Flask(__name__)
CORS(app)
currentIndex = 0
text_models = {}

matrixDictionary = {
   #Hogar
   'B078RTCRGM':MBot('B078RTCRGM'),
   'B086TW55T4':MBot('B086TW55T4'),
   'B07PGJSYYC':MBot('B07PGJSYYC'),
   #Hogar
   #Videojuegos
   'B07VGRJDFY':MBot('B07VGRJDFY'),
   'B07XF2ZXNG':MBot('B07XF2ZXNG'),
   'B084SFDDN3':MBot('B084SFDDN3'),
   #Videojuegos
   #Electronica
   'B07WLSQMHF':MBot('B07WLSQMHF'),
   'B0195Y0A42':MBot('B0195Y0A42'),
   'B07RK58K76':MBot('B07RK58K76')
   #Electronica
}

def constructCommentModel(array):
   for element in array:
      with open(element+'.txt') as f:
         text = f.read()
      text_model = markovify.Text(text)
      tempId = element
      text_models[tempId] = text_model 
   return

asinsArray = ['B07VGRJDFY', 'B07XF2ZXNG', 'B084SFDDN3', 'B078RTCRGM', 'B086TW55T4', 'B07PGJSYYC', 'B07WLSQMHF', 'B0195Y0A42', 'B07RK58K76']
constructCommentModel(asinsArray)

#Metodo de congruencia lineal
def generateSeed(inicial, a, c, m):
   while True:
      inicial = (a * inicial + c) % m
      yield inicial
   
#Metodo para generar números random
def random_sample(lower,upper,index, initial = 20200420162000):
   global currentIndex
   numbers = []
   glibc = generateSeed(initial, 1103515245, 12345, 2 ** 32)
   for i in range(10000):
      observation = (upper - lower) * (next(glibc) / (2 ** 32 - 1)) + lower
      numbers.append(int(observation))
   currentIndex += 1
   return numbers[index]

#sample = random_sample(30, 90, currentIndex)  ejemplo de uso metodo random

def generateMarkovComment(id,numberOfSentences):
   # Print five randomly-generated sentences
   currentComment = ''
   for i in range(numberOfSentences):
      tempComment = ''
      tempSentece = text_models[id].make_sentence()
      tempComment = tempSentece
   return tempComment

@app.route('/')
def hello_world():
   return 'Server running' 

@app.route('/generate-number',methods=['GET'])
def generateNumber():
   #Use example http://127.0.0.1:5000/generate-number?lower=1&upper=20
   global currentIndex
   lower = int(request.args.get('lower'))
   upper = int(request.args.get('upper'))
   if((lower and upper) or (upper < lower)):
      randomNumber = random_sample(lower, upper, currentIndex)
      return str(randomNumber), 200
   else:
      return "Error", 500

@app.route('/generate-comment',methods=['GET'])
#Use example http://127.0.0.1:5000/generate-comment?asin=B07PGJSYYC&length=3
def generateComment():
   productId = request.args.get('asin')
   length = request.args.get('length')
   if(productId and length):
      return generateMarkovComment(productId, int(length)), 200
   else:
      return "Error", 500

@app.route('/get-product-data',methods=['GET'])
#Use example http://127.0.0.1:5000/get-product-data?set=0&asin=B07PGJSYYC
def getProductData():
   setNumber = request.args.get('set')
   asin = request.args.get('asin')
   if(setNumber and asin):
      tempData = matrixDictionary[asin].nextData(int(setNumber))
      return tempData, 200
   else:
      return "Error", 500


@app.route('/get-all-products',methods=['GET'])
#Use example http://127.0.0.1:5000/get-all-products?category=1&set=0
def getAllProducts():
   category = request.args.get('category')
   setNumber = request.args.get('set')
   if(category and setNumber):
      tempArray = []
      if(category == "2"):
         tempData1 = matrixDictionary['B07VGRJDFY'].nextData(int(setNumber))
         tempData2 = matrixDictionary['B07XF2ZXNG'].nextData(int(setNumber))
         tempData3 = matrixDictionary['B084SFDDN3'].nextData(int(setNumber))
         tempArray.append(tempData1)
         tempArray.append(tempData2)
         tempArray.append(tempData3)
      elif(category == "1"):
         tempData1 = matrixDictionary['B078RTCRGM'].nextData(int(setNumber))
         tempData2 = matrixDictionary['B086TW55T4'].nextData(int(setNumber))
         tempData3 = matrixDictionary['B07PGJSYYC'].nextData(int(setNumber))
         tempArray.append(tempData1)
         tempArray.append(tempData2)
         tempArray.append(tempData3)
      elif(category == "3"):
         tempData1 = matrixDictionary['B07WLSQMHF'].nextData(int(setNumber))
         tempData2 = matrixDictionary['B0195Y0A42'].nextData(int(setNumber))
         tempData3 = matrixDictionary['B07RK58K76'].nextData(int(setNumber))
         tempArray.append(tempData1)
         tempArray.append(tempData2)
         tempArray.append(tempData3)
      return jsonify(tempArray), 200
   else:
      return "Error", 500
