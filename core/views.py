from django.shortcuts import render ,redirect

# Create your views here.
from core import models   # 引入我們app 的models 才可以access 裡面的table 
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText



carlist=[] 


def index(request):
    
    global carlist  # 宣告全域變數 
    
    if "carlist" in request.session:  #看session 有沒有在購物車購買的串列
        carlist=request.session["cartlist"]
    else :  # 重新購物
        carlist=[]
    cartnum=len(carlist) # 購物車商品數量

    productall=models.ProductModel.objects.all() # 取出目前所有的商品，一個個放在首頁，商品照片放在staitc，資料庫存照片檔名就好
    
    return render(request, "index.html",locals())
    
    
# productid 預設為0 這樣連到就會是空的頁面 不會報錯     
def detail(request,productid=None): 
    product=models.ProductModel.objects.get(id=productid)  # 從index html 取得的id，傳到這邊 ，再傳給detail.html
    return render(request,"detail.html",locals())
    


def cart(request):
    global carlist 
    carlist1= carlist 
    
    total=0 
    for unit in carlist: 
        total += int(unit[3])  # 商品資料的第四項為總價
        
        
    grandtotal=total+ 100 
    
    return render(request,"cart.html",locals())






def addtocart(request, ctype=None, productid=None ):
    global carlist 
    if ctype=="add": # 對應的function 內容，用網址列去控制 
        product=models.ProductModel.objects.get(id=productid) # 從資料庫取出要加入的商品(由id )
        
        flag=True # 設定檢查旗標
        
        for unit in carlist: #檢查商品是否已經存在
            if product.pname==unit[0]: 
                unit[2]=str(int(unit[2])+1) # 數量加一
                unit[3]=str(int(unit[3])+product.pprice) # 計算價錢 直接暴力從加一次==? 
                flag=False # 如果找到商品就 關閉檢查flag，否則就持續開啟
                
                break 

        if flag:  #如果flag 開啟 = 沒有找到商品
            temlist=[] 
            temlist.append(product.pname) # 將商品加入暫時串列
            temlist.append(str(product.pprice)) # 商品單價
            temlist.append("1") # 商品數量為1 因為我們本來的商品頁面 沒有設定一次能加多個數量的同一商品 所以就固定為一個
            
            # carlist是一個2為串列 所以unit[3] 是商品總價
            temlist.append(str(product.pprice)) # 商品總價
            
            carlist.append(temlist) #把單一商品資訊 加入購買總數
        
        request.session["carlist"]=carlist # 加入session 
        return redirect("/cart") 
        
    