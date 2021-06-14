# DSAI_HW4

- google silde: https://drive.google.com/file/d/1FAGsdAZw_mbuFgjZoz1Nr2M9QEXLMmXD/view?usp=sharing

### 下載需要的套件以及 XGBoost
XGBoost 可到 https://www.lfd.uci.edu/~gohlke/pythonlibs/#xgboost 下載 xgboost‑1.3.1‑cp36‑cp36m‑win_amd64.whl 後安裝

```
pip install xgboost‑1.3.1‑cp36‑cp36m‑win_amd64.whl
```
(參考此篇：https://hackmd.io/@allen108108/ryup_ppvV)

### 程式執行方式

### Dataset
- https://www.kaggle.com/c/instacart-market-basket-analysis/data 下載資料後將資料解壓縮，放到和程式碼同一個資料夾
- 並將路徑改到該資料夾
- (或下載此資料夾https://drive.google.com/drive/folders/191ThFZSKoWIqWaIIiKhDLupbTAMLUZH_?usp=sharing 不用解壓縮，和程式碼放到同一個資料夾)
![image](https://github.com/P76094046/DSAI_HW4/blob/main/%E6%93%B7%E5%8F%96.PNG)

### EDA
- User features: 
- Product features:
- User x Product features:

### Model
- parameters:
  - 'eval_metric':'logloss', 
  - 'max_depth':'5', 
  - 'colsample_bytree':'0.5', 
  - 'subsample':'0.75'  

