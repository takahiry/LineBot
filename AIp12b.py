# AIp12b.py: AI practices - 12 > program b: a Web proctor/guesser of AB game
# Jia-Sheng Heh, 10/24/2019, revised from AIp11dd.py

#################### AIp12b.py ####################

#####===== (1) Git/GitHub 遠端同步操作 =====#####
###=== (1.1) GitHub ===###
###=== (1.2) 註冊GitHub帳號 ===### 
###=== (1.3) Git安裝與安裝 ===### 
###=== (1.4) 工作目錄(repository)設定 ===###
###=== (1.5) 工作目錄同步 ===### 

#####===== (2) Heroku =====#####
###=== (2.1) Heroku ===###
###=== (2.2) 註冊Heroku帳號 ===###
###=== (2.3) 安裝命令行工具CLI ===###
###=== (2.4) 建立新應用 ===###

#####===== (3) 結合VScode/Flask/Git/Heroku建立網頁 =====#####
###=== (3.1) 建立新應用 ===###  
# 進入官網 —-> New App —-> 取專案名稱(AIp12x) —-> Deploy
###=== (3.2) VScode建立Flask專案描述檔案 ===###  
# 建立 (1) runtime.txt: 描述使用的python環境
# 建立 (2) requirements.txt: 描述程式運作所需要的套件
# 建立 (3) Profile: 告訴Heroku如何執行程式
#    web gunicorn AIp12b:app
# 建立本程式碼 (4) AIp12b.py:  (revised from AIp11dd.py)
###=== (3.3) 先在本機上測試本程式 ===###  
## (1) 建立 目錄/venv/.flaskenv 指定 flask程序
#    FLASK_APP=AIp12b.py
## (2) 終端機中執行flask，啟動flask伺服器
#    $ flask run
#    如果有問題的話，先執行 ...  $ export FLASK_APP=AIp11c.py
## (3) 在瀏覽器中調用 
# http://127.0.0.1:5000/      --> Hello Flask 2

###=== (3.4) 將程式部署到Heroku App,並測試 ===###  
# $ heroku login              // 登入 Heroku
# $ git init                  // 初始化專案
# $ heroku git:remote -a 專案名稱  // 專案名稱 = aip12x
# $ git add .                // 更新專案 
# $ git commit -m “更新的訊息”
# $ git push heroku master
# --> 部署的網址： https://aip12x.herokuapp.com/   
#---
# $ rm -f .git   // 清除 git 必要的話


#####===== (4) AIp12b.py =====##### ===> revised from AIp11dd.py ***

###=== (4.1) 載入軟件包與自製函數(initialY,computeAB,updateY,centerY,judgeX) ===###
from flask import Flask, request, url_for, redirect, render_template, Markup
import numpy as np
import pandas as pd
def initialY(NN):   #-- generate all possible solutions
    NN10 = 10**NN
    y = set(np.arange(10))
    Y = [(y1,y2,y3,y4) for y1 in y for y2 in y-{y1} for y3 in y-{y1,y2} for y4 in y-{y1,y2,y3}]
    YY = np.array(Y)
    YS = list()
    for ind in np.arange(YY.shape[0]): YS.append(set(Y[ind]))
    return YY,YS
def tableY(YY):     #-- tabulate YY to Ytable/Ydf (NO LONGER USED)
    Ytable = np.zeros((4,10),dtype=np.int)
    Ytable.shape
    for k in np.arange(4):
        for j in np.arange(10):
            Ytable[k,j] = np.sum(YY[:,k]==j)
    Ytable
    Ydf = pd.DataFrame(Ytable);   Ydf
    return Ytable, Ydf
def computeAB(X1,YY1,YS1):  #-- compute nA,nB
    ### (4*) form X array/sets (X-->XX,XS) #####
    XX1 = np.array(list(X1)*YY1.shape[0]).reshape(YY1.shape[0],4)
    XS1 = set(X1)
    ### (5*) calculate (nA,nB) outcomes
    nA1 = np.sum(XX1==YY1, axis=1)   #-- np.sum(nA==1): counts for 1A2B
    nB1 = np.zeros(YY1.shape[0],dtype=np.int)
    for ind in np.arange(YY1.shape[0]): nB1[ind] = 4 - len(XS1-YS1[ind]) - nA1[ind]
    return nA1,nB1
def updateY(YY1,YS1,IND1):  #-- update YY1,YS1
    ### (6*) iterate YY and YS
    YY2 = YY1[IND1]   
    YS2 = [YS1[i] for i in IND1]
    return YY2,YS2
