import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from afcat.monitor.libs import monitor_hosts, report
from afcat.monitor import models
from afcat.monitor.libs.lazysql import Paginator
from afcat.api.libs.public import Logger, response_format
logger = Logger(__name__)


@login_required(login_url="login")
def index(request):
    """
    监控首页
    :param request:
    :return:
    """
    return render(request, 'monitor/index.html')


def get_host_groups_status(request):
    """
    监控首页的dashboard获取数据API
    请求方式
    ?page=1&group_status_info=true&get_event_triggers_status=true&get_top_data=true
    group_status_info 获取主机组下正常与故障主机数量信息
    get_event_triggers_status： 获取最新告警状态信息
    get_top_data： 获取top10主机信息
    :param request:
    :return:
    """
    ret = response_format()
    ret['data'] = dict()
    try:
        host_groups_status = monitor_hosts.HostGroupsStatus()
        event_triggers_status = request.GET.get('get_event_triggers_status', None)
        group_status_info = request.GET.get('group_status_info', None)
        get_top_data = request.GET.get('get_top_data', None)
        if group_status_info is not None:
            group_status_info = host_groups_status.get_all_groups_status()
            ret['data'].update({'group_status_info': group_status_info})
        if event_triggers_status is not None:
            event_triggers_status = host_groups_status.get_event_triggers_status()
            ret['data'].update({'get_event_triggers_status': event_triggers_status})
        if get_top_data is not None:
            top_data = host_groups_status.get_top_data()
            ret['data'].update({'get_top_data': top_data})
    except Exception as e:
        logger.error("%s" % e, request)
        ret['info'] = "页面请求异常"
    return HttpResponse(json.dumps(ret))


def event_trigger(request):
    """
    告警页面
    :param request:
    :return:
    """
    return render(request, "monitor/event_trigger.html")


def get_event_trigger(request):
    """
    告警页面API接口
    ?page=3&group_id=49&host_id=0&ip_address=&issue_level=&ack=&trigger_end_time=&start_time=&end_time=
    ?page=1&group_id=4&get_hosts=true
    ?page=1&group_id=0&get_hosts=true&get_groups=true
    请求组 {"get_groups": true}获取所有的组
    请求主机 {"get_hosts": true, group_id: id} 当ID为0时请求所有启用的主机
    搜索过滤
    :param request: GET方式请求
    :return:
    """
    ret = response_format()
    ret['data'] = dict()
    try:
        get_groups = request.GET.get('get_groups')
        get_hosts = request.GET.get('get_hosts')
        get_hosts_groups = request.GET.get('get_hosts_groups')
        page = request.GET.get('page', 1)
        per_records = request.GET.get('per_records', 50)
        group_id = request.GET.get('group_id', None)
        host_id = request.GET.get('host_id', None)
        ip_address = request.GET.get('ip_address', None)
        issue_level = request.GET.get('issue_level', None)
        ack = request.GET.get('ack', None)
        start_time = request.GET.get('start_time', None)
        end_time = request.GET.get('end_time', None)
        trigger_end_time = request.GET.get('trigger_end_time', None)
        handler = monitor_hosts.SearchEventTrigger()
        if issue_level is not None:
            handler = monitor_hosts.EventTriggers(
                group_id=group_id,
                host_id=host_id,
                ip_address=ip_address,
                issue_level=issue_level,
                ack=ack,
                start_time=start_time,
                end_time=end_time,
                trigger_end_time=trigger_end_time
            )
            data = Paginator(handler.object_list(), per_page=int(per_records))
            data = data.page(page)
            ret['data'] = data.object_list
            ret['has_next'] = data.has_next()
        if get_groups:
            ret['data'].update({'get_groups': handler.get_group_info()})
        if get_hosts:
            group_id = request.GET.get('group_id')
            ret['data'].update({'get_hosts': monitor_hosts.EventTriggers().get_hosts(group_id)})

        if get_hosts_groups:
            ret['data'].update({'get_hosts_groups': handler.get_hosts_groups_rel()})
    except TypeError as e:
        logger.error("%s" % e, request)
        pass
    except json.JSONDecodeError as e:
        logger.error("%s" % e, request)
        pass
    if len(ret["data"]) is 0:
        # 只有空列表，前端才能识别是空对象，空字典，前端也会认为对象不为空
        ret['data'] = []
        ret["info"] = "没有数据"
        ret["category"] = "warning"
    return HttpResponse(json.dumps(ret))


