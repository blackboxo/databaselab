## 概述
这个是数据库的测试项目，主要存放MongoDB的测试代码

## 测试用例
### 插入
1. 将tags的数据逐条插入数据库，可以将需要插入的条数放入一个数组[5000,10000,50000],
    输入需测试的次数，取平均时间
    已经实现，实  现脚本,insert_experiment.py
2. 将tags的数据批量插入数据库，可以将需要插入的条数放入一个数组[5000,10000,50000],
    输入需测试的次数，取平均时间
    已经实现，实现脚本,insert_experiment_factory
### 删除
1.  将tags的数据逐条插入数据库，可以将需要插入的条数放入一个数组[5000,10000,50000],
    输入需测试的次数，取平均时间
    已经实现，实现脚本,delete_experiment_factory:
2. 将tags的数据批量插入数据库，可以将需要插入的条数放入一个数组[5000,10000,50000],
    输入需测试的次数，取平均时间
    已经实现，实现脚本,delete_experiment_factory:



## 功能简介
1. collection_factory:
   连接mongodb数据库操作，可以选择返回database或者collection
2. data_factory:
   返回list类型的数据集合，在插入或者删除操作的时候会用到
3. delete（insert）_experiment_factory:
   进行删除插入的操作测试
   
   
   
### 其他实验
todo，待补充
