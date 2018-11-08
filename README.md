## 概述
本项目为复旦大学计算机学院研究生2018秋季期的熊赟老师的高级数据库课程的课程project。
小组成员有：杨健、汪方野、刘名威、陈路路、叶天琦、朱明超、吴斌


## 测试用例

### 插入

INSERT INTO Posts
1. mysql指定主键/mongodb指定_id 将Posts的数据插入一个新表中
1.1 逐条插入(测10组：从limit前1万起递增1万，最后一组前10万)
1.2 批量插入(测10组：从limit前1万起递增1万，最后一组前10万)
2. mysql不指定主键/mongodb不指定_id 将Posts的数据插入一个新表中
2.1 逐条插入(测10组：从limit前1万起递增1万，最后一组前10万)
2.2 批量插入(测10组：从limit前1万起递增1万，最后一组前10万)


### 删除

DELETE * FROM Posts LIMIT ?
1. mysql指定主键/mongodb指定_id 将Posts的数据删除

1.1 逐条删除(测10组：从limit前1万起递增1万，最后一组前10万)

1.2 批量删除(测10组：从limit前1万起递增1万，最后一组前10万)

2. mysql不指定主键/mongodb不指定_id 将Posts的数据删除

2.1 逐条删除(测10组：从limit前1万起递增1万，最后一组前10万)

2.2 批量删除(测10组：从limit前1万起递增1万，最后一组前10万)

条件删除 DELETE * FROM Posts WHERE 

3. mysql指定主键/mongodb指定_id 批量删除 将post的数据逐条从数据库删除，比如总共删除10000条

4. mysql不指定主键/mongodb不指定_id 批量删除 


（在经过插入和删除的测试后，可以明显看到使用索引和批量操作使得数据库的性能更好，因此后续的查询和更新测试我们使用索引和批量测试）

### 查询

1.单表单条件查询：

根据帖子的id查询某个帖子的信息

SELECT * FROM Posts LIMIT ? (测10组：从limit前1万起递增1万，最后一组前10万)

2.单表多条件查询：

查询某个用户点击量大于1000的所有帖子

SELECT * FROM Posts WHERE OwnerUserId= ? (测10组：从limit前1万起递增1万，最后一组前10万) and ViewCount >1000

索引建立：(OwnerUserId, ViewCount) 

3.多表联合查询:

查询用户声誉大于某个值的用户的信息以及其post的基本信息和被喜欢数（探寻用户的声誉和其帖子受欢迎程度的关系）

SELECT Posts. Title, Posts.Tags, Posts. FavoriteCount, Users. DisplayName, Users. Reputation  FROM Posts,

Users WHERE Users.Id = Posts. OwnerUserId and Users. Reputation>? (测10个，值从1万起递增1万，最后一个为10万)

索引建立: Users (Id, Reputation)  Posts(OwnerUserId)外键？

4.聚合查询：

查询某个用户所有帖子的总被喜欢数：

SELECT SUM(Posts. FavoriteCount), Users. DisplayName, Users. Reputation  FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Users.Id=? (测10组：从limit前1万起递增1万，最后一组前10万)

索引建立: Posts(OwnerUserId)外键？


### 更新

1.单表单条件更新：

用户阅读了某条帖子后，给该条帖子的浏览量+1（如果浏览量为null则设置为1）

UPDATE Posts SET ViewCount= ViewCount+1 WHERE Id= ? (测10组：从limit前1万起递增1万，最后一组前10万)

索引建立:主键

2.单表多条件多值更新：

用户浏览了所有浏览量大于某个值并且分数大于20的帖子，并且喜欢了这个帖子

UPDATE Posts SET ViewCount= ViewCount+1, FavoriteCount=FavoriteCount+1 WHERE Score >20 and ViewCount>? (测10个，值从1万起递增1万，最后一个为10万)

索引建立: ？(Score, ViewCount) （ViewCount, Score）(ViewCount)

3.多表联查单表更新：

给每个浏览量大于某个值的帖子的作者的声望+1

UPDATE Users SET Reputation= Reputation+1 FROM Posts,Users WHERE Users.Id = Posts. OwnerUserId and Posts. ViewCount >?(测10个，值从1万起递增1万，最后一个为10万)

索引建立:

4.多表联查多表更新：

给每个浏览量大于某个值的帖子的浏览量+1，该作者的声望也+1

UPDATE Posts,Users SET Posts.ViewCount= Posts.ViewCount+1, Users.Reputation= Users.Reputation+1 WHERE Users.Id = Posts. OwnerUserId and Posts. ViewCount >?(测10个，值从1万起递增1万，最后一个为10万)

索引建立:


## 测试步骤
为了保证每一份测试结果的准确性和防止波动，我们对每一次测试进行三次取平均值作为最后结果写入表格中。

因此要把数据库的缓存功能给关闭，以防止第一次测试后因为缓存使得后两次测试的速度变快，导致结果不准确。

原始表的Posts数据有3000万条，为了不让增删改影响原始表的内容，我们需要每次操作前都将测试数据导入到新表中。

可以先做插入1/2，再接着做删除1/2