def get_host_groups(request):
    """
    搜索条件
    page=1&type=group&host_name=&ip_address=&status=&issue_time=&issue_level=&group_id=44
    :param request:
    :return: {
        'hostid': 主机id
        'group':所属组,
        'hostname': 主机名,
        'ip_address':主机IP,
        'status': 主机状态,
        'date': 状态发生时间,
        'detail': 详细信息,
        }
    """
    ret = response_format()
    ret['data'] = []
    host_name = request.GET.get('host_name', None)
    ip_address = request.GET.get('ip_address', None)
    status = request.GET.get('status', None)
    issue_time = request.GET.get('issue_time', None)
    issue_level = request.GET.get('issue_level', None)
    group_id = request.GET.get('group_id', None)
    if group_id or (host_name, ip_address, status, issue_time, issue_level) is not None:
        search_handle = monitor_hosts.SearchHostInfo(
            host_name=host_name,
            ip_address=ip_address,
            status=status,
            issue_time=issue_time,
            issue_level=issue_level,
            group_id=group_id
        )
        search_result = search_handle.filter_info()
        ret["data"] = search_result
        if len(ret["data"]) is 0:
            # 只有空列表，前端才能识别是空对象，空字典，前端也会认为对象不为空
            ret["info"] = "没有数据"
            ret["category"] = "warning"
    return HttpResponse(json.dumps(ret))


def host_groups(request):
    return render(request, 'monitor/host_groups.html', {'monitor_group': "active"})


def host_groups_detail(request, group_id):
    return render(request, 'monitor/host_groups.html', {'monitor_group': "active"})


def host_info(request, host_id, display_type):
    """
    主机信息页面
    需要从库里取出当前主机已添加要显示的图表及对应的图表数据
    :param request:
    :param host_id:
    :param display_type: data_graph,detail_info,multi_graph
    :return:
    """
    context = dict()
    get_host_info = monitor_hosts.SearchHostInfo().get_host_info_by_host_id(host_id)
    context.update(get_host_info)
    return render(request, 'monitor/host_info.html', context)


def host_graph_detail(request):
    """
    获取单台主机具体图形数据,同时将用户选择的图形保存到自定义数据表,
    ?page=1&type=detail_info&graph_name=MySQL+operations&graph_id=693&show_item=true
    :param request:
    :return:
    """
    ret = response_format()
    ret['data'] = dict()
    try:
        handler = monitor_hosts.SearchHostInfo()
        host_id = request.GET.get('host_id', None)
        graph_id = request.GET.get('graph_id', None)
        graph_name = request.GET.get('graph_name', None)
        if graph_id is None:
            response = handler.get_host_graphs_items(host_id)
        else:
            graph_data = handler.format_history_data_by_host_id_graph_id(graph_id)
            response = {'data': graph_data, 'name': graph_name, 'graph_id': 'graph%s' % graph_id}
        ret['data'] = response
    except TypeError as e:
        logger.error("%s" % e, request)
        pass
    return HttpResponse(json.dumps(ret))


def report_custom(request):
    """
    自定义报表页面
    :param request:
    :return:
    """
    return render(request, 'monitor/report_custom.html', {'monitor_report': "active"})


def report_default(request):
    """
    默认报表页面
    :param request:
    :return:
    """
    return render(request, 'monitor/report_default.html', {'monitor_report': "active"})


def export_data_to_file(request):
    """
    ?page=1&group_id=0&host_id=0&host_status=&ip_address=&issue_level=&issue_status=&ack=&start_time=&end_time=
    :param request:
    :return:
    """
    ret = response_format()
    ret['data'] = dict()
    try:
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 50)
        group_id = request.GET.get('group_id', None)
        host_id = request.GET.get('host_id', None)
        host_status = request.GET.get('host_status', None)
        ip_address = request.GET.get('ip_address', None)
        issue_level = request.GET.get('issue_level', None)
        issue_status = request.GET.get('issue_status', None)
        ack = request.GET.get('ack', None)
        start_time = request.GET.get('start_time', None)
        end_time = request.GET.get('end_time', None)
        handler = report.ExportFile(
            group_id=group_id,
            host_id=host_id,
            host_status=host_status,
            ip_address=ip_address,
            issue_level=issue_level,
            issue_status=issue_status,
            ack=ack,
            start_time=start_time,
            end_time=end_time
        )
        data = Paginator(handler.object_list(), per_page=int(per_page))
        data = data.page(page)
        ret['data'] = data.object_list
        ret['has_next'] = data.has_next()
    except ValueError as e:
        logger.error("%s" % e, request)
        pass
    if len(ret["data"]) is 0:
        # 只有空列表，前端才能识别是空对象，空字典，前端也会认为对象不为空
        ret['data'] = []
        ret["info"] = "没有数据"
        ret["category"] = "warning"
    return HttpResponse(json.dumps(ret))


def config_host_groups(request):
    """
    配置模版页面
    :param request:
    :return:
    """
    context = {'monitor_config': "active"}
    groups = models.Groups.objects.all()
    context['groups'] = groups
    return render(request, 'monitor/config_host_groups.html', context)


