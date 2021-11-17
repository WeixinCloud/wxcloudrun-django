import json
import traceback
import logging

from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from wxcloudrun.models import ToDoList
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger('log')

def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def match_uri_no_id(request, _):
    """
    获取todo list、创建todo、更新todo

     `` request `` 请求对象
    """

    try:
        rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
        if request.method == 'GET' or request.method == 'get':
            rsp = get_todo_list(request)
        elif request.method == 'POST' or request.method == 'post':
            rsp = create_todo(request)
        elif request.method == 'PUT' or request.method == 'put':
            rsp = update_todo_by_id(request)
        else:
            rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                                json_dumps_params={'ensure_ascii': False})
        logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
        return rsp
    except ObjectDoesNotExist as e:
        logger.info('exception stack: {}'.format(traceback.format_exc()))
        return JsonResponse({'code': -1, 'errorMsg': '请求异常: {} '.format(str(e))},
                            json_dumps_params={'ensure_ascii': False})



def match_uri_with_id(request, id, _):
    """
    查询或者删除todo

    `` request `` 请求对象
    ``id`` todoID
    """
    try:
        if request.method == 'DELETE' or request.method == 'delete':
            return delete_todo_by_id(request, id)
        elif request.method == 'GET' or request.method == 'get':
            return get_todo_by_id(request, id)
        else:
            return JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                                json_dumps_params={'ensure_ascii': False})
    except ObjectDoesNotExist as e:
        print(traceback.format_exc())
        return JsonResponse({'code': -1, 'errorMsg': '请求异常: {} '.format(str(e))},
                            json_dumps_params={'ensure_ascii': False})


def get_todo_list(request):
    """
    获取所有todo list

    `` request `` 请求对象
    """

    todo_list = ToDoList.objects.all()
    if todo_list is None:
        return JsonResponse({'code': 0, 'data': {}, 'errorMsg': 'todo list空'},
                            json_dumps_params={'ensure_ascii': False})

    data = []
    for todo in todo_list:
        context = model_to_dict(todo)
        data.append(context)
    return JsonResponse({'code': 0, 'data': data},
                        json_dumps_params={'ensure_ascii': False})


def create_todo(request):
    """
    创建todo

    `` request `` 请求对象
    """

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    base_err_resp = {'code': -1}

    todo = ToDoList()
    param_valid = True
    if 'title' not in body:
        base_err_resp['errorMsg'] = '缺少title参数'
        param_valid = False

    if param_valid and 'status' not in body:
        base_err_resp['errorMsg'] = '缺少status参数'
        param_valid = False

    if not param_valid:
        return JsonResponse(base_err_resp,
                            json_dumps_params={'ensure_ascii': False})

    todo.title = body['title']
    todo.status = body['status']

    todo = ToDoList.objects.create(title=body['title'], status=body['status'])
    return JsonResponse({'code': 0, "data": model_to_dict(todo), 'errorMsg': '创建成功'},
                        json_dumps_params={'ensure_ascii': False})


def get_todo_by_id(request, uid):
    """
    根据todoID查询todo

    `` request `` 请求对象
    ``uid`` todoID
    """

    todo = ToDoList.objects.get(id=uid)
    if todo is None:
        return JsonResponse({'code': 0, 'data': {}, 'errorMsg': 'todo不存在'},
                            json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': model_to_dict(todo)},
                        json_dumps_params={'ensure_ascii': False})


def update_todo_by_id(request):
    """
    根据todoID更新todo

    `` request `` 请求对象
    """

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    base_err_resp = {'code': -1}
    if 'id' not in body:
        base_err_resp['errorMsg'] = '缺少id参数'
        return JsonResponse(base_err_resp, json_dumps_params={'ensure_ascii': False})

    if 'title' not in body and 'status' not in body:
        base_err_resp['errorMsg'] = '缺少要更新的目标参数'
        return JsonResponse(base_err_resp, json_dumps_params={'ensure_ascii': False})

    todo = ToDoList.objects.get(id=body['id'])

    if 'title' in body:
        todo.title = body['title']
    if 'status' in body:
        todo.status = body['status']

    todo.save()
    return JsonResponse({'code': 0, 'errorMsg': '更新成功'},
                        json_dumps_params={'ensure_ascii': False})


def delete_todo_by_id(request, id):
    """
    根据todoID删除todo

    `` id `` todoID
    `` request `` 请求对象
    """

    todo = ToDoList.objects.get(id=id)
    todo.delete()
    return JsonResponse({'code': 0, 'errorMsg': '删除成功'},
                        json_dumps_params={'ensure_ascii': False})
