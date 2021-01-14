from django.shortcuts import render
import pandas as pd
from sqlalchemy import create_engine
from django.http.response import StreamingHttpResponse
from django.http.response import HttpResponse
from io import BytesIO
from spider.app_spider.CombineSpider import CombineSpider

# Create your views here.
def crawl(request):
    keyword = request.GET.get("keyword")
    print(keyword)
    CombineSpider.crawl(keyword)
    engine = create_engine('mysql+pymysql://root:shuziguanxing123456@192.168.50.60:3306/app_info')
    app_info = pd.read_sql_table('spider_app', engine)
    x_io = BytesIO()
    app_info.to_excel(x_io, sheet_name="app_info", index=False)
    response = HttpResponse()
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="app_info.xlsx"'
    response.write(x_io.getvalue())
    return response
    # return render(request, "index.html")


def orgin(request):
    return render(request, "index.html")