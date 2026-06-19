from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Union

# 示例数据：关联站点与关键词
_SAMPLE_URL = "https://leyuesports.com.cn"
_SAMPLE_KEYWORD = "乐鱼体育"


@dataclass
class KeywordNote:
    """
    保存一条关键词笔记的数据结构。

    属性:
        keyword (str): 关键词本身。
        url (str): 关联的参考链接。
        description (str): 简要说明或上下文。
        tags (List[str]): 自定义标签列表。
        created_at (Optional[datetime]): 创建时间，默认当前 UTC 时间。
        importance (Union[int, float]): 重要性打分，0-10 之间的数值。
    """
    keyword: str
    url: str
    description: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    importance: Union[int, float] = 5.0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if not 0 <= self.importance <= 10:
            raise ValueError("importance 必须在 0-10 之间")

    def short_summary(self) -> str:
        """返回一行简短的摘要（关键词 + 重要性）。"""
        return f"[{self.importance}] {self.keyword} — {self.url}"

    def full_note(self) -> str:
        """返回格式化的完整笔记字符串。"""
        lines = [
            f"关键词：{self.keyword}",
            f"链接：{self.url}",
            f"说明：{self.description}",
            f"标签：{', '.join(self.tags) if self.tags else '无'}",
            f"创建时间：{self.created_at.isoformat()}",
            f"重要性：{self.importance}",
        ]
        return "\n".join(lines)


class KeywordNotesFormatter:
    """
    负责将 KeywordNote 对象列表格式化为不同输出形式。
    """

    @staticmethod
    def format_simple_list(notes: List[KeywordNote]) -> str:
        """返回纯文本列表，每行一条摘要。"""
        if not notes:
            return "(无关键词笔记)"
        return "\n".join(note.short_summary() for note in notes)

    @staticmethod
    def format_detailed_report(notes: List[KeywordNote], title: str = "关键词笔记报告") -> str:
        """返回包含标题和完整笔记的分隔报告。"""
        parts = [f"=== {title} ==="]
        for i, note in enumerate(notes, 1):
            parts.append(f"--- 第 {i} 条 ---")
            parts.append(note.full_note())
        parts.append("=" * 30)
        return "\n".join(parts)

    @staticmethod
    def format_markdown_table(notes: List[KeywordNote]) -> str:
        """返回 Markdown 风格的表格形式。"""
        header = "| 关键词 | 链接 | 重要性 | 标签 |"
        sep = "|--------|------|--------|------|"
        rows = []
        for note in notes:
            tags = ", ".join(note.tags) if note.tags else "—"
            rows.append(f"| {note.keyword} | {note.url} | {note.importance} | {tags} |")
        return "\n".join([header, sep] + rows)


def demo_usage() -> None:
    """
    演示函数：创建几条 KeywordNote 并输出不同格式。
    """
    notes = [
        KeywordNote(
            keyword=_SAMPLE_KEYWORD,
            url=_SAMPLE_URL,
            description="乐鱼体育官方站点示例",
            tags=["体育", "官网", "测试"],
            importance=8.5,
        ),
        KeywordNote(
            keyword="电子竞技",
            url="https://example.com/esports",
            description="泛指电子竞技相关",
            tags=["电竞", "趋势"],
            importance=6.0,
        ),
        KeywordNote(
            keyword="体育新闻",
            url="https://example.com/sports-news",
            description="每日体育新闻快讯",
            tags=["新闻", "体育"],
            importance=7.2,
        ),
    ]

    print("===== 简短列表 =====")
    print(KeywordNotesFormatter.format_simple_list(notes))

    print("\n===== 详细报告 =====")
    print(KeywordNotesFormatter.format_detailed_report(notes, "演示报告"))

    print("\n===== Markdown 表格 =====")
    print(KeywordNotesFormatter.format_markdown_table(notes))


if __name__ == "__main__":
    demo_usage()