import json
from afcat.api.libs.public import APIView, response_format, Logger
from django.http import JsonResponse, HttpResponse

logger = Logger(__name__)

# Create your views here.


class AdminIndex(APIView):

    def __init__(self, **kwargs):
        super(AdminIndex, self).__init__(**kwargs)
        self.ret = response_format()
        self.ret['data'] = dict()

    def get(self, request, *args, **kwargs):
        method = request.GET.get('method', None) if request.method == 'GET' else request.POST.get("method", None)
        if method is not None:
            method = kwargs.get('method', '')
            if hasattr(self, method[0]):
                func = getattr(self, method[0])
                if callable(func):
                    if method[0] == "edit":
                        return func(request, **kwargs)
                    func(request, **kwargs)
            else:
                self.ret['info'] = "请求方法有误"
                self.ret['category'] = 'error'
        else:
            self.ret['info'] = "请指定请求方法"
            self.ret['category'] = 'info'
        if len(self.ret["data"]) is 0:
            # 只有空列表，前端才能识别是空对象，空字典，前端也会认为对象不为空
            self.ret['data'] = []
        return HttpResponse(json.dumps(self.ret))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def edit(self, request, method, **kwargs):
        api = kwargs.get('api', None)
        if len(method) > 1 and api is not None:
            if method[1] == 'record':
                self.ret = api.edit_record(request)
        else:
            self.ret['info'] = "请求方法有误"
            self.ret['category'] = 'error'
        return self.ret

    def drop(self, request, method, **kwargs):
        """
        删除指定数据
        :param request:
        :param method:drop.records
        :return:
        """
        api = kwargs.get('api', None)
        if len(method) > 1 and api is not None:
            if method[1] == 'records':
                records_id = request.GET.get('records_id', None)
                if type(records_id) is str:
                    try:
                        records_id = json.loads(records_id)
                    except Exception:
                        records_id = []
                        pass
                table_name = request.GET.get('table_name', "")
                self.ret.update(api.delete_records(request, table_name, records_id))
        else:
            self.ret['info'] = "请求方法有误"
            self.ret['category'] = 'error'

    def show(self, request, method, **kwargs):
        """
        列出指定的model或查看model数据
        :param request:
        :param method: show.tables,show.records
        :return:
        """
        api = kwargs.get('api', None)
        if len(method) > 1 and api is not None:
            if method[1] == 'tables':
                models = api.get_tables(request)
                # print(models)
                self.ret['data'].update({"models_list": models})
            if method[1] == 'records':
                table_name = request.GET.get('table_name', "")
                tables_data = api.get_tables_data(request, table_name)
                self.ret['has_next'] = tables_data.pop('has_next') if tables_data.get('has_next', False) else False
                self.ret['has_previous'] = tables_data.pop('has_previous') if tables_data.get(
                    'has_previous', False) else False
                self.ret['data'].update({"tables_data": tables_data, 'table_name': table_name})
        else:
            self.ret['info'] = "请求方法有误"
            self.ret['category'] = 'error'
