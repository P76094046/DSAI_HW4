# DSAI_HW4

- google silde: https://drive.google.com/file/d/1FAGsdAZw_mbuFgjZoz1Nr2M9QEXLMmXD/view?usp=sharing

### 下載需要的套件以及 XGBoost
XGBoost 可到 https://www.lfd.uci.edu/~gohlke/pythonlibs/#xgboost 下載 xgboost‑1.3.1‑cp36‑cp36m‑win_amd64.whl 後安裝

```
pip install xgboost‑1.3.1‑cp36‑cp36m‑win_amd64.whl
```
(參考此篇：https://hackmd.io/@allen108108/ryup_ppvV)


### 下載 Dataset
- 下載此資料夾 https://drive.google.com/drive/folders/191ThFZSKoWIqWaIIiKhDLupbTAMLUZH_?usp=sharing 和程式碼放到同一個資料夾
- 將當前路徑改到該資料夾後即可執行
- 資料關係如下圖
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

