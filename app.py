from flask import Flask
import markovify

app = Flask(__name__)
currenIndex = 0
text_models = {}

def constructCommentModel(file):
   with open(file) as f:
      text = f.read()
   text_model = markovify.Text(text)
   tempId = file.split('.')[0]
   text_models[tempId] = text_model 
   return

#constructCommentModel(id) Read markovify commments

#Metodo de congruencia lineal
def generateSeed(inicial, a, c, m):
   while True:
      inicial = (a * inicial + c) % m
      yield inicial
   
#Metodo para generar números random
def random_sample(lower,upper,index, initial = 20200420162000):
   global currenIndex
   numbers = []
   glibc = generateSeed(initial, 1103515245, 12345, 2 ** 32)
   for i in range(10000):
      observation = (upper - lower) * (next(glibc) / (2 ** 32 - 1)) + lower
      numbers.append(int(observation))
   currenIndex += 1
   return numbers[index]

#sample = random_sample(30, 90, currentIndex)  ejemplo de uso metodo random

def generateMarkovComment(id,numberOfSentences):
   # Print five randomly-generated sentences
   currentComment = ''
   for i in range(numberOfSentences):
      tempSentece = text_models[id].make_sentence()
      currentComment + tempSentece
   return currentComment

@app.route('/')
def hello_world(name):
   return 'Hello World ' + name

@app.route('/generate-number',methods=['GET'])
def generateNumber():
   global currenIndex
   lower = request.args.get('lower')
   upper = request.args.get('upper')
   randomNumber = random_sample(lower, upper, currentIndex)
   return randomNumber, 200


@app.route('/generate-comment',methods=['GET'])
def generateNumber():
   productId = request.args.get('id')
   randomCommnet = generateMarkovComment(productId)
   return randomCommnet, 200



@app.route('/get-product-data',methods=['GET'])
def getProductData():
   setNumber = request.args.get('set')
   return setNumber, 200


@app.route('/get-all-products',methods=['GET'])
def getAllProducts():
   setNumber = request.args.get('set')
   return setNumber, 200
   
