# %% [markdown]
# 新的代码仓库总侧区2024.05.15
# 

# %%
pip install pandas scikit-learn matplotlib


# %%
#安装包
!pip install -U scikit-learn


# %%
##安装pandas的包用于数据的读取与纳入
!pip install pandas


# %% [markdown]
# 导入数据-----

# %%
#2、数据规范化
#指定pandas为pd方便后续数据的读取
import pandas as pd

# %%
##复制右边的数据的路径用于数据的读取
data=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V.csv')

# %%
##查看数据
data.head

# %% [markdown]
# 1、分类变量的编码

# %%
#1、分类变量的编码
data.head


# %%
#1.1找出分类型的变量
data_category = data.select_dtypes(include=['object'])

# %%
#1.2查看
data_category

# %%
#1.3把分类之后的变量与之前的拼接在一起,这一步是在找剩下了的数值型变量
data_Number=data.select_dtypes(exclude=['object'])

# %%
#1.4查看数值型的变量有哪些
data_Number

# %%
#1.5看看数值型的变量名字
data_Number.columns.values

# %%
#1.6整合编码
from sklearn.preprocessing import OrdinalEncoder

# 创建并拟合编码器
encoder = OrdinalEncoder()
encoder.fit(data_category)

# 将分类变量进行编码转换
data_category_enc = pd.DataFrame(encoder.transform(data_category), columns=data_category.columns)



# %%
#1.7加载表头
data_category_enc

# %%
#1.8查看某一变量是否正确
data_category_enc['Age'].value_counts()

# %%
#1.9看之前的变量名字
data_category['Age'].value_counts()

# %%
#1.10将表格拼回去
data_enc=pd.concat([data_category_enc,data_Number],axis=1)
#axis=0为纵向拼接 axis=1是按列拼接

# %%
#1.11编码完成
data_enc

# %%
#1.12将新的编码后的数据输入文件夹中
data_enc.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码后.csv')

# %% [markdown]
# 2、缺失值插补

# %%
##复制右边的数据的路径用于数据的读取
data_enc=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码后2Q.csv')

# %%
#2.1分类变量无法使用均质填补，因此使用众数填补（即出现频率最高的数进行填补）
#加载sklearn 的函数
from sklearn.impute import SimpleImputer

# %%
#2.2众数填补的缺失值
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer


# 创建并拟合填充器
imp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
data_encImpute = pd.DataFrame(imp.fit_transform(data_enc))

# 设置列名
data_encImpute.columns = data_enc.columns



# %%
#2.3整合
data_encImpute

# %%
#2.4看之前的变量名字
data_encImpute['Prelaryngeal Lymph Node Metastasis Rate'].value_counts()

# %% [markdown]
# 3、数值数据矫正和归一化

# %%
##复制右边的数据的路径用于数据的读取
data_encImpute=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码插补缺失值后4Q.csv')

# %%
#3数值数据校准和归一化
data_scale=data_encImpute

# %%
#3.1
target=data_encImpute['IV Level Lymph Node Metastasis'].astype(int)


# %%
##3.2
target.value_counts()

# %%
from sklearn import preprocessing

# %%
#第一种方法
scaler=preprocessing.StandardScaler()
data_scaled=pd.DataFrame(scaler.fit_transform(data_scale))
data_scaled.columns=data_scale.columns

# %%
data_scaled


# %%
#第二种方法
scaler=preprocessing.RobustScaler()
data_scaled=pd.DataFrame(scaler.fit_transform(data_scale))
data_scaled.columns=data_scale.columns

# %%
data_scaled

# %%
#第三种方法
scaler=preprocessing.MinMaxScaler()
data_scaled=pd.DataFrame(scaler.fit_transform(data_scale))
data_scaled.columns=data_scale.columns

# %%
data_scaled

# %%
#将矫正后的数据保存下来
data_scaled.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/4.总V编码插补缺失值矫正后4Q.csv')

# %% [markdown]
# 4、降维（减少因子之间的多重共线性的问题）

# %%
data=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')

# %%
#查看特征变量
data.iloc[:,[0,2,4]]

# %%
data.shape

# %%
data.info()

# %% [markdown]
# #4.1移除低方差特征

# %%
data=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')



