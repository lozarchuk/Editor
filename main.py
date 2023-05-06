import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка
 
 
from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(600, 300)

spisok = QListWidget()
kartinka = QLabel('rfhnbyrf')
btn_papka = QPushButton('Folder')
btn_l = QPushButton('Left')
btn_r = QPushButton('Right')
btn_mir = QPushButton('Mirror')
btn_rezko = QPushButton('Sharpness')
btn_CHB = QPushButton('B/W')

VLine1 = QVBoxLayout()
HLine1 = QHBoxLayout()
VLine2 = QVBoxLayout()
HLine2 = QHBoxLayout()

VLine1.addWidget(btn_papka)
VLine1.addWidget(spisok)

HLine1.addWidget(btn_l)
HLine1.addWidget(btn_r)
HLine1.addWidget(btn_mir)
HLine1.addWidget(btn_rezko)
HLine1.addWidget(btn_CHB)

VLine2.addWidget(kartinka)

main_win.setLayout(HLine2)
HLine2.addLayout(VLine1)
HLine2.addLayout(VLine2)
VLine2.addLayout(HLine1)



def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result 

def showFilenamesList():
    extensions = ['.jpg', '.png', '.gif', '.jpeg', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    spisok.clear()
    for filename in filenames:
        spisok.addItem(filename)

class ImageEditor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.directory = None
        self.save_dir = 'Modified/'

    def loadImage(self, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        kartinka.hide()
        pixmapimage = QPixmap(path)
        w, h = kartinka.width(), kartinka.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        kartinka.setPixmap(pixmapimage)
        kartinka.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_mir(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_l(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_r(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_rezko(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)      


workimage = ImageEditor()

def showChosenImage():
    if spisok.currentRow() >= 0:
        filename = spisok.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)



spisok.currentRowChanged.connect(showChosenImage)
btn_papka.clicked.connect(showFilenamesList)
btn_CHB.clicked.connect(workimage.do_bw)    
btn_mir.clicked.connect(workimage.do_mir)
btn_l.clicked.connect(workimage.do_l)
btn_r.clicked.connect(workimage.do_r)
btn_rezko.clicked.connect(workimage.do_rezko)



main_win.show()
app.exec_()