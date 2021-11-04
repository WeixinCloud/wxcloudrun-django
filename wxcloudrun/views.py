import json

from django.http import HttpResponse
from django.http import JsonResponse

from wxcloudrun.models import User
from django.forms.models import model_to_dict


def create_or_update(request, _):
    """
    创建或者更新用户

     `` request `` 请求对象
    """

    if request.method == 'POST' or request.method == 'post':
        try:
            res = create(request)
            return res
        except Exception as e:
            resp = {'code': 10000, 'errorMsg': 'create user error: {} '.format(str(e))}
        return HttpResponse(json.dumps(resp), reason='Http Method Error', content_type='application/json')

    if request.method == 'PUT' or request.method == 'put':
        try:
            res = update_by_id(request)
            return res
        except Exception as e:
            return HttpResponse(json.dumps({'code': 10000, 'errorMsg': 'update user error : {} '.format(str(e))}),
                                content_type='application/json')

    resp = {'code': 10000, 'errorMsg': '请求方式错误'}
    return HttpResponse(json.dumps(resp), reason='Http Method Error', content_type='application/json')


def query_or_delete(request, id, _):
    """
    查询或者删除用户

    `` request `` 请求对象
    ``id`` 用户ID
    """
    if request.method == 'DELETE' or request.method == 'delete':
        try:
            res = delete_by_id(request, id)
            return res
        except Exception as e:
            return HttpResponse(json.dumps({'code': 10000, 'errorMsg': 'user not exist'}),
                                content_type='application/json')
    if request.method == 'GET' or request.method == 'get':
        try:
            res = get_user_by_id(request, id)
            return res
        except Exception as e:
            return HttpResponse(json.dumps({'code': 10000, 'errorMsg': 'user not exist'}),
                                content_type='application/json')

    resp = {'code': 10000, 'errorMsg': '请求方式错误'}
    return HttpResponse(json.dumps(resp), reason='Http Method Error', content_type='application/json')


def create(request):
    """
    创建用户

    `` request `` 请求对象
    """

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    baseErrResp = {'code': 10000}

    user = User()
    paramValid = True
    if 'name' not in body:
        baseErrResp['errorMsg'] = '缺少name参数'
        paramValid = False

    if paramValid and 'age' not in body:
        baseErrResp['errorMsg'] = '缺少age参数'
        paramValid = False

    if not paramValid:
        return HttpResponse(json.dumps(baseErrResp), content_type='application/json')

    user.name = body['name']
    user.age = body['age']
    if 'email' in body:
        user.email = body['email']
    if 'phone' in body:
        user.phone = body['phone']
    if 'description' in body:
        user.description = body['description']

    user.save()
    resp = {'code': 0, 'errorMsg': ''}
    return HttpResponse(json.dumps(resp), content_type='application/json')


def get_user_by_id(request, uid):
    """
    根据用户ID查询用户

    `` request `` 请求对象
    ``uid`` 用户ID
    """

    if request.method == 'GET' or request.method == 'get':
        try:
            user = User.objects.get(id=uid)
            if user is None:
                return JsonResponse({'code': 10000, 'data': {}, 'errorMsg': ''})
            return JsonResponse({'code': 0, 'data': model_to_dict(user)})
        except Exception as e:
            return HttpResponse(json.dumps({'code': 10000, 'errorMsg': 'user not exist'}),
                                content_type='application/json')
    else:
        resp = {'code': 10000, 'errorMsg': '请求方式错误'}
        return JsonResponse(data=resp)


def update_by_id(request):
    """
    根据用户ID更新用户

    `` request `` 请求对象
    """

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    baseErrResp = {'code': 10000}
    if 'id' not in body:
        baseErrResp['errorMsg'] = '缺少id参数'
        return JsonResponse(baseErrResp)

    if 'description' not in body and 'name' not in body and 'age' not in body and 'email' not in body and 'phone' not in body:
        baseErrResp['errorMsg'] = '缺少要跟新的目标参数'
        return JsonResponse(baseErrResp)

    user = User.objects.get(id=body['id'])

    if 'description' in body:
        user.description = body['description']
    if 'name' in body:
        user.name = body['name']
    if 'age' in body:
        user.age = body['age']
    if 'email' in body:
        user.email = body['email']
    if 'phone' in body:
        user.phone = body['phone']

    user.save()
    resp = {'code': 0, 'errorMsg': 'OK'}
    return JsonResponse(resp)


def delete_by_id(request, id):
    """
    根据用户ID删除用户

    `` id `` 用户ID
    `` request `` 请求对象
    """

    if request.method == 'DELETE' or request.method == 'delete':
        user = User.objects.get(id=id)
        user.delete()
        resp = {'code': 0, 'errorMsg': '删除成功'}
        return HttpResponse(json.dumps(resp), content_type='application/json')
    else:
        resp = {'code': 10000, 'errorMsg': '请求方式错误'}
        return HttpResponse(json.dumps(resp), reason='Http Method Error',
                            content_type='application/json')
