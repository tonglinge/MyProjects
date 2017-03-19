from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.http.response import HttpResponse
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from afcat.cmdb.libs import server, equipment
from afcat.cmdb.libs import base, excel
from afcat.cmdb.libs.common import save_file_for_upload, response_json, get_model, response_error, get_request_data
from afcat.api.libs.public import BaseView, Logger, response_format
from afcat.account.core.permission import permission_require
import os
logger = Logger(__name__)


class AdminIndex(BaseView):
    def get(self, request, *args, **kwargs):
        logger.info('', request=request)
        return render(request, 'cmdb/admin_index.html')

    def post(self, request, *args, **kwargs):
        logger.info('', request=request)
        return self.get(request, *args, **kwargs)


class Index(BaseView):
    def get(self, request, *args, **kwargs):
        logger.info('', request=request)
        return render(request, 'cmdb/cmdb_index_2.html')


@login_required(login_url="login")
def get_page_templates(request, template_name="cmdb/notfound.html"):
    """
    获取模板名称
    :param template_name: 模板名称
    :return: 无渲染，返回模板文件
    """
    try:
        params = request.GET
        template_file = "cmdb/%s.html" % template_name

        return render(request, template_file, {"param": params, "cmdb_asset": "active"})
    except Exception as e:
        logger.error("%s" % e, request)
        return render(request, "cmdb/notfound.html", {"param": None})


@login_required(login_url="login")
@permission_require("view_list")
def get_asset_list(request, perm_id_list=None):
    """
    获取所有资产基本信息, 包括: 服务器资产(server)/设备资产(equipment)/项目联系列表(projects/,需要接收一个参数model
    :param perm_id_list: 允许访问的资产ID
    :param request: {"page":2,"model":"equipment","condition":""}
    :return:返回json格式串
    """
    if request.method == "GET":
        try:
            get_param = get_request_data(request)
            page_index = get_param.get("page", 1)
            per_page_count = get_param.get("per_count", None)
            conditions = get_param.get("condition", "")
            asset_type = get_param.get("model")
            # 在当前条件中追加当前操作客户ID
            custid = request.session.get("custid")
            # 反射动态加载模块
            asset_obj = get_model(asset_type)
            if not asset_obj:  # 未找到模块
                return response_json("")
            server_info_list = asset_obj.get_asset_list(page_index, conditions, custid, perm_id_list)
            return response_json(server_info_list)
        except Exception as e:
            logger.error("%s" % e, request)
            return response_error("parm error", request)


@login_required(login_url="login")
# @permission_require("view_detail")
def get_asset_detail(request):
    """
    获取指定资产的详细信息,包括: server / equipment
    :param request:需要一个资产的ID号
    :return: 返回指定资产下的所有关联信息
    {'data':{'server':{},'cpu':{},'storageinfo':{},'ip':{},'staff':{},'nic':{},
                                        'storagecard':{},'software':{} }}
    """
    if request.method == "GET":
        # get_param = json.loads(request.GET["data"])
        get_param = get_request_data(request)
        server_id = get_param.get("sid", 0)
        asset_type = get_param.get("model")
        # 反射获取指定的资产类型模块,server/equipment
        asset_model = get_model(asset_type)
        if not asset_model:
            return response_json("")
        try:
            sid = int(server_id)
        except Exception as e:
            logger.error("%s" % e, request)
            sid = 0
        server_detail = asset_model.get_asset_details(sid)
        return response_json(server_detail)


