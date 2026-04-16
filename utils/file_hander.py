"""文件读取工具"""
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from utils.path_tool import get_abs_path
import hashlib
from utils.logger_handler import logger
from utils.config_loder import load_rag_config

def get_file_md5(file_path):
    """获取文件MD5值"""
    abs_path = get_abs_path(file_path)
    if not os.path.exists(abs_path):
        logger.error(f"文件不存在: {abs_path}")
        return None
    return hashlib.md5(open(abs_path, "rb").read()).hexdigest()

    

def read_pdf(file_path: str,password=None) -> list[Document]:
    """读取PDF文件"""
    abs_path = get_abs_path(file_path)
    loader = PyPDFLoader(abs_path,password=password)
    return loader.load()

def read_txt(file_path: str) -> list[Document]:
    """读取文本文件"""
    abs_path = get_abs_path(file_path)
    loader = TextLoader(abs_path, encoding="utf-8")
    return loader.load()