from flask import Flask, render_template, request, send_from_directory, send_file
from keras.models import load_model
import numpy as np
from keras.applications.vgg16 import preprocess_input
from keras.utils import image_utils, load_img
import os




app = Flask(__name__, static_folder='public')
model = load_model("Modelan.h5")
target_img = os.path.join(os.getcwd() , '/public/static/images')

@app.route('/')
def index_view():
    return send_from_directory(app.static_folder,'classification.html')
    
#Allow files with extension png, jpg and jpeg
ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT


# Function to load and prepare the image in right shape
def read_image(filename):
    img = load_img(filename, target_size=(320, 320))
    x = image_utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x
    

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename): #Checking file format
            filename = f.filename
            
            if(filename != ""):
              file_path = os.path.join(target_img, filename)
            
            f.save(file_path)

            img = read_image(file_path) #prepressing method

            class_prediction=model.predict(img) 
            classes_x=np.argmax(class_prediction,axis=1)
            if classes_x == 0:
              daun = "bercak"
              text = "menyemprotkan fungisida berbahan aktif azoksistrobin dan difenokonazol dengan dosis 10ml per 16 liter air atau sesuaikan dengan dosis yang tertera pada label kemasan."
            elif classes_x == 1:
              daun = "kering"
              text = "Cara mengatasinya tidak lain adalah dengan melakukan penyiraman. Jangan sampai tanaman kekurangan air lagi."
            elif classes_x == 2:
              daun = "kuning"
              text = "melarutkan pupuk NPK Mutiara 16-16-16 dengan takaran satu sendok makan dicampur dengan tiga liter air. Kemudian, aduk rata dan astikan pupuk NPK Mutiara 16-16-16 larut bercampur dengan air."
            elif classes_x == 3:
              daun = "keriting"
              text = "pemberian pupuk daun yang mengandung nitrogen dan ZPT Auxin serta Clorophil Stimulant secara teratur. Selain itu, gunakan juga ZPT Sitokinin yang mampu menghambat penuaan sel tanaman."
            elif classes_x == 4:
              daun = "layu"
              text = "Jangan mencabutnya, mengaplikasikan trichoderma jika terserang jamur, dan mengaplikasikan bakterisida berbahan aktif streptomisin sulfat atau Dazomet jika terserang bakteri."
            else:
              daun = "normal"
              text = "pertahankan kondisi daunnya dengan pemberian nutrisi yang tepat."
            #'daun' , 'prob' . 'user_image' these names we have seen in predict.html.

            print("cek daun "+ daun)
            print("Gambar " + filename)
            return render_template('predict.html', dauns=daun,solusi=text, filenam = filename)
        else:
            return "Unable to read the file. Please check file extension"
            
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False, port=8000)