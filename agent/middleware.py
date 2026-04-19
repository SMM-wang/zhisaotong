
from utils.logger_handler import logger
from langchain.agents.middleware import before_agent,after_agent,before_model,after_model,wrap_model_call,wrap_tool_call,dynamic_prompt
from langchain.agents.middleware import AgentState
from langchain_core.messages import SystemMessage
from langchain.tools.tool_node import ToolCallRequest
from langgraph.runtime import Runtime
from utils.prompts_loder import get_main_prompt, get_report_prompt


@wrap_tool_call
def monitor_tool(request: ToolCallRequest, handler):
    logger.info(f"[monitor_tool]工具调用: {request.tool_call['name']}")
    logger.info(f"[monitor_tool]工具调用参数: {request.tool_call['args']}")
    result = handler(request)
    if request.tool_call['name'] == "fill_context_for_report":
        if request.runtime.context is None:
            request.runtime.context = {}
        request.runtime.context["report"] = True
        logger.info("[monitor_tool] 检测到报告生成场景，已标记上下文")
    logger.info(f"[monitor_tool]工具返回: {result}")
    return result

@dynamic_prompt
def select_prompt(request):
    if request.runtime and request.runtime.context and request.runtime.context.get("report", False):
        logger.info("[prompt] 切换到报告生成提示词")
        return SystemMessage(get_report_prompt())
    return SystemMessage(get_main_prompt())

@before_model
def monitor_model(state: AgentState,
                  runtime: Runtime
                  ):
    logger.info(f"开始调用模型: {state}")
    return state
