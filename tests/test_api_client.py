import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import requests

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from src.script_generator.api_client import APIClient

class TestAPIClient(unittest.TestCase):
    """测试API客户端功能"""
    
    def setUp(self):
        """测试前准备工作"""
        self.api_client = APIClient(
            base_url="https://test-api.example.com/v1",
            timeout=5,
            retry_count=2,
            api_key="test-api-key"
        )
    
    @patch('requests.Session.get')
    def test_get_request(self, mock_get):
        """测试GET请求"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "data": "test data"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 执行请求
        result = self.api_client._make_request("status", method="GET")
        
        # 验证结果
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], "test data")
        
        # 验证请求参数
        mock_get.assert_called_once_with(
            "https://test-api.example.com/v1/status", 
            params=None, 
            timeout=5
        )
    
    @patch('requests.Session.post')
    def test_post_request(self, mock_post):
        """测试POST请求"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "generated": "test content"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # 执行请求
        data = {"prompt": "测试提示词"}
        result = self.api_client._make_request("generate", method="POST", data=data)
        
        # 验证结果
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["generated"], "test content")
        
        # 验证请求参数
        mock_post.assert_called_once_with(
            "https://test-api.example.com/v1/generate", 
            params=None, 
            json=data, 
            timeout=5
        )
    
    @patch('requests.Session.post')
    def test_generate_content(self, mock_post):
        """测试生成内容功能"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success", "content": "生成的内容"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # 执行请求
        result = self.api_client.generate_content(
            prompt="测试提示词",
            params={"temperature": 0.8}
        )
        
        # 验证结果
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["content"], "生成的内容")
        
        # 验证请求参数
        expected_data = {
            "prompt": "测试提示词",
            "temperature": 0.8
        }
        mock_post.assert_called_once()
        call_args = mock_post.call_args[1]
        self.assertEqual(call_args["json"]["prompt"], expected_data["prompt"])
        self.assertEqual(call_args["json"]["temperature"], expected_data["temperature"])
    
    @patch('requests.Session.get')
    def test_request_retry(self, mock_get):
        """测试请求重试功能"""
        # 设置第一次请求失败，第二次成功
        mock_get.side_effect = [
            requests.exceptions.ConnectionError("连接错误"),
            MagicMock(
                json=lambda: {"status": "success"},
                raise_for_status=lambda: None
            )
        ]
        
        # 执行请求
        with patch('time.sleep') as mock_sleep:  # 避免实际等待
            result = self.api_client._make_request("status", retry=1)
        
        # 验证结果
        self.assertEqual(result["status"], "success")
        
        # 验证重试
        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called_once()

if __name__ == '__main__':
    unittest.main()