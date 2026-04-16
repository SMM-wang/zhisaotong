from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_loder import load_chroma_config, load_rag_config
from utils.logger_handler import logger
import os
from model.model import embed_model
from utils.path_tool import get_abs_path


class VectorService():
    def __init__(self):
        self.vectorstore = Chroma(
            collection_name=load_chroma_config()["vectorstore_name"],
            persist_directory=load_chroma_config()["vectorstore_path"],
            embedding_function=embed_model,
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=load_chroma_config()["chunk_size"],
            chunk_overlap=load_chroma_config()["chunk_overlap"],
            separators=load_chroma_config()["splitter"],
        )
    
    def get_retriever(self):
        return self.vectorstore.as_retriever(search_kwargs={"k": load_rag_config()["top_k"]})

    def add_documents(self):
        """添加文档到向量数据库"""
        from utils.file_hander import get_file_md5, read_pdf, read_txt

        def check_documents_exist(md5_hex, file_path):
            md5_file = load_chroma_config()["md5_file"]
            if not os.path.exists(md5_file):
                logger.info("md5文件不存在,创建新文件")
                open(md5_file, "w", encoding="utf-8").close()
            with open(md5_file, "r", encoding="utf-8") as f:
                md5s = f.readlines()
                for m in md5s:
                    if md5_hex in m:
                        logger.info(f"文档{file_path}已存在,跳过")
                        return True
            return False

        def save_md5(md5_hex, file_path):
            md5_file = load_chroma_config()["md5_file"]
            with open(md5_file, "a", encoding="utf-8") as f:
                f.write(md5_hex + "\n")
            logger.info(f"文档{file_path}保存成功")

        base_path = get_abs_path(load_chroma_config()["file_path"])
        if not os.path.exists(base_path):
            logger.error(f"文件目录不存在: {base_path}")
            return
        all_files = os.listdir(base_path)
        file_path_list = [
            os.path.join(base_path, f) for f in all_files
            if f.lower().endswith(".txt") or f.lower().endswith(".pdf")
        ]
        logger.info(f"扫描到{len(file_path_list)}个文档")

        for file_path in file_path_list:
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                continue

            md5_hex = get_file_md5(file_path)
            if not md5_hex:
                logger.error(f"获取文件MD5失败: {file_path}")
                continue

            if check_documents_exist(md5_hex, file_path):
                continue

            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".pdf":
                raw_docs = read_pdf(file_path)
            elif ext == ".txt":
                raw_docs = read_txt(file_path)
            else:
                logger.warning(f"不支持的文件类型: {ext}")
                continue

            logger.info(f"开始分割文档: {file_path}")
            split_docs = self.splitter.split_documents(raw_docs)
            logger.info(f"文档分割完成,共{len(split_docs)}个文本块")

            self.vectorstore.add_documents(documents=split_docs)
            logger.info(f"文档已添加到向量数据库")

            save_md5(md5_hex, file_path)

        


    
    
