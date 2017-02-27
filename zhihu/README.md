# 模拟登录知乎

知乎必爬，先从如何解决登录验证开始

* Python版本：2.7.3

* 更新时间：2017.02.25

* **后续：哈哈\(^o^)/~，关注人的API链接终于找到了！**

## 原理

* 关注人获取：通过观察，关注人第一页的API为`https://www.zhihu.com/api/v4/members/mnichangxin/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20`，第二页为`https://www.zhihu.com/api/v4/members/mnichangxin/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20`，第三页为`https://www.zhihu.com/api/v4/members/mnichangxin/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=40&limit=20`。由此可见，不难得出链接中的`offset`和页数（page）的关系 => `offset = (page - 1) * 20`。有了这个关系之后，关注人列表就好爬了。

* 关注话题获取：同理以上，API为：`https://www.zhihu.com/api/v4/members/mnichangxin/following-topic-contributions?include=data%5B*%5D.topic.introduction&offset=' + offset + '&limit=20`

* 关注问题获取：同理以上，API为：`https://www.zhihu.com/api/v4/members/mnichangxin/following-questions?include=data%5B*%5D.created%2Canswer_count%2Cfollower_count%2Cauthor&offset=' + offset + '&limit=20`

## 大致流程

1. 获得关注人 => 遍历关注人列表
2. 访问关注人主页 => 获得关注话题和关注问题
