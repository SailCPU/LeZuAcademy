# 🔧 GitHub Pages 访问故障排除

## 🚨 常见问题及解决方案

### 问题 1：网站显示 404 错误

**可能原因：**
- GitHub Pages 还未完全部署
- 分支或文件夹设置错误
- 文件路径问题

**解决步骤：**

1. **检查 GitHub Pages 设置**
   - 访问：`https://github.com/SailCPU/LeZuAcademy/settings/pages`
   - 确认设置如下：
     - Source: "Deploy from a branch"
     - Branch: "master"
     - Folder: "/ (root)"

2. **检查部署状态**
   - 访问：`https://github.com/SailCPU/LeZuAcademy/actions`
   - 查看是否有 "pages build and deployment" 工作流
   - 确认最新的部署是否成功（绿色✅）

3. **等待时间**
   - 首次部署：最多等待 20 分钟
   - 后续更新：等待 5-10 分钟

### 问题 2：部署失败

**检查部署日志：**
1. 进入 Actions 选项卡
2. 点击最新的 "pages build and deployment"
3. 查看错误信息

**常见错误及解决：**
- **文件编码错误**：确保所有文件使用 UTF-8 编码
- **文件名包含特殊字符**：重命名包含中文或特殊字符的文件
- **文件过大**：检查是否有超大文件需要压缩

### 问题 3：网站可以访问但内容不对

**可能原因：**
- 缓存问题
- 文件更新未同步

**解决方法：**
1. 强制刷新浏览器：`Ctrl+F5` (Windows) 或 `Cmd+Shift+R` (Mac)
2. 清除浏览器缓存
3. 使用隐私/无痕模式访问

## 🔍 具体排查步骤

### 步骤 1：确认 GitHub 设置

1. 访问您的仓库：`https://github.com/SailCPU/LeZuAcademy`
2. 点击 **Settings** 选项卡
3. 在左侧菜单找到 **Pages**
4. 检查当前配置：

应该显示：
```
✅ Your site is published at https://sailcpu.github.io/LeZuAcademy/
```

如果显示其他信息，请按照提示修正。

### 步骤 2：测试替代访问方式

如果主域名无法访问，尝试：

1. **直接访问项目页面**：
   ```
   https://sailcpu.github.io/LeZuAcademy/projects/柯南侦探英语冒险-杨乐北的单词探案记/index.html
   ```

2. **使用原始文件链接**：
   ```
   https://raw.githubusercontent.com/SailCPU/LeZuAcademy/master/index.html
   ```

### 步骤 3：检查文件是否正确上传

在 GitHub 仓库主页确认可以看到：
- ✅ `index.html` 文件（根目录）
- ✅ `projects/` 文件夹
- ✅ 最新的提交记录

## 🚀 紧急替代方案

### 方案 1：使用 GitHub Codespaces 预览

1. 在 GitHub 仓库页面点击绿色的 **< > Code** 按钮
2. 选择 **Codespaces** 选项卡
3. 点击 **Create codespace on master**
4. 在 Codespaces 中运行：
   ```bash
   python3 -m http.server 8000
   ```
5. 在端口转发中打开 8000 端口

### 方案 2：使用 Netlify 部署

1. 访问 [Netlify.com](https://netlify.com)
2. 注册/登录账户
3. 点击 "New site from Git"
4. 连接 GitHub 账户
5. 选择 `LeZuAcademy` 仓库
6. 部署设置：
   - Branch: `master`
   - Publish directory: 留空
7. 点击 "Deploy site"

### 方案 3：检查网络和 DNS

有时候访问问题可能是网络相关：

1. **更换 DNS**：
   - 使用 Google DNS: `8.8.8.8`, `8.8.4.4`
   - 使用 Cloudflare DNS: `1.1.1.1`, `1.0.0.1`

2. **使用 VPN**：
   - 尝试使用不同地区的网络访问

3. **ping 测试**：
   ```bash
   ping sailcpu.github.io
   ```

## 📞 获取帮助

### 在线工具检查

1. **GitHub Pages 状态检查**：
   - 访问：`https://www.githubstatus.com/`
   - 检查 Pages 服务是否正常

2. **DNS 传播检查**：
   - 访问：`https://www.whatsmydns.net/`
   - 输入：`sailcpu.github.io`

### 联系支持

如果以上方法都无效：

1. **创建 GitHub Issue**：
   - 在仓库中创建新的 Issue
   - 描述具体的错误信息

2. **GitHub 社区论坛**：
   - 访问：`https://github.community/`
   - 搜索类似问题或发布新问题

## 💡 预防措施

为避免未来出现类似问题：

1. **定期检查部署状态**
2. **使用简单的文件名**（避免中文和特殊字符）
3. **保持文件大小适中**
4. **定期备份重要内容**

---

## 📋 快速检查清单

- [ ] GitHub Pages 设置正确
- [ ] 最新提交已推送到 master 分支
- [ ] index.html 文件存在于根目录
- [ ] 部署 Action 运行成功
- [ ] 等待足够的时间（20分钟）
- [ ] 尝试强制刷新浏览器
- [ ] 检查网络连接和 DNS 设置

**如果清单中有任何一项未完成，请先解决该问题！**