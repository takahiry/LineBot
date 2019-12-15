# AIp12d.py: AI practices - 12 > program d: a Chatbot of AB game
# Jia-Sheng Heh, 10/27/2019, revised from AIp12c.py and AIp12b.py

#################### AIp12b.py ####################

#####===== (1) Git/GitHub 遠端同步操作 =====#####
#####===== (2) Heroku =====#####
#####===== (3) LINE Developer建立bot =====#####
###=== (3.1) 申請 LINE Developer帳號 ===###  
###=== (3.2) 創建 bot 機器人 ===###  
###=== (3.3) 機器人訊息 ===###  
# LINE Developer —> Provider List —-> 選擇機器人 —-> Channel settings 
#   + Channel Secret 密碼* + Channel Access Token 密碼* ===> 用於webhook程式 (5.3)
#   ＋ QR code                                         ===> 用於加入群組

#####===== (4) 結合VScode/Flask/Git/Heroku建立網頁 =====#####
###=== (4.1) 建立新應用 ===###  
###=== (4.2) VScode建立Flask專案描述檔案 ===###  
# 建立 (1) runtime.txt:        描述使用的python環境
# 建立 (2) requirements.txt:   加上 line-bot-sdk
# 建立 (3) Profile:            web gunicorn AIp12d:app
# 建立本程式碼 (4) AIp12d.py
###=== (4.3) 先在本機上測試本程式 ==> 此步無法進行，可加入 heroku 偵錯 (參見4.5)
###=== (4.4) 將程式部署到Heroku App,並測試 ===###  
# $ heroku login              // 登入 Heroku
# $ git init                  // 初始化專案
# $ heroku git:remote -a 專案名稱  // 專案名稱 = aip12x
# $ git add .                // 更新專案 
# $ git commit -m “更新的訊息”
# $ git push heroku master   // --> 部署的網址： https://aip12x.herokuapp.com/   
###=== (4.5) 在部署Heroku時，同時偵錯 ===###  
# 建議 開設兩個 Terminals, 一個部署(如 4.4), 一個偵錯(如下行指令)
# $ heroku logs --tail --app aip12x   (偵錯指令)
# 偵錯時，在程式碼中 加入 print()

#####===== (5) AIp12d.py =====##### ===> 網路簡易範例

###=== (5.1) 載入軟件包 與自製函數(initialY,computeAB,updateY,centerY,judgeX) ===###  
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import( InvalidSignatureError )
from linebot.models import *    
from flask import Flask, request, abort #---------- 下述是加入 ABgame
from flask import url_for, redirect, render_template, Markup
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

###=== (5.2) 設定對話(kk,openF,answerF) ===###
Xactual = np.array([1,2,3,4])   
openF1 = "歡迎加入 AB 遊戲: 猜測四個相異的 0-9數字。A 表示數字對，而且位置也對；B 表示數字對，但位置不對。" 
openF2 = "來出個 四個0-9數字 的題目!!"                              #-- openF: 會話啟始(opening)
app = Flask(__name__)  # __name__ 代表目前執行的模組

###=== (5.3) LINE介面密碼 ===### (參考3.3)
##== (1) Channel Access Token
line_bot_api = LineBotApi("Nr6mCIsNGslpKJagqwGXYLetpQx0UF2bfmvDAupvFIMmZ/ntSDWrVcRAPOI+OUeklrEWYaU96foNY0rOD+4wXNNPkvAKVGdFbXkcu3r9fblG+zBFT7dx4wjhXksPINOC4G3q6XffuRn/WDIJXoXNEQdB04t89/1O/w1cDnyilFU=")  #-- YOUR_CHANNEL_ACCESS_TOKEN
##== (2) Channel Secret
handler = WebhookHandler("48f6b1096e13a1d04269785c75363a8c")  #-- YOUR_CHANNEL_SECRET

###=== (5.4) 監聽來自 /callback 的 Post Request  ===###
@app.route("/callback", methods=['POST']) 
def callback():
    print(">>>>>>>>> 1.testing")  # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print(">>>>>>>>> 2.testing")  # get request body as text
    body = request.get_data(as_text=True)
    print(">>>>>>>>> 3.testing"+body)
    app.logger.info("Request body: " + body)
    print(">>>>>>>>> 4.testing-body:"+body)
    # handle webhook body
    try:
        print(">>>>>>>>> 5.testing-try:...")
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

