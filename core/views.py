from django.shortcuts import HttpResponse
from django.shortcuts import render ,redirect

# Create your views here.
from core import models   # 引入我們app 的models 才可以access 裡面的table 
from smtplib import SMTP, SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText


message = ''
cartlist = []  #購買商品串列
customname = ''  #購買者姓名
customphone = ''  #購買者電話
customaddress = ''  #購買者地址
customemail = ''  #購買者電子郵件
final_grandtotal=0

def index(request):
    
    global cartlist  # 宣告全域變數 
    
    if "cartlist" in request.session:  #看session 有沒有在購物車購買的串列
        cartlist=request.session["cartlist"]
    else :  # 重新購物
        cartlist=[]
    cartnum=len(cartlist) # 購物車商品數量

    productall=models.ProductModel.objects.all() # 取出目前所有的商品，一個個放在首頁，商品照片放在staitc，資料庫存照片檔名就好
    
    return render(request, "index.html",locals())
    
    
# productid 預設為0 這樣連到就會是空的頁面 不會報錯     
def detail(request,productid=None): 
    product=models.ProductModel.objects.get(id=productid)  # 從index html 取得的id，傳到這邊 ，再傳給detail.html
    return render(request,"detail.html",locals())
    


def cart(request):
    global cartlist 
    cartlist1= cartlist  #把目前在訂購祝列 render 到購物車頁面
    
    total=0 
    for unit in cartlist: 
        total += int(unit[3])  # 商品資料的第四項為總價
        
        
    grandtotal=total+ 100 
    
    return render(request,"cart.html",locals())





def addtocart(request, ctype=None, productid=None ):
    global cartlist 
    if ctype=="add": # 對應的function 內容，用網址列去控制 
        product=models.ProductModel.objects.get(id=productid) # 從資料庫取出要加入的商品(由id )
        
        flag=True # 設定檢查旗標
        
        for unit in cartlist: #檢查商品是否已經存在
            if product.pname==unit[0]: 
                unit[2]=str(int(unit[2])+1) # 數量加一
                unit[3]=str(int(unit[3])+product.pprice) # 計算價錢 直接暴力從加一次==? 
                flag=False # 如果找到商品就 關閉檢查flag，否則就持續開啟
                
                break 

        if flag:  #如果flag 開啟 = 沒有找到商品
            temlist=[] 
            temlist.append(product.pname) # 將商品加入暫時串列 # unit[0]
            temlist.append(str(product.pprice)) # 商品單價# unit[1]
            temlist.append("1") # 商品數量為1 因為我們本來的商品頁面 沒有設定一次能加多個數量的同一商品 所以就固定為一個 # unit[2]
            
            # carlist是一個2為串列 所以unit[3] 是商品總價
            temlist.append(str(product.pprice)) # 商品總價# unit[3]
            
            cartlist.append(temlist) #把單一商品資訊 加入購買總數
        
        request.session["cartlist"]=cartlist # 加入session 
        return redirect("/cart/") 
    
   
    elif ctype=="update" : #在購物車頁面用按鈕去觸發這個判斷式區間。
        n=0 
        for unit in cartlist: 
            unit[2]=request.POST.get('qty'+str(n),"1") # qty 為數量的參數，但是他有順序參數，所以要加上n， 1為預設值數量
            unit[3]=str(int(unit[1])*int(unit[2]))  #  取得商品總價 
            n+=1 
        request.session["cartlist"]=cartlist
        return redirect("/cart/") # 重新router 到這個path 然後會在呼叫對應的function 就是cart function 然後把新的資料render 到cart.html
    
    elif ctype=="empty": #在購物車頁面用按鈕的網址去觸發這個判斷式區間。
        cartlist=[]
        request.session["cartlist"]=cartlist # 更新session 
        return redirect("/cart/")
    
    elif ctype=="remove": #在購物車頁面用按鈕的網址去觸發這個判斷式區間。
        del cartlist[int(productid)]
        request.session["cartlist"]=cartlist
        return redirect("/cart/")
    

def cartorder(request):
    global cartlist, message, customname, customphone, customaddress, customemail,final_grandtotal # 取得全域變數購物車資訊和購買者資訊
    cartlist1 = cartlist
    total = 0
    for unit in cartlist:  #計算商品總金額
        total += int(unit[3])
    grandtotal = total + 100
    final_grandtotal=grandtotal
    customname1 = customname  ##以區域變數傳給模版
    customphone1 = customphone
    customaddress1 = customaddress
    customemail1 = customemail
    message1 = message
    return render(request, "cartorder.html", locals())


def cartok(request):
    global cartlist, message, customname, customphone, customaddress, customemail # 取得全域變數購物車資訊和購買者資訊
    
    total=0 
    
    for unit in cartlist: 
        total += int(unit[3])
        
    grandtotal = total + 100
    message = ''
    customname = request.POST.get('CustomerName', '')
    customphone = request.POST.get('CustomerPhone', '')
    customaddress = request.POST.get('CustomerAddress', '')
    customemail = request.POST.get('CustomerEmail', '')
    paytype = request.POST.get('paytype', '')
    
    customname1 = customname # 等等要傳到cartok.html 顯示
    
    if customname==""  or customphone==" " or customaddress==" " or customemail== " " : 
        message = '姓名、電話、住址及電子郵件皆需輸 入'
        return redirect("/cartorder/")
    
    else: 
        # 建立訂單 寫入資料庫  
        unitorder = models.OrdersModel.objects.create(subtotal=total, shipping=100, grandtotal=grandtotal, customname=customname, customphone=customphone, customaddress=customaddress, customemail=customemail, paytype=paytype) #建立訂單
        mailto=customemail  #收件者
        for unit in cartlist:
            total = int(unit[1]) * int(unit[2])
            # 把""這一個顧客所定的所有東西，都加入cartlist"
            unitdetail=models.DetailModel.objects.create(dorder=unitorder,pname=unit[0],unitprice=unit[1],quantity=unit[2],dtotal=total)
            
        orderid=unitorder.id
        
        ## email section 
        
        carlits=[]
        request.session["carlist"]=cartlist
        return render(request,"cartok.html",locals())
            
            

def cartordercheck(request):  #查詢訂單
	orderid = request.GET.get('orderid', '')  #取得輸入id
	customemail = request.GET.get('customemail', '')  #取得輸email
	if orderid == '' and customemail == '':  #按查詢訂單鈕
		firstsearch = 1
	else:
		order = models.OrdersModel.objects.filter(id=orderid).first()
		if order == None or order.customemail != customemail:  #查不到資料
			notfound = 1
		else:  #找到符合的資料
			details = models.DetailModel.objects.filter(dorder=order)
	return render(request, "cartordercheck.html", locals())



from .ecpay_testing import main


def ecpay_view(request):
    global cartlist, message, customname, customphone, customaddress, customemail ,final_grandtotal
    
    return HttpResponse(main(cartlist, message, customname, customphone, customaddress, customemail,final_grandtotal ))