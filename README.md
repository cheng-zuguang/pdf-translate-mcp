# pdf-translate-mcp
According to the user input url address or uploaded pdf file for translation, and support to modify the translation content.
```
[用户输入 pdfUrl 和目标语言]
        ↓
[PDF 下载模块] → 保存本地
        ↓
[PDF 提取模块] → 文本分段提取
        ↓
[翻译模块] → 调用翻译器逐段翻译
        ↓
[翻译副本生成模块] → 生成结构化双语文档
        ↓
[用户查看/编辑] → 提供修改 API / 界面
```