###=== (5.5) 處理訊息  ===###
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global Xactual
    print(event)
    if event.message.id == "100001":
        return
    text = event.message.text
    print(">>>>>>>>>> TEXT = "+text)
    if (text=="Hi"):      reply_text = "Hello"
    elif(text=="機器人"):  reply_text = "有！我是機器人，在喔！"
    elif(text=="你好"):    reply_text = "你好啊..."
    elif(text.upper()=="H"):    
        reply_text = "關鍵字說明：(1)'介紹'--說明AB遊戲。(2)'舉例'--隨機產生X四位數字。(3)'變量'--顯示目前X四位數字。(4)'解題'--說明解題過程。(5)四位相異數字--出題。(0)其他關鍵字--Hi,你好,機器人"
    elif(text=="介紹"):    reply_text = openF1
    elif(text=="舉例"):    
        print(">>>>>>>>>> 舉例1")
        Xactual = np.random.choice(range(10),4,replace=False)
        print(">>>>>>>>>> 舉例2: Xactual = ",Xactual)
        reply_text = "".join(["X=",''.join(map(str,Xactual))])
    elif(text=="變量"):    
        reply_text = "".join(["X=",''.join(map(str,Xactual))])
    elif(text=="解題"):    
        X = Xactual
        print(">>>>>>>>>> 解題1: Xactual = ",X)
        #== (前4.4B) 產生所有可能解 (YY/YS) 與 確定題目 (Xactual) ==##
        NN = 4;   kk = 0;   answerF = "猜測過程："
        YY,YS = initialY(NN);   print("YY.shape = ",YY.shape)
        print(">>>>>>>>>> 解題2: YY[0:5] = ",YY[0],YY[1],YY[2],YY[3],YY[4])   
        ##== (前4.4C) 猜測迴圈 (X: YY/YS-->YY1/YS1) ==##
        while ((YY.shape[0]>1) & (kk<8)):
            kk = kk+1
            if (kk==1):    X = np.array([3,1,2,5])
            elif (kk==2):  X = np.array([4,7,9,8])
            else:          X = centerY(YY)
            nAX,nBX = judgeX(Xactual,X)
            print(">>>>>>>>>> 解題3: \n###### >> kk = ",kk,": 猜測 X = ",X,", nAX = ",nAX,", nBX = ",nBX,"######")  
            answerF = answerF + "第 "+str(kk)+" 次猜測: X = "+str(X)+", 可以得到 "+str(nAX)+"A"+str(nBX)+"B。"
            # Ytable,Ydf = tableY(YY);        print("Ydf = \n",Ydf)
            nA,nB = computeAB(X,YY,YS);     print("nA[0:5] = ",nA[0:5],", nB[0:5] = ",nB[0:5])
            IND = np.where((nA==nAX) & (nB==nBX))[0];   print("len(IND) = ",len(IND),", IND[0:6] = ",IND[0:6])   
            YY1,YS1 = updateY(YY,YS,IND);   print("YY1[0:3] = ", YY1[0:3] )
            YY = YY1;   YS = YS1
        print(">>>>>>>>>> 解題4: answerF = ",answerF)   
        answerF = answerF + "最後答案是 " + "".join(["for X=",''.join(map(str,YY))])
        print(">>>>>>>>>> 解題5: answerF = ",answerF)   
        reply_text = answerF
        # reply_text = "".join(["for X=",''.join(map(str,Xactual))])
    else:  # 如果非以上的選項，就會學你說話
        print(">>>>>>>>>> 出題1: text = ",text)
        try:
            V = int(text)
            Xactual = list(map(int, list(text)))
            print(">>>>>>>>>> 出題2: Xactual = ",text)
            reply_text = "".join(["設定 X=",text])
        except ValueError:
            Xstr = ''.join(map(str,Xactual))
            reply_text = "".join([text, "。 跟你說，現在的 X=",Xstr,"你可以試著'解題'看看..."]) 
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

###=== (5.6) 執行程式  ===###
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