@login_required(login_url="login")
@permission_require("change_get")
def asset_modify(request):
    """
    post:添加或更新资产信息
    get: 获取加载添加或编辑页面时的所有信息
    :param request: {"action":"","sid":0,"model":"server"}
    :return: 成功返回True, 否则返回False
    """
    result = response_format()
    try:
        request_data = get_request_data(request)
        # 获取要执行的模块
        model_obj = get_model(request_data.get("model"))
        if not model_obj:
            result["info"] = "未找到指定的模块"
            result["category"] = "error"
            result["status"] = False
            return response_json(result)

        if request.method == "GET":
            # 获取修改时所依赖的所有基表数据
            base_table_info = model_obj.load_related_base_configuration(request_data.get("custid"))
            #  如果是编辑则再加上资产的信息
            # if get_param.get("action", "new") == "edit":
            try:
                server_id = int(request_data.get("sid", 0))
                if server_id > 0:
                    # 编辑获取主机的所有信息
                    server_info = {"asset_info": model_obj.get_asset_base_info(server_id)}
                    base_table_info.update(server_info)
            except ValueError as e:
                logger.error("%s" % e, request)
                pass
            result["data"] = base_table_info
            return response_json(result)

        if request.method == "POST":
            result = model_obj.edit_asset(request_data)

            return response_json(result)
    except Exception as e:
        logger.error("%s" % e, request)
        result["info"] = "编辑资产信息失败!"
        result["category"] = "error"
        result["status"] = False
        return response_json(result)


def load_base_data(request):
    """
    获取基表数据信息
    :param request: 要获取的基表数据的表名列表
    :return: 结果字典的json格式
    """
    result = response_format()
    get_param = get_request_data(request)
    custid = request.session.get("custid")
    if request.method == "GET":
        try:
            tables = get_param.get("tables", [])
            data = base.get_base_data(custid, tables)
        except ValueError as e:
            logger.error("%s" % e, request)
            data = {}
            result["info"] = "获取数据失败"
            result["status"] = False
        result["data"] = data
        return response_json(result)

    if request.method == "POST":
        '''
        添加、更新表数据,传入的参数包括{'table': modelname, 'values':{}, 'action':'new/edit'}
        '''
        try:
            table = get_param.get("table", "")
            if get_param.get("action", "") not in ["new", "edit", "delete", "del"]:
                return response_error("参数错误", request)
            else:
                result = base.post_base_data(get_param)
                return response_json(result)
        except Exception as e:
            logger.error("%s" % e, request)
            return response_error("修改失败", request)


@require_POST
def post_servers_related_asset(request):
    """
    所有服务器资产、设备资产关联的资产或配置信息(添加,删除,修改)数据提交到此,如: cpu信息,网卡信息,ip信息,联系人  等
    :param request:
    :return:
    """
    post_data = get_request_data(request)
    action = post_data.get("action")
    if not action in ["new", "edit", "del"] or not post_data:
        return response_error("参数错误", request)
    else:
        # result = server.save_servers_related_asset(action, post_data, request.user)
        result = server.save_servers_related_asset(post_data)
        return response_json(result)


