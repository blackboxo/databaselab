## 概述
基于Stack Overflow 数据的数据库研究与应用

本项目为复旦大学计算机学院研究生2018秋季期的熊赟老师的高级数据库课程的课程project。

小组成员有：杨健、汪方野、刘名威、陈路路、叶天琦、朱明超、吴斌


## 测试用例

### 插入

INSERT INTO Posts

mysql指定主键/mongodb指定_id 将Posts的数据插入一个新表中

1 逐条插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_id_separate

2 批量插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_id_batch

mysql不指定主键/mongodb不指定_id 将Posts的数据插入一个新表中

3 逐条插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_separate

4 批量插入(测10组：从limit前1万起递增1万，最后一组前10万) insert_batch


### 删除

根据ID删除 DELETE * FROM Posts LIMIT num (测10组：num从1万起递增1万，最后一组为10万)

mysql指定主键/mongodb指定_id 将Posts的数据删除

1 逐条删除 delete_id_separate

2 批量删除 delete_id_batch


3.多条件删除 delete_multi-filters

删除浏览量小于某个值且分数低于20分的所有帖子 

DELETE * FROM Posts WHERE Score<20 and ViewCount<num (测10组：num从1万起递增1万，最后一组为10万) 

额外索引建立: （ViewCount, Score）


（在经过插入和删除的测试后，可以明显看到使用索引和批量操作使得数据库的性能更好，因此后续的查询和更新测试我们使用索引和批量测试）

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

SELECT Posts. Title, Posts.Tags, Posts. FavoriteCount, Users. DisplayName, Users. Reputation  FROM Posts,

Users WHERE Users.Id = Posts. OwnerUserId and Users. Reputation>num (测10组：num从1万起递增1万，最后一组为10万)

额外索引建立: 无

4.聚合查询 match_aggregate：

查询某个用户所有帖子的总被喜欢数：

SELECT SUM(Posts. FavoriteCount), Users. DisplayName, Users. Reputation  FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Users.Id<num (测10组：num从1万起递增1万，最后一组为10万)

额外索引建立: 无


### 更新

1.单表单条件更新 update_1-table_1-filter：

用户阅读了某条帖子后，给该条帖子的浏览量+1（如果浏览量为null则设置为1）

UPDATE Posts SET ViewCount= ViewCount+1 WHERE Id<num (测10组：num从1万起递增1万，最后一组为10万)

2.单表多条件多值更新 update_1-table_multi-filters：

用户浏览了所有浏览量大于某个值并且分数大于20的帖子，并且喜欢了这个帖子

UPDATE Posts SET ViewCount= ViewCount+1, FavoriteCount=FavoriteCount+1 WHERE Score >20 and ViewCount>num (测10组：num从1万起递增1万，最后一组为10万)

额外索引建立: （ViewCount, Score）

3.多表联查单表更新 update_multi-tables_1-update：

给每个浏览量大于某个值的帖子的作者的声望+1

UPDATE Users SET Reputation= Reputation+1 FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Posts. ViewCount >num (测10组：num从1万起递增1万，最后一组为10万)

额外索引建立: 无

4.多表联查多表更新 update_multi-tables_multi-updates：

给每个浏览量大于某个值的帖子的浏览量+1，该作者的声望也+1

UPDATE Posts,Users SET Posts.ViewCount= Posts.ViewCount+1, Users.Reputation= Users.Reputation+1 WHERE Users.Id = Posts. OwnerUserId and Posts. ViewCount >num (测10组：num从1万起递增1万，最后一组为10万)

额外索引建立: 无


## 测试Tips
为了保证每一份测试结果的准确性和防止波动，我们对每一次测试进行三次取平均值作为最后结果写入表格中。

因此要把数据库的缓存功能给关闭，以防止第一次测试后因为缓存使得后两次测试的速度变快，导致结果不准确。

原始表的Posts数据有3000万条，为了不让增删改影响原始表的内容，我们需要每次操作前都将测试数据导入到新表中。

由于查询和更新等操作涉及到索引的建立和删除，因此每种情况测试前先把索引建好，10组全部测试结束后要记得把索引给删除。

对于每个SQL语句通过explain来分析出建立什么样的索引最能提高效率。

json文件格式为[{type,num,time},{type,num,time}]


## 测试步骤
我们从Stack Overflow上获取到了3000万条数据，将其中部分数据导入我们的测试服务器。

需要写一个总的执行程序，运行以后就可以将这四个文件都测试一遍。

a. match.py 原始表Users和Posts 各100万条，查询测试在该表上进行

b. insert_delete.py 插入1/2和删除1/2一起测（写在同一个py文件中）。以插入1和删除1为例：

（循环开始前）新建表Posts_temp ->

（在每个循环中）将Posts的前num条逐条插入Posts_temp（令主键值等于原始表Id的值），并加入sumtime_insert_id_separate -> 将Posts_temp的前num条删除，并加入sumtime_delete_id_separate ->

（循环3次后）获得time_insert_id_separate和time_id_separate并分别写入json文件

c. insert_delete.py 测插入3和4。以插入4为例：

（在每个循环中）将Posts的前num条批量插入Posts_temp（让数据库自动生成主键的值），并加入sumtime_insert_batch -> 执行还原：DELETE * FROM Posts_temp ->

（循环3次后）获得time_insert_batch写入json文件

d. delete_filter.py 测删除3。

（循环开始前）将Posts表复制得到三张表Posts_delete_1,Posts_delete_2,Posts_delete_3,为这三张表建立对应查询索引（ViewCount, Score）->

（在每个循环中）对表Posts_delete_（循环次数）的数据进行条件删除，并加入sumtime_delete_multi-filters ->

（循环3次后）获得time_delete_multi-filters并写入json文件

e. update.py 测更新。以更新2为例：

（循环开始前）为Posts表建立对应查询索引（ViewCount, Score）

（在每个循环中）测UPDATE Posts SET ViewCount= ViewCount+1, FavoriteCount=FavoriteCount+1 WHERE Score >20 and ViewCount>num，并加入sumtime_update_1-table_multi-filters -> 还原表回更新前：UPDATE Posts SET ViewCount= ViewCount-1, FavoriteCount=FavoriteCount-1 WHERE Score >20 and ViewCount>num ->

（循环3次后）获得time_update_1-table_multi-filters并写入json文件