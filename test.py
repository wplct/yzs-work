import unittest
import os

# 用例的路径
case_path = os.path.join(os.getcwd(), "tests")
# 报告存放的路径
report_path = os.path.join(os.getcwd(), "report")


def all_cases():
    discover = unittest.defaultTestLoader.discover(case_path, pattern="test*.py", top_level_dir=None)
    return discover


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(all_cases())
