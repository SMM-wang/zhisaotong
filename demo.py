from utils.logger_handler import logger
from utils.prompts_loder import get_main_prompt, get_rag_summarize_prompt, get_report_prompt
from utils.file_hander import read_pdf, read_txt, get_file_md5
from utils.config_loder import load_rag_config
from rag.vector_service import VectorService
from rag.rag import rag_query



if __name__ == "__main__":
    # logger.info("这是一条info日志")
    # print(get_main_prompt())
    # print(get_rag_summarize_prompt())
    # print(get_report_prompt())
    # pdf_docs = read_pdf("data/扫地机器人100问.pdf")
    # print(pdf_docs)
    # txt_docs = read_txt("data/故障排除.txt")
    # print(txt_docs)
    # rag_config = load_rag_config()["md5_file"]
    # print(rag_config)
    # md5 = get_file_md5("prompts/main_prompt.txt")
    # print(md5)
    # vector_service = VectorService()
    # vector_service.add_documents()
    result = rag_query("扫地机器人如何清洁？")
    print(result)