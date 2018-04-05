from django.http import HttpResponse
from TestModel.models import Test

# 数据库操作
def testdb(request):
    list1 = Test.objects.all()
    response = ""
    response1 = ""
    for var in list1:
        response1 += var.name + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")