#!/bin/bash
# 构建MkDocs文档 (使用 EEnotes 仓库)

set -e

echo "🔨 构建MkDocs文档..."

# 进入文档源目录
cd docs_source

# 更新 submodule (如果需要)
git pull origin main || true

# 创建临时配置文件
# 1. 移除 custom_dir、overrides 相关配置
# 2. 移除自定义的 CSS/JS 引用
# 3. 设置 docs_dir 为当前目录
# 4. 设置 site_dir 为输出目录

# 移除 custom_dir 和所有包含 overrides/themes 的行
cat mkdocs.yml | \
  grep -v "custom_dir:" | \
  grep -v "overrides" | \
  grep -v "themes/" | \
  grep -v "javascripts/navigation.js" | \
  grep -v "stylesheets/custom.css" | \
  grep -v "stylesheets/neoteroi-mkdocs.css" | \
  grep -v "stylesheets/simpleLightbox.min.css" | \
  grep -v "stylesheets/pied_piper.css" > mkdocs.build.yml

# 添加目录配置
cat >> mkdocs.build.yml << 'EOF'

# Build configuration (custom overrides removed)
docs_dir: .
site_dir: ../static/notes
EOF

# 使用临时配置构建
mkdocs build --clean --config-file mkdocs.build.yml

# 修复生成文件的权限，确保 Nginx 可以读取
cd ../static/notes
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
cd ../../docs_source

# 清理临时文件
rm mkdocs.build.yml

echo "✅ 文档构建完成！"
echo "📄 输出目录: static/notes/"
echo "🌐 本地预览: cd docs_source && mkdocs serve"
