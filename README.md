# 電商系統 

# 作品功能簡介 
此作品為電商網站，功能有庫存管理、訂單處理、客戶服務等。消費者可以選擇商品，購買並且下單，後端這邊可以看到使用者的訂購資料，可以讓商家出貨。

---
# 作品介紹 

下圖為電商網站首頁 
這邊有所以的商品列表，消費者看點擊圖片觀看詳細商品介紹，或是點擊加入購物車。


![](https://hackmd.io/_uploads/r1MiNOC-a.png)
![](https://hackmd.io/_uploads/HJRkH_AWp.png)


下圖為商品詳細介紹頁面，有商品的簡介，和相關資訊。

![](https://hackmd.io/_uploads/HJpDr_0b6.png)

當我們點選加入購物車的時候，會到達下圖的購物車頁面。
這邊可以選擇繼續購物，或是更改購買商品的數量，以及結帳按鈕。

![](https://hackmd.io/_uploads/B1x_jB_CWp.png)

點選結帳，進入結帳頁面後，會需要輸入客戶的基本資料。

![](https://hackmd.io/_uploads/SkpMUu0W6.png)

點選確認購買後，會進入訂購完成畫面，且訂購資料已經傳送到後端資料庫

![](https://hackmd.io/_uploads/BkWxP_0-a.png)

後台SQLite資料庫有此筆買家訂單，id 23 為訂單編號
![](https://hackmd.io/_uploads/BkCyudC-T.png)
![](https://hackmd.io/_uploads/ByKg_ORZa.png)

且有訂購商品列表，dorder_id 為訂單編號23訂購的商品，目前有一台Macbook pro 14  
![](https://hackmd.io/_uploads/rkkJuOR-p.png)
![](https://hackmd.io/_uploads/SkfCwOAbT.png)

這樣賣家就可以從後台直接出貨了!                    




# 程式碼細節介紹


## 資料庫部分
如要新增產品則直接從django後台新增。

商品照片則自行加入static這個資料夾即可，django在載入的時候，會去static資料夾中搜尋這個檔名的照片來使用。
![](https://hackmd.io/_uploads/BkSWco6ba.png)


## router 部分 
這邊根據不同的功能，讓使用者連接到view裡面不同的function ，
另外再同一個名稱的router上有不同的引數，是為了判斷要執行這個function的哪一個部分。

```python=
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index),
    path("index/",views.index),
    path("detail/<int:productid>",views.detail),
    path("addtocart/<str:ctype>/",views.addtocart), # 參數有none 所以可以產生函式"多型"的效果
    path("addtocart/<str:ctype>/<int:productid>/",views.addtocart),
    path("cart/",views.cart), 
    path("cartorder/",views.cartorder),
    path("cartok/",views.cartok),
    path("cartordercheck/",views.cartordercheck),
    path('ecpay/', views.ecpay_view),
    
]

```


## 整體程式碼流程(使用者寫入資料庫 )： 

1. 前端使用form接收表單資料
2. 根據form的傳送位置
3. 到達router決定要把資料給到view中那一個function
4. function 再決定要怎麼處理資料
5. function使用ORM語言寫入資料庫
6. 把執行結果渲染在前端頁面 



