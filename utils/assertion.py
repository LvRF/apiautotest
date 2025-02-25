
'''
print('12/30【debug】assertion: ',case_data['assertion'])
assert_list = case_data['assertion'].split("\n")
for item in assert_list:
    source,method,target= item.split(",")
    source = source.split('.')[-1] # source是要校验的变量名
    target_value = jsonpath.jsonpath(response,'$..{}'.format(source))[0]
    Logger.info('12/30【debug】从response中取到的source值为：{}'.format(target_value))
    Logger.info('12/30【debug】assert的target值为：{}'.format(target))
    assert str(target_value)==str(target)

补充：1. 多种校验条件： ==;  !=;  >;  <;   is ;  is not
    2. 值中有引用变量
'''

'''
25/1/8 校验封装思路：
1、 封装 不同条件对应不同校验语句
2、 从接口返回中提取 目标校验变量
3、 选择校验条件 -->对应不同方法
4、 校验入口函数
'''
import jsonpath
import re
from utils.logger import Logger
from utils.load import LoadYaml


class Assertion:

    def __init__(self):
        self._ly = LoadYaml()
        pass


    def equal(self,source,target):
        # 等于
        try:
            exec("assert str(source).strip() == str(target).strip()")
        except:
            Logger.error("断言失败，{source} 不等于 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} == {target}".format(source=source,target=target))

    def unEqual(self,source,target):
        # 不等于
        try:
            exec("assert str(source).strip() != str(target).strip()")
        except:
            Logger.error("断言失败，{source} 等于 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} != {target}".format(source=source,target=target))

    def moreThan(self,source,target):
        # 大于
        try:
            exec("assert source > target")
        except:
            Logger.error("断言失败，{source} 不大于 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} > {target}".format(source=source,target=target))

    def lessThan(self,source,target):
        # 小于
        try:
            exec("assert source < target")
        except:
            Logger.error("断言失败，{source} 不小于 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} < {target}".format(source=source,target=target))

    def isTrue(self,source,target):
        # 是
        try:
            exec("assert source is target")
        except:
            Logger.error("断言失败，{source} 非 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} 是 {target}".format(source=source,target=target))

    def isNot(self,source,target):
        # 非
        try:
            exec("assert source is not target")
        except:
            Logger.error("断言失败，{source} 是 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} 非 {target}".format(source=source,target=target))

    def isIn(self,source,target):
        # 包含于。即 source是target的子集
        try:
            exec("assert str(source).strip() in str(target).strip()")
        except:
            Logger.error("断言失败，{source} 不包含于 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} 包含于 {target}".format(source=source,target=target))

    def notIn(self,source,target):
        # 不包含于。即 source不是target的子集
        try:
            exec("assert str(source).strip() not in str(target).strip()")
        except:
            Logger.error("断言失败，{source} 包含于 {target}".format(source=source,target=target))
            raise
        else:
            Logger.info("断言通过,{source} 不包含于 {target}".format(source=source,target=target))


    def getSourceValueFromResponse(self,response,source):
        if source:
            source = source.split('.')[ -1 ]  # source是要校验的变量名
            try:
                source_value = jsonpath.jsonpath(response, '$..{}'.format(source))[0]
            except AttributeError:
                Logger.error("获取断言[{}]字段失败".format(source))
                Logger.error("返回内容异常：{}".format(response))
                raise
        Logger.info('目标字段:{},从response中获取其值为：{}'.format(source,source_value))
        return source_value

    def getTargetValueFromYaml(self,target):
        if target and re.search("\${.*}", target):
            variable = re.findall(r'\$\{([^}]+)\}', target)[0]  # re.findall()结果为列表，故需通过下标取到具体变量名
            _tmp = self._ly.read()
            try:
                for key in variable.split('.'):  # 例如：key=['usergoodsbrowse_index','NO_001','id']
                    _tmp = _tmp[ key ]  # 实现循环多层取值，最后取出'id'的值
                    Logger.info("从yaml文件中，提取到变量{}的值为{}".format(variable, _tmp))
                return _tmp
            except TypeError:  # replace()进行替换时，参数值可能存在类型错误导致报错
                Logger.error("从yaml文件中，提取到变量{}的值异常".format(variable))
                return target
        else:
            Logger.info('target的值为：{}'.format(target))
            return target


    def chooseAssert(self,source,method,target):
        # 常见断言条件： ==; !=; >; <; is; is not; in; not in
        switch = {
            "==" : "equal",
            "!=" : "unEqual",
            ">" : "moreThan",
            "<" : "lessThan",
            "is" : "isTrue",
            "is not" : "isNot",
            "in" : "isIn",
            "not in" : "notIn",
        }
        func = "self." + switch.get(method) + "(source,target)"
        exec(func)


    # 断言入口
    @staticmethod
    def resultAssert(response,assertion): # assertion为 case_data['assertion']
        try:
            assert_list = assertion.split("\n")
        except:
            Logger.warning("断言内容异常，请检查{}".format(assertion))
            assert_list = []
        for assert_item in assert_list:
            source, method, target = assert_item.split(",")
            Logger.info("开始断言 {}".format(assert_item))
            source = Assertion().getSourceValueFromResponse(response,source)
            target = Assertion().getTargetValueFromYaml(target).strip()
            Assertion().chooseAssert(source,method,target)
            # Assertion().chooseAssert(str(source).strip(),method,str(target).strip())






