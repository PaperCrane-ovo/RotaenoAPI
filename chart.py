'''
定义谱面类
谱面不编号，id为曲名
'''
from os import read
from typing import Optional,List

_file = 'songlist.json'

class Chart:
    def __init__(self,parameters_list:dict):
        self.id:str = parameters_list['id']
        self.name:str = parameters_list['title_localized']['default']
        self.artist:str = parameters_list['artist']
        self.difficulties:dict = parameters_list['difficulties']
        self.alias:List[str] = parameters_list['alias']    
    
    def add_alias(self,alias:str):
        self.alias.append(alias)
        with open(_file,'r',encoding='utf-8') as f:
            import json5
            json = json5.load(f)
        for chart in json['songs']:
            if chart['id'] == self.id:
                chart['alias'].append(alias)
                break
        with open(_file,'w',encoding='utf-8') as f:
            json5.dump(json,f,ensure_ascii=False,indent=4,quote_keys=True,trailing_commas=False)
    def del_alias(self,alias:str):
        self.alias.remove(alias)
        with open(_file,'r',encoding='utf-8') as f:
            import json5
            json = json5.load(f)
        for chart in json['songs']:
            if chart['id'] == self.id:
                chart['alias'].remove(alias)
                break
        with open(_file,'w',encoding='utf-8') as f:
            json5.dump(json,f,ensure_ascii=False,indent=4,quote_keys=True,trailing_commas=False)
    
    def get_lower_case_name(self):
        return self.name.lower()
    
    def name_has_substring(self,substring:str):
        return substring in self.name or substring in self.get_lower_case_name()

class ChartList:
    def __init__(self,charts:Optional[List[Chart]]=None) -> None:
        self.charts = [] if charts is None else charts
        self.read_from_json(_file)
    
    def read_from_json(self,file_path:str):
        '''从json文件中读取谱面列表'''
        with open(file_path,'r',encoding='utf-8') as f:
            import json5
            data = json5.load(f)
            for chart in data['songs']:
                self.charts.append(Chart(chart))

    def write_to_json(self,file_path:str=_file): 
        '''将谱面列表写入json文件'''
        with open(file_path,'w',encoding='utf-8') as f:
            import json5
            json = {'songs':[]}
            for chart in self.charts:
                json['songs'].append(chart.__dict__)
            json5.dump(json,f,ensure_ascii=False,indent=4,quote_keys=True,trailing_commas=False)
        
    def get_song_by_alias(self, alias:str) -> Optional[Chart]:
        """
        根据别名获取谱面
        目前使用一个比较简单的方法，直接遍历，后续考虑使用hash
        """
        ret_val = []
        for chart in self.charts:
            if alias in chart.alias:
                ret_val.append(chart)
        if len(ret_val) == 0:
            return None
        return ret_val
    
    def get_song_by_id(self, id:str) -> Optional[Chart]:
        """
        根据编号获取谱面
        """
        for chart in self.charts:
            if id == chart.id:
                return chart
        return None
    
    def get_song_by_name(self, name:str) -> Optional[Chart]:
        """
        根据谱面名获取谱面
        """
        for chart in self.charts:
            if name == chart.get_lower_case_name() or name == chart.name:
                return chart
        return None
    
    def get_song(self,name_or_alias:str) -> Optional[Chart]:
        """
        根据谱面名或别名获取谱面
        """
        name_chart = self.get_song_by_name(name_or_alias)
        if name_chart is not None:
            return name_chart
        alias_chart = self.get_song_by_alias(name_or_alias)
        if alias_chart is not None:
            return alias_chart
        charts = self.search_song(name_or_alias)
        if charts is not None:
            return charts
        return None
    
    def get_song_list(self) -> List[Chart]:
        """
        获取谱面列表
        """
        return self.charts
    
    def get_alias(self,id:str) -> Optional[List[str]]:
        """
        根据编号获取谱面的别名
        """
        chart = self.get_song_by_id(id)
        if chart is not None:
            return chart.alias
        return None

    def search_song(self,substring:str) -> List[Chart]:
        """
        根据谱面名的子串搜索谱面
        """
        result = []
        for chart in self.charts:
            if chart.name_has_substring(substring):
                result.append(chart)
        if len(result) == 0:
            return None
        return result

    