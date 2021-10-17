import json

from django.http import HttpResponse
from django.http import JsonResponse

from cloudbaserun.models import User
from django.forms.models import model_to_dict


def create_or_update(request):
    if request.method == 'POST' or request.method == 'post':
        return create(request)

    if request.method == 'PUT' or request.method == 'put':
        return update_by_id(request)

    resp = {'errorcode': 405, 'errormsg': '请求方式错误'}
    return HttpResponse(json.dumps(resp), status=405, reason='Http Method Error', content_type='application/json')


def create(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    baseErrResp = {'errorcode': 400}

    user = User()
    paramValid = True
    if 'name' not in body:
        baseErrResp['errormsg'] = '缺少name参数'
        paramValid = False

    if paramValid and 'age' not in body:
        baseErrResp['errormsg'] = '缺少age参数'
        paramValid = False

    if not paramValid:
        return HttpResponse(json.dumps(baseErrResp), status=200, content_type='application/json')

    user.name = body['name']
    user.age = body['age']
    if 'email' in body:
        user.email = body['email']
    if 'phone' in body:
        user.phone = body['phone']
    if 'description' in body:
        user.description = body['description']
    user.save()

    resp = {'errorcode': 200}
    return HttpResponse(json.dumps(resp), status=200, content_type='application/json')


def get_user_by_id(request, uid):
    if request.method == 'GET' or request.method == 'get':
        user = User.objects.get(id=uid)
        if user is None:
            return JsonResponse({'errorcode': 200, 'data': {}})
        return JsonResponse({'errorcode': 200, 'data': model_to_dict(user)})
    else:
        resp = {'errorcode': 405, 'errormsg': '请求方式错误'}
        return JsonResponse(data=resp)


def update_by_id(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    baseErrResp = {'errorcode': 400}
    if 'id' not in body:
        baseErrResp['errormsg'] = '缺少id参数'
        return JsonResponse(baseErrResp)

    if 'description' not in body and 'name' not in body and 'age' not in body and 'email' not in body and 'phone' not in body:
        baseErrResp['errormsg'] = '缺少要跟新的目标参数'
        return JsonResponse(baseErrResp)

    user = User.objects.get(id=body['id'])
    if 'description' in body:
        user.description = body['description']
    if 'name' in body:
        user.name = body['name']
    if 'age' in body:
        user.age = body
    if 'email' in body:
        user.email = body['email']
    if 'phone' in body:
        user.phone = body['phone']
    user.save()

    resp = {'errorcode': 200, 'errormsg': 'OK'}
    return JsonResponse(resp)


def delete_by_id(request, id):
    if request.method == 'DELETE' or request.method == 'delete':
        user = User.objects.get(id=id)
        user.delete()
        resp = {'errorcode': 200, 'errormsg': '删除成功'}
        return HttpResponse(json.dumps(resp), content_type='application/json')
    else:
        resp = {'errorcode': 405, 'errormsg': '请求方式错误'}
        return HttpResponse(json.dumps(resp), status=405, reason='Http Method Error',
                            content_type='application/json')


def query_or_delete(request, id):
    print("=======query_or_delete=======")
    if request.method == 'DELETE' or request.method == 'delete':
        return delete_by_id(request, id)
    if request.method == 'GET' or request.method == 'get':
        return get_user_by_id(request, id)
    resp = {'errorcode': 405, 'errormsg': '请求方式错误'}
    return HttpResponse(json.dumps(resp), status=405, reason='Http Method Error', content_type='application/json')
