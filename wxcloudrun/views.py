import json
import traceback

from django.http import JsonResponse
from django.http import HttpResponse
from wxcloudrun.models import ToDoList
from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """
    html_content= '<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"/><link rel=\"icon\" href=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/favicon.ico\"/><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"/><meta name=\"theme-color\" content=\"#000000\"/><meta name=\"description\" content=\"Web site created using create-react-app\"/><link rel=\"apple-touch-icon\" href=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/logo192.png\"/><link rel=\"manifest\" href=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/manifest.json\"/><title>Todo List</title><link href=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/static/css/2.20aa2d7b.chunk.css\" rel=\"stylesheet\"><link href=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/static/css/main.d8680f04.chunk.css\" rel=\"stylesheet\"></head><body><noscript>You need to enable JavaScript to run this app.</noscript><div id=\"root\"></div><script>!function(e){function t(t){for(var n,l,a=t[0],p=t[1],i=t[2],f=0,s=[];f<a.length;f++)l=a[f],Object.prototype.hasOwnProperty.call(o,l)&&o[l]&&s.push(o[l][0]),o[l]=0;for(n in p)Object.prototype.hasOwnProperty.call(p,n)&&(e[n]=p[n]);for(c&&c(t);s.length;)s.shift()();return u.push.apply(u,i||[]),r()}function r(){for(var e,t=0;t<u.length;t++){for(var r=u[t],n=!0,a=1;a<r.length;a++){var p=r[a];0!==o[p]&&(n=!1)}n&&(u.splice(t--,1),e=l(l.s=r[0]))}return e}var n={},o={1:0},u=[];function l(t){if(n[t])return n[t].exports;var r=n[t]={i:t,l:!1,exports:{}};return e[t].call(r.exports,r,r.exports,l),r.l=!0,r.exports}l.m=e,l.c=n,l.d=function(e,t,r){l.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},l.r=function(e){\"undefined\"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:\"Module\"}),Object.defineProperty(e,\"__esModule\",{value:!0})},l.t=function(e,t){if(1&t&&(e=l(e)),8&t)return e;if(4&t&&\"object\"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(l.r(r),Object.defineProperty(r,\"default\",{enumerable:!0,value:e}),2&t&&\"string\"!=typeof e)for(var n in e)l.d(r,n,function(t){return e[t]}.bind(null,n));return r},l.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return l.d(t,\"a\",t),t},l.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},l.p=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/\";var a=this.webpackJsonptodo=this.webpackJsonptodo||[],p=a.push.bind(a);a.push=t,a=a.slice();for(var i=0;i<a.length;i++)t(a[i]);var c=p;r()}([])</script><script src=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/static/js/2.18b41bed.chunk.js\"></script><script src=\"https://cloudbase-run-todolist-92bb28a0d-1258016615.tcloudbaseapp.com/static/js/main.bde3e603.chunk.js\"></script></body></html>'
    return HttpResponse(html_content)


def match_uri_no_id(request, _):
    """
    获取todo list、创建todo、更新todo

     `` request `` 请求对象
    """

    try:
        if request.method == 'GET' or request.method == 'get':
            return get_todo_list(request)
        elif request.method == 'POST' or request.method == 'post':
            return create_todo(request)
        elif request.method == 'PUT' or request.method == 'put':
            return update_todo_by_id(request)
        else:
            return JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                                json_dumps_params={'ensure_ascii': False})
    except ObjectDoesNotExist as e:
        print(traceback.format_exc())
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