def report_excel(request):
    """
    导出excel文件
    :param request: 请求包括{"model":"server/equipment","key":"ip/sys","value":""}
    :return:
    """
    from datetime import datetime

    if request.method == "GET":
        try:
            print(request.GET)
            model_name = request.GET.get("model", "")
            custid = request.session.get("custid")
            model_obj = get_model(model_name)
            excel_file = model_obj.export_excel(custid, **request.GET)
            response = HttpResponse(excel_file,
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=%s_%s.xlsx" % (
                model_name, datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
            return response
        except Exception as e:
            logger.error("%s" % e, request)
            return response_error("参数错误", request)


@require_GET
def staffs_list(request):
    """
    添加、修改、删除联系人信息
    :param request:
    :return:
    """
    request_data = get_request_data(request)
    result = base.get_staffs_list(request_data)
    return response_json(result)


@require_POST
def post_equipment_boardcard(request):
    """
    添加,编辑,删除网络设备板卡信息
    :param request: {"action":"new", "value":{"equipment_id":10011,"sn":"sn02938485","cardname":"card0","slot":"a01",
                    "remark":"xxxx","ports":"1,2,3,4,5,6"} }
    :return:成功或失败信息
    """
    post_data = get_request_data(request)
    op_type = int(post_data.get("optype", 0))
    if op_type == 1:
        # 修改板卡信息
        result = equipment.post_boardcard(post_data, request.user)
    if op_type == 2:
        # 修改端口信息
        result = equipment.post_boardport(post_data)
    return response_json(result)


def server_boardcard(request):
    """
    POST: 添加、修改、删除主机板卡信息
    GET: 获取主机板卡的详细信息及 板卡的所有端口信息
    :param request:
    :return:
    """
    post_data = get_request_data(request)
    if request.method == "POST":
        result = server.post_server_card(post_data)
    if request.method == "GET":
        card_id = post_data.get("cardid", 0)
        result = server.host_card_ports_detail(card_id)
    return response_json(result)


@require_GET
def get_port_map(request):
    """
    网络设备修改和编辑端口映射时返回对端端口的类型及端口信息
    :param request:
    :return:
    """
    result = equipment.get_port_map_info(request.GET, request.session.get("custid"))
    return render(request, "cmdb/equipment_card_port_search.html", {"portlist": result})


@require_POST
def post_port_map(request):
    """
    编辑网络设备端口映射信息(添加、修改、删除)
    :param request:
    :return:
    """
    request_data = get_request_data(request)
    result = equipment.post_port_map_info(request_data)
    return response_json(result)


@login_required(login_url="login")
@require_GET
def get_vg_detail(request):
    """
    获取host主机下vg的详细信息接口,包括lv,pv信息
    :param request:
    :return:
    """
    request_data = get_request_data(request)
    vgid = request_data.get("id", 0)
    result = server.get_vg_related_detail(int(vgid))
    return response_json(result)


@login_required(login_url="login")
def db_backup_manage(request):
    """
    数据备份管理页面
    :param request:
    :return:
    """
    return render(request, "cmdb/sysconfig_dbmanage.html")


@login_required(login_url="login")
@require_GET
def down_excel_templates(request):
    """
    获取导入excel文件下载模板,需要传入一个要下载的模板类型名template_name,包括：assets,equipment,server,base
    其中base为集表数据模板,如果要下载基表数据模板,需要接收基表名,base_table
    :param request:接收模板类型
    :return:返回excel文件模板
    """
    try:
        template_type = request.GET.get("template_type")
        file_type = request.GET.get("file_type")
        if not template_type:
            # 传入的参数名错误
            return render(request, "cmdb/notfound.html", {"param": None})
        else:
            request_data = {"template_type": template_type,"user": request.user,
                            "custid":request.session.get("custid"), "file_type": file_type}

            template = excel.DownTemplate(**request_data)
            excel_file = template.get_template()
            # if not file_name:
            #     # 传入参数值错误
            #     return render(request, "cmdb/notfound.html", {"param": None})
            # response = StreamingHttpResponse(file_iterator(file))
            # response['Content-Type'] = 'application/octet-stream'
            # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
            response = HttpResponse(excel_file,
                                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = "attachment; filename=%s" % (template.filename)
            return response

    except Exception as e:
        logger.error(e)

@login_required(login_url="login")
@require_POST
def import_excel_data(request):
    """
    上传excel,导入数据
    :param request:
    :return:
    """
    from django.conf import settings
    result = response_format()
    try:
        file_obj = request.FILES['file']
        # upload file to tmp folder
        save_file_path = os.path.join(settings.BASE_DIR, "cmdb/exceltemplate/")
        file_name = save_file_for_upload(save_file_path, file_obj)
        if file_name:
            # upload success
            request_data = get_request_data(request)
            xls = excel.ImportData(**{"template_name": request_data.get("template_type"),
                                      "module": request_data.get("module"),
                                      "file_name": file_name,
                                      "cust_id": request_data.get("custid")})

            if xls.avaible:
                excel_data = xls.read_xls_data()
                if xls.avaible:
                    if excel_data:
                        model_obj = get_model(request_data.get("module"))
                        if model_obj:
                            result = model_obj.import_excel(request_data, excel_data)
                    else:
                        result["info"] = "文件无数据记录!"
                        result["category"] = "warning"
                        result["status"] = False
                else:
                    result["info"] = "模板文件或格式错误!"
                    result["category"] = "error"
                    result["status"] = False
            else:
                result["info"] = "模板文件误或格式错误!"
                result["category"] = "error"
                result["status"] = False
        else:
            result["info"] = "文件上传失败!"
            result["category"] = "error"

        # return HttpResponse(file_name)
    except Exception as e:
        logger.error(e)
        result["info"] = "导入失败,请确认导入模板与选择分类一致!"
    # delete file
    os.remove(os.path.join(save_file_path, file_name))
    return response_json(result)


