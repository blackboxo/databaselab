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
    
3. 有无索引对比：
   db.getCollection('posts').delete_many({'Score':{'$lt': 20},{'ViewCount':{'$lt': 10000}}})
   数量10000~100000,1w递增
   db.getCollection('posts').ensureIndex({"ViewCount":1,"Score":1},{"name":"mongo_index_name"})
   db.runCommand({"dropIndexes":"posts","index":"mongo_index_name"}) 
   
### 查询

1.单表单条件查询 match_1-table_1-filter：

根据帖子的id查询某个帖子的信息

SELECT * FROM Posts LIMIT num (测10组：num从1万起递增1万，最后一组为10万)


2.单表多条件查询 match_1-table_multi-filters：

查询某个用户点击量大于1000的所有帖子

SELECT * FROM Posts WHERE ViewCount >1000 and OwnerUserId< num (测10组：num从1万起递增1万，最后一组为10万) 

额外索引建立: 无


3.多表联合查询 match_multi-tables:

查询用户声誉大于某个值的用户的信息以及其post的基本信息和被喜欢数（探寻用户的声誉和其帖子受欢迎程度的关系）

SELECT Posts. Title, Posts.Tags, Posts. FavoriteCount, Users. DisplayName, Users. Reputation  FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Users. Reputation>num (测10组：num从1万起递增1万，最后一组为10万)

额外索引建立: 无


4.聚合查询 match_aggregate：

查询某个用户所有帖子的总被喜欢数：

SELECT SUM(Posts. FavoriteCount), Users. DisplayName, Users. Reputation  FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Users.Id<num (测10组：num从1万起递增1万，最后一组为10万)

额外索引建立: 无


5.有无索引对比查询 match_index
查询所有浏览量大于某个值并且分数大于20的帖子的标题、分数和浏览量

db.getCollection('posts').find({'Score':{'$gt': 20},{'ViewCount':{'$gt': 10000}}})
数量10000~100000,1w递增
db.getCollection('posts').ensureIndex({"ViewCount":1,"Score":1},{"name":"mongo_index_name"})
db.runCommand({"dropIndexes":"posts","index":"mongo_index_name"}) 

### 更新
1.单表单条件更新 update_batch：

用户表id为1的用户，更新display_name

2.单表多条件多值更新 update_batch_mutiple：

用户表id为1，display_name的用户，更新display_name

3.多表联查单表更新 update_batch_mutiple_query_one_update：

用户表id为1,post表id为1的用户，更新display_name

额外索引建立: 无

4.多表联查多表更新 update_batch_mutiple_query_mutiple_update：

用户表id为1,post表id为1的用户，更新display_name、posts表的1000

额外索引建立: 无   

## 功能简介
1. collection_factory:
   连接mongodb数据库操作，可以选择返回database或者collection
2. data_factory:
   返回list类型的数据集合，在插入或者删除操作的时候会用到
3. delete（insert）_experiment_factory:
   进行删除插入的操作测试
   
   
### 其他实验
todo，待补充
