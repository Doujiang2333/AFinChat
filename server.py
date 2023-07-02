from functools import wraps
from scarpy_for_eastmoney import get_eastmoney_news
from quart import jsonify, render_template
import baostock as bs
import json
import asyncio
import quart
import quart_cors
import httpx

# 调用Openai的API需要境外网络环境，请根据实际情况设置代理
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

app = quart_cors.cors(quart.Quart(__name__))

@app.get("/logo.png")
async def plugin_logo():
    filename = './logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json", encoding='utf-8') as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    with open("./openapi.yaml", encoding='utf-8') as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")
    
def retry_on_exception(max_retries=3, delay=10):
    """装饰器，用于在函数抛出异常时进行重试"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}. Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
            raise Exception(f"Failed after {max_retries} retries")
        return wrapper
    return decorator

@retry_on_exception(max_retries=3, delay=10)
@app.get("/news/<string:keywords>")
async def websearch_for_news(keywords):
    news = await get_eastmoney_news(keywords)
    return json.dumps(news)

@retry_on_exception(max_retries=3, delay=5)
@app.get("/financialstatement/<string:stockcode>/<string:company_type>/<string:report_type>/<string:report_date>")
async def get_financestatement(stockcode, company_type, report_type, report_date):
    url = f"http://www.cninfo.com.cn/data20/financialData/get{report_type}?scode={stockcode}&sign={company_type}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    res = response.json()
    data = res.get('data', {}).get('records', [{}])[0]
    if report_date in data:
        return jsonify(data[report_date])
    else:
        return jsonify({"error": "No data for the given report date"}), 404

@retry_on_exception(max_retries=3, delay=5)
@app.get("/stockquotes/<string:stockcode>/<string:adjustflag>/<string:start_date>/<string:end_date>/<string:freq>")
async def get_stockquotes(stockcode, adjustflag, start_date, end_date, freq):
    bs.login()
    if stockcode[:1] == '6':
        stockcode_long = 'sh.' + stockcode
    else:
        stockcode_long = 'sz.' + stockcode
    loop = asyncio.get_event_loop()
    rs = await loop.run_in_executor(None, bs.query_history_k_data_plus, stockcode_long,
        "date,close,volume,amount,adjustflag",
        start_date, end_date, freq, adjustflag)
    bs.logout()
    res = rs.get_data().set_index('date').to_dict()
    return jsonify(res)

@retry_on_exception(max_retries=3, delay=5)
@app.route('/legal-info')
def legal_info():
    return render_template('legal_info.html')
                              
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5023)