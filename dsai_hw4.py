# -*- coding: utf-8 -*-
"""dsai-hw4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W9KIUsqlJHcPUU82QKpy5M5hGuM_z0bQ
"""

import xgboost as xgb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gc
import sklearn as sk
from sklearn.model_selection import GridSearchCV
# import seaborn as sns
#%%

gc.enable()

orders = pd.read_csv( "./instacart-market-basket-analysis/orders.csv/orders.csv")
order_products__train = pd.read_csv("./instacart-market-basket-analysis/order_products__train.csv/order_products__train.csv")
order_products__prior = pd.read_csv("./instacart-market-basket-analysis/order_products__prior.csv/order_products__prior.csv")
aisles = pd.read_csv("./instacart-market-basket-analysis/aisles.csv/aisles.csv")
departments = pd.read_csv("./instacart-market-basket-analysis/departments.csv/departments.csv")
products = pd.read_csv("./instacart-market-basket-analysis/products.csv/products.csv")

#%% 

# aisles['aisle'] = aisles['aisle'].astype('category')
departments['department'] = departments['department'].astype('category')
products['product_name'] = products['product_name'].astype('category')


kwargs = dict( alpha=0.5, histtype='stepfilled', edgecolor='none')  # , color='steelblue'
fig, ax = plt.subplots(1, 3, figsize=(15,5))

order_num = orders.groupby('user_id')['order_number'].max()

ax[0].hist(orders['days_since_prior_order'], **kwargs);
ax[1].hist(orders['order_hour_of_day'], **kwargs);
ax[2].hist(order_num, **kwargs);

ax[0].set_title("days_since_prior_order ")
ax[1].set_title("order_hour_of_day")
ax[2].set_title("order_number")
fig.tight_layout()
plt.show()

#%% 

"""## For user info"""

orders_prior = orders.loc[np.where(orders['eval_set'] == 'prior')]
orders_train = orders.loc[np.where(orders['eval_set'] == 'train')]
# orders_test = orders.loc[np.where(orders['eval_set'] == 'test')] 
orders_test = orders.loc[orders.eval_set=='test',("user_id", "order_id") ]
# orders_prior.head()

orders_tmp = orders[((orders.eval_set=='train') | (orders.eval_set=='test'))]
orders_tmp = orders_tmp[['user_id', 'eval_set', 'order_id']]
user_info = pd.DataFrame()

info_p = pd.merge(orders_prior, order_products__prior, on = 'order_id', how = 'inner')

del [orders_prior, order_products__prior]
gc.collect()

#%%
avg_days_btw_orders = info_p.groupby('user_id')['days_since_prior_order'].mean().astype(np.float32)
# num_orders = info_p.groupby('user_id').size()
num_orders = info_p.groupby('user_id')['order_number'].max()
user_info['avg_days_btw_orders'] = avg_days_btw_orders
user_info['num_orders'] = num_orders
user_info = user_info.reset_index()

user_reorder_rate = info_p.groupby('user_id')['reordered'].mean().to_frame('user_reorder_rate')

user_info = user_info.join(user_reorder_rate)
user_info = user_info.fillna(0)

times = info_p.groupby(['user_id', 'product_id'])[['order_id']].count()
times.columns = ['times']    # 買了幾次同一個產品
times = times.reset_index()

info_p['order_back'] = info_p.groupby('user_id')['order_number'].transform(max) - info_p.order_number +1 
order_5 = info_p[info_p.order_back <= 5]
order_5 = order_5.groupby(['user_id','product_id'])[['order_back']].count()
order_5 = order_5.reset_index()

user_prod = pd.merge(user_info, times, on = 'user_id')
user_prod['prod_reordered_rate_by_user'] = user_prod['times'] / user_prod['num_orders']          ## 商品被同一消費者重新購買的機率
user_prod = user_prod.drop(['avg_days_btw_orders', 'num_orders', 'user_reorder_rate'], axis = 1)

user_prod = user_prod.merge(order_5, on = ['user_id', 'product_id'], how = 'left')

user_prod = user_prod.fillna(0)

del [times, num_orders, order_5]
gc.collect()

#%%

"""## For Product info"""

t3 = info_p.groupby('product_id')['reordered'].sum()
t4 = info_p.groupby('product_id').size()
prod_info_p = pd.DataFrame(t3 / t4, columns=['prod_reordered_rate'])
prod_info_p['sales volumn'] = info_p.groupby('product_id')['order_id'].count()

del [info_p, t3, t4]
gc.collect()


prod_info_p = prod_info_p.fillna(value=0)
#%%

"""## For User x Product

## Combining all features
- user_prod
- user_info
- prod_info_p
"""

Data = user_prod.merge(user_info, how = 'left', on = 'user_id')


del user_info
gc.collect()

Data = Data.merge(prod_info_p, how = 'left', on = 'product_id')

del prod_info_p
gc.collect()


Data = Data.merge(orders_tmp, on = 'user_id', how = 'left')

del orders_tmp
gc.collect()

Data_train = Data[Data.eval_set == 'train']
Data_test = Data[Data.eval_set == 'test']

del Data
gc.collect()

Data_train = Data_train.merge(order_products__train[['product_id','order_id', 'reordered']], on=['product_id','order_id'], how='left')

del order_products__train
gc.collect()

Data_train['reordered'] = Data_train['reordered'].fillna(0)

Data_train = Data_train.set_index(['user_id', 'product_id'])
Data_train = Data_train.drop(['eval_set', 'order_id'], axis=1)

'''
corr = Data_train.corr()
ax = sns.heatmap(
    corr, 
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    horizontalalignment='right'
);
'''

Data_test = Data_test.set_index(['user_id', 'product_id'])

Data_test = Data_test.drop(['eval_set','order_id'], axis=1)

#%%

"""## Training: XGBoost"""

parameters = {'eval_metric':'logloss', 
              'max_depth':'5', 
              'colsample_bytree':'0.5',    # 0.4
              'subsample':'0.75'
             }
X_train, y_train = Data_train.drop('reordered', axis=1), Data_train.reordered

XGB = xgb.XGBClassifier(objective='binary:logistic', parameters=parameters, num_boost_round=10)
model = XGB.fit(X_train, y_train)
xgb.plot_importance(model)

model.get_xgb_params()

#%%

"""## Prediction"""

test_pred = model.predict(Data_test).astype(int)
test_pred = (model.predict_proba(Data_test)[:,1] >= 0.21).astype(int)
# test_pred[0:10]

Data_test['prediction'] = test_pred

final = Data_test.reset_index()
final = final[['product_id', 'user_id', 'prediction']]
gc.collect()

final = final.merge(orders_test, on='user_id', how='left')

final = final.drop('user_id', axis=1)

final['product_id'] = final.product_id.astype(int)

## Remove all unnecessary objects
del orders
del orders_test
gc.collect()


d = dict()
for row in final.itertuples():
    if row.prediction== 1:
        try:
            d[row.order_id] += ' ' + str(row.product_id)
        except:
            d[row.order_id] = str(row.product_id)

for order in final.order_id:
    if order not in d:
        d[order] = 'None'
        

sub = pd.DataFrame.from_dict(d, orient='index')
sub.reset_index(inplace=True)
sub.columns = ['order_id', 'products']

# sub.shape[0]
# print(sub.shape[0]==75000)

sub.to_csv('submission.csv', index=False)
