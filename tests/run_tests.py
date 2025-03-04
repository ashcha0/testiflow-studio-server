import unittest
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

# 创建测试套件
def create_test_suite():
    # 获取测试目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建测试加载器
    loader = unittest.TestLoader()
    
    # 从测试目录加载所有测试
    suite = loader.discover(test_dir, pattern="test_*.py")
    
    return suite

if __name__ == "__main__":
    # 创建测试套件
    test_suite = create_test_suite()
    
    # 创建测试运行器
    runner = unittest.TextTestRunner(verbosity=2)
    
    # 运行测试
    result = runner.run(test_suite)
    
    # 根据测试结果设置退出代码
    sys.exit(not result.wasSuccessful())