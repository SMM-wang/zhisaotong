"""提示词加载器"""
import os
from utils.path_tool import get_abs_path

def load_prompt(filename):
    filepath = get_abs_path(os.path.join("prompts", filename))
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def get_main_prompt():
    return load_prompt("main_prompt.txt")

def get_rag_summarize_prompt():
    return load_prompt("rag_summarize.txt")

def get_report_prompt():
    return load_prompt("report_prompt.txt")