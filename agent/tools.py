from langchain_core.tools import tool
import random
from rag.rag import rag_query
from utils.path_tool import get_abs_path
from utils.config_loder import load_agent_config
import os
from utils.logger_handler import logger


location = ["北京","上海","广州","深圳"]
user_id = ["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"]

@tool(description="获取当前用户的ID")
def get_user_id():
   """- 核心能力：无入参，精准获取当前发起请求的用户唯一标识（ID字符串），ID格式为数字字符串（如"1001"）；
   - 出参：字符串类型的用户ID（如"1002"）；
   - 使用场景：当需要基于「当前用户的ID」检索其专属使用记录、生成个性化使用报告时，如未知用户ID可先调用此工具获取用户ID，再进行后续操作；
   - 调用规则：无需传入任何参数，直接触发调用即可。"""
   return random.choice(user_id)
  
@tool(description="获取当前月份")
def get_current_month():
   """- 核心能力：无入参，精准获取系统当前月份的标准字符串，格式固定为YYYY-MM（如"2025-06"）；
   - 出参：字符串类型的月份（严格遵循"YYYY-MM"格式，如"2025-12"）；
   - 使用场景：当用户未明确指定月份，且需要基于「当前月份」检索用户记录、生成个性化使用报告/数据统计时，调用此工具；
   - 调用规则：无需传入任何参数，直接触发调用即可。"""
   return "2025-06"

external_data = {}
def get_external_data():
    """
    获取外部数据:
    {
        "user_id": {
            "month": {"特征":"xxx", "效率":"xxx", ...}
            "month": {"特征":"xxx", "效率":"xxx", ...}
            "month": {"特征":"xxx", "效率":"xxx", ...}
        },
        "user_id": {
            "month": {"特征":"xxx", "效率":"xxx", ...}
            "month": {"特征":"xxx", "效率":"xxx", ...}
            "month": {"特征":"xxx", "效率":"xxx", ...}
        },
    }
    """
    if not external_data:
       file_path = get_abs_path(load_agent_config()["external_data_path"])
       if not os.path.exists(file_path):
            raise FileNotFoundError(f"外部数据文件不存在: {file_path}")
       with open(file_path, "r", encoding="utf-8") as f:
           lines = f.readlines()
           for line in lines[1:]:
               line = line.strip()
               arr : list[str] = line.split(",")
            #    "用户ID","特征","清洁效率","耗材","对比","时间"
               user_id = arr[0].replace('"','')
               month = arr[5].replace('"','')
               feature = arr[1].replace('"','')
               efficiency = arr[2].replace('"','')
               material = arr[3].replace('"','')
               compare = arr[4].replace('"','')

               if user_id not in external_data:
                   external_data[user_id] = {}
                   
               external_data[user_id][month] = {
                    "特征":feature,
                    "效率":efficiency,
                    "耗材":material,
                    "对比":compare
                    }
    return external_data

# @tool(description="获取指定用户在指定月份的扫记录")
def fetch_external_data(user_id: str, month: str):
   """- 核心能力：入参为user_id（用户ID）和month（月份），检索指定用户在指定月份的扫地/扫拖机器人完整使用记录；
   - 出参：字符串类型的结构化使用记录，包含清洁效率、耗材状态、使用对比等核心报告数据；
   - 使用场景：当需要为用户生成报告时，如未知用户ID或月份信息，可先通过get_user_id/get_current_month或用户指定获取入参，再调用此工具；
   - 调用规则：必须同时传入纯文本字符串类型的user_id和month参数，user_id为数字字符串，month严格遵循"YYYY-MM"格式。"""
   get_external_data()
   if user_id not in external_data or month not in external_data[user_id]:
       logger.error(f"用户{user_id}在{month}没有扫记录")
       return f"用户{user_id}在{month}没有扫记录"
   return f"用户{user_id}在{month}的扫记录为: {external_data[user_id][month]}"



@tool(description="获取扫地/扫拖机器人的专业问答、建议、故障处理、环境适配、选购指南、维护保养等相关资料")
def rag_summarize(query: str):
   """- 核心能力：入参为query（检索词），从向量库精准检索扫地/扫拖机器人的常用问答、专业使用建议、故障处理、环境适配、选购指南、维护保养等相关资料；
   - 出参：字符串类型的专业资料内容，包含与检索词匹配的精准解答、建议及知识点；
   - 使用场景：当回答用户问题需要补充扫地/扫拖机器人的专业信息、行业知识，现有常识无法精准解答时，调用此工具获取专业内容；
   - 调用规则：必须传入纯文本字符串类型的query参数，参数为贴合用户问题的核心检索词。"""
   return rag_query(query)

@tool(description="获取天气服务类，用户提问，获取城市的天气信息")
def get_weather(city: str) -> str:
    return f"{city}的天气是晴朗的天气,26摄氏度"

@tool(description="获取用户位置服务类，用户提问，获取用户的位置信息")
def get_user_location() -> str:
    return random.choice(location)

@tool(description="报告生成上下文注入工具：调用后触发中间件自动为报告生成场景动态注入上下文信息，为后续提示词切换提供上下文支撑")
def fill_context_for_report():
    logger.info("[fill_context_for_report] 检测到报告生成场景，上下文已标记")
    return "上下文已注入，报告生成流程已启动"