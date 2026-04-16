"""配置文件加载器"""
import yaml
from utils.path_tool import get_abs_path

def load_rag_config():
    with open(get_abs_path("config/RAG.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_agent_config():
    with open(get_abs_path("config/agent.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_prompt_config():
    with open(get_abs_path("config/prompt.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_chroma_config():
    with open(get_abs_path("config/chroma.yaml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)