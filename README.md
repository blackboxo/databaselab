## 概述
本项目为复旦大学计算机学院研究生2018秋季期的熊赟老师的高级数据库课程的课程project。

小组成员有：杨健、汪方野、刘名威、陈路路、叶天琦、朱明超、吴斌


## 测试用例

### 插入

INSERT INTO Posts
1. mysql指定主键/mongodb指定_id 将Posts的数据插入一个新表中

1.1 逐条插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_index_separate

1.2 批量插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_index_batch

2. mysql不指定主键/mongodb不指定_id 将Posts的数据插入一个新表中

2.1 逐条插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_separate

2.2 批量插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_batch


### 删除

DELETE * FROM Posts LIMIT num (测10组：num从1万起递增1万，最后一组为10万)
1. mysql指定主键/mongodb指定_id 将Posts的数据删除

1.1 逐条删除(测10组：从limit前1万起递增1万，最后一组前10万) delete_index_separate

1.2 批量删除(测10组：从limit前1万起递增1万，最后一组前10万) delete_index_batch

2. mysql不指定主键/mongodb不指定_id 将Posts的数据删除

2.1 逐条删除(测10组：从limit前1万起递增1万，最后一组前10万) delete_separate

2.2 批量删除(测10组：从limit前1万起递增1万，最后一组前10万) delete_batch

条件删除 删除浏览量小于某个值的所有帖子

DELETE * FROM Posts WHERE ViewCount<num (测10组：num从1万起递增1万，最后一组为10万)

3. mysql指定主键/mongodb指定_id 批量删除 (测10组，值从1万起递增1万，最后一个为10万)  delete_index_filter

4. mysql不指定主键/mongodb不指定_id 批量删除 (测10组，值从1万起递增1万，最后一个为10万) delete_filter


（在经过插入和删除的测试后，可以明显看到使用索引和批量操作使得数据库的性能更好，因此后续的查询和更新测试我们使用索引和批量测试）

### 查询

1.单表单条件查询 match_1-table_1-filter：

根据帖子的id查询某个帖子的信息

SELECT * FROM Posts LIMIT num (测10组：num从1万起递增1万，最后一组为10万)

2.单表多条件查询 match_1-table_multi-filters：

查询某个用户点击量大于1000的所有帖子

SELECT * FROM Posts WHERE OwnerUserId< num (测10组：num从1万起递增1万，最后一组为10万) and ViewCount >1000

索引建立：(OwnerUserId, ViewCount) 

3.多表联合查询 match_multi-tables:

查询用户声誉大于某个值的用户的信息以及其post的基本信息和被喜欢数（探寻用户的声誉和其帖子受欢迎程度的关系）

SELECT Posts. Title, Posts.Tags, Posts. FavoriteCount, Users. DisplayName, Users. Reputation  FROM Posts,

Users WHERE Users.Id = Posts. OwnerUserId and Users. Reputation>num (测10组：num从1万起递增1万，最后一组为10万)

索引建立: Users (Id, Reputation)  Posts(OwnerUserId)外键？

4.聚合查询 match_aggregate：

查询某个用户所有帖子的总被喜欢数：

SELECT SUM(Posts. FavoriteCount), Users. DisplayName, Users. Reputation  FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Users.Id<num (测10组：num从1万起递增1万，最后一组为10万)

索引建立: Posts(OwnerUserId)外键？


### 更新

1.单表单条件更新 update_1-table_1-filter：

用户阅读了某条帖子后，给该条帖子的浏览量+1（如果浏览量为null则设置为1）

UPDATE Posts SET ViewCount= ViewCount+1 WHERE Id<num (测10组：num从1万起递增1万，最后一组为10万)

索引建立:主键

2.单表多条件多值更新 update_1-table_multi-filters：

用户浏览了所有浏览量大于某个值并且分数大于20的帖子，并且喜欢了这个帖子

UPDATE Posts SET ViewCount= ViewCount+1, FavoriteCount=FavoriteCount+1 WHERE Score >20 and ViewCount>num (测10组：num从1万起递增1万，最后一组为10万)

索引建立: ？(Score, ViewCount) （ViewCount, Score）(ViewCount)

3.多表联查单表更新 update_multi-tables_1-update：

给每个浏览量大于某个值的帖子的作者的声望+1

UPDATE Users SET Reputation= Reputation+1 FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Posts. ViewCount >num (测10组：num从1万起递增1万，最后一组为10万)

索引建立:

4.多表联查多表更新 update_multi-tables_multi-updates：

给每个浏览量大于某个值的帖子的浏览量+1，该作者的声望也+1

UPDATE Posts,Users SET Posts.ViewCount= Posts.ViewCount+1, Users.Reputation= Users.Reputation+1 WHERE Users.Id = Posts. OwnerUserId and Posts. ViewCount >num (测10组：num从1万起递增1万，最后一组为10万)

索引建立:


## 测试Tips
为了保证每一份测试结果的准确性和防止波动，我们对每一次测试进行三次取平均值作为最后结果写入表格中。

因此要把数据库的缓存功能给关闭，以防止第一次测试后因为缓存使得后两次测试的速度变快，导致结果不准确。

原始表的Posts数据有3000万条，为了不让增删改影响原始表的内容，我们需要每次操作前都将测试数据导入到新表中。

由于查询和更新等操作涉及到索引的建立和删除，因此每种情况测试前先把索引建好，10组全部测试结束后要记得把索引给删除。

对于每个SQL语句通过explain来分析出建立什么样的索引最能提高效率。

json文件格式为[{type,num,time}{type,num,time},]


## 测试步骤
我们从Stack Overflow上获取到了3000万条数据，将其中部分数据导入我们的测试服务器。

a. 原始表Users和Posts 各100万条，查询测试在该表上进行

b. 插入1/2和删除1/2一起测（写在同一个py文件中）。以插入1.1和删除1.1为例：

（循环开始前）新建表Posts_temp->为该表建Id索引->

（在每个循环中）将Posts的前num条插入Posts_temp，并加入sumtime_insert_index_separate->将Posts_temp的前num条删除，并加入sumtime_delete_index_separate->

（循环3次后）获得time_insert_index_separate和time_delete_index_separate并分别写入json文件

c. 测删除3和4。以删除3为例：

（循环开始前）新建表Posts_temp->为该表建Id索引->

（在每个循环中）将Posts的前100万条？插入Posts_temp->对Posts_temp的进行条件删除，并加入sumtime_delete_index_filter->

（循环3次后）获得time_delete_index_filter并写入json文件

d. 测更新。以更新2为例：

（循环开始前）为Posts表建立对应查询索引（）

（在每个循环中）测UPDATE Posts SET ViewCount= ViewCount+1, FavoriteCount=FavoriteCount+1 WHERE Score >20 and ViewCount>num，并加入sumtime_update_1-table_multi-filters -> 还原表回更新前：UPDATE Posts SET ViewCount= ViewCount-1, FavoriteCount=FavoriteCount-1 WHERE Score >20 and ViewCount>num

（循环3次后）获得time_update_1-table_multi-filters并写入json文件，并删除Posts表对应查询索引（）