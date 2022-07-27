# ETL README

1. 对出现次数小于 10000 次的属性进行删除。
2. 将属性名全部转为小写，空格使用下划线填充。
3. directors 和 director 没有在同一部电影中同时出现，合并成属性 directors。
4. dvd_release_date 和 vhs_release_date 同样没有在同一部电影中同时出现，合并成属性 date。但不同的 date 名字中还包含了信息，代表了不同的电影载体，是 DVD 还是 VHS，所以添加一个属性 supporter。
5. date 里其实包含了 year 属性的信息以及额外的月份和日期三种信息。所以，将 date 属性进行拆分，拆分成 year，month，day 三个属性。同时，将月份由英文转化为数字。