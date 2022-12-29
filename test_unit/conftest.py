# conftest.py
import pytest

# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     outcome = yield
#     report = outcome.get_result()
#     if item.function.__doc__ is None:
#         report.description = str(item.function.__name__)		# 如果没有三引号注释（'''注释'''），就提取函数名到case的输出文案中，就是上面的test_id
#     else:
#         report.description = str(item.function.__doc__)			# 提取三引号注释（'''注释'''）到case的输出文案中
#     # report.nodeid = report.nodeid.encode("unicode_escape").decode("utf-8")  # 再把编码改回来
