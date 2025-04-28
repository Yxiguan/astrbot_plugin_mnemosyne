import openai
from google import genai
from typing import List, Union
import os


class OpenAIEmbeddingAPI:
    """
    OpenAI 兼容的 Embedding 服务封装类
    功能：支持通过环境变量或参数指定 API 密钥
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: str = None,
        base_url: str = None,
    ):
        """
        :param model: 使用的嵌入模型名称
        :param api_key: 可选 API 密钥（优先于环境变量）
        :param base_url: 自定义 API 端点（用于兼容本地部署）
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or "https://api.openai.com/v1"
        if not self.api_key:
            raise ValueError("必须提供 OpenAI API 密钥或设置 OPENAI_API_KEY 环境变量")

        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    def test_connection(self):
        # 测试与embedding 的连接
        try:
            response = self.client.embeddings.create(input=["你好"], model=self.model)
        except Exception as e:
            raise ConnectionError(
                f"Embedding Connection error: {e}\n 请检查Embedding 模型配置是否正确，是否可以访问"
            )

    def get_embeddings(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        获取文本嵌入向量
        :param texts: 输入文本（单条字符串或字符串列表）
        :return: 嵌入向量列表
        """
        try:
            if isinstance(texts, str):
                texts = [texts]

            response = self.client.embeddings.create(input=texts, model=self.model)
        except Exception as e:
            raise ConnectionError(
                f"Embedding Connection error: {e}\n 请检查Embedding 模型配置是否正确，是否可以访问"
            )
        return [data.embedding for data in response.data]

class GeminiEmbeddingAPI:

    def __init__(self, model: str = "gemini-embedding-exp-03-07", api_key: str = None):
        """
        :param model: 使用的嵌入模型名称
        :param api_key: 可选 API 密钥（优先于环境变量）
        """
        self.model = model
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("必须提供 Gemini API 密钥或设置 GEMINI_API_KEY 环境变量")

        self.client = genai.Client(api_key=self.api_key)

    def test_connection(self):
        # 测试与 Gemini 的连接
        try:
            response = self.client.models.embed_content(
                model=self.model, contents="hello world"
            )
        except Exception as e:
            raise ConnectionError(
                f"Gemini Embedding Connection error: {e}\n 请检查模型配置是否正确，是否可以访问"
            )

    def get_embeddings(self, texts: Union[str, List[str]]) -> List[List[float]]:
        """
        获取文本嵌入向量
        :param texts: 输入文本（单条字符串或字符串列表）
        :return: 嵌入向量列表
        """
        try:
            if isinstance(texts, str):
                texts = [texts]

            response = self.client.models.embed_content(model=self.model, contents=texts)
            embeddings = [embedding.values for embedding in response.embeddings]
            return embeddings

        except Exception as e:
            raise ConnectionError(
                f"Gemini Embedding Connection error: {e}\n 请检查模型配置是否正确，是否可以访问"
            )