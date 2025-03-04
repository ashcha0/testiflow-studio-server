import requests
import time
import logging
from typing import Dict, Any, Optional

from config.constants import API_BASE_URL, API_TIMEOUT, API_RETRY_COUNT

logger = logging.getLogger(__name__)

class APIClient:
    """API客户端封装，处理与生成服务的通信"""
    
    def __init__(self, base_url: str = API_BASE_URL, 
                 timeout: int = API_TIMEOUT,
                 retry_count: int = API_RETRY_COUNT,
                 api_key: Optional[str] = None):
        """初始化API客户端
        
        Args:
            base_url: API基础URL
            timeout: 请求超时时间(秒)
            retry_count: 重试次数
            api_key: API密钥
        """
        self.base_url = base_url
        self.timeout = timeout
        self.retry_count = retry_count
        self.session = requests.Session()
        
        # 设置默认请求头
        self.session.headers.update({
            "Authorization": "Bearer sk-eaa4f9161a724d7fbdf2451c0ff94f00",
            "Content-Type": "application/json"
        })
        
        if api_key:
            self.session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    def _make_request(self, endpoint: str, method: str = 'GET', 
                     params: Dict = None, data: Dict = None, 
                     retry: int = None) -> Dict:
        """发送API请求并处理响应
        
        Args:
            endpoint: API端点
            method: 请求方法 (GET, POST等)
            params: URL参数
            data: 请求体数据
            retry: 重试次数
            
        Returns:
            Dict: API响应数据
            
        Raises:
            requests.exceptions.RequestException: 请求错误
        """
        if retry is None:
            retry = self.retry_count
            
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(retry + 1):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, timeout=self.timeout)
                elif method.upper() == 'POST':
                    response = self.session.post(url, params=params, json=data, timeout=self.timeout)
                else:
                    raise ValueError(f"不支持的请求方法: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt < retry:
                    wait_time = 2 ** attempt  # 指数退避
                    logger.warning(f"请求失败，{wait_time}秒后重试: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"请求失败，已达到最大重试次数: {e}")
                    raise
    
    def generate_content(self, prompt: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成内容
        
        Args:
            prompt: 提示词
            params: 生成参数
            
        Returns:
            Dict: 生成结果
        """
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            **(params or {})
        }
        
        response = self._make_request('v1/chat/completions', method='POST', data=data)
        
        if not response or 'choices' not in response:
            logger.error(f"API响应格式错误: {response}")
            return {"content": ""}
            
        content = response['choices'][0]['message']['content']
        return {"content": content}
    def check_status(self) -> Dict[str, Any]:
        """检查API服务状态
        
        Returns:
            Dict: 服务状态信息
        """
        return self._make_request("status")