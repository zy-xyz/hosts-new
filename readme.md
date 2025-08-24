\# 🛡️ hosts-new



轻量级、可自定义的广告 / 跟踪 / 恶意域名屏蔽项目。  

基于多线程抓取 → 进程池清洗 → 三类别输出，规则实时更新。



---



\## 📦 规则文件



| 文件       | 作用说明                                       | 原始直链 | 加速镜像 |

|------------|------------------------------------------------|----------|----------|

| `accelerate.txt` | GitHub加速链接 | \[GitHub](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/accelerate.txt) | \[ghfast.top](https://ghfast.top/https://raw.githubusercontent.com/zy-xyz/hosts-new/main/accelerate.txt) |

| `easylist.txt`   | AdGuard Home 可直接订阅的规则 | \[GitHub](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/easylist.txt) | \[ghfast.top](https://ghfast.top/https://raw.githubusercontent.com/zy-xyz/hosts-new/main/easylist.txt) |

| `adblock.txt`    | adblock规则 | \[GitHub](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/adblock.txt) | \[ghfast.top](https://ghfast.top/https://raw.githubusercontent.com/zy-xyz/hosts-new/main/adblock.txt) |



> 若 GitHub 链接加载失败，请优先使用 \*\*ghfast.top\*\* 镜像；如仍无法访问，请检查本地网络或稍后重试。



---



\## 🚀 快速开始





1. \*\*自建更新\*\*  

&nbsp;  ```bash

&nbsp;  git clone https://github.com/zy-xyz/hosts-new.git

&nbsp;  cd hosts-new

&nbsp;  python3 main.py          # 生成最新规则

&nbsp;  ```





