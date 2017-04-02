# 爬取知乎数据

爬取知乎根话题下精华问题前100条，获得活跃回答者

* Python版本：2.7.13

* 更新时间：2017.04.02

## 原理

### 知乎根话题

知乎的全部话题通过父子关系构成一个有根无循环的有向图。`根话题` 即为所有话题的最上层的父话题。`根话题` 的精华问题即为知乎的 Top1000 高票回答

### 步骤

1. 爬取 `根话题` 下的精华问题，URL为 `https://www.zhihu.com/topic/19776749/top-answers?page=` + `num`，`num` 为页码，并且获得每个问题的 `ID` 

2. 爬取每个问题下的每个回答者，`JSON` API 为 `https://www.zhihu.com/api/v4/questions/28626263/answers?include=data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=`+ `offset` + `&limit=20&sort_by=default`，其中 `offset = 20 * (num - 1) + 3`

3. 爬取每个问题下的每个回答下的评论者，`JSON` API 为 `https://www.zhihu.com/api/v4/answers/41992632/comments?status=open&include=data%5B%2A%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author&limit=10&order=normal&offset=` + `offset`，`offset = 10 * (num - 1)`

4. 将回答者和评论者进行合并，也就是一个问题下的活跃用户的集合。并作为一行存入 `CSV` 文件中，构成一条记录

