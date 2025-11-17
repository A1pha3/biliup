#!/usr/bin/env python3
"""
文档质量检查脚本
检查中文文档的语法、标点、术语和格式规范
"""

import re
import os
from pathlib import Path
from typing import List, Tuple, Dict

class DocQualityChecker:
    def __init__(self, docs_dir: str = "docs/content/docs"):
        self.docs_dir = Path(docs_dir)
        self.issues = []
        
    def check_all_files(self):
        """检查所有 Markdown 文件"""
        md_files = list(self.docs_dir.rglob("*.md"))
        print(f"找到 {len(md_files)} 个文档文件")
        
        for md_file in md_files:
            self.check_file(md_file)
        
        return self.issues
    
    def check_file(self, filepath: Path):
        """检查单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # 检查各种问题
            self.check_punctuation(filepath, lines)
            self.check_spacing(filepath, lines)
            self.check_terminology(filepath, lines)
            self.check_code_blocks(filepath, content)
            
        except Exception as e:
            print(f"错误: 无法读取文件 {filepath}: {e}")
    
    def check_punctuation(self, filepath: Path, lines: List[str]):
        """检查标点符号使用"""
        for i, line in enumerate(lines, 1):
            # 跳过代码块
            if line.strip().startswith('```') or line.strip().startswith('    '):
                continue
            
            # 检查中文标点后是否有多余空格
            if re.search(r'[，。！？；：、][ ]+', line):
                self.issues.append({
                    'file': str(filepath),
                    'line': i,
                    'type': '标点符号',
                    'issue': '中文标点符号后有多余空格',
                    'content': line.strip()
                })
            
            # 检查英文/数字后使用中文括号
            if re.search(r'[a-zA-Z0-9][（）]', line):
                self.issues.append({
                    'file': str(filepath),
                    'line': i,
                    'type': '标点符号',
                    'issue': '英文/数字后应使用英文括号',
                    'content': line.strip()
                })
    
    def check_spacing(self, filepath: Path, lines: List[str]):
        """检查中英文混排的空格"""
        for i, line in enumerate(lines, 1):
            # 跳过代码块、链接、front matter
            if (line.strip().startswith('```') or 
                line.strip().startswith('    ') or
                line.strip().startswith('+++') or
                line.strip().startswith('---') or
                '[' in line and '](' in line):
                continue
            
            # 检查中文和英文之间缺少空格（排除特殊情况）
            # 中文后直接跟英文字母
            if re.search(r'[\u4e00-\u9fff][a-zA-Z]', line):
                # 排除常见的合理情况
                if not re.search(r'(https?://|www\.|\.md|\.py|\.rs|\.js|\.ts)', line):
                    self.issues.append({
                        'file': str(filepath),
                        'line': i,
                        'type': '空格',
                        'issue': '中文和英文之间缺少空格',
                        'content': line.strip()[:100]
                    })
            
            # 英文后直接跟中文
            if re.search(r'[a-zA-Z][\u4e00-\u9fff]', line):
                if not re.search(r'(https?://|www\.|\.md|\.py|\.rs|\.js|\.ts)', line):
                    self.issues.append({
                        'file': str(filepath),
                        'line': i,
                        'type': '空格',
                        'issue': '英文和中文之间缺少空格',
                        'content': line.strip()[:100]
                    })
    
    def check_terminology(self, filepath: Path, lines: List[str]):
        """检查术语一致性"""
        # 常见术语对照表
        terminology_map = {
            'cookie': 'Cookie',
            'api': 'API',
            'url': 'URL',
            'json': 'JSON',
            'yaml': 'YAML',
            'toml': 'TOML',
            'http': 'HTTP',
            'https': 'HTTPS',
            'websocket': 'WebSocket',
            'id': 'ID',
        }
        
        for i, line in enumerate(lines, 1):
            # 跳过代码块
            if line.strip().startswith('```') or line.strip().startswith('    '):
                continue
            
            for wrong, correct in terminology_map.items():
                # 检查小写术语（排除代码中的情况）
                if re.search(rf'\b{wrong}\b', line, re.IGNORECASE):
                    if '`' not in line:  # 不在代码标记中
                        actual = re.search(rf'\b{wrong}\b', line, re.IGNORECASE).group()
                        if actual != correct and actual.lower() == wrong:
                            self.issues.append({
                                'file': str(filepath),
                                'line': i,
                                'type': '术语',
                                'issue': f'术语 "{actual}" 应为 "{correct}"',
                                'content': line.strip()[:100]
                            })
    
    def check_code_blocks(self, filepath: Path, content: str):
        """检查代码块格式"""
        # 检查代码块是否有语言标识
        code_blocks = re.finditer(r'```(\w*)\n', content)
        for match in code_blocks:
            if not match.group(1):
                line_num = content[:match.start()].count('\n') + 1
                self.issues.append({
                    'file': str(filepath),
                    'line': line_num,
                    'type': '代码块',
                    'issue': '代码块缺少语言标识',
                    'content': '```'
                })
    
    def generate_report(self):
        """生成检查报告"""
        if not self.issues:
            print("\n✅ 未发现问题！所有文档符合规范。")
            return
        
        print(f"\n⚠️  发现 {len(self.issues)} 个问题：\n")
        
        # 按类型分组
        by_type = {}
        for issue in self.issues:
            issue_type = issue['type']
            if issue_type not in by_type:
                by_type[issue_type] = []
            by_type[issue_type].append(issue)
        
        # 打印每种类型的问题
        for issue_type, issues in sorted(by_type.items()):
            print(f"\n## {issue_type} ({len(issues)} 个问题)")
            print("-" * 80)
            
            # 只显示前10个同类问题
            for issue in issues[:10]:
                print(f"\n文件: {issue['file']}")
                print(f"行号: {issue['line']}")
                print(f"问题: {issue['issue']}")
                print(f"内容: {issue['content']}")
            
            if len(issues) > 10:
                print(f"\n... 还有 {len(issues) - 10} 个类似问题")
        
        # 生成统计
        print("\n" + "=" * 80)
        print("统计信息:")
        for issue_type, issues in sorted(by_type.items()):
            print(f"  {issue_type}: {len(issues)} 个")
        print(f"  总计: {len(self.issues)} 个")

def main():
    print("=" * 80)
    print("biliup 文档质量检查工具")
    print("=" * 80)
    
    checker = DocQualityChecker()
    checker.check_all_files()
    checker.generate_report()
    
    print("\n" + "=" * 80)
    print("检查完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()
