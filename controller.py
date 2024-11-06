from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import cv2 as cv
import ntpath
import numpy as np
import os
from UI import Ui_MainWindow
import glob


#宣告全域的字串變數
folder="nothing"
image1="nothing" #儲存圖片位址的變數
image2="nothing"

class MainWindow_controller(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    #點擊buttom觸發相對應的功能
    def setup_control(self):
        self.ui.load_1.clicked.connect(self.open_file1) 
        self.ui.load_2.clicked.connect(self.open_file2)
        self.ui.load_folder.clicked.connect(self.open_folder)
        self.ui.one_1.clicked.connect(self.Draw_Contour)
        self.ui.one_2.clicked.connect(self.Count_Rings)
        self.ui.two_1.clicked.connect(self.Corner_detection )
        self.ui.two_2.clicked.connect(self.Intrinsic_matrix)
        self.ui.two_3.clicked.connect(self.Extrinsic_matrix)
        self.ui.two_4.clicked.connect(self.Distortion_matrix)
        self.ui.two_5.clicked.connect(self.Undistorted_result)
        self.ui.three_1.clicked.connect(self.AR_onboard)
        self.ui.three_2.clicked.connect(self.AR_vertically)
        self.ui.four_1.clicked.connect(self.Disparity_Map_and_Disparity_Value)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open folder")

        #使用 ntpath 庫從路徑中獲取檔名，並在table處顯示資料夾名稱
        self.ui.folder_name.setText(ntpath.basename(folder_path))

        #檢查是否有成功讀取檔案，如果沒有成功，filename為空字串
        if len(folder_path)!=0:
            global folder #告訴程式要改變全域變數 
            folder=folder_path #folder:儲存資料夾位置

    def open_file1(self):
        #“Open file” 是開始視窗後上方標題列的名稱 
        filename, filetype = QFileDialog.getOpenFileName(self,"Open file") 

        #使用 ntpath 庫從路徑中獲取檔名，並在table處顯示檔名
        self.ui.img1_name.setText(ntpath.basename(filename))

        #檢查是否有成功讀取檔案，如果沒有成功，filename為空字串
        if len(filename)!=0:
            global image1 #告訴程式要改變全域變數 
            image1=filename #img1:儲存檔案位置
    
    def open_file2(self):
        filename, filetype = QFileDialog.getOpenFileName(self,"Open file") 
        self.ui.img2_name.setText(ntpath.basename(filename))
        if len(filename)!=0:
            global image2
            image2=filename

    #檢查是否有讀到資料夾/圖片
    def check(self,check):
        if check=="nothing":
            return False
        else:
            return True
   
    def Find_Contour(self,img1,img2):
        
        #轉灰階
        gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

        #remove noise
        blur1 = cv.GaussianBlur(gray1, (5,5), 0)
        blur2 = cv.GaussianBlur(gray2, (5,5), 0)

        #edge detection 
        edge1=cv.Canny(blur1,30,150) #(圖片,最小門檻值,最大門檻值)
        edge2=cv.Canny(blur2,30,150)

        #(繪製的圖像,取所有的Contour,壓縮取回的Contour像素點，只取長寬及對角線的end points)
        contours1, _ = cv.findContours(edge1, cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE) #countours:為list，其中每個元素都是影像中的一個輪廓
        contours2, _ = cv.findContours(edge2, cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)

        return contours1,contours2
   
    def Draw_Contour(self):

        if self.check(image1) and self.check(image2):
            img1=cv.imread(image1)
            img2=cv.imread(image2)

            #reize
            img1=cv.resize(img1,(round(img1.shape[1]/2),round(img1.shape[0]/2)))#round:四捨五入(不然會有錯誤)
            img2=cv.resize(img2,(round(img2.shape[1]/2),round(img2.shape[0]/2)))

            c1,c2=self.Find_Contour(img1,img2)
        
            cv.drawContours(img1, c1, -1, (255,255,0), 2)
            cv.drawContours(img2, c2, -1, (255,255,0), 2)

            cv.imshow("img1",img1)
            cv.imshow("img2",img2)

            cv.waitKey(0)
            cv.destroyAllWindows()
    
    def Count_Rings(self):
        if self.check(image1) and self.check(image2):
            img1=cv.imread(image1)
            img2=cv.imread(image2)

            #reize
            img1=cv.resize(img1,(round(img1.shape[1]/2),round(img1.shape[0]/2)))#round:四捨五入(不然會有錯誤)
            img2=cv.resize(img2,(round(img2.shape[1]/2),round(img2.shape[0]/2)))

            c1,c2=self.Find_Contour(img1,img2)

            count1 = int(len(c1)/4)
            self.ui.result1.setText("There are " + str(count1) + " rings in img1.jpg")
            count2 = int(len(c2)/4)
            self.ui.result2.setText("There are " + str(count2) + " rings in img2.jpg")

    def Corner_detection(self):
        if self.check(folder):
            chess_row=8 #8條橫線(不含最外)
            chess_col=11 
            images=glob.glob(os.path.join(folder, "*.bmp")) #讀取所有圖檔
            file_num=len(images) #計算圖片個數
            for i in range(1,file_num+1):
                    img= cv.imread(folder+'/'+str(i)+".bmp")
                    ok,corners=cv.findChessboardCorners(img,(chess_col,chess_row),None)
                    if ok:
                            cv.drawChessboardCorners(img,(chess_col,chess_row),corners,ok)
                            img_v2=cv.resize(img,(512,512))
                    cv.imshow("Chessboard",img_v2)
                    cv.waitKey(500) #暫停500毫秒=0.5秒
            cv.destroyAllWindows()

    def Intrinsic_matrix(self):
        if self.check(folder):
            # 設定 criteria的參數值
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01) #TERM_CRITERIA_EPS測誤差有關#TERM_CRITERIA_MAX_ITER迭帶次數

            chess_row=8 
            chess_col=11 
            chess_size=88

            objp = np.zeros((chess_size,3), np.float32)
            #mgrid創造兩個二維數組（同行同值和同列同值)，並對產生的結果轉置(T)，接著reshape固定兩欄自動分配列數(-1)
            objp[:,:2] = np.mgrid[0:chess_col,0:chess_row].T.reshape(-1,2) #objp[][0]和[][1]儲存產生的兩個結果

            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.

            images=glob.glob(os.path.join(folder, "*.bmp")) #讀取所有圖檔
            file_num=len(images) #計算圖片個數
            sort_img=[]
            #將圖片照順序儲存
            for i in range(1,file_num+1):
                file_name=folder+'/'+str(i)+".bmp"
                sort_img.append(file_name)

            for fname in sort_img:
                img = cv.imread(fname)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv.findChessboardCorners(gray, (chess_col,chess_row), None)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    objpoints.append(objp)
                    #cornerSubPix對檢測到的角點作進一步的優化計算，可使角點的精度達到亞像素級別
                    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria) #(圖片,角點,區域大小,(-1,-1)代表忽略,停止優化的標準)
                    imgpoints.append(corners2)

            h,w=gray.shape[::-1]
            #ret:重投影誤差；mtx:相機的內參矩陣；dist:相機畸變參數；rvecs:標定棋盤格世界坐標係到相機坐標系的旋轉參數；tvecs:平移參數  
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (w,h), None, None)#(世界坐標系中的點,其對應的圖像點,圖像的大小,內參數矩陣,畸變矩陣)   
            print("Intrinsic:\n")
            print(mtx)

    def Extrinsic_matrix(self):
        if self.check(folder):
            
            num=int(self.ui.photo_num.currentText())

            # 設定 criteria的參數值
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01) #TERM_CRITERIA_EPS測誤差有關#TERM_CRITERIA_MAX_ITER迭帶次數

            chess_row=8 
            chess_col=11 
            chess_size=88

            objp = np.zeros((chess_size,3), np.float32)
            #mgrid創造兩個二維數組（同行同值和同列同值)，並對產生的結果轉置(T)，接著reshape固定兩欄自動分配列數(-1)
            objp[:,:2] = np.mgrid[0:chess_col,0:chess_row].T.reshape(-1,2) #objp[][0]和[][1]儲存產生的兩個結果

            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.

            images=glob.glob(os.path.join(folder, "*.bmp")) #讀取所有圖檔
            file_num=len(images) #計算圖片個數
            sort_img=[]
            #將圖片照順序儲存
            for i in range(1,file_num+1):
                file_name=folder+'/'+str(i)+".bmp"
                sort_img.append(file_name)

            for fname in sort_img:
                img = cv.imread(fname)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv.findChessboardCorners(gray, (chess_col,chess_row), None)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    objpoints.append(objp)
                    #cornerSubPix對檢測到的角點作進一步的優化計算，可使角點的精度達到亞像素級別
                    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria) #(圖片,角點,區域大小,(-1,-1)代表忽略,停止優化的標準)
                    imgpoints.append(corners2)
                    
            h,w=gray.shape[::-1]
            #ret:重投影誤差；mtx:相機的內參矩陣；dist:相機畸變參數；rvecs:標定棋盤格世界坐標係到相機坐標系的旋轉參數；tvecs:平移參數  
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (w,h), None, None)#(世界坐標系中的點,其對應的圖像點,圖像的大小,內參數矩陣,畸變矩陣)   


            R = cv.Rodrigues(rvecs[num-1]) #將向量轉成矩陣
            ext = np.hstack((R[0], tvecs[num-1]))#陣列橫向合併
            print(ext,"\n")

    def Distortion_matrix(self):
        if self.check(folder):
            # 設定 criteria的參數值
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01) #TERM_CRITERIA_EPS測誤差有關#TERM_CRITERIA_MAX_ITER迭帶次數

            chess_row=8 
            chess_col=11 
            chess_size=88

            objp = np.zeros((chess_size,3), np.float32)
            #mgrid創造兩個二維數組（同行同值和同列同值)，並對產生的結果轉置(T)，接著reshape固定兩欄自動分配列數(-1)
            objp[:,:2] = np.mgrid[0:chess_col,0:chess_row].T.reshape(-1,2) #objp[][0]和[][1]儲存產生的兩個結果

            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.

            images=glob.glob(os.path.join(folder, "*.bmp")) #讀取所有圖檔
            file_num=len(images) #計算圖片個數
            sort_img=[]
            #將圖片照順序儲存
            for i in range(1,file_num+1):
                file_name=folder+'/'+str(i)+".bmp"
                sort_img.append(file_name)

            for fname in sort_img:
                img = cv.imread(fname)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv.findChessboardCorners(gray, (chess_col,chess_row), None)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    objpoints.append(objp)
                    #cornerSubPix對檢測到的角點作進一步的優化計算，可使角點的精度達到亞像素級別
                    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria) #(圖片,角點,區域大小,(-1,-1)代表忽略,停止優化的標準)
                    imgpoints.append(corners2)
                    
            h,w=gray.shape[::-1]
            #ret:重投影誤差；mtx:相機的內參矩陣；dist:相機畸變參數；rvecs:標定棋盤格世界坐標係到相機坐標系的旋轉參數；tvecs:平移參數  
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (w,h), None, None)#(世界坐標系中的點,其對應的圖像點,圖像的大小,內參數矩陣,畸變矩陣)   
            print(dist)

    def Undistorted_result(self):
        if self.check(folder):
            # 設定 criteria的參數值
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01) #TERM_CRITERIA_EPS測誤差有關#TERM_CRITERIA_MAX_ITER迭帶次數

            chess_row=8 
            chess_col=11 
            chess_size=88

            objp = np.zeros((chess_size,3), np.float32)
            #mgrid創造兩個二維數組（同行同值和同列同值)，並對產生的結果轉置(T)，接著reshape固定兩欄自動分配列數(-1)
            objp[:,:2] = np.mgrid[0:chess_col,0:chess_row].T.reshape(-1,2) #objp[][0]和[][1]儲存產生的兩個結果

            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.

            images=glob.glob(os.path.join(folder, "*.bmp")) #讀取所有圖檔
            file_num=len(images) #計算圖片個數
            sort_img=[]
            #將圖片照順序儲存
            for i in range(1,file_num+1):
                file_name=folder+'/'+str(i)+".bmp"
                sort_img.append(file_name)

            for fname in sort_img:
                img = cv.imread(fname)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv.findChessboardCorners(gray, (chess_col,chess_row), None)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    objpoints.append(objp)
                    #cornerSubPix對檢測到的角點作進一步的優化計算，可使角點的精度達到亞像素級別
                    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria) #(圖片,角點,區域大小,(-1,-1)代表忽略,停止優化的標準)
                    imgpoints.append(corners2)

            h,w=gray.shape[::-1]
            #ret:重投影誤差；mtx:相機的內參矩陣；dist:相機畸變參數；rvecs:標定棋盤格世界坐標係到相機坐標系的旋轉參數；tvecs:平移參數  
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (w,h), None, None)#(世界坐標系中的點,其對應的圖像點,圖像的大小,內參數矩陣,畸變矩陣)   

            #得到的自由縮放係數對攝像機矩陣進行優化。第四個參數為alpha，會影響ROI
            newcameramatrix,ROI= cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, None)

            #undistort
            for undis in sort_img:
                img = cv.imread(undis)
                dst=cv.undistort(img,mtx,dist,None,newcameramatrix)
                img=cv.resize(img,(512,512))
                cv.imshow("img",img)
                # 裁剪圖片
                x, y, w, h = ROI
                dst = dst[y:y+h, x:x+w]
                dst=cv.resize(dst,(512,512))
                cv.imshow("Undistorted Result",dst)
                cv.waitKey(500)
            cv.destroyAllWindows()

    #畫線
    def draw(self,Image, Imgpts, Lines):
        count=0
        for i in range(Lines):
                #(影像, 開始座標, 結束座標, 顏色, 線條寬度) #.ravel()將多維數組轉換為一維數組的功能，如果沒有必要，不會產生源數據的副本
                Image = cv.line(Image, tuple(Imgpts[count].ravel()), tuple(Imgpts[count+1].ravel()), (0, 0, 255), 5) 
                count+=2
        return Image  

    #前三個字母轉換
    def change13(self,Axis,Node,x):
        y=5
        for i in range(Node):
            Axis[i][0]=Axis[i][0]+x
            Axis[i][1]=Axis[i][1]+y
        return Axis

    #後三個字母轉換
    def change46(self,Axis,Node,x):
        y=2
        for i in range(Node):
            Axis[i][0]=Axis[i][0]+x
            Axis[i][1]=Axis[i][1]+y
        return Axis

    def AR_onboard(self):
        #讀取使用者輸入
        Word=self.ui.lineEdit.text()

        #和第二題相似
        #檢查輸入長度是否符合規定，且所有字符都是字母
        if self.check(folder) and len(Word)<=6 and Word.isalpha(): 

            lib_onboard="./Q2_lib/alphabet_lib_onboard.txt"

            #通過FileStorage類讀取yaml 文件，FILE_STORAGE_READ用於讀取
            fs = cv.FileStorage(lib_onboard, cv.FILE_STORAGE_READ)

            Word=Word.upper() #將字母皆轉為大寫

            # 設定 criteria的參數值
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01) #TERM_CRITERIA_EPS測誤差有關#TERM_CRITERIA_MAX_ITER迭帶次數

            chess_row=8 
            chess_col=11 
            chess_size=88

            objp = np.zeros((chess_size,3), np.float32)
            #mgrid創造兩個二維數組（同行同值和同列同值)，並對產生的結果轉置(T)，接著reshape固定兩欄自動分配列數(-1)
            objp[:,:2] = np.mgrid[0:chess_col,0:chess_row].T.reshape(-1,2) #objp[][0]和[][1]儲存產生的兩個結果

            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.

            images=glob.glob(os.path.join(folder, "*.bmp")) #讀取所有圖檔
            file_num=len(images) #計算圖片個數
            sort_img=[]
            #將圖片照順序儲存
            for i in range(1,file_num+1):
                file_name=folder+'/'+str(i)+".bmp"
                sort_img.append(file_name)

            for fname in sort_img:
                img = cv.imread(fname)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv.findChessboardCorners(gray, (chess_col,chess_row), None)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    objpoints.append(objp)
                    #cornerSubPix對檢測到的角點作進一步的優化計算，可使角點的精度達到亞像素級別
                    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria) #(圖片,角點,區域大小,(-1,-1)代表忽略,停止優化的標準)
                    imgpoints.append(corners2)

            h,w=gray.shape[::-1]
            #ret:重投影誤差；mtx:相機的內參矩陣；dist:相機畸變參數；rvecs:標定棋盤格世界坐標係到相機坐標系的旋轉參數；tvecs:平移參數
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (w,h), None, None)#(世界坐標系中的點,其對應的圖像點,圖像的大小,內參數矩陣,畸變矩陣)      

            #在每張圖上畫上字母
            for i in range(file_num):
                img = cv.imread(sort_img[i])
                x1=7
                x2=7
                #依序將字母畫上
                for j in range(len(Word)): 
                    ch = fs.getNode(Word[j]).mat() #getNode獲得FileNode，mat()將 FileNode 轉換為矩陣
                    lines=ch.shape[0] #矩陣的列數代表字母的筆劃數
                    node=lines*2
                    if j<3:
                        axis = np.float32(ch).reshape(-1, 3)#將陣列內的數字儲存為浮點數，並使用reshape()來改變array的shape，(-1,3):自動計算列數、行數為3
                        axis=self.change13(axis,node,x1)
                        x1-=3
                        #將3D座標投影到2D平面上
                        imgpts, _ = cv.projectPoints(axis, rvecs[i], tvecs[i], mtx, dist)
                        imgpts=np.asarray(imgpts,dtype=int) #將陣列裡的值轉為整數
                    else:
                        axis = np.float32(ch).reshape(-1, 3)#將陣列內的數字儲存為浮點數，並使用reshape()來改變array的shape，(-1,3):自動計算列數、行數為3
                        axis=self.change46(axis,node,x2)
                        x2-=3
                        #將3D座標投影到2D平面上
                        imgpts, _ = cv.projectPoints(axis, rvecs[i], tvecs[i], mtx, dist)
                        imgpts=np.asarray(imgpts,dtype=int) #將陣列裡的值轉為整數
                    #將字母畫上圖
                    img = self.draw(img, imgpts, lines)
                img = cv.resize(img, (512, 512))
                cv.imshow('img', img)
                cv.waitKey(1000)

            cv.destroyAllWindows()

    def AR_vertically(self):

       #讀取使用者輸入
        Word=self.ui.lineEdit.text()

        #和第二題相似
        #檢查輸入長度是否符合規定，且所有字符都是字母
        if self.check(folder) and len(Word)<=6 and Word.isalpha(): 

            lib_vertical="./Q2_lib/alphabet_lib_vertical.txt"

            #通過FileStorage類讀取yaml 文件，FILE_STORAGE_READ用於讀取
            fs = cv.FileStorage(lib_vertical, cv.FILE_STORAGE_READ)

            #和第二題相似
            # 設定 criteria的參數值
            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01) #TERM_CRITERIA_EPS測誤差有關#TERM_CRITERIA_MAX_ITER迭帶次數

            chess_row=8 
            chess_col=11 
            chess_size=88

            objp = np.zeros((chess_size,3), np.float32)
            #mgrid創造兩個二維數組（同行同值和同列同值)，並對產生的結果轉置(T)，接著reshape固定兩欄自動分配列數(-1)
            objp[:,:2] = np.mgrid[0:chess_col,0:chess_row].T.reshape(-1,2) #objp[][0]和[][1]儲存產生的兩個結果

            objpoints = [] # 3d point in real world space
            imgpoints = [] # 2d points in image plane.

            images=glob.glob(os.path.join(folder, "*.bmp")) #讀取所有圖檔
            file_num=len(images) #計算圖片個數
            sort_img=[]
            #將圖片照順序儲存
            for i in range(1,file_num+1):
                file_name=folder+'/'+str(i)+".bmp"
                sort_img.append(file_name)

            for fname in sort_img:
                img = cv.imread(fname)
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv.findChessboardCorners(gray, (chess_col,chess_row), None)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    objpoints.append(objp)
                    #cornerSubPix對檢測到的角點作進一步的優化計算，可使角點的精度達到亞像素級別
                    corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria) #(圖片,角點,區域大小,(-1,-1)代表忽略,停止優化的標準)
                    imgpoints.append(corners2)

            h,w=gray.shape[::-1]
            #ret:重投影誤差；mtx:相機的內參矩陣；dist:相機畸變參數；rvecs:標定棋盤格世界坐標係到相機坐標系的旋轉參數；tvecs:平移參數
            ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, (w,h), None, None)#(世界坐標系中的點,其對應的圖像點,圖像的大小,內參數矩陣,畸變矩陣)      

            #在每張圖上畫上字母
            for i in range(file_num):
                img = cv.imread(sort_img[i])
                x1=7
                x2=7
                #依序將字母畫上
                for j in range(len(Word)): 
                    ch = fs.getNode(Word[j]).mat() #getNode獲得FileNode，mat()將 FileNode 轉換為矩陣
                    lines=ch.shape[0] #矩陣的列數代表字母的筆劃數
                    node=lines*2
                    if j<3:
                        axis = np.float32(ch).reshape(-1, 3)#將陣列內的數字儲存為浮點數，並使用reshape()來改變array的shape，(-1,3):自動計算列數、行數為3
                        axis=self.change13(axis,node,x1)
                        x1-=3
                        #將3D座標投影到2D平面上
                        imgpts, _ = cv.projectPoints(axis, rvecs[i], tvecs[i], mtx, dist)
                        imgpts=np.asarray(imgpts,dtype=int) #將陣列裡的值轉為整數
                    else:
                        axis = np.float32(ch).reshape(-1, 3)#將陣列內的數字儲存為浮點數，並使用reshape()來改變array的shape，(-1,3):自動計算列數、行數為3
                        axis=self.change46(axis,node,x2)
                        x2-=3
                        #將3D座標投影到2D平面上
                        imgpts, _ = cv.projectPoints(axis, rvecs[i], tvecs[i], mtx, dist)
                        imgpts=np.asarray(imgpts,dtype=int) #將陣列裡的值轉為整數
                    #將字母畫上圖
                    img = self.draw(img, imgpts, lines)
                img = cv.resize(img, (512, 512))
                cv.imshow('img', img)
                cv.waitKey(1000)

            cv.destroyAllWindows()

    def Disparity_Map_and_Disparity_Value(self):
        # mouse callback function
        def draw_circle(event, x, y, flags, param):
            if event == cv.EVENT_LBUTTONDOWN: #按滑鼠左鍵
                if disparity[y][x] < 0:
                    print(disparity[y][x])
                    print("failure case")
                    return
                else:
                    #校正x值(y值已被處理)，減掉兩張圖片的差距
                    new_x=x-disparity[y][x]
                    #再圖上顯示圓點
                    point=(int(new_x), int(y))
                    print(point, (x,y))
                    #更新的時候先show出最原本的圖案(沒有點的)，在更新程有點的圖
                    cv.imshow('imgR_dot', img2)
                    cv.circle(img2_c, point, 30, (0,100,255), -1)
                    cv.imshow('imgR_dot', img2_c)

        if self.check(image1) and self.check(image2):
            img1=cv.imread(image1) #imgL
            img2=cv.imread(image2)
            gray1= cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            gray2= cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

            #Compute disparity map
            stereo = cv.StereoBM_create(numDisparities=256, blockSize=25) #numDisparities：最大與最小視差值之差；blockSize：必須是> = 1的奇數
            disparity = stereo.compute(gray1, gray2).astype(np.float32) / 16.0 #Disparity range must be positive and divisible by 16.

            # normalize
            norm_disparity = cv.normalize(disparity, disparity, alpha=255,beta=0, norm_type=cv.NORM_MINMAX,dtype=cv.CV_8U) #CV_8U - 8位無符號整數（0..255 ）

            # focal_len = 4019.84 
            # baseline = 342.789
            # Cx = 279.184 #C𝑥_𝑟𝑖𝑔ℎ𝑡−Cx_𝑙𝑒𝑓𝑡
            # dist = abs( - Cx) #d(distance) = (point) - Cx
            # depth = int(focal_len * baseline / dist) #Z(depth) = focal_length * baseline / d

            #resize
            cv.namedWindow('disparity', cv.WINDOW_NORMAL)
            cv.resizeWindow('disparity', (255, 190))
            cv.imshow("disparity",norm_disparity)

            cv.namedWindow('imgR_dot', cv.WINDOW_NORMAL)
            cv.namedWindow('imgL', cv.WINDOW_NORMAL)
            cv.resizeWindow('imgL', (255, 190))
            cv.resizeWindow('imgR_dot', (255, 190))

            cv.imshow('imgR_dot', img2)
            cv.imshow('imgL', img1)
            while(1):
                cv.imshow('imgL', img1)
                img2_c = img2.copy() #不更動原本img2的圖
                cv.setMouseCallback('imgL', draw_circle) #當滑鼠有動作時，會呼叫draw_circle函式(滑鼠回調函數
                #按esc離開程式
                if cv.waitKey(20) & 0xFF == 27:
                    break
            cv.waitKey(0)
            cv.destroyAllWindows()


