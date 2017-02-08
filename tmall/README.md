# 爬取天猫商品评论数据

爬虫日常~~，尝试爬取天猫的数据

* Python版本：2.7.3

* 更新时间：2017.02.08

* 使用：运行提示输入要爬取的评论页数，在本地会自动创建一个csv文件，能用Excel直接查看

* 爬取原理：通过观察，天猫的商品数据都是动态加载的，存储在一个名为 `https://rate.tmall.com/list_detail_rate.htm?itemId=537734028319&spuId=696624585&sellerId=197232874&order=3&currentPage=` 这么一个JS文件中。所以通过爬取这样的文件并改变 `currentPage=` 的值来实现评论爬取
