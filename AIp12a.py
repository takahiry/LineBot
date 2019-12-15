# AIp12a.py: AI practices - 12 > program a: a test program for gitHub and Heroku
# Jia-Sheng Heh, 10/21/2019, revised from AIp11c.py

#################### AIp12a.py ####################

#####===== (1) Git/GitHub 遠端同步操作 =====##### ----> AIp11c.py ===> 本程式 AIp12a.py ***
# [Youtube: github简单使用教程]
# [Git 與 Github 版本控制基本指令與操作入門教學 | TechBridge 技術共筆部落格]

###=== (1.1) GitHub ===### [維基]
# 透過Git進行版本控制的軟體原始碼代管服務平台，
# 同時提供付費帳戶和免費帳戶，都可以建立公開或私有的程式碼倉庫(repo)，免費用戶的私有倉庫最多指定三個合作者
# 到2015年，已有超過兩千八百萬註冊用戶和5700萬程式碼庫，為了世界上最大的程式碼存放網站和開源社群。
# 由GitHub公司的開發者Chris Wanstrath、PJ Hyett和Tom Preston-Werner開發，於 2018年被微軟收購

###=== (1.2) 註冊GitHub帳號 ===### 
##== public/private repo: free/限制三位協作者 
##== github.com 註冊帳號
##== GitHub網站中 New Repository --> repository name 
#      --> 簡短專案描述 x( 初始化 README.md / .gitignore / LICENSE授權 )
#      --> create —-> 會有一個 SSH的 git網址

###=== (1.3) Git安裝與安裝 ===### 
##==   (1.3.1) Git安裝 ==##
##        $ brew install git    
##        $ git --version
##==   (1.3.1) Git設定 ==##
##        $ git config --global user.name "使用者名稱"
##        $ git config --global user.email "使用者郵箱" 
##        $ git config --list

###=== (1.4) 工作目錄(repository)設定 ===### -------------------
##==   (1.4.1) 建立本機的repository專案工作目錄 ==##
#       $ cd 目錄
#       $ git init     --> 設定本機的repository (.git隱藏目錄，可以Shift-Cmd->顯示)
##==   (1.4.2) 本機/遠端 repository連結 ==##
#       $ git remote add origin git網址

###=== (1.5) 工作目錄同步 ===### 
##==   (1.5.1) 檢視狀態,增修與commit ==##
#       $ git status   --> 檢視repository狀態
#       $ git add 檔名  --> 新增追蹤檔案
#       $ git add *    —-> 新增本目錄中所有檔案
#       $ git rm 檔名   --> 刪除追蹤檔案
#       $ git commit -m “1STcommitALL”  --> 本地工作目錄儲存，並設定儲存訊息
##==   (1.5.2) GitHub同步：本機/遠端 repository連結 ==##
#       $ git push -u origin master     --> push到遠端工作目錄


#####===== (2) Heroku =====#####
# [Youtube: Python Flask 網站開發 - Heroku 雲端主機教學 By 彭彭]

###=== (2.1) Heroku ===### [維基]
# 支援多種程式語言的雲平台即服務，從支擾Ruby，到Java、Node.js、Scala、Clojure、Python以及PHP和Perl
# 從2007年6月起開發，在2010年被Salesforce.com收購

###=== (2.2) 註冊Heroku帳號 ===###
# 進入官網 https://id.heroku.com/signup --> 電郵帳號 --> Sign Up 
# --> 收信，再線上確認 --> Password / Confirm Password --> Save

###=== (2.3) 安裝命令行工具CLI ===###
# 安裝Heroku命令行工具 (Heroku CLI)

###=== (2.4) 建立新應用 ===###  -----------------------------------
# 進入官網 —-> New App —-> 取專案名稱(test-program-peng) —-> Deploy


#####===== (3) 結合VScode/Flask/Git/Heroku建立網頁 =====#####

###=== (3.1) 建立新應用 ===###  ...沿用 (2.4)
# 進入官網 —-> New App —-> 取專案名稱(AIp12x) —-> Deploy

###=== (3.2) VScode建立Flask專案描述檔案 ===###  
# $ cd ../AIp12x
# 建立 (1) runtime.txt: 描述使用的python環境
#    python-3.6.4
# 建立 (2) requirements.txt: 描述程式運作所需要的套件
#    Flask
#    gunicorn
# 建立 (3) Profile: 告訴Heroku如何執行程式
#    web gunicorn app:app
# 建立本程式碼 (4) AIp12a.py:  (revised from AIp11c.py)

from flask import Flask
import sys

app = Flask(__name__)    # __name__ 代表目前執行的模組

@app.route("/")      #== 函式的裝飾(Decorator): 以函式為基礎，提供附加的功能
def home():
    print("This is route_home")
    #sys.stdout.flush()
    return "Hello Flask 2"

@app.route("/test")  #== 代表我們要處理的網站路徑
def test():
    print("This is test")
    #sys.stdout.flush()
    return "This is a Test"

if __name__=="__main__":  # 如果以上程式執行
    app.run()   # 立刻啟動伺服器

###=== (3.3) 將程式部署到Heroku App,並測試 ===###  
# $ heroku login              // 登入 Heroku
# $ git init                  // 初始化專案
# $ heroku git:remote -a 專案名稱  // 專案名稱 = aip12x
# $ git add .                // 更新專案
# $ git commit -m “更新的訊息”
# $ git push heroku master

# $ rm -f .git   // 清除 git 必要的話

# --> 部署的網址： https://aip12x.herokuapp.com/   