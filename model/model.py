from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings


class QwenEmbeddings(Embeddings):
    def __init__(self, model_name="qwen3-vl-embedding"):
        self.model_name = model_name
        try:
            import dashscope
        except ImportError:
            raise ImportError("请安装 dashscope: pip install dashscope")
        self.dashscope = dashscope

    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            input_data = [{"text": text}]
            response = self.dashscope.MultiModalEmbedding.call(
                model=self.model_name,
                input=input_data
            )
            if response.status_code == 200:
                output = response.output
                if isinstance(output, dict):
                    embeddings.append(output["embeddings"][0]["embedding"])
                else:
                    embeddings.append(output.embeddings[0]["embedding"])
            else:
                raise ValueError(f"嵌入失败: {response.message}")
        return embeddings

    def embed_query(self, text):
        return self.embed_documents([text])[0]


def get_chat_model(model_name="qwen3-max-2026-01-23", temperature=0.7, **kwargs):
    chat_models = {
        "qwen3-max-2026-01-23": ChatTongyi(model_name=model_name, **kwargs),
        "qwen3-max": ChatTongyi(model_name="qwen3-max", **kwargs),
        "qwen-plus": ChatTongyi(model_name="qwen-plus", **kwargs),
        "qwen-turbo": ChatTongyi(model_name="qwen-turbo", **kwargs),
    }
    return chat_models.get(model_name, ChatTongyi(model_name=model_name, **kwargs))


def get_embedding_model(model_name="qwen3-vl-embedding", **kwargs):
    embedding_models = {
        "qwen3-vl-embedding": QwenEmbeddings(model_name=model_name),
        "text-embedding-3-small": DashScopeEmbeddings(model="text-embedding-3-small", **kwargs),
        "text-embedding-3-large": DashScopeEmbeddings(model="text-embedding-3-large", **kwargs),
    }
    return embedding_models.get(model_name, QwenEmbeddings(model_name=model_name))

llm = get_chat_model("qwen3-max-2026-01-23")
embed_model = get_embedding_model("qwen3-vl-embedding")
if __name__ == "__main__":
    import os
    # os.environ["DASHSCOPE_API_KEY"] = "your-api-key"
    llm = get_chat_model("qwen3-max-2026-01-23")
    response = llm.invoke("你是谁？")
    print(response.content)

    embed_model = get_embedding_model("qwen3-vl-embedding")
    docs = embed_model.embed_documents(["你好世界", "这是一个测试"])
    print(f"嵌入维度: {len(docs[0])}")
