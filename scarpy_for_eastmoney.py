import urllib.parse
import json
import requests
import httpx

def get_eastmoney_url(stock_name):
    '''根据股票名称和页数获得url'''
    base_url = 'https://search-api-web.eastmoney.com/search/jsonp'
    payload = {
        "cb": "jQuery35109996067915300615_1688032629703",
        "param": {
            "uid": "",
            "keyword": stock_name,
            "type": ["cmsArticleWebOld"],
            "client": "web",
            "clientType": "web",
            "clientVersion": "curr",
            "param": {
                "cmsArticleWebOld": {
                    "searchScope": "default",
                    "sort": "default",
                    "pageIndex": 1,
                    "pageSize": 10,
                    "preTag": "<em>",
                    "postTag": "</em>"
                }
            }
        },
        "_": "1688032629704"
    }
    # 修改payload中的值
    payload["param"]["keyword"] = stock_name
    # 将payload转换为URL参数
    payload_str = json.dumps(payload["param"])
    payload["param"] = payload_str
    encoded_params = urllib.parse.urlencode(payload, doseq=True)
    # 构造新的URL
    new_url = f"{base_url}?{encoded_params}"
    return new_url

async def get_eastmoney_news(stock_name):
    '''根据url获取页面信息'''
    url = get_eastmoney_url(stock_name)
    em_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" }
    
    async with httpx.AsyncClient() as client:
        r0 = await client.get(url, headers=em_headers)
        
    response = r0.text
    json_data = response[response.index('(') + 1 : response.rindex(')')]
    data = json.loads(json_data)
    articles = data['result']['cmsArticleWebOld']
    news_lst = []
    for article in articles[:-2]:
        title = article['title'].replace('</em>','').replace('<em>','')
        date = article['date'].replace('</em>', '').replace('<em>','')
        abstract = article['content'].replace('</em>', '').replace('<em>','')
        source = article['url']
        media_name = article['mediaName'].replace('</em>', '').replace('<em>','')
        news_dict = {
            "title": title,
            "abstract": abstract,
            "source": source,
            "media_name": media_name,
            "date": date
    }
        news_lst.append(news_dict)
    return news_lst