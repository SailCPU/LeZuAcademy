# 🌐 GitHub Pages 部署指南

## 📋 部署步骤

### 1. 登录 GitHub 并进入仓库

1. 打开浏览器，访问 [GitHub.com](https://github.com)
2. 登录您的账户
3. 进入仓库：`https://github.com/SailCPU/LeZuAcademy`

### 2. 启用 GitHub Pages

1. 在仓库页面中，点击 **Settings**（设置）选项卡
2. 在左侧菜单中找到 **Pages**（页面）选项
3. 在 **Source**（源）部分：
   - 选择 **Deploy from a branch**（从分支部署）
   - **Branch**（分支）选择：`master` 或 `main`
   - **Folder**（文件夹）选择：`/ (root)`（根目录）
4. 点击 **Save**（保存）

### 3. 等待部署完成

- 部署通常需要几分钟时间
- 在 **Pages** 设置页面会显示部署状态
- 部署成功后会显示您的网站地址

## 🌟 预期的网站地址

您的网站将在以下地址可访问：
```
https://sailcpu.github.io/LeZuAcademy/
```

## 📱 网站结构

部署后，访问者可以通过以下链接访问不同部分：

- **主页**：`https://sailcpu.github.io/LeZuAcademy/`
- **柯南侦探英语冒险**：`https://sailcpu.github.io/LeZuAcademy/projects/柯南侦探英语冒险-杨乐北的单词探案记/`
- **其他项目**：`https://sailcpu.github.io/LeZuAcademy/projects/`
- **文档**：`https://sailcpu.github.io/LeZuAcademy/docs/`

## 🔧 故障排除

### 如果网站无法访问：

1. **检查部署状态**：
   - 在仓库的 **Actions** 选项卡查看部署日志
   - 确保没有错误信息

2. **检查文件路径**：
   - 确保 `index.html` 在根目录下
   - 检查文件编码是否为 UTF-8

3. **等待时间**：
   - 首次部署可能需要 10-20 分钟
   - 后续更新通常 2-5 分钟生效

### 如果需要更新网站：

1. 在本地修改文件
2. 使用 git 提交更改：
   ```bash
   git add .
   git commit -m "更新内容"
   git push origin master
   ```
3. GitHub Pages 会自动重新部署

## 🎯 自定义域名（可选）

如果您有自己的域名，可以：

1. 在 **Pages** 设置中的 **Custom domain**（自定义域名）字段输入您的域名
2. 在您的域名提供商处配置 DNS：
   - 添加 CNAME 记录指向 `sailcpu.github.io`
   - 或添加 A 记录指向 GitHub Pages IP 地址

## 📊 监控和分析

- GitHub Pages 自动支持 HTTPS
- 您可以在 Google Analytics 中添加网站进行访问统计
- 使用 GitHub 的 **Insights** 查看仓库访问情况

## 🔄 持续更新

每次您向 `master` 分支推送代码时，GitHub Pages 都会自动重新构建和部署您的网站。这意味着：

- 修改项目内容后，只需 `git push` 即可更新线上版本
- 添加新的章节或项目会自动在网站上体现
- 无需手动干预，完全自动化

## 💡 优化建议

1. **性能优化**：
   - 压缩图片文件大小
   - 使用 CDN 加载外部资源

2. **SEO 优化**：
   - 为每个页面添加合适的 `<title>` 和 `<meta>` 标签
   - 使用语义化的 HTML 结构

3. **用户体验**：
   - 确保移动端适配
   - 添加加载动画和交互反馈

---

## 📞 联系支持

如果在部署过程中遇到问题，可以：
- 查看 [GitHub Pages 官方文档](https://docs.github.com/en/pages)
- 在 GitHub 仓库中创建 Issue
- 联系技术支持

🎉 **祝您部署成功！您的教育项目很快就能在全球范围内访问了！**