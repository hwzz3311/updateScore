import json

from django.http import QueryDict
from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponse
from django.views.generic import View


# Heavy duty JsonResponse
from updateScore.models import Score

class scoreData(View):
	def get(self,request):
		startIndex = request.GET.get('startIndex')
		endIndex = request.GET.get('endIndex')
		if startIndex and endIndex:
			allScore =Score.objects.all().order_by("-score")[startIndex:endIndex]
		else:
			allScore =Score.objects.all().order_by("-score")
		json_list=[]
		i=1;
		for data in allScore:
			json_dict = {}
			json_dict["score"] = data.score
			json_dict["clientNum"] = data.clientNum
			json_dict["rank"] = i
			i +=1
			json_list.append(json_dict)
		return HttpResponse(json.dumps(json_list), content_type='application/json')

	def post(self,request):
		clientNum = request.POST.get('clientNum','')
		score = request.POST.get('score','')
		try:
			if int(score) >0 and int(score) < 10000000:
				Score.objects.create(clientNum=clientNum,score=int(score))
				return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
			else:
				return HttpResponse('{"status":"fail","msg":"分数错误"}', content_type='application/json')
		except:
			return HttpResponse('{"status":"fail","msg":"分数错误"}', content_type='application/json')

	def put(self,request):
		data=request_body_serialze(request)
		clientNum = data.get("clientNum")  #获取传递参数
		score = data.get("score")  #获取传递参数
		if int(score) >0 and int(score) < 10000000:
			scoreData = Score.objects.filter(clientNum=clientNum)[0]
			if scoreData == None:
				return HttpResponse('{"status":"fail","msg":"客户端不存在"}', content_type='application/json')
			else:
				scoreData.score = score
				scoreData.save()
				return HttpResponse('{"status":"success","msg":"分数更新成功"}', content_type='application/json')
		else:
			return HttpResponse('{"status":"fail","msg":"分数错误"}', content_type='application/json')

def page_not_found(request):
	return HttpResponse("{'state':'404'}", content_type='application/json')

def page_error(request):
	return HttpResponse("{'state':'503'}", content_type='application/json')


def page_prohibit(request):
	return HttpResponse("{'state':'403'}", content_type='application/json')

from django.http.request import QueryDict
# 将put提交的数据转换为dict
def request_body_serialze(request):
	querydict=QueryDict(request.body.decode("utf-8"),encoding="utf-8")
	response_dict={}
	try:
		for key,val in querydict.items():

			response_dict[key]=val
	except:
		pass
	return response_dict