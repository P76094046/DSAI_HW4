# DSAI_HW4

- report google silde: https://drive.google.com/file/d/1FAGsdAZw_mbuFgjZoz1Nr2M9QEXLMmXD/view?usp=sharing

### 下載需要的套件以及 XGBoost
XGBoost 可到 https://www.lfd.uci.edu/~gohlke/pythonlibs/#xgboost 下載 xgboost‑1.3.1‑cp36‑cp36m‑win_amd64.whl 後安裝

```
pip install xgboost‑1.3.1‑cp36‑cp36m‑win_amd64.whl
```
(參考此篇：https://hackmd.io/@allen108108/ryup_ppvV)


### 下載 Dataset
- 下載此資料夾 https://drive.google.com/drive/folders/191ThFZSKoWIqWaIIiKhDLupbTAMLUZH_?usp=sharing 和程式碼放到同一個資料夾
- 將當前路徑改到該資料夾後即可執行  
資料關係如下圖  
![image](https://github.com/P76094046/DSAI_HW4/blob/main/images/%E6%93%B7%E5%8F%96.PNG)

### Feature Engineering
新增了一些可用於訓練的 features
- **User features**: 
  - num_orders: 訂單數量
  - avg_days_btw_orders: 平均訂單時間間隔
- **Product features**:
  -  sales volume: 銷售量
  - prod_reordered_rate: 被再次訂購的比例
- **User x Product features**:
  - prod_reordered_rate_by_user: 商品被同一消費者重新購買的機率
  - user_reorder_rate: 消費者再次購買同一項商品的比例(第二次購買的東西有多少是第一次買過的)
  - prod_reordered_rate: 商品被再次購買的機率
  - order_back: 商品在消費者的最後五筆訂單中出現幾次

### Model: XGBoost classifier
- parameters:
  - 'eval_metric':'logloss'
  - 'max_depth':'5'
  - 'colsample_bytree':'0.5'
  - 'subsample':'0.75'  
 
訓練結果可以看出比較重要的特徵，如下圖。  
![image](https://github.com/P76094046/DSAI_HW4/blob/main/images/%E4%B8%8B%E8%BC%89.png)



