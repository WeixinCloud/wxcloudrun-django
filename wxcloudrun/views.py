import json

from django.http import HttpResponse
from django.http import JsonResponse

from wxcloudrun.models import ToDoList
from django.forms.models import model_to_dict


def match_uri_no_id(request, _):
    """
    获取todo list、创建todo、更新todo

     `` request `` 请求对象
    """

    if request.method == 'GET' or request.method == 'get':
        try:
            res = get_todo_list(request)
            return res
        except Exception as e:
            return HttpResponse(json.dumps({'code': -1, 'errorMsg': 'get todo list error'}),
                                content_type='application/json')
    
    elif request.method == 'POST' or request.method == 'post':
        try:
            res = create_todo(request)
            return res
        except Exception as e:
            resp = {'code': -1, 'errorMsg': 'create todo error: {} '.format(str(e))}
        return HttpResponse(json.dumps(resp), reason='Http Method Error', content_type='application/json')

    elif request.method == 'PUT' or request.method == 'put':
        try:
            res = update_todo_by_id(request)
            return res
        except Exception as e:
            return HttpResponse(json.dumps({'code': -1, 'errorMsg': 'update todo error : {} '.format(str(e))}),
                                content_type='application/json')

    resp = {'code': -1, 'errorMsg': '请求方式错误'}
    return HttpResponse(json.dumps(resp), reason='Http Method Error', content_type='application/json')


def match_uri_with_id(request, id, _):
    """
    查询或者删除todo

    `` request `` 请求对象
    ``id`` todoID
    """
    if request.method == 'DELETE' or request.method == 'delete':
        try:
            res = delete_todo_by_id(request, id)
            return res
        except Exception as e:
            return HttpResponse(json.dumps({'code': 0, 'errorMsg': 'todo not exist'}),
                                content_type='application/json')
    elif request.method == 'GET' or request.method == 'get':
        try:
            res = get_todo_by_id(request, id)
            return res
        except Exception as e:
            return HttpResponse(json.dumps({'code': -1, 'errorMsg': 'todo not exist'}),
                                content_type='application/json')

    resp = {'code': -1, 'errorMsg': '请求方式错误'}
    return HttpResponse(json.dumps(resp), reason='Http Method Error', content_type='application/json')

def get_todo_list(request):
    """
    获取所有todo list

    `` request `` 请求对象
    """

    if request.method == 'GET' or request.method == 'get':
        try:
            todo_list = ToDoList.objects.all()
            if todo_list is None:
                return JsonResponse({'code': 0, 'data': {}, 'errorMsg': 'todo list null'})

            data = []
            for todo in todo_list:
                context = model_to_dict(todo)
                data.append(context)

            return JsonResponse({'code': 0, 'data': data}, json_dumps_params={'ensure_ascii':False})
        except Exception as e:
            return HttpResponse(json.dumps({'code': -1, 'errorMsg': 'get todo list error'}),
                                content_type='application/json')
    else:
        resp = {'code': -1, 'errorMsg': '请求方式错误'}
        return JsonResponse(data=resp)

def create_todo(request):
    """
    创建todo

    `` request `` 请求对象
    """

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    baseErrResp = {'code': -1}

    todo = ToDoList()
    paramValid = True
    if 'title' not in body:
        baseErrResp['errorMsg'] = '缺少title参数'
        paramValid = False

    if paramValid and 'status' not in body:
        baseErrResp['errorMsg'] = '缺少status参数'
        paramValid = False

    if not paramValid:
        return HttpResponse(json.dumps(baseErrResp), content_type='application/json')

    todo.title = body['title']
    todo.status = body['status']

    todo.save()
    resp = {'code': 0, 'errorMsg': ''}
    return HttpResponse(json.dumps(resp), content_type='application/json')


def get_todo_by_id(request, uid):
    """
    根据todoID查询todo

    `` request `` 请求对象
    ``uid`` todoID
    """

    if request.method == 'GET' or request.method == 'get':
        try:
            todo = ToDoList.objects.get(id=uid)
            if todo is None:
                return JsonResponse({'code': -1, 'data': {}, 'errorMsg': ''})
            return JsonResponse({'code': 0, 'data': model_to_dict(todo)}, json_dumps_params={'ensure_ascii':False})
        except Exception as e:
            return HttpResponse(json.dumps({'code': -1, 'errorMsg': 'todo not exist'}),
                                content_type='application/json')
    else:
        resp = {'code': -1, 'errorMsg': '请求方式错误'}
        return JsonResponse(data=resp)


def update_todo_by_id(request):
    """
    根据todoID更新todo

    `` request `` 请求对象
    """

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    baseErrResp = {'code': -1}
    if 'id' not in body:
        baseErrResp['errorMsg'] = '缺少id参数'
        return JsonResponse(baseErrResp)

    if 'title' not in body and 'status' not in body:
        baseErrResp['errorMsg'] = '缺少要更新的目标参数'
        return JsonResponse(baseErrResp)

    todo = ToDoList.objects.get(id=body['id'])

    if 'title' in body:
        todo.title = body['title']
    if 'status' in body:
        todo.status = body['status']

    todo.save()
    resp = {'code': 0, 'errorMsg': 'OK'}
    return JsonResponse(resp)


def delete_todo_by_id(request, id):
    """
    根据todoID删除todo

    `` id `` todoID
    `` request `` 请求对象
    """

    if request.method == 'DELETE' or request.method == 'delete':
        todo = ToDoList.objects.get(id=id)
        todo.delete()
        resp = {'code': 0, 'errorMsg': '删除成功'}
        return HttpResponse(json.dumps(resp), content_type='application/json')
    else:
        resp = {'code': -1, 'errorMsg': '请求方式错误'}
        return HttpResponse(json.dumps(resp), reason='Http Method Error',
                            content_type='application/json')
