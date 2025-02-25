# 封装json的读写、yaml的读、写、更新操作
'''
用法说明：
1、def test1(data: list[int]) -> dict[str, int]:
在test1这个函数中，data: list[int] 表示函数期望接收一个整数列表作为参数，-> dict[str, int] 表示函数返回值期望是一个键为字符串、值为整数的字典。
2、json.load(f): 读取 JSON 数据，并将其转换为 Python 对象(其类型取决于 JSON 数据的结构。常见的返回值类型有列表、字典或其它类型)。
【拓展】 json.load()：主要用于从文件对象中读取 JSON 数据并将其解析为 Python 对象。(读取文件对象时使用)
       json.loads()：用于将包含 JSON 数据的字符串解析为 Python 对象。(平常使用)
3、json.dumps(): dumps函数的主要作用是将 Python 对象（如字典、列表、元组等）转换为 JSON 格式的字符串。
【拓展】 json.dumps()：用于将 Python 对象（如字典、列表等）转换为 JSON 格式的字符串。
       json.dump()：用于将 Python 对象转换为 JSON 格式，并直接写入到文件对象中。
4、当设置ensure_ascii=False时(想要中文显示时，需设置这个)，json.dumps()不会对非 ASCII 字符(比如 中文)进行转义，而是直接按照字符的原始编码进行输出。
    这样生成的 JSON 字符串可能包含非 ASCII 字符，使得 JSON 数据更便于阅读和理解。
'''

import json
import yaml


class LoadJson:
    # 加载 json 文件，读取、写入 json 文件

    def __init__(self) ->None:
        self.file_path = "./data/case_data.json"

    def write(self,data):
        with open(self.file_path,'w') as f: # 是否设置encoding="UTF-8"，写入的json文件编码格式都是：GB2312
            json.dump(data,f,ensure_ascii=False)

    def read(self):
        # with open(self.file_path,'r',encoding='utf-8') as f:  #要读取的文件中包含中文，中文在不同编码格式下的二进制表现形式是不同的，源文件是用‘utf-8’编码的，所以这里需设置'utf-8'的编码格式。
        with open(self.file_path,'r',encoding='GB2312') as f:  #源文件是用‘GB2312’编码的，所以这里需设置'GB2312'的编码格式。
            json_dict = json.load(f)
            return json_dict


class LoadYaml:
    # 加载 yaml 文件，读取、写入、更新 yaml 文件内容
    def __init__(self) -> None:
        self.filepath = "./config/config.yaml"

    def read(self) ->dict:
        with open(self.filepath,'r') as f:
            # yaml.load() 用于将YAML格式的字符串或文件内容解析为 Python 对象。
            yaml_dict = yaml.load(f,Loader=yaml.FullLoader)# Loader=yaml.FullLoader是为了更加安全地加载 YAML 数据，避免潜在的安全漏洞。
            return yaml_dict

    def write(self,data) -> None:
        '''
        向 yaml 文件中追加内容
        '''
        with open(self.filepath,'a+') as f:
            f.seek(0)  # seek()方法用于移动文件读取指针到指定位置。比如 f.seek(3,0)中，“0”代表从文件开头开始偏移，偏移3个单位
            # yaml.dump() 用于将python对象解析为Yaml格式的字符串，并将其写入到文件对象中。
            yaml.dump(data,f,sort_keys=False,allow_unicode=True) # sort_keys参数用于控制是否对字典的键进行排序。
            #allow_unicode参数：控制是否允许在 YAML 文件中直接使用 Unicode 字符（非 ASCII 字符）。当allow_unicode=True时，Unicode字符(比如：中文)可以直接在 YAML 文件中表示。 为False时：中文字符会被进行编码或转义处理。

    def update(self,data) -> None:
        with open(self.filepath,'w') as f:
            yaml.dump(data,f,sort_keys=False,allow_unicode=True)


if __name__=='__main__':
    pass