data_feature = data[["Age","Sex","Classification of BMI",
                     "Tumor border","Aspect ratio","Ingredients","Internal echo pattern","Internal echo homogeneous","Calcification","Tumor internal vascularization","Tumor Peripheral blood flow",
                     "Size","Location","Mulifocality","Hashimoto","Extrathyroidal extension","Side of position","T staging",
                     "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis","Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
                     "age","size",
                     "Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
                     "Prelaryngeal Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastases Number",
                     "Pretracheal Lymph Node Metastasis Rate","Pretracheal Lymph Node Metastases Number",
                     "Paratracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number",
                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]


data_target=data['Ipsilateral Lateral Lymph Node Metastasis']



# %%
from sklearn.feature_selection import VarianceThreshold


# 创建方差阈值选择器
sel = VarianceThreshold(threshold=(.8 * (1 - .8))) #如果觉得不够可以把特征筛选选大或者选小

# 应用方差阈值选择器到数据
data_sel = sel.fit_transform(data)


# %%
data_sel

# %%
a=sel.get_support(indices=True)

# %%
#表明被保存下来的变量6,7,70,73,76,79,82,86,90,93被剔除掉了
a

# %%
#看哪些变量被保留了，保留了88个
data.iloc[:,a]

# %%
data_sel=data.iloc[:,a]

# %%
data_sel.info()

# %% [markdown]
# #4.2单变量特征的选择

# %%
from sklearn.feature_selection import SelectKBest, chi2



# %%
data=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')
data_feature = data[["Age","Sex","Classification of BMI",
                     "Tumor border","Aspect ratio","Ingredients","Internal echo pattern","Internal echo homogeneous","Calcification","Tumor internal vascularization","Tumor Peripheral blood flow",
                     "Size","Location","Mulifocality","Hashimoto","Extrathyroidal extension","Side of position","T staging",
                     "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis","Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
                     "age","size",
                     "Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
                     "Prelaryngeal Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastases Number",
                     "Pretracheal Lymph Node Metastasis Rate","Pretracheal Lymph Node Metastases Number",
                     "Paratracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number",
                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]

data_feature.shape
data_target=data['Ipsilateral Lateral Lymph Node Metastasis']
data_target.unique()#二分类

# %%
set_kit=SelectKBest(chi2,k=15)#选取k值最高的10(5)个元素
data_sel=set_kit.fit_transform(data_feature,data_target)
data_sel.shape

# %%
a=set_kit.get_support(indices=True)

# %%
a

# %%
data_sel=data_feature.iloc[:,a]

# %%
data_sel

# %%
data_sel.info()

# %% [markdown]
# #4.3递归特征消除RFE---线性模型。

# %%
from sklearn.feature_selection import RFE, RFECV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR #知识向量回归模型
from sklearn.model_selection import cross_val_score #知识向量回归模型


# %%
data=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')
data_feature = data[["Age","Sex","Classification of BMI",
                     "Tumor border","Aspect ratio","Ingredients","Internal echo pattern","Internal echo homogeneous","Calcification","Tumor internal vascularization","Tumor Peripheral blood flow",
                     "Size","Location","Mulifocality","Hashimoto","Extrathyroidal extension","Side of position","T staging",
                     "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis","Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
                     "age","size",
                     "Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
                     "Prelaryngeal Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastases Number",
                     "Pretracheal Lymph Node Metastasis Rate","Pretracheal Lymph Node Metastases Number",
                     "Paratracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number",
                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]

data_feature.shape
data_target=data['Ipsilateral Lateral Lymph Node Metastasis']
data_target.unique()#二分类

# %%
estimator=SVR(kernel='linear')
sel=RFE(estimator,n_features_to_select=15,step=1) #筛选出的变量，每递增一次就要删除一个特征，把权重最低的删掉

# %%
data_target=data['Ipsilateral Lateral Lymph Node Metastasis']
data_target.unique()#二分类

# %%
sel.fit(data_feature,data_target)#跑得太久，1个小时以上，要跑过的导入进去

# %%
a=sel.get_support(indices=True)

# %%
a

# %%
data_sel=data_feature.iloc[:,a]

# %%
data_sel

# %%
data_sel.info()

# %% [markdown]
# #4.4RFECV-结合了交叉验证

# %%
from sklearn.feature_selection import RFE, RFECV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR #知识向量回归模型
from sklearn.model_selection import cross_val_score #知识向量回归模型

# %%
#1.模型构建
RFC_ = RandomForestClassifier()  # 随机森林
RFC_.fit(data_sel, data_target)  # 拟合模型
c = RFC_.feature_importances_  # 特征重要性
print('重要性：')
print(c)

# %%

selector = RFECV(RFC_, step=1, cv=10,min_features_to_select=10)  # 采用交叉验证cv就是10倍交叉验证，每次排除一个特征，筛选出最优特征
selector.fit(data_sel, data_target)
X_wrapper = selector.transform(data_sel)  # 最优特征
score = cross_val_score(RFC_, X_wrapper, data_target, cv=5).mean()  # 最优特征分类结果
print(score)
print('最佳数量和排序')
print(selector.support_)
print(selector.n_features_)
print(selector.ranking_)


# %%
print(selector.support_)
feature_names = data_sel.columns
selected_features = feature_names[selector.support_]
print(selected_features)
print(selector.ranking_)

# %%
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.bar(range(len(selector.ranking_)), selector.ranking_)
plt.xticks(range(len(selector.ranking_)), feature_names, rotation=90)
plt.xlabel('Feature')
plt.ylabel('Ranking')
plt.title('Feature Importance Ranking')
plt.show()

# %%
!pip install matplotlib
import matplotlib.pyplot as plt
#绘图：

score = []
best_score = 0
best_features = 0

for i in range(1, 8):
    X_wrapper = RFE(RFC_, n_features_to_select=i, step=1).fit_transform(data_sel, data_target)  # 最优特征
    once = cross_val_score(RFC_, X_wrapper, data_target, cv=10).mean()
    score.append(once)
    
    if once > best_score:
        best_score = once
        best_features = i
    
    print("当前最高得分:", best_score)
    print("最佳特征数量:", best_features)
    print("得分列表:", score)
    
plt.figure(figsize=[20, 5])
plt.plot(range(1, 8), score)
plt.show()
from sklearn.model_selection import StratifiedKFold
rfecv=RFECV(estimator=RFC_,step=1,cv=StratifiedKFold(2),scoring='accuracy')
rfecv.fit(data,data_target)
print("最优特征数量：%d" % rfecv.n_features_)
print("选择的特征：", rfecv.support_)
print("特征排名：", rfecv.ranking_)
print("Optimal number of features: %d" % selector.n_features_)

# plot number of features vs. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross-validation score (number of correct classifications)")
plt.plot(range(1, len(selector.cv_results_['mean_test_score']) + 1), selector.cv_results_['mean_test_score'])
plt.show()
print("Optimal number of features: %d" % rfecv.n_features_)

# plot number of features vs. cross-validation scores
plt.figure()
plt.xlabel("Number of features selected")
plt.ylabel("Cross-validation score (number of correct classifications)")
plt.plot(range(1, len(rfecv.cv_results_['mean_test_score']) + 1), rfecv.cv_results_['mean_test_score'])
plt.show()

# %%
rfecv.get_support(indices=True)

# %%
a

# %%
data.iloc[:,a]

# %%
data_sel=data.iloc[:,a]

# %%
data_sel.info()

# %% [markdown]
# #4.5基于L1范数的特征选取-seleformodel 模型特征选择-----分类的线性回归，SVM LINEARSVC

# %%
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression #知识向量回归模型
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import StratifiedKFold

# %%
clf = LogisticRegression()
clf.fit(data_feature, data_target)

model = SelectFromModel(clf, prefit=True)
data_new = model.transform(data_feature)

# %%
model.get_support(indices=True)

# %%
a=model.get_support(indices=True)

# %%
data_features=pd.DataFrame(data_feature)
data_features.columns=data_feature.columns

# %%
data_featurenew=data_features.iloc[:,a]


# %%
data_featurenew

# %%
data_featurenew.info()

# %% [markdown]
# #4.6基于树模型--

# %%

data=pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')
data_feature = data[["Age","Sex","Classification of BMI",
                     "Tumor border","Aspect ratio","Ingredients","Internal echo pattern","Internal echo homogeneous","Calcification","Tumor internal vascularization","Tumor Peripheral blood flow",
                     "Size","Location","Mulifocality","Hashimoto","Extrathyroidal extension","Side of position","T staging",
                     "Ipsilateral Central Lymph Node Metastasis","Prelaryngeal Lymph Node Metastasis","Pretracheal Lymph Node Metastasis","Paratracheal Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
                     "age","size",
                     "Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
                     "Prelaryngeal Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastases Number",
                     "Pretracheal Lymph Node Metastasis Rate","Pretracheal Lymph Node Metastases Number",
                     "Paratracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number",
                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]

data_feature.shape
data_target=data['Ipsilateral Lateral Lymph Node Metastasis']
data_target.unique()#二分类

# %%
clf = ExtraTreesClassifier()
clf.fit(data_feature, data_target)
clf.feature_importances_

# %%
model=SelectFromModel(clf,prefit=True)
x_new=model.transform(data_feature)

# %%
x_new


# %%
model.get_support(indices=True)

# %%
a=model.get_support(indices=True)

# %%
data_features=pd.DataFrame(data_feature)
data_features.columns=data_feature.columns
data_featurenew=data_features.iloc[:,a]

# %%
data_featurenew

# %%
data_featurenew.info()

# %% [markdown]
# 筛选变量

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, average_precision_score, cohen_kappa_score, brier_score_loss



# 加载数据
train_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')
test_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码插补缺失值矫正后CQ.csv')

# 提取特征和目标
feature_cols = ["Tumor border","Calcification","Tumor internal vascularization","Extrathyroidal extension","Prelaryngeal Lymph Node Metastasis",
                "Ipsilateral Central Lymph Node Metastasis","Pretracheal Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number","Recurrent Laryngeal Nerve Lymph Node Metastasis Rate"]
target_col = 'Ipsilateral Lateral Lymph Node Metastasis'

train_features = train_data[feature_cols]
train_target = train_data[target_col]

test_features = test_data[feature_cols]
test_target = test_data[target_col]

# 数值变量标准化
num_cols = ["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Prelaryngeal Lymph Node Metastases Number","Pretracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number","Recurrent Laryngeal Nerve Lymph Node Metastasis Rate"]
cat_cols = ["Tumor border","Calcification","Tumor internal vascularization","Extrathyroidal extension","Prelaryngeal Lymph Node Metastasis",
                "Ipsilateral Central Lymph Node Metastasis","Pretracheal Lymph Node Metastasis",]

scaler = MinMaxScaler()
train_features[num_cols] = scaler.fit_transform(train_features[num_cols])
test_features[num_cols] = scaler.transform(test_features[num_cols])

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(train_features, train_target, test_size=0.3, random_state=2)

# 定义模型和参数空间
model_param_grid = {
   'Logistic Regression': (LogisticRegression(), {'C': [0.01, 0.1, 1, 10, 100],'random_state': [33]}),
    'Decision Tree': (DecisionTreeClassifier(), {'max_depth': [5, 7, 10, 15], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4],'random_state': [33]}),
    'Random Forest': (RandomForestClassifier(), {'n_estimators': [100, 200, 300],'max_depth': [3, 5, 7],'min_samples_split': [2, 5, 10],
                                                 'min_samples_leaf': [1, 2, 4],'max_features': ['sqrt', 'log2', None],'random_state': [33]}),
    'Gradient Boosting': (GradientBoostingClassifier(), {'n_estimators': [100, 200, 300], 'learning_rate': [0.05, 0.1, 0.2], 'max_depth': [1, 3, 5],'random_state': [33]}),
    'Support Vector Machine': (SVC(probability=True), {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto']}),
    'K-Nearest Neighbors': (KNeighborsClassifier(), {'n_neighbors': [3, 5, 7, 9, 11]}),
    'Gaussian Naive Bayes': (GaussianNB(), {}),
    'Neural Network': (MLPClassifier(), {'hidden_layer_sizes': [(10,), (20,), (50,), (100,)], 'activation': ['relu', 'tanh'], 'solver': ['adam', 'sgd']}),
}

# 定义颜色列表
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'brown', ]

# 初始化最佳AUC和最佳模型
best_auc = 0
best_model_name = ''
best_model = None

# 创建评价指标的空列表
train_accuracy_scores = []
train_auc_scores = []
train_precision_scores = []
train_specificity_scores = []
train_sensitivity_scores = []
train_npv_scores = []
train_ppv_scores = []
train_recall_scores = []
train_f1_scores = []
train_fpr_scores = []
train_rmse_scores = []
train_r2_scores = []
train_mae_scores = []
train_tn_scores = []
train_fp_scores = []
train_fn_scores = []
train_tp_scores = []
train_lift_scores = []
train_brier_scores = []
train_kappa_scores = []
# 拟合模型并绘制训练集的ROC曲线
plt.figure(figsize=(8, 6))

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_train_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_train_pred_prob = best_model_temp.decision_function(class_x_tra)

    # 计算AUC值
    auc = roc_auc_score(class_y_tra, y_train_pred_prob)

    # 如果当前模型的AUC值是最高的，则更新最佳模型和最佳AUC
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_model = best_model_temp

    # 计算ROC曲线
    fpr, tpr, _ = roc_curve(class_y_tra, y_train_pred_prob)

    # 绘制ROC曲线
    plt.plot(fpr, tpr, color=color, label='%s (AUC = %0.3f)' % (name, auc))

    # 计算其他评价指标
    #train_y_pred = best_model_temp.predict(class_x_tra)
    #train_accuracy = accuracy_score(class_y_tra, train_y_pred)
    #train_precision = precision_score(class_y_tra, train_y_pred)
    #train_cm = confusion_matrix(class_y_tra, train_y_pred)
    #train_tn, train_fp, train_fn, train_tp = train_cm.ravel()
    #train_specificity = train_tn / (train_tn + train_fp)
    #train_sensitivity = recall_score(class_y_tra, train_y_pred)
    #train_npv = train_tn / (train_tn + train_fn)
    #train_ppv = train_tp / (train_tp + train_fp)
    #train_recall = train_sensitivity
    #train_f1 = f1_score(class_y_tra, train_y_pred)
    #train_fpr = train_fp / (train_fp + train_tn)
    #train_rmse = mean_squared_error(class_y_tra, y_train_pred_prob, squared=False)
    #train_r2 = r2_score(class_y_tra, y_train_pred_prob)
    #train_mae = mean_absolute_error(class_y_tra, y_train_pred_prob)
    #train_auc = roc_auc_score(class_y_tra, y_train_pred_prob)
    #train_lift = average_precision_score(class_y_tra, y_train_pred_prob) / (sum(class_y_tra) / len(class_y_tra))
    #train_kappa = cohen_kappa_score(class_y_tra, train_y_pred)
    #train_brier = brier_score_loss(class_y_tra, y_train_pred_prob)
    
    
    # 将评价指标添加到列表中
    #train_accuracy_scores.append(train_accuracy)
    #train_auc_scores.append(train_auc)
    #train_precision_scores.append(train_precision)
    #train_specificity_scores.append(train_specificity)
    #train_sensitivity_scores.append(train_sensitivity)
    #train_npv_scores.append(train_npv)
    #train_ppv_scores.append(train_ppv)
    #train_recall_scores.append(train_recall)
    #train_f1_scores.append(train_f1)
    #train_fpr_scores.append(train_fpr)
    #train_rmse_scores.append(train_rmse)
    #train_r2_scores.append(train_r2)
    #train_mae_scores.append(train_mae)
    #train_tn_scores.append(train_tn)
    #train_fp_scores.append(train_fp)
    #train_fn_scores.append(train_fn)
    #train_tp_scores.append(train_tp)
    #train_lift_scores.append(train_lift)
    #train_brier_scores.append(train_brier)
    #train_kappa_scores.append(train_kappa)
    
plt.grid(True)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC For Ipsilateral Lateral Lymph Node Metastasis-RFE with Cross-Validation (RFE-CV) (Train set)')
plt.legend(loc='lower right')
# 保存图像为TIFF格式

formats = ['tiff']
dpis = [1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/Supplementary material 2 figures/Figure1D-1-ROC All Machine Learning Algorithms-RFE with Cross-Validation (RFE-CV)_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 打印最佳模型的名称和AUC值
print(f"最佳模型: {best_model_name} with AUC = {best_auc}")

# 使用最佳模型在验证集上进行评估
if hasattr(best_model, 'predict_proba'):
    y_val_pred_prob = best_model.predict_proba(class_x_val)[:, 1]
else:
    y_val_pred_prob = best_model.decision_function(class_x_val)

# 计算验证集上的AUC值
val_auc = roc_auc_score(class_y_val, y_val_pred_prob)

# 打印验证集上的AUC值
print(f"测试集上的AUC = {val_auc}")

# 使用最佳模型在外验证集上进行评估
if hasattr(best_model, 'predict_proba'):
    y_test_pred_prob = best_model.predict_proba(test_features)[:, 1]
else:
    y_test_pred_prob = best_model.decision_function(test_features)

# 计算外验证集上的AUC值
test_auc = roc_auc_score(test_target, y_test_pred_prob)

# 打印外验证集上的AUC值
print(f"外验证集上的AUC = {test_auc}")

# 绘制验证集和外验证集的ROC曲线
fpr_val, tpr_val, _ = roc_curve(class_y_val, y_val_pred_prob)
fpr_test, tpr_test, _ = roc_curve(test_target, y_test_pred_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='goldenrod', label='Train Set (AUC = %0.3f)' % best_auc)
plt.plot(fpr_val, tpr_val, color='orange', label='Test Set (AUC = %0.3f)' % val_auc)
plt.plot(fpr_test, tpr_test, color='gold', label='Validation Set (AUC = %0.3f)' % test_auc)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线
plt.grid(True)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Ipsilateral Lateral Lymph Node Metastasis Random Forest-RFE with Cross-Validation (RFE-CV)')
plt.legend(loc='lower right')
# 保存图像为TIFF格式
formats = ['tiff']
dpis = [1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/Supplementary material 2 figures/Figure1D-2-ROC Random Forest-RFE with Cross-Validation (RFE-CV)_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 净收益计算函数
def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        n = len(y_true)
        if thresh == 1.0:  # 避免除以0
            net_benefit = 0
        else:
            net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        net_benefits.append(net_benefit)
    return net_benefits

# 决策阈值
decision_thresholds = np.linspace(0, 1, 101)

# 计算净收益
net_benefits_train = calculate_net_benefit(class_y_tra, y_train_pred_prob, decision_thresholds)
net_benefits_val = calculate_net_benefit(class_y_val, y_val_pred_prob, decision_thresholds)
net_benefits_test = calculate_net_benefit(test_target, y_test_pred_prob, decision_thresholds)

# 计算所有人都进行干预时的净收益
all_positive_train = np.ones_like(class_y_tra)
all_positive_val = np.ones_like(class_y_val)
all_positive_test = np.ones_like(test_target)
net_benefit_all_train = calculate_net_benefit(class_y_tra, all_positive_train, decision_thresholds)
net_benefit_all_val = calculate_net_benefit(class_y_val, all_positive_val, decision_thresholds)
net_benefit_all_test = calculate_net_benefit(test_target, all_positive_test, decision_thresholds)

# 绘制DCA曲线
plt.figure(figsize=(8, 6))
plt.plot(decision_thresholds, net_benefits_train, color='goldenrod', lw=2, label='Training set')
plt.plot(decision_thresholds, net_benefits_val, color='orange', lw=2, label='Validation set')
plt.plot(decision_thresholds, net_benefits_test, color='gold', lw=2, label='Test set')
plt.plot(decision_thresholds, net_benefit_all_val, color='gray', lw=2, linestyle='--', label='All')
plt.plot(decision_thresholds, np.zeros_like(decision_thresholds), color='darkred', lw=2, linestyle='-', label='None')
plt.xlabel('Threshold Probability', fontsize=12)
plt.ylabel('Net Benefit', fontsize=12)
plt.title('DCA for Ipsilateral Lateral Lymph Node Metastasis Random Forest-RFE with Cross-Validation (RFE-CV)', fontsize=14)
plt.legend(loc="lower right", fontsize=10)
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
# 保存图像为TIFF格式
formats = ['tiff']
dpis = [ 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/Supplementary material 2 figures/Figure1D-3-DCA Random Forest-RFE with Cross-Validation (RFE-CV)_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 打印XGBoost最佳参数
print("最佳模型的参数设置:")
print(grid_search.best_params_)

# 创建训练集评价指标的DataFrame
#train_metrics_df = pd.DataFrame({
    #'Model': list(model_param_grid.keys()),
    #'Accuracy': train_accuracy_scores,
    #'AUC': train_auc_scores,
    #'Precision': train_precision_scores,
    #'Specificity': train_specificity_scores,
    #'Sensitivity': train_sensitivity_scores,
    #'Negative Predictive Value': train_npv_scores,
    #'Positive Predictive Value': train_ppv_scores,
    #'Recall': train_recall_scores,
    #'F1 Score': train_f1_scores,
    #'False Positive Rate': train_fpr_scores,
    #'RMSE': train_rmse_scores,
    #'R2': train_r2_scores,
    #'MAE': train_mae_scores,
    #'True Negatives': train_tn_scores,
    #'False Positives': train_fp_scores,
    #'False Negatives': train_fn_scores,
    #'True Positives': train_tp_scores,
    #'Lift': train_lift_scores,
    #'Brier Score': train_brier_scores,
    #'Kappa': train_kappa_scores,
#})

# 显示训练集评价指标DataFrame
#print(train_metrics_df)

# 将训练集评价指标DataFrame导出为CSV文件

# 将训练集评价指标DataFrame导出为CSV文件
#train_metrics_df.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/1.筛选变量/侧区单变量特征选择.csv', index=False)


# %% [markdown]
# ##1.1.1训练集的ROC曲线

# %% [markdown]
# 最终选择的这一个版本

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, average_precision_score, cohen_kappa_score, brier_score_loss



# 加载数据
train_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')
test_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码插补缺失值矫正后CQ.csv')

# 提取特征和目标
feature_cols = ["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
target_col = 'Ipsilateral Lateral Lymph Node Metastasis'

train_features = train_data[feature_cols]
train_target = train_data[target_col]

test_features = test_data[feature_cols]
test_target = test_data[target_col]

# 数值变量标准化
num_cols = ["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
cat_cols = ["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",]

scaler = MinMaxScaler()
train_features[num_cols] = scaler.fit_transform(train_features[num_cols])
test_features[num_cols] = scaler.transform(test_features[num_cols])

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(train_features, train_target, test_size=0.3, random_state=2)

# 定义模型和参数空间
model_param_grid = {
   'Logistic Regression': (LogisticRegression(random_state=33), {'C': [0.01, 0.1, 1, 10,100]}),
    'Decision Tree': (DecisionTreeClassifier(random_state=33), {'max_depth': [5, 7, 10, 15], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}),
    'Random Forest': (RandomForestClassifier(random_state=33), {'n_estimators': [100, 500, 1000],'max_depth': [1,3, 5, 7,12],'min_samples_split': [1, 5, 12],
                                                 'min_samples_leaf': [1, 2, 4],'max_features': ['sqrt', 'log2', None]}),
    'Gradient Boosting': (GradientBoostingClassifier(random_state=33), {'n_estimators': [100, 200, 300], 'learning_rate': [0.05, 0.1, 0.2], 'max_depth': [1, 3, 5]}),
    'Support Vector Machine': (SVC(probability=True, random_state=33), {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto']}),
    'K-Nearest Neighbors': (KNeighborsClassifier(), {'n_neighbors': [3, 5, 7, 9, 11]}),
    'Gaussian Naive Bayes': (GaussianNB(), {}),
    'Neural Network': (MLPClassifier(random_state=33), {'hidden_layer_sizes': [(10,), (20,), (50,), (100,)], 'activation': ['relu', 'tanh'], 'solver': ['adam', 'sgd']}),
}

# 定义颜色列表
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'brown', ]

# 初始化最佳AUC和最佳模型
best_auc = 0
best_model_name = ''
best_model = None

# 创建评价指标的空列表
train_accuracy_scores = []
train_auc_scores = []
train_precision_scores = []
train_specificity_scores = []
train_sensitivity_scores = []
train_npv_scores = []
train_ppv_scores = []
train_recall_scores = []
train_f1_scores = []
train_fpr_scores = []
train_rmse_scores = []
train_r2_scores = []
train_mae_scores = []
train_tn_scores = []
train_fp_scores = []
train_fn_scores = []
train_tp_scores = []
train_lift_scores = []
train_brier_scores = []
train_kappa_scores = []
# 拟合模型并绘制训练集的ROC曲线
plt.figure(figsize=(8, 6))

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_train_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_train_pred_prob = best_model_temp.decision_function(class_x_tra)

    # 计算AUC值
    auc = roc_auc_score(class_y_tra, y_train_pred_prob)

    # 如果当前模型的AUC值是最高的，则更新最佳模型和最佳AUC
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_model = best_model_temp

    # 计算ROC曲线
    fpr, tpr, _ = roc_curve(class_y_tra, y_train_pred_prob)

    # 绘制ROC曲线
    plt.plot(fpr, tpr, color=color, label='%s (AUC = %0.3f)' % (name, auc))

    # 计算其他评价指标
    train_y_pred = best_model_temp.predict(class_x_tra)
    train_accuracy = accuracy_score(class_y_tra, train_y_pred)
    train_precision = precision_score(class_y_tra, train_y_pred)
    train_cm = confusion_matrix(class_y_tra, train_y_pred)
    train_tn, train_fp, train_fn, train_tp = train_cm.ravel()
    train_specificity = train_tn / (train_tn + train_fp)
    train_sensitivity = recall_score(class_y_tra, train_y_pred)
    train_npv = train_tn / (train_tn + train_fn)
    train_ppv = train_tp / (train_tp + train_fp)
    train_recall = train_sensitivity
    train_f1 = f1_score(class_y_tra, train_y_pred)
    train_fpr = train_fp / (train_fp + train_tn)
    train_rmse = mean_squared_error(class_y_tra, y_train_pred_prob, squared=False)
    train_r2 = r2_score(class_y_tra, y_train_pred_prob)
    train_mae = mean_absolute_error(class_y_tra, y_train_pred_prob)
    train_auc = roc_auc_score(class_y_tra, y_train_pred_prob)
    train_lift = average_precision_score(class_y_tra, y_train_pred_prob) / (sum(class_y_tra) / len(class_y_tra))
    train_kappa = cohen_kappa_score(class_y_tra, train_y_pred)
    train_brier = brier_score_loss(class_y_tra, y_train_pred_prob)
    
    
    # 将评价指标添加到列表中
    train_accuracy_scores.append(train_accuracy)
    train_auc_scores.append(train_auc)
    train_precision_scores.append(train_precision)
    train_specificity_scores.append(train_specificity)
    train_sensitivity_scores.append(train_sensitivity)
    train_npv_scores.append(train_npv)
    train_ppv_scores.append(train_ppv)
    train_recall_scores.append(train_recall)
    train_f1_scores.append(train_f1)
    train_fpr_scores.append(train_fpr)
    train_rmse_scores.append(train_rmse)
    train_r2_scores.append(train_r2)
    train_mae_scores.append(train_mae)
    train_tn_scores.append(train_tn)
    train_fp_scores.append(train_fp)
    train_fn_scores.append(train_fn)
    train_tp_scores.append(train_tp)
    train_lift_scores.append(train_lift)
    train_brier_scores.append(train_brier)
    train_kappa_scores.append(train_kappa)
    
plt.grid(True)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC For Ipsilateral Lateral Lymph Node Metastasis (Train set)')
plt.legend(loc='lower right')
# 保存图像为TIFF格式


plt.show()

# 打印最佳模型的名称和AUC值
print(f"最佳模型: {best_model_name} with AUC = {best_auc}")

# 使用最佳模型在验证集上进行评估
if hasattr(best_model, 'predict_proba'):
    y_val_pred_prob = best_model.predict_proba(class_x_val)[:, 1]
else:
    y_val_pred_prob = best_model.decision_function(class_x_val)

# 计算验证集上的AUC值
val_auc = roc_auc_score(class_y_val, y_val_pred_prob)

# 打印验证集上的AUC值
print(f"测试集上的AUC = {val_auc}")

# 使用最佳模型在外验证集上进行评估
if hasattr(best_model, 'predict_proba'):
    y_test_pred_prob = best_model.predict_proba(test_features)[:, 1]
else:
    y_test_pred_prob = best_model.decision_function(test_features)

# 计算外验证集上的AUC值
test_auc = roc_auc_score(test_target, y_test_pred_prob)

# 打印外验证集上的AUC值
print(f"外验证集上的AUC = {test_auc}")

# 绘制验证集和外验证集的ROC曲线
fpr_val, tpr_val, _ = roc_curve(class_y_val, y_val_pred_prob)
fpr_test, tpr_test, _ = roc_curve(test_target, y_test_pred_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='goldenrod', label='Train Set (AUC = %0.3f)' % best_auc)
plt.plot(fpr_val, tpr_val, color='orange', label='Test Set (AUC = %0.3f)' % val_auc)
plt.plot(fpr_test, tpr_test, color='gold', label='Validation Set (AUC = %0.3f)' % test_auc)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线
plt.grid(True)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Ipsilateral Lateral Lymph Node Metastasis Random Forest Prediction')
plt.legend(loc='lower right')
# 保存图像为TIFF格式

plt.show()

# 净收益计算函数
def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        n = len(y_true)
        if thresh == 1.0:  # 避免除以0
            net_benefit = 0
        else:
            net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        net_benefits.append(net_benefit)
    return net_benefits

# 决策阈值
decision_thresholds = np.linspace(0, 1, 101)

# 计算净收益
net_benefits_train = calculate_net_benefit(class_y_tra, y_train_pred_prob, decision_thresholds)
net_benefits_val = calculate_net_benefit(class_y_val, y_val_pred_prob, decision_thresholds)
net_benefits_test = calculate_net_benefit(test_target, y_test_pred_prob, decision_thresholds)

# 计算所有人都进行干预时的净收益
all_positive_train = np.ones_like(class_y_tra)
all_positive_val = np.ones_like(class_y_val)
all_positive_test = np.ones_like(test_target)
net_benefit_all_train = calculate_net_benefit(class_y_tra, all_positive_train, decision_thresholds)
net_benefit_all_val = calculate_net_benefit(class_y_val, all_positive_val, decision_thresholds)
net_benefit_all_test = calculate_net_benefit(test_target, all_positive_test, decision_thresholds)

# 绘制DCA曲线
plt.figure(figsize=(8, 6))
plt.plot(decision_thresholds, net_benefits_train, color='goldenrod', lw=2, label='Training set')
plt.plot(decision_thresholds, net_benefits_val, color='orange', lw=2, label='Validation set')
plt.plot(decision_thresholds, net_benefits_test, color='gold', lw=2, label='Test set')
plt.plot(decision_thresholds, net_benefit_all_val, color='gray', lw=2, linestyle='--', label='All')
plt.plot(decision_thresholds, np.zeros_like(decision_thresholds), color='darkred', lw=2, linestyle='-', label='None')
plt.xlabel('Threshold Probability', fontsize=12)
plt.ylabel('Net Benefit', fontsize=12)
plt.title('DCA for Ipsilateral Lateral Lymph Node Metastasis Random Forest Prediction', fontsize=14)
plt.legend(loc="lower right", fontsize=10)
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
# 保存图像为TIFF格式

plt.show()

# 打印XGBoost最佳参数
print("最佳模型的参数设置:")
print(grid_search.best_params_)

# 创建训练集评价指标的DataFrame
train_metrics_df = pd.DataFrame({
    'Model': list(model_param_grid.keys()),
    'Accuracy': train_accuracy_scores,
    'AUC': train_auc_scores,
    'Precision': train_precision_scores,
    'Specificity': train_specificity_scores,
    'Sensitivity': train_sensitivity_scores,
    'Negative Predictive Value': train_npv_scores,
    'Positive Predictive Value': train_ppv_scores,
    'Recall': train_recall_scores,
    'F1 Score': train_f1_scores,
    'False Positive Rate': train_fpr_scores,
    'RMSE': train_rmse_scores,
    'R2': train_r2_scores,
    'MAE': train_mae_scores,
    'True Negatives': train_tn_scores,
    'False Positives': train_fp_scores,
    'False Negatives': train_fn_scores,
    'True Positives': train_tp_scores,
    'Lift': train_lift_scores,
    'Brier Score': train_brier_scores,
    'Kappa': train_kappa_scores,
})

# 显示训练集评价指标DataFrame
print(train_metrics_df)

# 将训练集评价指标DataFrame导出为CSV文件

# 将训练集评价指标DataFrame导出为CSV文件
train_metrics_df.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/1.训练集的评价指标新.csv', index=False)



# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, average_precision_score, cohen_kappa_score, brier_score_loss



# 加载数据
train_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')
test_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码插补缺失值矫正后CQ.csv')

# 提取特征和目标
feature_cols = ["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
target_col = 'Ipsilateral Lateral Lymph Node Metastasis'

train_features = train_data[feature_cols]
train_target = train_data[target_col]

test_features = test_data[feature_cols]
test_target = test_data[target_col]

# 数值变量标准化
num_cols = ["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
cat_cols = ["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",]

scaler = MinMaxScaler()
train_features[num_cols] = scaler.fit_transform(train_features[num_cols])
test_features[num_cols] = scaler.transform(test_features[num_cols])

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(train_features, train_target, test_size=0.3, random_state=2)

# 定义模型和参数空间
model_param_grid = {
   'Logistic Regression': (LogisticRegression(), {'C': [0.01, 0.1, 1, 10, 100]}),
    'Decision Tree': (DecisionTreeClassifier(), {'max_depth': [5, 7, 10, 15], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}),
    'Random Forest': (RandomForestClassifier(), {'n_estimators': [100, 200, 300],'max_depth': [3, 5, 7],'min_samples_split': [2, 5, 10],
                                                 'min_samples_leaf': [1, 2, 4],'max_features': ['sqrt', 'log2', None],'random_state': [33]}),
    'Gradient Boosting': (GradientBoostingClassifier(), {'n_estimators': [100, 200, 300], 'learning_rate': [0.05, 0.1, 0.2], 'max_depth': [1, 3, 5]}),
    'Support Vector Machine': (SVC(probability=True), {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto']}),
    'K-Nearest Neighbors': (KNeighborsClassifier(), {'n_neighbors': [3, 5, 7, 9, 11]}),
    'Gaussian Naive Bayes': (GaussianNB(), {}),
    'Neural Network': (MLPClassifier(), {'hidden_layer_sizes': [(10,), (20,), (50,), (100,)], 'activation': ['relu', 'tanh'], 'solver': ['adam', 'sgd']}),
}

# 定义颜色列表
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'brown', ]

# 初始化最佳AUC和最佳模型
best_auc = 0
best_model_name = ''
best_model = None

# 创建评价指标的空列表
train_accuracy_scores = []
train_auc_scores = []
train_precision_scores = []
train_specificity_scores = []
train_sensitivity_scores = []
train_npv_scores = []
train_ppv_scores = []
train_recall_scores = []
train_f1_scores = []
train_fpr_scores = []
train_rmse_scores = []
train_r2_scores = []
train_mae_scores = []
train_tn_scores = []
train_fp_scores = []
train_fn_scores = []
train_tp_scores = []
train_lift_scores = []
train_brier_scores = []
train_kappa_scores = []
# 拟合模型并绘制训练集的ROC曲线
plt.figure(figsize=(8, 6))

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_train_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_train_pred_prob = best_model_temp.decision_function(class_x_tra)

    # 计算AUC值
    auc = roc_auc_score(class_y_tra, y_train_pred_prob)

    # 如果当前模型的AUC值是最高的，则更新最佳模型和最佳AUC
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_model = best_model_temp

    # 计算ROC曲线
    fpr, tpr, _ = roc_curve(class_y_tra, y_train_pred_prob)

    # 绘制ROC曲线
    plt.plot(fpr, tpr, color=color, label='%s (AUC = %0.3f)' % (name, auc))

    # 计算其他评价指标
    train_y_pred = best_model_temp.predict(class_x_tra)
    train_accuracy = accuracy_score(class_y_tra, train_y_pred)
    train_precision = precision_score(class_y_tra, train_y_pred)
    train_cm = confusion_matrix(class_y_tra, train_y_pred)
    train_tn, train_fp, train_fn, train_tp = train_cm.ravel()
    train_specificity = train_tn / (train_tn + train_fp)
    train_sensitivity = recall_score(class_y_tra, train_y_pred)
    train_npv = train_tn / (train_tn + train_fn)
    train_ppv = train_tp / (train_tp + train_fp)
    train_recall = train_sensitivity
    train_f1 = f1_score(class_y_tra, train_y_pred)
    train_fpr = train_fp / (train_fp + train_tn)
    train_rmse = mean_squared_error(class_y_tra, y_train_pred_prob, squared=False)
    train_r2 = r2_score(class_y_tra, y_train_pred_prob)
    train_mae = mean_absolute_error(class_y_tra, y_train_pred_prob)
    train_auc = roc_auc_score(class_y_tra, y_train_pred_prob)
    train_lift = average_precision_score(class_y_tra, y_train_pred_prob) / (sum(class_y_tra) / len(class_y_tra))
    train_kappa = cohen_kappa_score(class_y_tra, train_y_pred)
    train_brier = brier_score_loss(class_y_tra, y_train_pred_prob)
    
    
    # 将评价指标添加到列表中
    train_accuracy_scores.append(train_accuracy)
    train_auc_scores.append(train_auc)
    train_precision_scores.append(train_precision)
    train_specificity_scores.append(train_specificity)
    train_sensitivity_scores.append(train_sensitivity)
    train_npv_scores.append(train_npv)
    train_ppv_scores.append(train_ppv)
    train_recall_scores.append(train_recall)
    train_f1_scores.append(train_f1)
    train_fpr_scores.append(train_fpr)
    train_rmse_scores.append(train_rmse)
    train_r2_scores.append(train_r2)
    train_mae_scores.append(train_mae)
    train_tn_scores.append(train_tn)
    train_fp_scores.append(train_fp)
    train_fn_scores.append(train_fn)
    train_tp_scores.append(train_tp)
    train_lift_scores.append(train_lift)
    train_brier_scores.append(train_brier)
    train_kappa_scores.append(train_kappa)
    
plt.grid(True)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC For Ipsilateral Lateral Lymph Node Metastasis (Train set)')
plt.legend(loc='lower right')
# 保存图像为TIFF格式

formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/roc_curve侧区训练集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# 打印最佳模型的名称和AUC值
print(f"最佳模型: {best_model_name} with AUC = {best_auc}")

# 使用最佳模型在验证集上进行评估
if hasattr(best_model, 'predict_proba'):
    y_val_pred_prob = best_model.predict_proba(class_x_val)[:, 1]
else:
    y_val_pred_prob = best_model.decision_function(class_x_val)

# 计算验证集上的AUC值
val_auc = roc_auc_score(class_y_val, y_val_pred_prob)

# 打印验证集上的AUC值
print(f"测试集上的AUC = {val_auc}")

# 使用最佳模型在外验证集上进行评估
if hasattr(best_model, 'predict_proba'):
    y_test_pred_prob = best_model.predict_proba(test_features)[:, 1]
else:
    y_test_pred_prob = best_model.decision_function(test_features)

# 计算外验证集上的AUC值
test_auc = roc_auc_score(test_target, y_test_pred_prob)

# 打印外验证集上的AUC值
print(f"外验证集上的AUC = {test_auc}")

# 绘制验证集和外验证集的ROC曲线
fpr_val, tpr_val, _ = roc_curve(class_y_val, y_val_pred_prob)
fpr_test, tpr_test, _ = roc_curve(test_target, y_test_pred_prob)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='goldenrod', label='Train Set (AUC = %0.3f)' % best_auc)
plt.plot(fpr_val, tpr_val, color='orange', label='Test Set (AUC = %0.3f)' % val_auc)
plt.plot(fpr_test, tpr_test, color='gold', label='Validation Set (AUC = %0.3f)' % test_auc)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线
plt.grid(True)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Ipsilateral Lateral Lymph Node Metastasis Random Forest Prediction')
plt.legend(loc='lower right')
# 保存图像为TIFF格式
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/3.最佳模型的ROC和DCA/roc_curve侧区三集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# 净收益计算函数
def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        n = len(y_true)
        if thresh == 1.0:  # 避免除以0
            net_benefit = 0
        else:
            net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        net_benefits.append(net_benefit)
    return net_benefits

# 决策阈值
decision_thresholds = np.linspace(0, 1, 101)

# 计算净收益
net_benefits_train = calculate_net_benefit(class_y_tra, y_train_pred_prob, decision_thresholds)
net_benefits_val = calculate_net_benefit(class_y_val, y_val_pred_prob, decision_thresholds)
net_benefits_test = calculate_net_benefit(test_target, y_test_pred_prob, decision_thresholds)

# 计算所有人都进行干预时的净收益
all_positive_train = np.ones_like(class_y_tra)
all_positive_val = np.ones_like(class_y_val)
all_positive_test = np.ones_like(test_target)
net_benefit_all_train = calculate_net_benefit(class_y_tra, all_positive_train, decision_thresholds)
net_benefit_all_val = calculate_net_benefit(class_y_val, all_positive_val, decision_thresholds)
net_benefit_all_test = calculate_net_benefit(test_target, all_positive_test, decision_thresholds)

# 绘制DCA曲线
plt.figure(figsize=(8, 6))
plt.plot(decision_thresholds, net_benefits_train, color='goldenrod', lw=2, label='Training set')
plt.plot(decision_thresholds, net_benefits_val, color='orange', lw=2, label='Validation set')
plt.plot(decision_thresholds, net_benefits_test, color='gold', lw=2, label='Test set')
plt.plot(decision_thresholds, net_benefit_all_val, color='gray', lw=2, linestyle='--', label='All')
plt.plot(decision_thresholds, np.zeros_like(decision_thresholds), color='darkred', lw=2, linestyle='-', label='None')
plt.xlabel('Threshold Probability', fontsize=12)
plt.ylabel('Net Benefit', fontsize=12)
plt.title('DCA for Ipsilateral Lateral Lymph Node Metastasis Random Forest Prediction', fontsize=14)
plt.legend(loc="lower right", fontsize=10)
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
# 保存图像为TIFF格式
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/3.最佳模型的ROC和DCA/DCA_curve侧区三集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# 打印XGBoost最佳参数
print("最佳模型的参数设置:")
print(grid_search.best_params_)

# 创建训练集评价指标的DataFrame
train_metrics_df = pd.DataFrame({
    'Model': list(model_param_grid.keys()),
    'Accuracy': train_accuracy_scores,
    'AUC': train_auc_scores,
    'Precision': train_precision_scores,
    'Specificity': train_specificity_scores,
    'Sensitivity': train_sensitivity_scores,
    'Negative Predictive Value': train_npv_scores,
    'Positive Predictive Value': train_ppv_scores,
    'Recall': train_recall_scores,
    'F1 Score': train_f1_scores,
    'False Positive Rate': train_fpr_scores,
    'RMSE': train_rmse_scores,
    'R2': train_r2_scores,
    'MAE': train_mae_scores,
    'True Negatives': train_tn_scores,
    'False Positives': train_fp_scores,
    'False Negatives': train_fn_scores,
    'True Positives': train_tp_scores,
    'Lift': train_lift_scores,
    'Brier Score': train_brier_scores,
    'Kappa': train_kappa_scores,
})

# 显示训练集评价指标DataFrame
print(train_metrics_df)

# 将训练集评价指标DataFrame导出为CSV文件

# 将训练集评价指标DataFrame导出为CSV文件
train_metrics_df.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/1.训练集的评价指标.csv', index=False)



# %% [markdown]
# ##1.1.3训练集的DCA曲线

# %%
#训练集的决策曲线
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

# 定义风险阈值
thresholds = np.linspace(0, 1, 100)
tra_net_benefit = []

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_tra_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_tra_pred_prob = best_model_temp.decision_function(class_x_tra)

    tra_model_net_benefit = []

    # 计算每个阈值下的净收益
    for threshold in thresholds:
        tra_predictions = (y_tra_pred_prob >= threshold).astype(int)
        tp = np.sum((class_y_tra == 1) & (tra_predictions == 1))
        fp = np.sum((class_y_tra == 0) & (tra_predictions == 1))
        fn = np.sum((class_y_tra == 1) & (tra_predictions == 0))
        tn = np.sum((class_y_tra == 0) & (tra_predictions == 0))
        
        net_benefit = (tp / len(class_y_tra)) - (fp / len(class_y_tra)) * (threshold / (1 - threshold))
        tra_model_net_benefit.append(net_benefit)
        
    tra_net_benefit.append(tra_model_net_benefit)

# 转换为数组
tra_net_benefit = np.array(tra_net_benefit)

# 计算所有人都进行干预时的净收益
tra_all_predictions = np.ones_like(class_y_tra)  # 将所有预测标记为阳性（正类）
tp_all = np.sum((class_y_tra == 1) & (tra_all_predictions == 1))
fp_all = np.sum((class_y_tra == 0) & (tra_all_predictions == 1))

net_benefit_all = (tp_all / len(class_y_tra)) - (fp_all / len(class_y_tra)) * (thresholds / (1 - thresholds))
net_benefit_none = np.zeros_like(thresholds)
names = [
    'Logistic Regression',
    'Decision Tree',
    'Random Forest',
    'Gradient Boosting',
    'Support Vector Machine',
    'K-Nearest Neighbors',
    'Gaussian Naive Bayes',
    'Neural Network',
]

# 绘制DCA曲线
for i in range(tra_net_benefit.shape[0]):
    plt.plot(thresholds, tra_net_benefit[i], color=colors[i], label=names[i])

# 绘制"None"和"All"线
plt.plot(thresholds, net_benefit_none, color='black', linestyle='-', label='None')
plt.plot(thresholds, net_benefit_all, color='gray', linestyle='--', label='All')


# 设置y轴的限制
plt.xlim(0, 0.8)
plt.ylim(-0.1,0.5)

# 设置图形属性
plt.xlabel('Threshold')
plt.ylabel('Net Benefit')
plt.title('DCA For Ipsilateral Lateral Lymph Node Metastasis (Train set)')
plt.legend(loc='upper right')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

# 显示图形
# 保存图像为TIFF格式

formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/DCA_curve侧区训练集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# %%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

# 定义风险阈值
thresholds = np.linspace(0, 1, 100)
tra_net_benefit = []

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_tra_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_tra_pred_prob = best_model_temp.decision_function(class_x_tra)

    tra_model_net_benefit = []

    # 计算每个阈值下的净收益
    for threshold in thresholds:
        tra_predictions = (y_tra_pred_prob >= threshold).astype(int)
        tp = np.sum((class_y_tra == 1) & (tra_predictions == 1))
        fp = np.sum((class_y_tra == 0) & (tra_predictions == 1))
        fn = np.sum((class_y_tra == 1) & (tra_predictions == 0))
        tn = np.sum((class_y_tra == 0) & (tra_predictions == 0))

        net_benefit = (tp / len(class_y_tra)) - (fp / len(class_y_tra)) * (threshold / (1 - threshold))
        tra_model_net_benefit.append(net_benefit)

    tra_net_benefit.append(tra_model_net_benefit)

# 转换为数组
tra_net_benefit = np.array(tra_net_benefit)

# 计算所有人都进行干预时的净收益
tra_all_predictions = np.ones_like(class_y_tra)  # 将所有预测标记为阳性（正类）
tp_all = np.sum((class_y_tra == 1) & (tra_all_predictions == 1))
fp_all = np.sum((class_y_tra == 0) & (tra_all_predictions == 1))

net_benefit_all = (tp_all / len(class_y_tra)) - (fp_all / len(class_y_tra)) * (thresholds / (1 - thresholds))
net_benefit_none = np.zeros_like(thresholds)
names = [
    'Logistic Regression',
    'Decision Tree',
    'Random Forest',
    'Gradient Boosting',
    'Support Vector Machine',
    'K-Nearest Neighbors',
    'Gaussian Naive Bayes',
    'Neural Network',
]

# 绘制DCA曲线
plt.figure(figsize=(10, 8))
for i in range(tra_net_benefit.shape[0]):
    plt.plot(thresholds, tra_net_benefit[i], color=colors[i], label=names[i])

# 绘制"None"和"All"线
plt.plot(thresholds, net_benefit_none, color='black', linestyle='-', label='None')
plt.plot(thresholds, net_benefit_all, color='gray', linestyle='--', label='All')

# 设置y轴的限制
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)

# 设置图形属性
plt.xlabel('Threshold')
plt.ylabel('Net Benefit')
plt.title('DCA For Ipsilateral Lateral Lymph Node Metastasis (Train set)')
plt.legend(loc='upper right')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
#训练集的校准曲线
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
from scipy.stats import ttest_ind

# 创建一个空列表来存储每个模型的校准曲线和Brier Score
train_calibration_curves = []
train_brier_scores = []

# 对每个模型进行循环
for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_train_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_train_pred_prob = best_model_temp.decision_function(class_x_tra)



    # 计算校准曲线
    train_fraction_of_positives, train_mean_predicted_value = calibration_curve(class_y_tra, y_train_pred_prob, n_bins=10)
    train_calibration_curves.append((train_fraction_of_positives, train_mean_predicted_value, name, color))

    # 计算Brier分数
    train_brier_score = brier_score_loss(class_y_tra, y_train_pred_prob)
    train_brier_scores.append((name, train_brier_score))

    # 打印Brier分数
    print(f'{name} - Train Brier Score: {train_brier_score:.3f}')

# 绘制校准曲线和Brier Score
fig, ax1 = plt.subplots(figsize=(10, 6))

for curve in train_calibration_curves:
    train_fraction_of_positives, train_mean_predicted_value, name, color = curve
    
    # 获取对应模型的Brier Score
    train_brier_score = next((score for model, score in train_brier_scores if model == name), None)
    
    # 将Brier Score赋予线颜色标注名称的后面
    if train_brier_score is not None:
        name += f' (Train Brier Score: {train_brier_score:.3f})'
    
    ax1.plot(train_mean_predicted_value, train_fraction_of_positives, "s-", label=name, color=color)
    
# 绘制"Perfectly calibrated"曲线
ax1.plot([0, 1], [0, 1], "k:",label="Perfectly calibrated")
    
ax1.set_ylabel("Fraction of positives")
ax1.set_xlabel("Mean predicted value")
ax1.set_ylim([-0.05, 1.05])
ax1.legend(loc="lower right")

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.title("Calibration Curves For Ipsilateral Lateral Lymph Node Metastasis (Train set)")
plt.tight_layout()
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/DCA_curve侧区训练集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()



# %% [markdown]
# ##1.1.4训练集的校准曲线

# %%
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np

# 创建一个空列表来存储每个模型的校准曲线和 Brier Score
train_calibration_curves = []
train_brier_scores = []

# 对每个模型进行循环
for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_train_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_train_pred_prob = best_model_temp.decision_function(class_x_tra)

    # 计算校准曲线
    train_fraction_of_positives, train_mean_predicted_value = calibration_curve(class_y_tra, y_train_pred_prob, n_bins=10)
    train_calibration_curves.append((train_fraction_of_positives, train_mean_predicted_value, name, color))

    # 计算 Brier 分数
    train_brier_score = brier_score_loss(class_y_tra, y_train_pred_prob)
    train_brier_scores.append((name, train_brier_score))

    # 打印 Brier 分数
    print(f'{name} - Train Brier Score: {train_brier_score:.3f}')

# 绘制校准曲线和 Brier Score
fig, ax1 = plt.subplots(figsize=(10, 6))

for curve in train_calibration_curves:
    train_fraction_of_positives, train_mean_predicted_value, name, color = curve
    
    # 获取对应模型的 Brier Score
    train_brier_score = next((score for model, score in train_brier_scores if model == name), None)
    
    # 将 Brier Score 赋予线颜色标注名称的后面
    if train_brier_score is not None:
        name += f' (Train Brier Score: {train_brier_score:.3f})'
    
    ax1.plot(train_mean_predicted_value, train_fraction_of_positives, "s-", label=name, color=color)
    
# 绘制 "Perfectly calibrated" 曲线
ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
    
ax1.set_ylabel("Fraction of positives")
ax1.set_xlabel("Mean predicted value")
ax1.set_ylim([-0.05, 1.05])
ax1.legend(loc="lower right")

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.title("Calibration Curves For Ipsilateral Lateral Lymph Node Metastasis (Train set)")
plt.tight_layout()

# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/校准曲线侧区训练集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()


# %% [markdown]
# ##1.1.5训练集的精确召回曲线

# %%
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np

# 初始化存储精确召回曲线和平均精确度的列表
train_precision_recall_curves = []
train_average_precision_scores = []

# 遍历每个模型
for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_train_pred_prob = best_model_temp.predict_proba(class_x_tra)[:, 1]
    else:
        y_train_pred_prob = best_model_temp.decision_function(class_x_tra)

    # 计算精确召回曲线
    train_precision, train_recall, _ = precision_recall_curve(class_y_tra, y_train_pred_prob)
    train_average_precision = average_precision_score(class_y_tra, y_train_pred_prob)

    # 存储结果
    train_precision_recall_curves.append((train_precision, train_recall, f'{name} (AUPR: {train_average_precision:.3f})', color))
    train_average_precision_scores.append((f'{name} (AUPR: {train_average_precision:.3f})', train_average_precision))

    # 打印平均精确度
    print(f'{name} - Train Average Precision: {train_average_precision:.3f}')

# 绘制精确召回曲线
fig, ax2 = plt.subplots(figsize=(10, 6))

for curve in train_precision_recall_curves:
    train_precision, train_recall, name, color = curve
    ax2.plot(train_recall, train_precision, "-", color=color, label=name)

# 添加随机猜测曲线
plt.plot([0, 1], [class_y_tra.mean(), class_y_tra.mean()], linestyle='--', color='black', label='Random Guessing')

ax2.set_xlabel("Recall")
ax2.set_ylabel("Precision")
ax2.set_ylim([0.0, 1.05])
ax2.set_xlim([0.0, 1.0])
ax2.legend(loc="lower left")
ax2.grid(True)

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.title("Precision Recall Curves For Ipsilateral Lateral Lymph Node Metastasis (Train set)")
plt.tight_layout()

# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/精确召回曲线侧区训练集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()


# %% [markdown]
# 学习曲线

# %% [markdown]
# ##2.1.1验证集-内验证集的ROC曲线

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, r2_score, mean_absolute_error, brier_score_loss, average_precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import cohen_kappa_score

# 加载数据
data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')

# 导入数据
data_feature = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                  "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
data_target = data['Ipsilateral Lateral Lymph Node Metastasis']

# 数值变量标准化
data_featureNum = data[["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
scaler = MinMaxScaler()
data_featureNum = scaler.fit_transform(data_featureNum)

data_featureCata = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                  "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",]]
data_featureCata = np.array(data_featureCata)

# 整合数据
data_feature = np.hstack((data_featureCata, data_featureNum))

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(data_feature, data_target, test_size=0.3, random_state=2)

# 定义模型和参数空间
model_param_grid= {
'Logistic Regression': (LogisticRegression(random_state=33), {'C': [0.01, 0.1]}),
    'Decision Tree': (DecisionTreeClassifier(random_state=33), {'max_depth': [5, 7, 10, 15], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}),
    'Random Forest': (RandomForestClassifier(random_state=33), {'n_estimators': [100, 500, 1000],'max_depth': [None,1,3, 5, 7,12],'min_samples_split': [None,1, 5, 12],
                                                 'min_samples_leaf': [None,1, 2, 7],'max_features': ['sqrt', 'log2', None]}),
    'Gradient Boosting': (GradientBoostingClassifier(random_state=33), {'n_estimators': [100, 200, 300], 'learning_rate': [0.05, 0.1, 0.2], 'max_depth': [1, 3, 5]}),
    'Support Vector Machine': (SVC(probability=True, random_state=33), {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto']}),
    'K-Nearest Neighbors': (KNeighborsClassifier(), {'n_neighbors': [3, 5, 7, 9, 11]}),
    'Gaussian Naive Bayes': (GaussianNB(), {}),
    'Neural Network': (MLPClassifier(random_state=33), {'hidden_layer_sizes': [(10,), (20,)]}),
}

# 定义颜色列表
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'brown']

# 初始化最佳AUC和最佳模型
best_auc = 0
best_model_name = ''
best_model = None

# 创建评价指标的空列表
Val_accuracy_scores = []
Val_auc_scores = []
Val_precision_scores = []
Val_specificity_scores = []
Val_sensitivity_scores = []
Val_npv_scores = []
Val_ppv_scores = []
Val_recall_scores = []
Val_f1_scores = []
Val_fpr_scores = []
Val_rmse_scores = []
Val_r2_scores = []
Val_mae_scores = []
Val_tn_scores = []
Val_fp_scores = []
Val_fn_scores = []
Val_tp_scores = []
Val_lift_scores = []
Val_brier_scores = []
Val_kappa_scores = []

# 拟合模型并绘制ROC曲线
plt.figure(figsize=(8, 6))

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算验证集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_Val_pred_prob = best_model_temp.predict_proba(class_x_val)[:, 1]
    else:
        y_Val_pred_prob = best_model_temp.decision_function(class_x_val)

    # 计算AUC值
    auc = roc_auc_score(class_y_val, y_Val_pred_prob)

    # 如果当前模型的AUC值是最高的，则更新最佳模型和最佳AUC
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_model = best_model_temp

    # 计算ROC曲线
    fpr, tpr, _ = roc_curve(class_y_val, y_Val_pred_prob)

    # 绘制ROC曲线
    plt.plot(fpr, tpr, color=color, label='%s (AUC = %0.3f)' % (name, auc))

    # 计算其他评价指标
    Val_y_pred = best_model_temp.predict(class_x_val)
    Val_accuracy = accuracy_score(class_y_val, Val_y_pred)
    Val_precision = precision_score(class_y_val, Val_y_pred)
    Val_cm = confusion_matrix(class_y_val, Val_y_pred)
    Val_tn, Val_fp, Val_fn, Val_tp = Val_cm.ravel()
    Val_specificity = Val_tn / (Val_tn + Val_fp)
    Val_sensitivity = recall_score(class_y_val, Val_y_pred)
    Val_npv = Val_tn / (Val_tn + Val_fn)
    Val_ppv = Val_tp / (Val_tp + Val_fp)
    Val_recall = Val_sensitivity
    Val_f1 = f1_score(class_y_val, Val_y_pred)
    Val_fpr = Val_fp / (Val_fp + Val_tn)
    Val_rmse = mean_squared_error(class_y_val, y_Val_pred_prob, squared=False)
    Val_r2 = r2_score(class_y_val, y_Val_pred_prob)
    Val_mae = mean_absolute_error(class_y_val, y_Val_pred_prob)
    Val_kappa = cohen_kappa_score(class_y_val, Val_y_pred)
    Val_auc = roc_auc_score(class_y_val, y_Val_pred_prob)
    Val_lift = average_precision_score(class_y_val, y_Val_pred_prob) / (sum(class_y_val) / len(class_y_val))
    Val_brier = brier_score_loss(class_y_val, y_Val_pred_prob)

    # 将评价指标添加到列表中
    Val_accuracy_scores.append(Val_accuracy)
    Val_auc_scores.append(auc)
    Val_precision_scores.append(Val_precision)
    Val_specificity_scores.append(Val_specificity)
    Val_sensitivity_scores.append(Val_sensitivity)
    Val_npv_scores.append(Val_npv)
    Val_ppv_scores.append(Val_ppv)
    Val_recall_scores.append(Val_recall)
    Val_f1_scores.append(Val_f1)
    Val_fpr_scores.append(Val_fpr)
    Val_rmse_scores.append(Val_rmse)
    Val_r2_scores.append(Val_r2)
    Val_mae_scores.append(Val_mae)
    Val_tn_scores.append(Val_tn)
    Val_fp_scores.append(Val_fp)
    Val_fn_scores.append(Val_fn)
    Val_tp_scores.append(Val_tp)
    Val_lift_scores.append(Val_lift)
    Val_brier_scores.append(Val_brier)
    Val_kappa_scores.append(Val_kappa)

plt.grid(True)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC For Ipsilateral Lateral Lymph Node Metastasis (Test set)')
plt.legend(loc='lower right')


plt.show()

# 打印最佳模型的名称和AUC值
print(f"最佳模型: {best_model_name} with AUC = {best_auc}")

# 创建训练集评价指标的DataFrame
Val_metrics_df = pd.DataFrame({
    'Model': list(model_param_grid.keys()),
    'Accuracy': Val_accuracy_scores,
    'AUC': Val_auc_scores,
    'Precision': Val_precision_scores,
    'Specificity': Val_specificity_scores,
    'Sensitivity': Val_sensitivity_scores,
    'Negative Predictive Value': Val_npv_scores,
    'Positive Predictive Value': Val_ppv_scores,
    'Recall': Val_recall_scores,
    'F1 Score': Val_f1_scores,
    'False Positive Rate': Val_fpr_scores,
    'RMSE': Val_rmse_scores,
    'R2': Val_r2_scores,
    'MAE': Val_mae_scores,
    'True Negatives': Val_tn_scores,
    'False Positives': Val_fp_scores,
    'False Negatives': Val_fn_scores,
    'True Positives': Val_tp_scores,
    'Lift': Val_lift_scores,
    'Brier Score': Val_brier_scores,
    'Kappa': Val_kappa_scores,  
})

# 显示训练集评价指标DataFrame
print(Val_metrics_df)

# 将训练集评价指标DataFrame导出为CSV文件
Val_metrics_df.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/2.测试集（内验证）的评价指标新.csv', index=False)


# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, average_precision_score, cohen_kappa_score, brier_score_loss

# 加载数据
data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')

# 导入数据
data_feature = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                     "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
                     "age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
                     "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
data_target = data['Ipsilateral Lateral Lymph Node Metastasis']

# 数值变量标准化
data_featureNum = data[["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
                        "Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
                        "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
scaler = MinMaxScaler()
data_featureNum = scaler.fit_transform(data_featureNum)

data_featureCata = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                         "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",]]
data_featureCata = np.array(data_featureCata)

# 整合数据
data_feature = np.hstack((data_featureCata, data_featureNum))

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(data_feature, data_target, test_size=0.3, random_state=2)

# 定义模型和参数空间
model_param_grid= {
    'Logistic Regression': (LogisticRegression(), {'C': [0.00001, 0.0001]}),
    'Decision Tree': (DecisionTreeClassifier(), {'max_depth': [5, 7, 10, 15], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}),
    'Random Forest': (RandomForestClassifier(), {'n_estimators': [100, 200, 300],'max_depth': [3, 5, 7],'min_samples_split': [2, 5, 10],'min_samples_leaf': [1, 2, 4],
                                                 'max_features': ['sqrt', 'log2', None],'random_state': [33]}),
    'Gradient Boosting': (GradientBoostingClassifier(), {'n_estimators': [50, 100, 100]}),
    'Support Vector Machine': (SVC(probability=True), {'C': [0.01, 0.1, 1, 10, 40]}),
    'K-Nearest Neighbors': (KNeighborsClassifier(), {'n_neighbors': [1, 2, 5, 7]}),
    'Gaussian Naive Bayes': (GaussianNB(), {}),
    'Neural Network': (MLPClassifier(), {'hidden_layer_sizes': [(1,), (2,), (3,)]}),
}

# 定义颜色列表
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'brown']

# 初始化最佳AUC和最佳模型
best_auc = 0
best_model_name = ''
best_model = None

# 创建评价指标的空列表
Val_accuracy_scores = []
Val_auc_scores = []
Val_precision_scores = []
Val_specificity_scores = []
Val_sensitivity_scores = []
Val_npv_scores = []
Val_ppv_scores = []
Val_recall_scores = []
Val_f1_scores = []
Val_fpr_scores = []
Val_rmse_scores = []
Val_r2_scores = []
Val_mae_scores = []
Val_tn_scores = []
Val_fp_scores = []
Val_fn_scores = []
Val_tp_scores = []
Val_lift_scores = []
Val_brier_scores = []
Val_kappa_scores = []

# 拟合模型并绘制ROC曲线
plt.figure(figsize=(8, 6))

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算验证集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_Val_pred_prob = best_model_temp.predict_proba(class_x_val)[:, 1]
    else:
        y_Val_pred_prob = best_model_temp.decision_function(class_x_val)

    # 计算AUC值
    auc = roc_auc_score(class_y_val, y_Val_pred_prob)

    # 如果当前模型的AUC值是最高的，则更新最佳模型和最佳AUC
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_model = best_model_temp

    # 计算ROC曲线
    fpr, tpr, _ = roc_curve(class_y_val, y_Val_pred_prob)

    # 绘制ROC曲线
    plt.plot(fpr, tpr, color=color, label='%s (AUC = %0.3f)' % (name, auc))

    # 计算其他评价指标
    Val_y_pred = best_model_temp.predict(class_x_val)
    Val_accuracy = accuracy_score(class_y_val, Val_y_pred)
    Val_precision = precision_score(class_y_val, Val_y_pred)
    Val_cm = confusion_matrix(class_y_val, Val_y_pred)
    Val_tn, Val_fp, Val_fn, Val_tp = Val_cm.ravel()
    Val_specificity = Val_tn / (Val_tn + Val_fp)
    Val_sensitivity = recall_score(class_y_val, Val_y_pred)
    Val_npv = Val_tn / (Val_tn + Val_fn)
    Val_ppv = Val_tp / (Val_tp + Val_fp)
    Val_recall = Val_sensitivity
    Val_f1 = f1_score(class_y_val, Val_y_pred)
    Val_fpr = Val_fp / (Val_fp + Val_tn)
    Val_rmse = mean_squared_error(class_y_val, y_Val_pred_prob, squared=False)
    Val_r2 = r2_score(class_y_val, y_Val_pred_prob)
    Val_mae = mean_absolute_error(class_y_val, y_Val_pred_prob)
    Val_kappa = cohen_kappa_score(class_y_val, Val_y_pred)
    Val_lift = average_precision_score(class_y_val, y_Val_pred_prob) / (sum(class_y_val) / len(class_y_val))
    Val_brier = brier_score_loss(class_y_val, y_Val_pred_prob)

    # 将评价指标添加到列表中
    Val_accuracy_scores.append(Val_accuracy)
    Val_auc_scores.append(auc)
    Val_precision_scores.append(Val_precision)
    Val_specificity_scores.append(Val_specificity)
    Val_sensitivity_scores.append(Val_sensitivity)
    Val_npv_scores.append(Val_npv)
    Val_ppv_scores.append(Val_ppv)
    Val_recall_scores.append(Val_recall)
    Val_f1_scores.append(Val_f1)
    Val_fpr_scores.append(Val_fpr)
    Val_rmse_scores.append(Val_rmse)
    Val_r2_scores.append(Val_r2)
    Val_mae_scores.append(Val_mae)
    Val_tn_scores.append(Val_tn)
    Val_fp_scores.append(Val_fp)
    Val_fn_scores.append(Val_fn)
    Val_tp_scores.append(Val_tp)
    Val_lift_scores.append(Val_lift)
    Val_brier_scores.append(Val_brier)
    Val_kappa_scores.append(Val_kappa)

plt.grid(True)
plt.plot([0, 1], [0, 1], 'k--')  # 绘制对角线

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC For Ipsilateral Lateral Lymph Node Metastasis (Test set)')
plt.legend(loc='lower right')

# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/roc-curve侧区测试集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# 打印最佳模型的名称和AUC值
print(f"最佳模型: {best_model_name} with AUC = {best_auc}")

# 创建验证集评价指标的DataFrame
Val_metrics_df = pd.DataFrame({
    'Model': list(model_param_grid.keys()),
    'Accuracy': Val_accuracy_scores,
    'AUC': Val_auc_scores,
    'Precision': Val_precision_scores,
    'Specificity': Val_specificity_scores,
    'Sensitivity': Val_sensitivity_scores,
    'Negative Predictive Value': Val_npv_scores,
    'Positive Predictive Value': Val_ppv_scores,
    'Recall': Val_recall_scores,
    'F1 Score': Val_f1_scores,
    'False Positive Rate': Val_fpr_scores,
    'RMSE': Val_rmse_scores,
    'R2': Val_r2_scores,
    'MAE': Val_mae_scores,
    'True Negatives': Val_tn_scores,
    'False Positives': Val_fp_scores,
    'False Negatives': Val_fn_scores,
    'True Positives': Val_tp_scores,
    'Lift': Val_lift_scores,
    'Brier Score': Val_brier_scores,
    'Kappa': Val_kappa_scores,
})

# 显示验证集评价指标DataFrame
print(Val_metrics_df)

# 将验证集评价指标DataFrame导出为CSV文件
Val_metrics_df.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/2.测试集（内验证）的评价指标.csv', index=False)


# %% [markdown]
# ##2.1.3验证集-内验证集的决策曲线

# %%
#内验证集的决策曲线
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

# 定义风险阈值
thresholds = np.linspace(0, 1, 100)
val_net_benefit = []


for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_val_pred_prob = best_model_temp.predict_proba(class_x_val)[:, 1]
    else:
        y_val_pred_prob = best_model_temp.decision_function(class_x_val)

    val_model_net_benefit = []

    # 计算每个阈值下的净收益
    for threshold in thresholds:
        val_predictions = (y_val_pred_prob >= threshold).astype(int)
        tp = np.sum((class_y_val == 1) & (val_predictions == 1))
        fp = np.sum((class_y_val == 0) & (val_predictions == 1))
        fn = np.sum((class_y_val == 1) & (val_predictions == 0))
        tn = np.sum((class_y_val == 0) & (val_predictions == 0))
        
        net_benefit = (tp / len(class_y_val)) - (fp / len(class_y_val)) * (threshold / (1 - threshold))
        val_model_net_benefit.append(net_benefit)

    val_net_benefit.append(val_model_net_benefit)

# 转换为数组
val_net_benefit = np.array(val_net_benefit)

# 计算所有人都进行干预时的净收益
val_all_predictions = np.ones_like(class_y_val)  # 将所有预测标记为阳性（正类）
tp_all = np.sum((class_y_val == 1) & (val_all_predictions == 1))
fp_all = np.sum((class_y_val == 0) & (val_all_predictions == 1))

net_benefit_all = (tp_all / len(class_y_val)) - (fp_all / len(class_y_val)) * (thresholds / (1 - thresholds))
net_benefit_none = np.zeros_like(thresholds)

names = [
    'Logistic Regression',
    'Decision Tree',
    'Random Forest',
    'Gradient Boosting',
    'Support Vector Machine',
    'K-Nearest Neighbors',
    'Gaussian Naive Bayes',
    'Neural Network',
]

# 绘制DCA曲线
for i in range(val_net_benefit.shape[0]):
    plt.plot(thresholds, val_net_benefit[i], color=colors[i], label=names[i])

# 绘制"None"和"All"线
plt.plot(thresholds, net_benefit_none, color='black', linestyle='-', label='None')
plt.plot(thresholds, net_benefit_all, color='gray', linestyle='--', label='All')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
# 设置y轴的限制
plt.xlim(0, 0.8)
plt.ylim(-0.1,0.5)

# 设置图形属性
plt.xlabel('Threshold')
plt.ylabel('Net Benefit')
plt.title('DCA For Ipsilateral Lateral Lymph Node Metastasis (Test set)')
plt.legend(loc='upper right')

# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/DCA_curve侧区测试集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# %% [markdown]
# ##2.1.4验证集-内验证集的校准曲线

# %%
#内验证集的校准曲线
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
from scipy.stats import ttest_ind

# 创建一个空列表来存储每个模型的校准曲线和Brier Score
val_calibration_curves = []
val_brier_scores = []

# 对每个模型进行循环
for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_val_pred_prob = best_model_temp.predict_proba(class_x_val)[:, 1]
    else:
        y_val_pred_prob = best_model_temp.decision_function(class_x_val)

    # 计算校准曲线
    val_fraction_of_positives, val_mean_predicted_value = calibration_curve(class_y_val, y_val_pred_prob, n_bins=10)
    val_calibration_curves.append((val_fraction_of_positives, val_mean_predicted_value, name, color))

    # 计算Brier分数
    val_brier_score = brier_score_loss(class_y_val, y_val_pred_prob)
    val_brier_scores.append((name, val_brier_score))

    # 打印Brier分数
    print(f'{name} - Brier Score: {val_brier_score:.3f}')

# 绘制校准曲线和Brier Score
fig, ax1 = plt.subplots(figsize=(10, 6))

for curve in val_calibration_curves:
    val_fraction_of_positives, val_mean_predicted_value, name, color = curve
    
    # 获取对应模型的Brier Score
    val_brier_score = next((score for model, score in val_brier_scores if model == name), None)
    
    # 将Brier Score赋予线颜色标注名称的后面
    if val_brier_score is not None:
        name += f' (Brier Score: {val_brier_score:.3f})'
    
    ax1.plot(val_mean_predicted_value, val_fraction_of_positives, "s-", label=name, color=color)
    
# 绘制"Perfectly calibrated"曲线
ax1.plot([0, 1], [0, 1], "k:",label="Perfectly calibrated")
    
ax1.set_ylabel("Fraction of positives")
ax1.set_xlabel("Mean predicted value")
ax1.set_ylim([-0.05, 1.05])
ax1.legend(loc="lower right")

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.title("Calibration Curves For Ipsilateral Lateral Lymph Node Metastasis (Test set)")
plt.tight_layout()
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/校准曲线侧区测试集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# %% [markdown]
# ##2.1.5验证集-内验证集的绘制精确-召回曲线及AUPR值

# %%
#内验证集的精确召回曲线
from sklearn.metrics import precision_recall_curve, average_precision_score
import numpy as np

# 初始化存储精确召回曲线和平均精确度的列表
val_precision_recall_curves = []
val_average_precision_scores = []

# 遍历每个模型
for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_val_pred_prob = best_model_temp.predict_proba(class_x_val)[:, 1]
    else:
        y_val_pred_prob = best_model_temp.decision_function(class_x_val)

    # 计算精确召回曲线
    val_precision, val_recall, _ = precision_recall_curve(class_y_val, y_val_pred_prob)
    val_average_precision = average_precision_score(class_y_val, y_val_pred_prob)

    # 存储结果
    val_precision_recall_curves.append((val_precision, val_recall, f'{name} (AUPR: {val_average_precision:.3f})', color))
    val_average_precision_scores.append((f'{name} (AUPR: {val_average_precision:.3f})', val_average_precision))

    # 打印平均精确度
    print(f'{name} - Average Precision: {val_average_precision:.3f}')

# 绘制精确召回曲线
fig, ax2 = plt.subplots(figsize=(10, 6))

for curve in val_precision_recall_curves:
    val_precision, val_recall, name, color = curve
    ax2.plot(val_recall, val_precision, "-", color=color, label=name)

# 添加随机猜测曲线
plt.plot([0, 1], [class_y_val.mean(), class_y_val.mean()], linestyle='--', color='black', label='Random Guessing')

ax2.set_xlabel("Recall")
ax2.set_ylabel("Precision")
ax2.set_ylim([0.0, 1.05])
ax2.set_xlim([0.0, 1.0])
ax2.legend(loc="lower left")
ax2.grid(True)

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.title("Precision Recall Curves For Ipsilateral Lateral Lymph Node Metastasis (Test set)")
plt.tight_layout()
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/精确召回曲线侧区测试集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, r2_score, mean_absolute_error, cohen_kappa_score, average_precision_score, brier_score_loss
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

# 加载数据
data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')

# 导入数据
data_feature = data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                     "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis",
                     "age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                     "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
data_target = data['Ipsilateral Lateral Lymph Node Metastasis']

# 数值变量标准化
data_featureNum = data[["age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                        "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                        "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
scaler = MinMaxScaler()
data_featureNum = scaler.fit_transform(data_featureNum)

data_featureCata = data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                         "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis"]]
data_featureCata = np.array(data_featureCata)

# 整合数据
data_feature = np.hstack((data_featureCata, data_featureNum))

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(data_feature, data_target, test_size=0.3, random_state=2)

# 定义模型和参数空间
model_param_grid = {
   'Logistic Regression': (LogisticRegression(random_state=33), {'C': [0.01, 0.1, 1, 10,100]}),
    'Decision Tree': (DecisionTreeClassifier(random_state=33), {'max_depth': [5, 7, 10, 15], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}),
    'Random Forest': (RandomForestClassifier(random_state=33), {'n_estimators': [100, 500, 1000],'max_depth': [1,3, 5, 7,12],'min_samples_split': [1, 5, 12],
                                                 'min_samples_leaf': [1, 2, 4],'max_features': ['sqrt', 'log2', None]}),
    'Gradient Boosting': (GradientBoostingClassifier(random_state=33), {'n_estimators': [100, 200, 300], 'learning_rate': [0.05, 0.1, 0.2], 'max_depth': [1, 3, 5]}),
    'Support Vector Machine': (SVC(probability=True, random_state=33), {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto']}),
    'K-Nearest Neighbors': (KNeighborsClassifier(), {'n_neighbors': [3, 5, 7, 9, 11]}),
    'Gaussian Naive Bayes': (GaussianNB(), {}),
    'Neural Network': (MLPClassifier(random_state=33), {'hidden_layer_sizes': [(10,), (20,), (50,), (100,)], 'activation': ['relu', 'tanh'], 'solver': ['adam', 'sgd']}),
}

# 定义颜色列表
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'brown']

# 初始化最佳AUC和最佳模型
best_auc = 0
best_model_name = ''
best_model = None

# 加载外验证集数据
external_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码插补缺失值矫正后CQ.csv')

# 导入数据
external_feature = external_data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                                  "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis",
                                  "age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                                  "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                                  "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
external_target = external_data['Ipsilateral Lateral Lymph Node Metastasis']
external_target.unique()  # 二分类

# 预处理外验证集数据
external_featureCata = external_data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                                      "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis"]]

external_featureNum = external_data[["age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                                     "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]

external_featureNum = scaler.transform(external_featureNum)
external_feature = np.hstack((external_featureCata, external_featureNum))

# Lists for evaluation metrics
Ext_accuracy_scores = []
Ext_auc_scores = []
Ext_precision_scores = []
Ext_specificity_scores = []
Ext_sensitivity_scores = []
Ext_npv_scores = []
Ext_ppv_scores = []
Ext_recall_scores = []
Ext_f1_scores = []
Ext_fpr_scores = []
Ext_rmse_scores = []
Ext_r2_scores = []
Ext_mae_scores = []
Ext_tn_scores = []
Ext_fp_scores = []
Ext_fn_scores = []
Ext_tp_scores = []
Ext_lift_scores = []
Ext_brier_scores = []
Ext_kappa_scores = []

# Fit models and plot ROC curve for external validation set
plt.figure(figsize=(8, 6))

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # Predict probabilities on external validation set
    if hasattr(best_model_temp, 'predict_proba'):
        y_test_pred_prob = best_model_temp.predict_proba(external_feature)[:, 1]
    else:
        y_test_pred_prob = best_model_temp.decision_function(external_feature)

    # Calculate AUC
    auc = roc_auc_score(external_target, y_test_pred_prob)

    # Update best model if current model has higher AUC
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_model = best_model_temp

    # Calculate ROC curve
    fpr, tpr, _ = roc_curve(external_target, y_test_pred_prob)

    # Plot ROC curve
    plt.plot(fpr, tpr, color=color, label='%s (AUC = %0.3f)' % (name, auc))

    # Calculate other evaluation metrics
    y_test_pred = best_model_temp.predict(external_feature)
    Ext_accuracy = accuracy_score(external_target, y_test_pred)
    Ext_precision = precision_score(external_target, y_test_pred)
    Ext_cm = confusion_matrix(external_target, y_test_pred)
    Ext_tn, Ext_fp, Ext_fn, Ext_tp = Ext_cm.ravel()
    Ext_specificity = Ext_tn / (Ext_tn + Ext_fp)
    Ext_sensitivity = recall_score(external_target, y_test_pred)
    Ext_npv = Ext_tn / (Ext_tn + Ext_fn)
    Ext_ppv = Ext_tp / (Ext_tp + Ext_fp)
    Ext_recall = Ext_sensitivity
    Ext_f1 = f1_score(external_target, y_test_pred)
    Ext_fpr = Ext_fp / (Ext_fp + Ext_tn)
    Ext_rmse = mean_squared_error(external_target, y_test_pred_prob, squared=False)
    Ext_r2 = r2_score(external_target, y_test_pred_prob)
    Ext_mae = mean_absolute_error(external_target, y_test_pred_prob)
    Ext_kappa = cohen_kappa_score(external_target, y_test_pred)
    Ext_lift = average_precision_score(external_target, y_test_pred_prob) / (sum(external_target) / len(external_target))
    Ext_brier = brier_score_loss(external_target, y_test_pred_prob)

    # Append evaluation metrics to lists
    Ext_accuracy_scores.append(Ext_accuracy)
    Ext_auc_scores.append(auc)
    Ext_precision_scores.append(Ext_precision)
    Ext_specificity_scores.append(Ext_specificity)
    Ext_sensitivity_scores.append(Ext_sensitivity)
    Ext_npv_scores.append(Ext_npv)
    Ext_ppv_scores.append(Ext_ppv)
    Ext_recall_scores.append(Ext_recall)
    Ext_f1_scores.append(Ext_f1)
    Ext_fpr_scores.append(Ext_fpr)
    Ext_rmse_scores.append(Ext_rmse)
    Ext_r2_scores.append(Ext_r2)
    Ext_mae_scores.append(Ext_mae)
    Ext_tn_scores.append(Ext_tn)
    Ext_fp_scores.append(Ext_fp)
    Ext_fn_scores.append(Ext_fn)
    Ext_tp_scores.append(Ext_tp)
    Ext_lift_scores.append(Ext_lift)
    Ext_brier_scores.append(Ext_brier)
    Ext_kappa_scores.append(Ext_kappa)

plt.grid(True)
plt.plot([0, 1], [0, 1], 'k--')  # Diagonal line
plt.grid(color='lightgray', linestyle='-', linewidth=1)  # Background grid lines
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC for Ipsilateral Lateral Lymph Node Metastasis (Validation Set)')
plt.legend(loc='lower right')
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/roc-curve侧区验证集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# Print best model name and AUC
print(f"Best model: {best_model_name} with AUC = {best_auc}")

# Create DataFrame for external validation metrics
Ext_metrics_df = pd.DataFrame({
    'Model': list(model_param_grid.keys()),
    'Accuracy': Ext_accuracy_scores,
    'AUC': Ext_auc_scores,
    'Precision': Ext_precision_scores,
    'Specificity': Ext_specificity_scores,
    'Sensitivity': Ext_sensitivity_scores,
    'Negative Predictive Value': Ext_npv_scores,
    'Positive Predictive Value': Ext_ppv_scores,
    'Recall': Ext_recall_scores,
    'F1 Score': Ext_f1_scores,
    'False Positive Rate': Ext_fpr_scores,
    'RMSE': Ext_rmse_scores,
    'R2': Ext_r2_scores,
    'MAE': Ext_mae_scores,
    'True Negatives': Ext_tn_scores,
    'False Positives': Ext_fp_scores,
    'False Negatives': Ext_fn_scores,
    'True Positives': Ext_tp_scores,
    'Lift': Ext_lift_scores,
    'Brier Score': Ext_brier_scores,
    'Kappa': Ext_kappa_scores,  
})

# Display DataFrame
print(Ext_metrics_df)

# Export metrics to CSV
Ext_metrics_df.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/3.验证集的评价指标.csv', index=False)


# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, r2_score, mean_absolute_error, cohen_kappa_score, average_precision_score, brier_score_loss
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

# 加载数据
data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')

# 导入数据
data_feature = data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                     "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis",
                     "age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                     "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
data_target = data['Ipsilateral Lateral Lymph Node Metastasis']

# 数值变量标准化
data_featureNum = data[["age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                        "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                        "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
scaler = MinMaxScaler()
data_featureNum = scaler.fit_transform(data_featureNum)

data_featureCata = data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                         "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis"]]
data_featureCata = np.array(data_featureCata)

# 整合数据
data_feature = np.hstack((data_featureCata, data_featureNum))

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(data_feature, data_target, test_size=0.3, random_state=2)

# 定义模型和参数空间
model_param_grid = {
    'Logistic Regression': (LogisticRegression(), {'C': [0.00000000000000000000000001, 0.0000000000000001]}),
    'Decision Tree': (DecisionTreeClassifier(), {'max_depth': [5, 7, 10, 15], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}),
    'Random Forest': (RandomForestClassifier(), {'n_estimators': [100, 200, 300], 'max_depth': [3, 5, 7], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4],
                                                 'max_features': ['sqrt', 'log2', None], 'random_state': [33]}),
    'Gradient Boosting': (GradientBoostingClassifier(), {'n_estimators': [10, 30, 50]}),
    'Support Vector Machine': (SVC(probability=True), {'C': [0.00000001, 0.001]}),
    'K-Nearest Neighbors': (KNeighborsClassifier(), {'n_neighbors': [3, 5, 7, 9, 11]}),
    'Gaussian Naive Bayes': (GaussianNB(), {}),
    'Neural Network': (MLPClassifier(), {'hidden_layer_sizes': [(0.05,), (1,), (1.5,)]}),
}

# 定义颜色列表
colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'brown']

# 初始化最佳AUC和最佳模型
best_auc = 0
best_model_name = ''
best_model = None

# 加载外验证集数据
external_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码插补缺失值矫正后CQ.csv')

# 导入数据
external_feature = external_data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                                  "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis",
                                  "age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                                  "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                                  "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
external_target = external_data['Ipsilateral Lateral Lymph Node Metastasis']
external_target.unique()  # 二分类

# 预处理外验证集数据
external_featureCata = external_data[["Tumor border", "Calcification", "Tumor internal vascularization", "Size", "Location", "Extrathyroidal extension",
                                      "T staging", "Ipsilateral Central Lymph Node Metastasis", "Recurrent Laryngeal Nerve Lymph Node Metastasis"]]

external_featureNum = external_data[["age", "size", "Ipsilateral Central Lymph Node Metastasis Rate", "Ipsilateral Central Lymph Node Metastases Number",
                                     "Pretracheal Lymph Node Metastases Number", "Paratracheal Lymph Node Metastasis Rate",
                                     "Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]

external_featureNum = scaler.transform(external_featureNum)
external_feature = np.hstack((external_featureCata, external_featureNum))

# Lists for evaluation metrics
Ext_accuracy_scores = []
Ext_auc_scores = []
Ext_precision_scores = []
Ext_specificity_scores = []
Ext_sensitivity_scores = []
Ext_npv_scores = []
Ext_ppv_scores = []
Ext_recall_scores = []
Ext_f1_scores = []
Ext_fpr_scores = []
Ext_rmse_scores = []
Ext_r2_scores = []
Ext_mae_scores = []
Ext_tn_scores = []
Ext_fp_scores = []
Ext_fn_scores = []
Ext_tp_scores = []
Ext_lift_scores = []
Ext_brier_scores = []
Ext_kappa_scores = []

# Fit models and plot ROC curve for external validation set
plt.figure(figsize=(8, 6))

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # Predict probabilities on external validation set
    if hasattr(best_model_temp, 'predict_proba'):
        y_test_pred_prob = best_model_temp.predict_proba(external_feature)[:, 1]
    else:
        y_test_pred_prob = best_model_temp.decision_function(external_feature)

    # Calculate AUC
    auc = roc_auc_score(external_target, y_test_pred_prob)

    # Update best model if current model has higher AUC
    if auc > best_auc:
        best_auc = auc
        best_model_name = name
        best_model = best_model_temp

    # Calculate ROC curve
    fpr, tpr, _ = roc_curve(external_target, y_test_pred_prob)

    # Plot ROC curve
    plt.plot(fpr, tpr, color=color, label='%s (AUC = %0.3f)' % (name, auc))

    # Calculate other evaluation metrics
    y_test_pred = best_model_temp.predict(external_feature)
    Ext_accuracy = accuracy_score(external_target, y_test_pred)
    Ext_precision = precision_score(external_target, y_test_pred)
    Ext_cm = confusion_matrix(external_target, y_test_pred)
    Ext_tn, Ext_fp, Ext_fn, Ext_tp = Ext_cm.ravel()
    Ext_specificity = Ext_tn / (Ext_tn + Ext_fp)
    Ext_sensitivity = recall_score(external_target, y_test_pred)
    Ext_npv = Ext_tn / (Ext_tn + Ext_fn)
    Ext_ppv = Ext_tp / (Ext_tp + Ext_fp)
    Ext_recall = Ext_sensitivity
    Ext_f1 = f1_score(external_target, y_test_pred)
    Ext_fpr = Ext_fp / (Ext_fp + Ext_tn)
    Ext_rmse = mean_squared_error(external_target, y_test_pred_prob, squared=False)
    Ext_r2 = r2_score(external_target, y_test_pred_prob)
    Ext_mae = mean_absolute_error(external_target, y_test_pred_prob)
    Ext_kappa = cohen_kappa_score(external_target, y_test_pred)
    Ext_lift = average_precision_score(external_target, y_test_pred_prob) / (sum(external_target) / len(external_target))
    Ext_brier = brier_score_loss(external_target, y_test_pred_prob)

    # Append evaluation metrics to lists
    Ext_accuracy_scores.append(Ext_accuracy)
    Ext_auc_scores.append(auc)
    Ext_precision_scores.append(Ext_precision)
    Ext_specificity_scores.append(Ext_specificity)
    Ext_sensitivity_scores.append(Ext_sensitivity)
    Ext_npv_scores.append(Ext_npv)
    Ext_ppv_scores.append(Ext_ppv)
    Ext_recall_scores.append(Ext_recall)
    Ext_f1_scores.append(Ext_f1)
    Ext_fpr_scores.append(Ext_fpr)
    Ext_rmse_scores.append(Ext_rmse)
    Ext_r2_scores.append(Ext_r2)
    Ext_mae_scores.append(Ext_mae)
    Ext_tn_scores.append(Ext_tn)
    Ext_fp_scores.append(Ext_fp)
    Ext_fn_scores.append(Ext_fn)
    Ext_tp_scores.append(Ext_tp)
    Ext_lift_scores.append(Ext_lift)
    Ext_brier_scores.append(Ext_brier)
    Ext_kappa_scores.append(Ext_kappa)

plt.grid(True)
plt.plot([0, 1], [0, 1], 'k--')  # Diagonal line
plt.grid(color='lightgray', linestyle='-', linewidth=1)  # Background grid lines
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC for Ipsilateral Lateral Lymph Node Metastasis (Validation Set)')
plt.legend(loc='lower right')
# 保存图像

plt.show()

# Print best model name and AUC
print(f"Best model: {best_model_name} with AUC = {best_auc}")

# Create DataFrame for external validation metrics
Ext_metrics_df = pd.DataFrame({
    'Model': list(model_param_grid.keys()),
    'Accuracy': Ext_accuracy_scores,
    'AUC': Ext_auc_scores,
    'Precision': Ext_precision_scores,
    'Specificity': Ext_specificity_scores,
    'Sensitivity': Ext_sensitivity_scores,
    'Negative Predictive Value': Ext_npv_scores,
    'Positive Predictive Value': Ext_ppv_scores,
    'Recall': Ext_recall_scores,
    'F1 Score': Ext_f1_scores,
    'False Positive Rate': Ext_fpr_scores,
    'RMSE': Ext_rmse_scores,
    'R2': Ext_r2_scores,
    'MAE': Ext_mae_scores,
    'True Negatives': Ext_tn_scores,
    'False Positives': Ext_fp_scores,
    'False Negatives': Ext_fn_scores,
    'True Positives': Ext_tp_scores,
    'Lift': Ext_lift_scores,
    'Brier Score': Ext_brier_scores,
    'Kappa': Ext_kappa_scores,  
})

# Display DataFrame
print(Ext_metrics_df)

# Export metrics to CSV
Ext_metrics_df.to_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/3.验证集的评价指标.csv', index=False)


# %%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score

# 定义风险阈值
thresholds = np.linspace(0, 1, 100)
Ext_net_benefit = []

for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_Ext_pred_prob = best_model_temp.predict_proba(external_feature)[:, 1]
    else:
        y_Ext_pred_prob = best_model_temp.decision_function(external_feature)

    Ext_model_net_benefit = []

    # 计算每个阈值下的净收益
    for threshold in thresholds:
        Ext_predictions = (y_Ext_pred_prob >= threshold).astype(int)
        tp = np.sum((external_target == 1) & (Ext_predictions == 1))
        fp = np.sum((external_target == 0) & (Ext_predictions == 1))
        fn = np.sum((external_target == 1) & (Ext_predictions == 0))
        tn = np.sum((external_target == 0) & (Ext_predictions == 0))
        
        net_benefit = (tp / len(external_target)) - (fp / len(external_target)) * (threshold / (1 - threshold))
        Ext_model_net_benefit.append(net_benefit)

    Ext_net_benefit.append(Ext_model_net_benefit)

# 转换为数组
Ext_net_benefit = np.array(Ext_net_benefit)

# 计算所有人都进行干预时的净收益
Ext_all_predictions = np.ones_like(external_target)  # 将所有预测标记为阳性（正类）
tp_all = np.sum((external_target == 1) & (Ext_all_predictions == 1))
fp_all = np.sum((external_target == 0) & (Ext_all_predictions == 1))

net_benefit_all = (tp_all / len(external_target)) - (fp_all / len(external_target)) * (thresholds / (1 - thresholds))
net_benefit_none = np.zeros_like(thresholds)

names = [
    'Logistic Regression',
    'Decision Tree',
    'Random Forest',
    'Gradient Boosting',
    'Support Vector Machine',
    'K-Nearest Neighbors',
    'Gaussian Naive Bayes',
    'Neural Network',
]

# 绘制DCA曲线
for i in range(Ext_net_benefit.shape[0]):
    plt.plot(thresholds, Ext_net_benefit[i], color=colors[i], label=names[i])

# 绘制"None"和"All"线
plt.plot(thresholds, net_benefit_none, color='black', linestyle='-', label='None')
plt.plot(thresholds, net_benefit_all, color='gray', linestyle='--', label='All')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
# 设置y轴的限制
plt.xlim(0, 0.6)
plt.ylim(-0.1, 0.5)

# 设置图形属性
plt.xlabel('Threshold')
plt.ylabel('Net Benefit')
plt.title('DCA For Ipsilateral Lateral Lymph Node Metastasis (Validation Set)')
plt.legend(loc='upper right')
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/DCA-curve侧区验证集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()


# %%
#外验证集的校准曲线
from sklearn.calibration import calibration_curve
from sklearn.metrics import brier_score_loss
from scipy.stats import ttest_ind

# 创建一个空列表来存储每个模型的校准曲线和Brier Score
Ext_calibration_curves = []
Ext_brier_scores = []

# 对每个模型进行循环
for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_Ext_pred_prob = best_model_temp.predict_proba(external_feature)[:, 1]
    else:
        y_Ext_pred_prob = best_model_temp.decision_function(external_feature)



    # 计算校准曲线
    Ext_fraction_of_positives, Ext_mean_predicted_value = calibration_curve(external_target, y_Ext_pred_prob, n_bins=10)
    Ext_calibration_curves.append((Ext_fraction_of_positives, Ext_mean_predicted_value, name, color))

    # 计算Brier分数
    Ext_brier_score = brier_score_loss(external_target, y_Ext_pred_prob)
    Ext_brier_scores.append((name, Ext_brier_score))

    # 打印Brier分数
    print(f'{name} - Brier Score: {Ext_brier_score:.3f}')

# 绘制校准曲线和Brier Score
fig, ax1 = plt.subplots(figsize=(10, 6))

for curve in Ext_calibration_curves:
    Ext_fraction_of_positives, Ext_mean_predicted_value, name, color = curve
    
    # 获取对应模型的Brier Score
    Ext_brier_score = next((score for model, score in Ext_brier_scores if model == name), None)
    
    # 将Brier Score赋予线颜色标注名称的后面
    if Ext_brier_score is not None:
        name += f' (Brier Score: {Ext_brier_score:.3f})'
    
    ax1.plot(Ext_mean_predicted_value, Ext_fraction_of_positives, "s-", label=name, color=color)
    
# 绘制"Perfectly calibrated"曲线
ax1.plot([0, 1], [0, 1], "k:",label="Perfectly calibrated")
    
ax1.set_ylabel("Fraction of positives")
ax1.set_xlabel("Mean predicted value")
ax1.set_ylim([-0.05, 1.05])
ax1.legend(loc="lower right")

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.title("Calibration Curves For Ipsilateral Lateral Lymph Node Metastasis (Validation set)")
plt.tight_layout()
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/校准曲线侧区验证集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# %%
#外验证集的精确召回曲线
from sklearn.metrics import precision_recall_curve, average_precision_score
import numpy as np

# 初始化存储精确召回曲线和平均精确度的列表
Ext_precision_recall_curves = []
Ext_average_precision_scores = []

# 遍历每个模型
for (name, (model, param_grid)), color in zip(model_param_grid.items(), colors):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_

    # 计算训练集上的预测概率
    if hasattr(best_model_temp, 'predict_proba'):
        y_Ext_pred_prob = best_model_temp.predict_proba(external_feature)[:, 1]
    else:
        y_Ext_pred_prob = best_model_temp.decision_function(external_feature)

    # 计算精确召回曲线
    Ext_precision, Ext_recall, _ = precision_recall_curve(external_target, y_Ext_pred_prob)
    Ext_average_precision = average_precision_score(external_target, y_Ext_pred_prob)

    # 存储结果
    Ext_precision_recall_curves.append((Ext_precision, Ext_recall, f'{name} (AUPR: {Ext_average_precision:.3f})', color))
    Ext_average_precision_scores.append((f'{name} (AUPR: {Ext_average_precision:.3f})', Ext_average_precision))

    # 打印平均精确度
    print(f'{name} - Average Precision: {Ext_average_precision:.3f}')

# 绘制精确召回曲线
fig, ax2 = plt.subplots(figsize=(10, 6))

for curve in Ext_precision_recall_curves:
    Ext_precision, Ext_recall, name, color = curve
    ax2.plot(Ext_recall, Ext_precision, "-", color=color, label=name)

# 添加随机猜测曲线
plt.plot([0, 1], [external_target.mean(), external_target.mean()], linestyle='--', color='black', label='Random Guessing')

ax2.set_xlabel("Recall")
ax2.set_ylabel("Precision")
ax2.set_ylim([0.0, 1.05])
ax2.set_xlim([0.0, 1.0])
ax2.legend(loc="lower left")
ax2.grid(True)

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)
plt.title("Precision Recall Curves For Ipsilateral Lateral Lymph Node Metastasis (Validation set)")
plt.tight_layout()
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/精确召回曲线侧区验证集_{dpi}dpi.{fmt}', format=fmt, dpi=dpi)

plt.show()

# %%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve, GridSearchCV

def plot_learning_curve_with_external(estimator, title, X_train, y_train, X_val, y_val, cv=None, n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(f"Learning Curve For Ipsilateral Lateral Lymph Node Metastasis: {title}")
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    
    train_sizes, train_scores, val_scores = learning_curve(estimator, X_train, y_train, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes, scoring='roc_auc')
    
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    val_scores_mean = np.mean(val_scores, axis=1)
    val_scores_std = np.std(val_scores, axis=1)
    
    external_scores = []
    for train_size in train_sizes:
        X_train_subset = X_train[:int(train_size)]
        y_train_subset = y_train[:int(train_size)]
        estimator.fit(X_train_subset, y_train_subset)
        if hasattr(estimator, 'predict_proba'):
            y_val_pred_prob = estimator.predict_proba(X_val)[:, 1]
        else:
            y_val_pred_prob = estimator.decision_function(X_val)
        external_score = roc_auc_score(y_val, y_val_pred_prob)
        external_scores.append(external_score)
    
    plt.grid()
    
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color="red")
    plt.fill_between(train_sizes, val_scores_mean - val_scores_std, val_scores_mean + val_scores_std, alpha=0.1, color="green")
    plt.fill_between(train_sizes, external_scores - np.std(external_scores), external_scores + np.std(external_scores), alpha=0.1, color="blue")
    
    plt.plot(train_sizes, train_scores_mean, 'o-', color="red", label=f"Train score (mean ROC AUC={train_scores_mean[-1]:.3f})")
    plt.plot(train_sizes, val_scores_mean, 'o-', color="green", label=f"Test score (mean ROC AUC={val_scores_mean[-1]:.3f})")
    plt.plot(train_sizes, external_scores, 'o-', color="blue", label=f"Validation score (mean ROC AUC={np.mean(external_scores):.3f})")
    
    for i, train_size in enumerate(train_sizes):
        plt.text(train_size, train_scores_mean[i], f'{train_scores_mean[i]:.3f}', color='red')
        plt.text(train_size, val_scores_mean[i], f'{val_scores_mean[i]:.3f}', color='green')
        plt.text(train_size, external_scores[i], f'{external_scores[i]:.3f}', color='blue')
    
    
    plt.legend(loc="best")

    formats = ['tiff']
    dpis = [300, 1200]
    for fmt in formats:
        for dpi in dpis:
            plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/2.筛选模型/侧区学习曲线_{title}_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')
    plt.show()

# 绘制所有模型的学习曲线（训练集和外部验证集）
for name, (model, param_grid) in model_param_grid.items():
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
    grid_search.fit(class_x_tra, class_y_tra)
    best_model_temp = grid_search.best_estimator_
    
    plot_learning_curve_with_external(best_model_temp, name, class_x_tra, class_y_tra, external_feature, external_target, cv=10, n_jobs=-1)


# %% [markdown]
# 重要性值条形图

# %%
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')

# 导入数据
data_feature = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension","T staging",
                "Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
                "age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number","Pretracheal Lymph Node Metastases Number",
                "Paratracheal Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"
]]
data_target = data['Ipsilateral Lateral Lymph Node Metastasis']

# 数值变量标准化
data_featureNum = data[["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number","Pretracheal Lymph Node Metastases Number",
                "Paratracheal Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
scaler = MinMaxScaler()
data_featureNum = scaler.fit_transform(data_featureNum)

data_featureCata = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension","T staging",
                "Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",]]
data_featureCata = np.array(data_featureCata)

# 整合数据
data_feature = np.hstack((data_featureCata, data_featureNum))

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(data_feature, data_target, test_size=0.3, random_state=2)

# 进行随机森林模型的参数搜索
rf_model = RandomForestClassifier()
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None],'random_state': [33]
}

grid_search = GridSearchCV(estimator=rf_model, param_grid=rf_param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
grid_search.fit(class_x_tra, class_y_tra)
best_rf_model = grid_search.best_estimator_

# 提取随机森林模型的特征变量重要性
feature_importances = best_rf_model.feature_importances_

# 创建特征重要性DataFrame
feature_cols = ["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                  "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

# 计算每个特征的重要性百分比
total_importance = importance_df['Importance'].abs().sum()
importance_df['ImportancePercent'] = importance_df['Importance'] / total_importance

# 按照重要性绝对值排序
importance_df = importance_df.reindex(importance_df['Importance'].abs().sort_values(ascending=False).index)

plt.figure(figsize=(12, 8))
# Scaling factor for bubble sizes based on importance values
sizes = np.abs(importance_df['Importance']) * 3000  

# Using colormap to set color intensity based on size
norm = plt.Normalize(sizes.min(), sizes.max())
colors = plt.cm.YlOrBr(norm(sizes))    #plt.cm.Blues/plt.cm.Greens/plt.cm.YlOrBr

# Scatter plot with bubble sizes, and labels for importance values and percentages
scatter = plt.scatter(importance_df['Importance'], importance_df['Feature'], s=sizes, color=colors)

# Adding labels and annotations
for i, row in importance_df.iterrows():
    imp_value = row['Importance']
    imp_percent = f" ({row['ImportancePercent']:.3%})"
    plt.annotate(f"{imp_value:.3f}{imp_percent}", (imp_value, row['Feature']), fontsize=12,
                 ha='center', va='center', xytext=(np.sign(imp_value)*50, 0), textcoords='offset points')

# Customizing plot appearance
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importances and Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.grid(True)
plt.gca().invert_yaxis()

# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/泡泡图_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()


# %%
#绘制所有变量的重要性值条形图
plt.figure(figsize=(12, 8))
bars = plt.barh(importance_df['Feature'], importance_df['Importance'], color=colors)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importances and Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.gca().invert_yaxis()


for i, row in importance_df.iterrows():
 imp_value = row['Importance']
 imp_percent = f" ({row['ImportancePercent']:.3%})"
 plt.annotate(f"{imp_value:.3f}{imp_percent}", (imp_value, row['Feature']), fontsize=12,
 ha='center', va='center', xytext=(np.sign(imp_value)*50, 0), textcoords='offset points')

# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/重要性值和贡献度条形图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 绘制所有变量的重要性值条形图
plt.figure(figsize=(12, 8))
bars = plt.barh(importance_df['Feature'], importance_df['Importance'], color=colors)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importances for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.gca().invert_yaxis()

# 添加重要性值标签
for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.3f}', va='center')

# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/重要性值条形图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()


!pip install seaborn
import seaborn as sns

# 计算贡献度百分比
importance_df['Contribution'] = importance_df['Importance'] / importance_df['Importance'].sum()

# 绘制带有百分比标签的条形图
plt.figure(figsize=(12, 8))
bars = plt.barh(importance_df['Feature'], importance_df['Contribution'],color=colors)
plt.xlabel('Contribution')
plt.ylabel('Feature')
plt.title('Feature Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.gca().invert_yaxis()

# 添加贡献度百分比标签
for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.3%}', va='center')

    
# 保存图像
formats = ['tiff', 'eps', 'png']
dpis = [300, 1200]
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/贡献度条形图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()


# 计算贡献度百分比
importance_df['Contribution'] = importance_df['Importance'] / importance_df['Importance'].sum()

# 绘制饼图
plt.figure(figsize=(12, 8))
plt.pie(importance_df['Contribution'], labels=importance_df['Feature'], autopct='%1.3f%%', startangle=140, colors=sns.color_palette("tab10"))
plt.title('Feature Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
# 保存图像
formats = ['tiff', 'eps', 'png']    
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/饼图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()



# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm



# 取前十位特征，并重新计算百分比使总和为100%
top10_importance_df = importance_df.head(10)
top10_importance_sum = top10_importance_df['Importance'].abs().sum()
top10_importance_df['ImportancePercent'] = top10_importance_df['Importance'] / top10_importance_sum

# 绘制前十位特征的重要性泡泡图
plt.figure(figsize=(12, 8))
norm = plt.Normalize(top10_importance_df['ImportancePercent'].min(), top10_importance_df['ImportancePercent'].max())
sizes = top10_importance_df['ImportancePercent'] * 3000  # 根据百分比调整泡泡大小
colors = cm.YlOrBr(norm(top10_importance_df['ImportancePercent']))  # 使用规范化后的百分比来调整颜色plt.cm.YlOrBr

scatter = plt.scatter(top10_importance_df['Importance'], top10_importance_df['Feature'], s=sizes, color=colors)
for i, row in top10_importance_df.iterrows():
    imp_value = row['Importance']
    imp_percent = f" ({row['ImportancePercent']:.3%})"
    plt.annotate(f"{imp_value:.3f}{imp_percent}", (imp_value, row['Feature']), fontsize=12,
                 ha='center', va='center', xytext=(np.sign(imp_value)*50, 0), textcoords='offset points')
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Top 10 Feature Importances and Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.grid(True)
plt.gca().invert_yaxis()

# 保存图像
formats = ['tiff', 'eps', 'png']    
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/10泡泡图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 绘制前十位特征的贡献形图-----------------------------------------------
plt.figure(figsize=(12, 8))
bars = plt.barh(top10_importance_df['Feature'], top10_importance_df['ImportancePercent'], color=colors)
plt.xlabel('Importance Percent')
plt.ylabel('Feature')
plt.title('Top 10 Feature Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.gca().invert_yaxis()

# 添加重要性百分比标签
for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.3%}', va='center')
# 保存图像
formats = ['tiff', 'eps', 'png']
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/10贡献度图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 绘制前10个特征的贡献度饼图---------------------------------------------------
plt.figure(figsize=(12, 8))
plt.pie(top10_importance_df['ImportancePercent'], labels=top10_importance_df['Feature'], autopct='%1.3f%%', startangle=140, colors=sns.color_palette("tab10"))
plt.title('Top 10 Feature Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
 # 保存图像
formats = ['tiff', 'eps', 'png']   
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/10贡献度饼图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 绘制重要性值和贡献度的条形图--------------------------------------------------------
plt.figure(figsize=(12, 8))
bars = plt.barh(top10_importance_df['Feature'], top10_importance_df['Importance'], color=colors)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Top 10 Feature Importances and Contributions for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.gca().invert_yaxis()


for i, row in top10_importance_df.iterrows():
 imp_value = row['Importance']
 imp_percent = f" ({row['ImportancePercent']:.3%})"
 plt.annotate(f"{imp_value:.3f}{imp_percent}", (imp_value, row['Feature']), fontsize=12,
 ha='center', va='center', xytext=(np.sign(imp_value)*50, 0), textcoords='offset points')
# 保存图像
formats = ['tiff', 'eps', 'png']
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/10重要性值贡献度条形图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()


 
#前十重要性条形图----------------------------------------------------------------------------------
plt.figure(figsize=(12, 8))
bars = plt.barh(top10_importance_df['Feature'], top10_importance_df['Importance'], color=colors)
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Top 10 Importances for Ipsilateral Lateral Lymph Node Metastasis Random Forest Model')
plt.gca().invert_yaxis()

#添加重要性值标签
for bar in bars:
 width = bar.get_width()
 plt.text(width, bar.get_y() + bar.get_height()/2, f'{width:.3f}', va='center')


# 保存图像
formats = ['tiff', 'eps', 'png']
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/10重要性值图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()



# %% [markdown]
# 热图

# %%
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')

# 导入数据
data_feature = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension","T staging",
                "Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
                "age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number","Pretracheal Lymph Node Metastases Number",
                "Paratracheal Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"
]]
data_target = data['Ipsilateral Lateral Lymph Node Metastasis']

# 数值变量标准化
data_featureNum = data[["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number","Pretracheal Lymph Node Metastases Number",
                "Paratracheal Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]]
scaler = MinMaxScaler()
data_featureNum = scaler.fit_transform(data_featureNum)

data_featureCata = data[["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension","T staging",
                "Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis"]]
data_featureCata = np.array(data_featureCata)

# 整合数据
data_feature = np.hstack((data_featureCata, data_featureNum))

# 分为训练集和验证集
class_x_tra, class_x_val, class_y_tra, class_y_val = train_test_split(data_feature, data_target, test_size=0.3, random_state=2)

# 进行随机森林模型的参数搜索
rf_model = RandomForestClassifier()
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None],
    'random_state': [33]
}

grid_search = GridSearchCV(estimator=rf_model, param_grid=rf_param_grid, cv=10, n_jobs=-1, scoring='roc_auc')
grid_search.fit(class_x_tra, class_y_tra)
best_rf_model = grid_search.best_estimator_

# 提取随机森林模型的特征变量重要性
feature_importances = best_rf_model.feature_importances_

# 创建特征重要性DataFrame
feature_cols = ["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                  "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

# 选择排名前十的特征
top10_features = importance_df.head(10)['Feature']

# 确保数据没有缺失值
class_x_tra_df = pd.DataFrame(class_x_tra, columns=feature_cols).fillna(0)

# 重新排序数据框列以匹配特征重要性排序
class_x_tra_sorted = class_x_tra_df[importance_df['Feature']]
class_x_tra_top10_sorted = class_x_tra_df[top10_features]

import matplotlib.pyplot as plt
import seaborn as sns

# 假设 dpis 是一个包含所需 DPI 值的列表
dpis = [300,1200]

# 绘制全样本和全部特征的热图
plt.figure(figsize=(12, 8))
sns.heatmap(class_x_tra_sorted.corr(), annot=True, cmap='coolwarm', linewidths=0.5, center=0)
plt.title('Ipsilateral Lateral Lymph Node Metastasis Heatmap of All Features')

# 保存图像
formats = ['tiff', 'eps', 'png']
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/热图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()

# 绘制前十个特征的热图
plt.figure(figsize=(12, 8))
corr_matrix_top10 = class_x_tra_top10_sorted.corr()
sns.heatmap(corr_matrix_top10, annot=True, cmap='coolwarm', center=0, linewidths=0.5, cbar_kws={"shrink": 0.8})
plt.title('Ipsilateral Lateral Lymph Node Metastasis Heatmap of Top 10 Features')

# 保存图像
for fmt in formats:
    for dpi in dpis:
        plt.savefig(f'/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/1.侧区的结果/4.可视化/10热图侧区_{dpi}dpi.{fmt}', format=fmt, dpi=dpi, bbox_inches='tight')

plt.show()


# %%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import roc_auc_score, roc_curve


# 其他代码
# 加载数据
C_train_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总编码插补缺失值矫正后CQ.csv')
C_test_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/1.总V编码插补缺失值矫正后CQ.csv')
IIQ_train_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/2.总编码插补缺失值矫正后2Q.csv')
IIQ_test_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/2.总V编码插补缺失值矫正后2Q.csv')
IIIQ_train_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/3.总编码插补缺失值矫正后3Q.csv')
IIIQ_test_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/3.总V编码插补缺失值矫正后3Q.csv')
IVQ_train_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/4.总编码插补缺失值矫正后4Q.csv')
IVQ_test_data = pd.read_csv('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/p数据/4.总V编码插补缺失值矫正后4Q.csv')

# 提取特征和目标
C_feature_cols = ["Tumor border","Calcification","Tumor internal vascularization","Size","Location","Extrathyroidal extension",
                  "T staging","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",
"Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
C_target_col = 'Ipsilateral Lateral Lymph Node Metastasis'

IIQ_feature_cols = ["Aspect ratio","Tumor Peripheral blood flow","Location","Mulifocality","Extrathyroidal extension", 
                    "Side of position","Ipsilateral Central Lymph Node Metastasis","Pretracheal Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastasis Rate","Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate"]
IIQ_target_col = 'II Level Lymph Node Metastasis'

IIIQ_feature_cols = ["Tumor border","Calcification","Tumor internal vascularization","Hashimoto",
"Location","Extrathyroidal extension","Ipsilateral Central Lymph Node Metastasis","Recurrent Laryngeal Nerve Lymph Node Metastasis",
"age","size","Ipsilateral Central Lymph Node Metastasis Rate",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",]#3Q选好了
IIIQ_target_col = 'III Level Lymph Node Metastasis'

IVQ_feature_cols = ["Tumor border","Aspect ratio","Calcification","Tumor internal vascularization","Extrathyroidal extension","Side of position","T staging",
 "Paratracheal Lymph Node Metastasis","age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number",]   #4区选好了
IVQ_target_col = 'IV Level Lymph Node Metastasis'

# 数据处理函数
def preprocess_data(train_data, test_data, feature_cols, target_col, num_cols):
    train_features = train_data[feature_cols]
    train_target = train_data[target_col]
    test_features = test_data[feature_cols]
    test_target = test_data[target_col]
    
    scaler = MinMaxScaler()
    train_features[num_cols] = scaler.fit_transform(train_features[num_cols])
    test_features[num_cols] = scaler.transform(test_features[num_cols])
    
    x_tra, x_val, y_tra, y_val = train_test_split(train_features, train_target, test_size=0.3, random_state=2)
    
    return x_tra, x_val, y_tra, y_val, test_features, test_target

C_num_cols = ["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate","Recurrent Laryngeal Nerve Lymph Node Metastasis Number"]
IIQ_num_cols = ["age","size","Ipsilateral Central Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastasis Rate","Prelaryngeal Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastasis Rate","Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate"]
IIIQ_num_cols = ["age","size","Ipsilateral Central Lymph Node Metastasis Rate",
"Pretracheal Lymph Node Metastases Number","Paratracheal Lymph Node Metastasis Rate",]
IVQ_num_cols = ["T staging","age","size","Ipsilateral Central Lymph Node Metastasis Rate","Ipsilateral Central Lymph Node Metastases Number",
"Pretracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastasis Rate","Paratracheal Lymph Node Metastases Number",]

# 预处理数据
C_x_tra, C_x_val, C_y_tra, C_y_val, C_test_features, C_test_target = preprocess_data(
    C_train_data, C_test_data, C_feature_cols, C_target_col, C_num_cols)
IIQ_x_tra, IIQ_x_val, IIQ_y_tra, IIQ_y_val, IIQ_test_features, IIQ_test_target = preprocess_data(
    IIQ_train_data, IIQ_test_data, IIQ_feature_cols, IIQ_target_col, IIQ_num_cols)
IIIQ_x_tra, IIIQ_x_val, IIIQ_y_tra, IIIQ_y_val, IIIQ_test_features, IIIQ_test_target = preprocess_data(
    IIIQ_train_data, IIIQ_test_data, IIIQ_feature_cols, IIIQ_target_col, IIIQ_num_cols)
IVQ_x_tra, IVQ_x_val, IVQ_y_tra, IVQ_y_val, IVQ_test_features, IVQ_test_target = preprocess_data(
    IVQ_train_data, IVQ_test_data, IVQ_feature_cols, IVQ_target_col, IVQ_num_cols)

# 定义模型和参数空间
model_param_grid = {
    'Random Forest': (RandomForestClassifier(), {'n_estimators': [100, 200, 300], 
                                                'max_depth': [3, 5, 7], 'min_samples_split': [2, 5, 10],
                                                'min_samples_leaf': [1, 2, 4], 'max_features': ['sqrt', 'log2', None],
                                                'random_state': [33]})
}

# 绘制ROC曲线函数
def plot_roc_curve(best_model, x_train, y_train, x_val, y_val, x_test, y_test, colors, label_prefix):
    y_train_pred_prob = best_model.predict_proba(x_train)[:, 1]
    y_val_pred_prob = best_model.predict_proba(x_val)[:, 1]
    y_test_pred_prob = best_model.predict_proba(x_test)[:, 1]
    
    train_auc = roc_auc_score(y_train, y_train_pred_prob)
    val_auc = roc_auc_score(y_val, y_val_pred_prob)
    test_auc = roc_auc_score(y_test, y_test_pred_prob)
    
    fpr, tpr, _ = roc_curve(y_train, y_train_pred_prob)
    plt.plot(fpr, tpr, color=colors[0], label=f'{label_prefix} Train AUC = {train_auc:.3f}')
    

    fpr, tpr, _ = roc_curve(y_val, y_val_pred_prob)
    plt.plot(fpr, tpr, color=colors[1], label=f'{label_prefix} Test AUC = {val_auc:.3f}')
    
    fpr, tpr, _ = roc_curve(y_test, y_test_pred_prob)
    plt.plot(fpr, tpr, color=colors[2], label=f'{label_prefix}  Validation AUC = {test_auc:.3f}')

# 寻找最佳模型并绘制ROC曲线
plt.figure(figsize=(12, 8))
colors_C = ['goldenrod', 'orange', 'gold']
colors_IIQ = ['#C71585', 'red','pink', ]
colors_IIIQ = ['darkblue', 'blue', 'skyblue']
colors_IVQ = ['darkgreen', 'green', 'lightgreen']

# 侧区数据
grid_search = GridSearchCV(estimator=model_param_grid['Random Forest'][0], param_grid=model_param_grid['Random Forest'][1], cv=10, n_jobs=-1, scoring='roc_auc' )
grid_search.fit(C_x_tra, C_y_tra)
best_model_C = grid_search.best_estimator_
plot_roc_curve(best_model_C, C_x_tra, C_y_tra, C_x_val, C_y_val, C_test_features, C_test_target, colors_C, 'Ipsilateral Lateral Lymph Node Metastasis')

# 2区数据
grid_search.fit(IIQ_x_tra, IIQ_y_tra)
best_model_IIQ = grid_search.best_estimator_
plot_roc_curve(best_model_IIQ, IIQ_x_tra, IIQ_y_tra, IIQ_test_features, IIQ_test_target,IIQ_x_val, IIQ_y_val, colors_IIQ, 'Level II Lymph Node Metastasis')

# 3区数据
grid_search.fit(IIIQ_x_tra, IIIQ_y_tra)
best_model_IIIQ = grid_search.best_estimator_
plot_roc_curve(best_model_IIIQ, IIIQ_x_tra, IIIQ_y_tra, IIIQ_x_val, IIIQ_y_val, IIIQ_test_features, IIIQ_test_target, colors_IIIQ, 'Level III Lymph Node Metastasis')

# 4区数据
grid_search.fit(IVQ_x_tra, IVQ_y_tra)
best_model_IVQ = grid_search.best_estimator_
plot_roc_curve(best_model_IVQ, IVQ_x_tra, IVQ_y_tra, IVQ_x_val, IVQ_y_val, IVQ_test_features, IVQ_test_target, colors_IVQ, 'Level IV Lymph Node Metastasis')

# 绘制对角线
plt.plot([0, 1], [0, 1], 'k--')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves for Lymph Node Metastasis Random Forest Prediction(All sets)')
plt.legend(loc='lower right')
# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区全集.tiff', format='tiff', dpi=1200)
# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区全集300.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区全集.eps', format='eps', dpi=1200)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区全集300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区全集.png', format='png', dpi=1200)

plt.show()



# %%
# 绘制训练集的ROC曲线函数
def plot_roc_curve_train(best_model, x_train, y_train, colors, label_prefix):
    y_train_pred_prob = best_model.predict_proba(x_train)[:, 1]
    train_auc = roc_auc_score(y_train, y_train_pred_prob)
    fpr, tpr, _ = roc_curve(y_train, y_train_pred_prob)
    plt.plot(fpr, tpr, color=colors, label=f'{label_prefix} Train AUC = {train_auc:.3f}')

# 寻找最佳模型并绘制训练集的ROC曲线
plt.figure(figsize=(12, 8))
colors_train = {
    'C': 'goldenrod',
    'IIQ': 'darkred',
    'IIIQ': 'darkblue',
    'IVQ': 'darkgreen'
}

# 绘制侧区数据的训练集ROC曲线
plot_roc_curve_train(best_model_C, C_x_tra, C_y_tra, colors_train['C'], 'Ipsilateral Lateral Lymph Node Metastasis')

# 绘制2区数据的训练集ROC曲线
plot_roc_curve_train(best_model_IIQ, IIQ_x_tra, IIQ_y_tra, colors_train['IIQ'], 'Level II Lymph Node Metastasis')

# 绘制3区数据的训练集ROC曲线
plot_roc_curve_train(best_model_IIIQ, IIIQ_x_tra, IIIQ_y_tra, colors_train['IIIQ'], 'Level III Lymph Node Metastasis')

# 绘制4区数据的训练集ROC曲线
plot_roc_curve_train(best_model_IVQ, IVQ_x_tra, IVQ_y_tra, colors_train['IVQ'], 'Level IV Lymph Node Metastasis')

# 绘制对角线
plt.plot([0, 1], [0, 1], 'k--')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves for Lymph Node Metastasis Random Forest Prediction (Train Set)')
plt.legend(loc='lower right')
# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区训练集.tiff', format='tiff', dpi=1200)
# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区训练集300.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区训练集.eps', format='eps', dpi=1200)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区训练集300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区训练集.png', format='png', dpi=1200)
plt.show()


# %%
# 绘制训练集的ROC曲线函数
def plot_roc_curve_val(best_model, x_val, y_val, colors, label_prefix):
    y_val_pred_prob = best_model.predict_proba(x_val)[:, 1]
    test_auc = roc_auc_score(y_val, y_val_pred_prob)
    fpr, tpr, _ = roc_curve(y_val, y_val_pred_prob)
    plt.plot(fpr, tpr, color=colors, label=f'{label_prefix} Validation AUC = {test_auc:.3f}')

# 寻找最佳模型并绘制训练集的ROC曲线
plt.figure(figsize=(12, 8))
colors_val = {
    'C': 'orange',
    'IIQ': '#C71585',
    'IIIQ': 'blue',
    'IVQ': 'green'
}

# 绘制训练集的ROC曲线函数
def plot_roc_curve_test(best_model, x_test, y_test, colors, label_prefix):
    y_test_pred_prob = best_model.predict_proba(x_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_test_pred_prob)
    fpr, tpr, _ = roc_curve(y_test, y_test_pred_prob)
    plt.plot(fpr, tpr, color=colors, label=f'{label_prefix} Validation AUC = {test_auc:.3f}')

# 寻找最佳模型并绘制训练集的ROC曲线
plt.figure(figsize=(12, 8))
colors_test = {
    'C': 'gold',
    'IIQ': '#C71585',
    'IIIQ': 'skyblue',
    'IVQ': 'lightgreen'
}


# 绘制侧区数据的训练集ROC曲线
plot_roc_curve_val(best_model_C, C_x_val, C_y_val, colors_test['C'], 'Ipsilateral Lateral Lymph Node Metastasis')


# 绘制2区数据的训练集ROC曲线
plot_roc_curve_test(best_model_IIQ, IIQ_test_features, IIQ_test_target, colors_val['IIQ'], 'Level II Lymph Node Metastasis')

# 绘制3区数据的训练集ROC曲线
plot_roc_curve_val(best_model_IIIQ, IIIQ_x_val, IIIQ_y_val,  colors_val['IIIQ'], 'Level III Lymph Node Metastasis')

# 绘制4区数据的训练集ROC曲线
plot_roc_curve_val(best_model_IVQ, IVQ_x_val, IVQ_y_val,  colors_val['IVQ'], 'Level IV Lymph Node Metastasis')

# 绘制对角线
plt.plot([0, 1], [0, 1], 'k--')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves for Lymph Node Metastasis Random Forest Prediction (Test Set)')
plt.legend(loc='lower right')

# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区测试集.tiff', format='tiff', dpi=1200)
# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区测试集300.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区测试集.eps', format='eps', dpi=1200)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区测试集300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区测试集.png', format='png', dpi=1200)
plt.show()

# %%
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

# 绘制训练集的ROC曲线函数
def plot_roc_curve_test(best_model, x_test, y_test, colors, label_prefix):
    y_test_pred_prob = best_model.predict_proba(x_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_test_pred_prob)
    fpr, tpr, _ = roc_curve(y_test, y_test_pred_prob)
    plt.plot(fpr, tpr, color=colors, label=f'{label_prefix} Validation AUC = {test_auc:.3f}')

# 寻找最佳模型并绘制训练集的ROC曲线
plt.figure(figsize=(12, 8))
colors_test = {
    'C': 'gold',
    'IIQ': 'pink',
    'IIIQ': 'skyblue',
    'IVQ': 'lightgreen'
}

# 绘制侧区数据的训练集ROC曲线
plot_roc_curve_test(best_model_C, C_test_features, C_test_target, colors_test['C'], 'Ipsilateral Lateral Lymph Node Metastasis')

# 绘制2区数据的训练集ROC曲线
plot_roc_curve_test(best_model_IIQ, IIQ_x_val, IIQ_y_val, colors_test['IIQ'], 'Level II Lymph Node Metastasis')

# 绘制3区数据的训练集ROC曲线
plot_roc_curve_test(best_model_IIIQ, IIIQ_test_features, IIIQ_test_target, colors_test['IIIQ'], 'Level III Lymph Node Metastasis')

# 绘制4区数据的训练集ROC曲线
plot_roc_curve_test(best_model_IVQ, IVQ_test_features, IVQ_test_target, colors_test['IVQ'], 'Level IV Lymph Node Metastasis')

# 绘制对角线
plt.plot([0, 1], [0, 1], 'k--')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curves for Lymph Node Metastasis Random Forest Prediction (Validation Set)')
plt.legend(loc='lower right')

# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区验证集.tiff', format='tiff', dpi=1200)
# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区验证集300.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区验证集.eps', format='eps', dpi=1200)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区验证集300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/roc_curve侧区验证集.png', format='png', dpi=1200)

plt.show()



# %%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

# 净收益计算函数
def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        n = len(y_true)
        net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        net_benefits.append(net_benefit)
    return net_benefits

# 绘制DCA曲线函数
def plot_dca_curve(model, x_train, y_train, x_val, y_val, x_test, y_test, colors, label_prefix):
    decision_thresholds = np.linspace(0, 1, 100)
    
    y_train_pred_prob = model.predict_proba(x_train)[:, 1]
    y_val_pred_prob = model.predict_proba(x_val)[:, 1]
    y_test_pred_prob = model.predict_proba(x_test)[:, 1]
    
    net_benefits_train = calculate_net_benefit(y_train, y_train_pred_prob, decision_thresholds)
    net_benefits_val = calculate_net_benefit(y_val, y_val_pred_prob, decision_thresholds)
    net_benefits_test = calculate_net_benefit(y_test, y_test_pred_prob, decision_thresholds)
    
    plt.plot(decision_thresholds, net_benefits_train, color=colors[0], lw=2, label=f'{label_prefix} Train')
    plt.plot(decision_thresholds, net_benefits_val, color=colors[1], lw=2, label=f'{label_prefix} Test')
    plt.plot(decision_thresholds, net_benefits_test, color=colors[2], lw=2, label=f'{label_prefix} Validation')
# 计算All线和None线
def calculate_all_net_benefit(y_true, thresholds):
    n = len(y_true)
    all_net_benefits = []
    for thresh in thresholds:
        tp = np.sum(y_true == 1)
        fp = np.sum(y_true == 0)
        net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        all_net_benefits.append(net_benefit)
    return all_net_benefits

# 生成12根线的DCA曲线
plt.figure(figsize=(12, 8))

plot_dca_curve(best_model_C, C_x_tra, C_y_tra, C_x_val, C_y_val, C_test_features, C_test_target, ['goldenrod', 'orange', 'gold'], 'Ipsilateral Lateral Lymph Node Metastasis')
plot_dca_curve(best_model_IIQ, IIQ_x_tra, IIQ_y_tra, IIQ_test_features, IIQ_test_target,IIQ_x_val, IIQ_y_val, ['#C71585', 'red', 'pink'], 'Level II Lymph Node Metastasis')
plot_dca_curve(best_model_IIIQ, IIIQ_x_tra, IIIQ_y_tra, IIIQ_x_val, IIIQ_y_val, IIIQ_test_features, IIIQ_test_target, ['darkblue', 'blue', 'skyblue'], 'Level III Lymph Node Metastasis')
plot_dca_curve(best_model_IVQ, IVQ_x_tra, IVQ_y_tra, IVQ_x_val, IVQ_y_val, IVQ_test_features, IVQ_test_target, ['darkgreen', 'green', 'lightgreen'], 'Level IV Lymph Node Metastasis')

# None线
plt.plot(np.linspace(0, 1, 100), np.zeros(100), 'k-', lw=2, label='None')

# 使用IVQ的数据计算All线
all_net_benefits_train = calculate_all_net_benefit(IVQ_y_tra, np.linspace(0, 1, 100))
all_net_benefits_val = calculate_all_net_benefit(IVQ_y_val, np.linspace(0, 1, 100))
all_net_benefits_test = calculate_all_net_benefit(IVQ_test_target, np.linspace(0, 1, 100))

# 绘制All线（分别使用训练集、验证集和测试集数据）
plt.plot(np.linspace(0, 1, 100), all_net_benefits_train, 'gray', linestyle='--', lw=2, label='All Train')
plt.plot(np.linspace(0, 1, 100), all_net_benefits_val, 'darkgray', linestyle='--', lw=2, label='All Validation')
plt.plot(np.linspace(0, 1, 100), all_net_benefits_test, 'lightgray', linestyle='--', lw=2, label='All Test')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('Threshold Probability', fontsize=12)
plt.ylabel('Net Benefit', fontsize=12)
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
plt.title('DCA for Lymph Node Metastasis Random Forest Prediction (All sets)', fontsize=14)
plt.legend(loc='upper right', fontsize=10)

# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve侧区全集.tiff', format='tiff', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve侧区全集300.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve侧区全集.eps', format='eps', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve侧区全集300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve侧区全集.png', format='png', dpi=1200)

plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

# 净收益计算函数
def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        n = len(y_true)
        net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        net_benefits.append(net_benefit)
    return net_benefits

# 绘制训练集DCA曲线函数
def plot_dca_curve_train(model, x_train, y_train, color, label):
    decision_thresholds = np.linspace(0, 1, 100)
    y_train_pred_prob = model.predict_proba(x_train)[:, 1]
    net_benefits_train = calculate_net_benefit(y_train, y_train_pred_prob, decision_thresholds)
    plt.plot(decision_thresholds, net_benefits_train, color=color, lw=2, label=label)

# 生成4根线的DCA曲线
plt.figure(figsize=(12, 8))

colors_train = {
    'C': 'goldenrod',
    'IIQ': 'darkred',
    'IIIQ': 'darkblue',
    'IVQ': 'darkgreen'
}

# 绘制同侧侧区数据的训练集DCA曲线
plot_dca_curve_train(best_model_C, C_x_tra, C_y_tra, colors_train['C'], 'Ipsilateral Lateral Lymph Node Metastasis')

# 绘制II区数据的训练集DCA曲线
plot_dca_curve_train(best_model_IIQ, IIQ_x_tra, IIQ_y_tra, colors_train['IIQ'], 'Level II Lymph Node Metastasis')

# 绘制III区数据的训练集DCA曲线
plot_dca_curve_train(best_model_IIIQ, IIIQ_x_tra, IIIQ_y_tra, colors_train['IIIQ'], 'Level III Lymph Node Metastasis')

# 绘制IV区数据的训练集DCA曲线
plot_dca_curve_train(best_model_IVQ, IVQ_x_tra, IVQ_y_tra, colors_train['IVQ'], 'Level IV Lymph Node Metastasis')

# None线
plt.plot(np.linspace(0, 1, 100), np.zeros(100), 'k-', lw=2, label='None')

# 使用IVQ的数据计算All线
decision_thresholds = np.linspace(0, 1, 100)
all_net_benefits_train = calculate_net_benefit(IVQ_y_tra, np.ones_like(IVQ_y_tra), decision_thresholds)

# 绘制All线
plt.plot(decision_thresholds, all_net_benefits_train, 'gray', linestyle='--', lw=2, label='All Train')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('Threshold Probability', fontsize=12)
plt.ylabel('Net Benefit', fontsize=12)
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
plt.title('DCA for Lymph Node Metastasis Random Forest Prediction (Train Set)', fontsize=14)
plt.legend(loc='upper right', fontsize=10)

# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve_train.tiff', format='tiff', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve_train300.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve_train.eps', format='eps', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve_train300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve_train.png', format='png', dpi=1200)

plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

# 净收益计算函数
def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        n = len(y_true)
        net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        net_benefits.append(net_benefit)
    return net_benefits

# 绘制测试集DCA曲线函数
def plot_dca_curve_test(model, x_test, y_test, color, label):
    decision_thresholds = np.linspace(0, 1, 100)
    y_test_pred_prob = model.predict_proba(x_test)[:, 1]
    net_benefits_test = calculate_net_benefit(y_test, y_test_pred_prob, decision_thresholds)
    plt.plot(decision_thresholds, net_benefits_test, color=color, lw=2, label=label)

# 生成4根线的DCA曲线
plt.figure(figsize=(12, 8))

colors_test = {
    'C': 'gold',
    'IIQ': 'pink',
    'IIIQ': 'skyblue',
    'IVQ': 'lightgreen'
}

# 绘制同侧侧区数据的测试集DCA曲线
plot_dca_curve_test(best_model_C, C_test_features, C_test_target, colors_test['C'], 'Ipsilateral Lateral Lymph Node Metastasis')

# 绘制II区数据的测试集DCA曲线
plot_dca_curve_test(best_model_IIQ, IIQ_x_val, IIQ_y_val, colors_test['IIQ'], 'Level II Lymph Node Metastasis')

# 绘制III区数据的测试集DCA曲线
plot_dca_curve_test(best_model_IIIQ, IIIQ_test_features, IIIQ_test_target, colors_test['IIIQ'], 'Level III Lymph Node Metastasis')

# 绘制IV区数据的测试集DCA曲线
plot_dca_curve_test(best_model_IVQ, IVQ_test_features, IVQ_test_target, colors_test['IVQ'], 'Level IV Lymph Node Metastasis')

# None线
plt.plot(np.linspace(0, 1, 100), np.zeros(100), 'k-', lw=2, label='None')

# 使用IVQ的数据计算All线
decision_thresholds = np.linspace(0, 1, 100)
all_net_benefits_test = calculate_net_benefit(IVQ_test_target, np.ones_like(IVQ_test_target), decision_thresholds)

# 绘制All线
plt.plot(decision_thresholds, all_net_benefits_test, 'gray', linestyle='--', lw=2, label='All Validation')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('Threshold Probability', fontsize=12)
plt.ylabel('Net Benefit', fontsize=12)
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
plt.title('DCA for Lymph Node Metastasis Random Forest Prediction (Validation Set)', fontsize=14)
plt.legend(loc='upper right', fontsize=10)

# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve验证集.tiff', format='tiff', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve验证集300.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve验证.eps', format='eps', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve验证300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve验证.png', format='png', dpi=1200)

plt.show()


# %%
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score

# 净收益计算函数
def calculate_net_benefit(y_true, y_prob, thresholds):
    net_benefits = []
    for thresh in thresholds:
        y_pred = (y_prob >= thresh).astype(int)
        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        n = len(y_true)
        net_benefit = (tp / n) - (fp / n) * (thresh / (1 - thresh))
        net_benefits.append(net_benefit)
    return net_benefits

# 绘制验证集DCA曲线函数
def plot_dca_curve_val(model, x_val, y_val, color, label):
    decision_thresholds = np.linspace(0, 1, 100)
    y_val_pred_prob = model.predict_proba(x_val)[:, 1]
    net_benefits_val = calculate_net_benefit(y_val, y_val_pred_prob, decision_thresholds)
    plt.plot(decision_thresholds, net_benefits_val, color=color, lw=2, label=label)

# 生成4根线的DCA曲线
plt.figure(figsize=(12, 8))

colors_val = {
    'C': 'orange',
    'IIQ': '#C71585',
    'IIIQ': 'blue',
    'IVQ': 'green'
}

# 绘制同侧侧区数据的验证集DCA曲线
plot_dca_curve_val(best_model_C, C_x_val, C_y_val, colors_val['C'], 'Ipsilateral Lateral Lymph Node Metastasis')

# 绘制II区数据的验证集DCA曲线
plot_dca_curve_val(best_model_IIQ, IIQ_test_features, IIQ_test_target, colors_val['IIQ'], 'Level II Lymph Node Metastasis')

# 绘制III区数据的验证集DCA曲线
plot_dca_curve_val(best_model_IIIQ, IIIQ_x_val, IIIQ_y_val, colors_val['IIIQ'], 'Level III Lymph Node Metastasis')

# 绘制IV区数据的验证集DCA曲线
plot_dca_curve_val(best_model_IVQ, IVQ_x_val, IVQ_y_val, colors_val['IVQ'], 'Level IV Lymph Node Metastasis')

# None线
plt.plot(np.linspace(0, 1, 100), np.zeros(100), 'k-', lw=2, label='None')

# 使用IVQ的数据计算All线
decision_thresholds = np.linspace(0, 1, 100)
all_net_benefits_val = calculate_net_benefit(IVQ_y_val, np.ones_like(IVQ_y_val), decision_thresholds)

# 绘制All线
plt.plot(decision_thresholds, all_net_benefits_val, 'gray', linestyle='--', lw=2, label='All Test')

# 设置背景灰色格子线
plt.grid(color='lightgray', linestyle='-', linewidth=1)

plt.xlabel('Threshold Probability', fontsize=12)
plt.ylabel('Net Benefit', fontsize=12)
plt.xlim(0, 0.8)
plt.ylim(-0.1, 0.5)
plt.title('DCA for Lymph Node Metastasis Random Forest Prediction (Test Set)', fontsize=14)
plt.legend(loc='upper right', fontsize=10)

# 保存图像为TIFF格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve测试集.tiff', format='tiff', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve测试集.tiff', format='tiff', dpi=300)
# 保存图像为EPS格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve测试.eps', format='eps', dpi=1200)
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve测试300.eps', format='eps', dpi=300)
# 保存图像为PNG格式
plt.savefig('/Users/zj/Desktop/4.机器学习/1.侧区/文章/JCEM/revised/1.结果/2.PYTHON的结果/5.全部的曲线与r的对比/dca_curve测试.png', format='png', dpi=1200)

plt.show()



