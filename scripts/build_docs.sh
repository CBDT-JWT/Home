#!/bin/bash
# 构建MkDocs文档

set -e

echo "🔨 构建MkDocs文档..."

cd docs_source
mkdocs build --clean

echo "✅ 文档构建完成！"
echo "📄 输出目录: static/notes/"
echo "🌐 本地预览: cd docs_source && mkdocs serve"