def create_new_group(request):
    """
    创建主机组，同时关联组与主机关系
    创建：?page=1&hosts_id=%5B%2210084%22%5D&group_name=group
    修改：?page=1&hosts_id=%5B%2210084%22%5D&group_name=newgroup&group_id=52&modify=true
    删除：?page=1&group_id=53&group_name=%E9%A3%92%E9%A3%92&delete=true
    :param request:
    {'hosts_id': [], 'group_name': '', get_hosts_groups: true}
    :return:
    """
    ret = response_format()
    ret['data'] = dict()
    try:
        get_hosts_groups = request.GET.get('get_hosts_groups')
        group_name = request.GET.get("group_name", None)
        group_id = request.GET.get("group_id", None)
        hosts_id = request.GET.get("hosts_id", None)
        if hosts_id is not None:
            hosts_id = json.loads(hosts_id)
        modify = request.GET.get("modify", None)
        delete = request.GET.get("delete", None)
        if group_name is not None:
            config_hosts_group = monitor_hosts.ConfigHostsGroup(
                hosts_id=hosts_id,
                group_name=group_name,
                group_id=group_id,
                modify=modify,
                delete=delete,
                response=ret)
            ret = config_hosts_group.create_hosts_group_rel()
        if get_hosts_groups:
            handler = monitor_hosts.SearchEventTrigger()
            ret['data'] = handler.get_hosts_groups_rel()
    except json.JSONDecodeError as e:
        logger.error("%s" % e, request)
        pass
    if len(ret["data"]) is 0:
        # 只有空列表，前端才能识别是空对象，空字典，前端也会认为对象不为空
        ret['data'] = []
    return HttpResponse(json.dumps(ret))


def config_template(request):
    """
    配置模版页面
    :param request:
    :return:
    """
    return render(request, 'monitor/config_template.html', {'monitor_config': "active"})


def config_host_management(request):
    """
    主机管理页面
    :param request:
    :return:
    """
    return render(request, 'monitor/config_host_management.html', {'monitor_config': "active"})


def config_host(request):
    """
    主机管理页面
    :param request:
    :return:
    """
    return render(request, 'monitor/config_host.html', {'monitor_config': "active"})


def config_host_detail(request):
    """

    :param request:
    :return:
    """
    ret = response_format()
    ret['data'] = dict()
    try:
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 50)
        filter_host = request.GET.get('filter_host', None)
        filter_dns = request.GET.get('filter_dns', None)
        filter_ip = request.GET.get('filter_ip', None)
        filter_port = request.GET.get('filter_port', None)
        filter_rst = request.GET.get('filter_rst', None)
        filter_set = request.GET.get('filter_set', None)
        handler = monitor_hosts.ConfigHost(
            filter_host=filter_host,
            filter_dns=filter_dns,
            filter_ip=filter_ip,
            filter_port=filter_port,
            filter_rst=filter_rst,
            filter_set=filter_set
        )
        data = Paginator(handler.object_list(), per_page=int(per_page))
        data = data.page(page)
        ret['data'] = data.object_list
        ret['has_next'] = data.has_next()
    except ValueError as e:
        logger.error("%s" % e, request)
        pass
    if len(ret["data"]) is 0:
        # 只有空列表，前端才能识别是空对象，空字典，前端也会认为对象不为空
        ret['data'] = []
        ret["info"] = "没有数据"
        ret["category"] = "warning"
    return HttpResponse(json.dumps(ret))


def config_host_add(request):
    """
    主机管理页面
    :param request:
    :return:
    """
    return render(request, 'monitor/config_host_add.html', {'monitor_config': "active"})


def config_host_edit(request, host_id):
    """

    :param request:
    :return:
    """
    ret = response_format()
    ret['data'] = dict()
    try:
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 50)
        filter_host = request.GET.get('filter_host', None)
        filter_dns = request.GET.get('filter_dns', None)
        filter_ip = request.GET.get('filter_ip', None)
        filter_port = request.GET.get('filter_port', None)
        filter_rst = request.GET.get('filter_rst', None)
        filter_set = request.GET.get('filter_set', None)
        handler = monitor_hosts.ConfigHost(
            filter_host=filter_host,
            filter_dns=filter_dns,
            filter_ip=filter_ip,
            filter_port=filter_port,
            filter_rst=filter_rst,
            filter_set=filter_set
        )
        data = Paginator(handler.object_list(), per_page=int(per_page))
        data = data.page(page)
        ret['data'] = data.object_list
        ret['has_next'] = data.has_next()
    except ValueError as e:
        logger.error("%s" % e, request)
        pass
    if len(ret["data"]) is 0:
        # 只有空列表，前端才能识别是空对象，空字典，前端也会认为对象不为空
        ret['data'] = []
        ret["info"] = "没有数据"
        ret["category"] = "warning"
    return HttpResponse(json.dumps(ret))


def config_media(request):
    """
    媒介页面
    :param request:
    :return:
    """
    return render(request, 'monitor/config_action_media.html', {'monitor_config': "active", 'monitor_action': "active"})


def config_behaviour(request):
    """
    行为页面
    :param request:
    :return:
    """
    return render(request, 'monitor/config_action_behaviour.html', {'monitor_config': "active", 'monitor_action': "active"})


def lasted_data(request):
    """
    最新数据页面
    :param request:
    :return:
    """
    return render(request, 'monitor/new_data.html')


def queue_status(request):
    """
    队列页面
    :param request:
    :return:
    """
    return render(request, 'monitor/queue.html')

