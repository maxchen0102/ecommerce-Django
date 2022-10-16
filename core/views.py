from django.shortcuts import render

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






        
        
    