def centerY(ZZ):            #-- center of ZZ array
    Zmean0 = ZZ.mean(axis=0);                 # print("Zmean0 = ",Zmean0)
    Zmean = np.array(list(Zmean0)*ZZ.shape[0]).reshape(ZZ.shape[0],4);   # print("Zmean = ",Zmean)
    D = ((ZZ-Zmean)*(ZZ-Zmean)).sum(axis=1);  # print("D = ",D)
    return ZZ[D.argmin()]
def judgeX(X,Xactual):      #-- judge (nA,nB) of X
    nAX = np.sum(X==Xactual);                     
    nBX = 4 - len(set(X) - set(Xactual)) - nAX;   
    # print("nAX = ",nAX,", nBX = ",nBX)
    return nAX,nBX

###=== (4.2) 設定對話(kk,openF,answerF) ===###
# Xactual = np.array([3,1,4,5])   
kk = 0
openF = "<H3>歡迎加入 AB 遊戲: 電腦猜題</H3>    <p>這是一個猜測四個相異的 0-9數字的問題</p>" \
        "<p>A 表示數字對，而且位置也對</p>       <p>B 表示數字對，但位置不對</p>" \
        "<p>現在，你來當 出題者 喔... (電腦是 猜題者 guesser)"  \
        "<hr><p>來出個題吧!!</p>"                                 #-- openF: 會話啟始(opening)
answerF = openF + "<hr color='orange'>" + "<H3>猜測過程：</H3>"   #-- answerF: 互動時答覆(answering) 

app = Flask(__name__)   

###=== (4.3) 會話啟始(kk,X-->openF-->) ===###
@app.route("/")                   
def index():
    global openF
    return render_template('conversationDD.html', sayF=Markup(openF))

###=== (4.4) 會話互動(interaction: Questioning-Answering)) ===###
@app.route("/interact")           
def interact():
    global kk, X, openF, answerF              
    ##== (4.4A) Questioning: 互動時取得詢問值(query d1/,,/d4-->Y-->nA/nB) ==##
    dd = request.values['dd'];
    Xactual = np.array(list(dd)).astype(np.int)
    print("Xactual =",Xactual)
    ##== (4.4B) 產生所有可能解 (YY/YS) 與 確定題目 (Xactual) ==##
    NN = 4;   
    YY,YS = initialY(NN);   print("YY.shape = ",YY.shape)
    print("YY[0:5] = ",YY[0],YY[1],YY[2],YY[3],YY[4])   
    ##== (4.4C) 猜測迴圈 (X: YY/YS-->YY1/YS1) ==##
    while ((YY.shape[0]>1) & (kk<8)):
        kk = kk+1
        if (kk==1):    X = np.array([3,1,2,5])
        elif (kk==2):  X = np.array([4,7,9,8])
        else:          X = centerY(YY)
        nAX,nBX = judgeX(Xactual,X)
        print("\n###### >> kk = ",kk,": 猜測 X = ",X,", nAX = ",nAX,", nBX = ",nBX,"######")  
        answerF = answerF + "<p> 第 "+str(kk)+" 次猜測: X = "+str(X)+", 可以得到 "+str(nAX)+"A"+str(nBX)+"B </p>"
        # Ytable,Ydf = tableY(YY);        print("Ydf = \n",Ydf)
        nA,nB = computeAB(X,YY,YS);     print("nA[0:5] = ",nA[0:5],", nB[0:5] = ",nB[0:5])
        IND = np.where((nA==nAX) & (nB==nBX))[0];   print("len(IND) = ",len(IND),", IND[0:6] = ",IND[0:6])   
        YY1,YS1 = updateY(YY,YS,IND);   print("YY1[0:3] = ", YY1[0:3] )
        YY = YY1;   YS = YS1
    ##== (8.4D) 會話結語(closing: open/answerF-->convF-->closing say) ==##    
    print("\n>> answerF = ",answerF)    
    print("\n>> The Result YY = ",YY)    
    # return redirect(url_for("closing",convF=answerF,answer=str(YY)))
    return redirect(url_for("closing",answer=str(YY)))
    # answerF = answerF + "最後答案是 X ＝ " + str(YY)
    # return "<html><body>" + answerF + "</body></html>"

###=== (4.5) 會話結話(closing: open/answerF-->convF-->closing say) ===###
@app.route("/closing/<string:answer>")   # /<string:convF>   
def closing(answer):
    global answerF
    print("*** closing ***")
    # convF1 = convF
    convF1 = answerF + "最後答案是 X ＝ " + answer
    return "<html><body>" + convF1 + "</body></html>"

if __name__ == '__main__':
    app.run() 