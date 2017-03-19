Ya Lian Cloud
=============

启动方式
====
    非安装启动
            通过cloud_client.py启动

    安装后启动
            python3.5 setup.py build
            python3.5 setup.py install
            命令行执行cloud_client启动



菜单添加
====
    一   菜单的URL与菜单英文名关系密切，
        菜单的英文名实际对应的是url以'/'分割的名称

        如，监控首页url，/tracker/index/   菜单的英文名为index
        主机页面 url, /tracker/host/  菜单的英文名为host
        创建主机ur， /tracker/host/create/  菜单的英文名为create


编码规范
====

    前端
        命名规范
                class命名 样式命名以a-zA-Z_0-9组合，对于多个单词组合，以 - 短横线连接,如 btn-color
                对于用于事件绑定的class，必须字节定义一个class名称，为了区别于样式和带有事件绑定的样式，事件样式须以a-zA-Z_0-9组合

                    对于多个单词，必须以_下划线连接， 如：user_info,

                对于函数或变量命名
                    对于含有构造方法的函数，及需要以new关键字实例化对象时，该命名以大写开头,如：Person, Animal
                    对于普通函数命名则按驼峰命名规则，例如:showData,getDate

    后台
        命名规范
                class类名 须每个单词首字母大写 ，如：PublicTools, Person
                函数方法及其它变量必须小写命名 ，多个单词组合须以下划线连接，如：show,get,hash_data

api
====
   URL规范

   1    在主项目afcat下的urls里新增api的url, /api/v1/app_name/?args...
   2    在api app下新建对应的需要使用API的app名称，格式:app_name_views.py
   3    在api app下urls新建url规则，规则必须按照app名称开头,如^/app_name/....


        对响应格式，统一导入模块api.libs.public.response_format
        具体格式输出方法，参照response_format的doc


api 使用规范
    所有API操作必须继承from api.libs.public import APIView
    该APIView帮助我们避免了不规范的url书写方式

    对于想使用api模块进行操作，通过定义对应的http方法
    如get请求
        def get(self, request, *args, **kwargs):
            api = kwargs.get('api', None)
            api.api模块的属性方法


    默认API请求都要求用户登录方可获取数据，如果需要免登录开放API，则需要重写dispatch方法
    复制下面代码即可
        def dispatch(self, request, *args, **kwargs):
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed
            return handler(request, *args, **kwargs)


    对于重写dispatch方法后，比如get方法不需要验证，但是post方法又需要认证登录，则可以导入
    from api.libs.public import my_login_required
    该模块与login_required使用方式完全一样，
    如
        @my_login_required(login_url='login')
        def post(self, request, *args, **kwargs):
            ret = response_format()
            return HttpResponse(json.dumps(ret))


定义视图view，必须继承
====
    from api.libs.public import BaseView

    默认该view强制要求登录验证，如果对于不想认证的http 方法，也可按照API方式进行处理修改

