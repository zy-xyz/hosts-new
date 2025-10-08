# 🛡️ hosts-new



轻量级、可自定义的广告 / 跟踪 / 恶意域名屏蔽项目。  

基于多线程抓取 → 进程池清洗 → 三类别输出，规则实时更新。



---



## 📦 规则文件


| 文件               | 作用说明                       | 原始直链                                                                                        | 加速镜像                                                                                                    |                                                                                           |                                                                                                       |
| ---------------- | -------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `accelerate.txt` | GitHub加速steam加速         | [GitHub](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/accelerate.txt) | [ghfast.top](https://ghfast.top/https://raw.githubusercontent.com/zy-xyz/hosts-new/main/accelerate.txt) |                                                                                           |                                                                                                       |
| `easylist.txt`   | AdGuard Home可直接订阅的规则                                                                                            | [GitHub](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/easylist.txt) | [ghfast.top](https://ghfast.top/https://raw.githubusercontent.com/zy-xyz/hosts-new/main/easylist.txt) |
| `adblock.txt`    | adblock规则                 | [GitHub](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/adblock.txt)    | [ghfast.top](https://ghfast.top/https://raw.githubusercontent.com/zy-xyz/hosts-new/main/adblock.txt)    |                                                                                           |                                                                                                       |




> 若 GitHub 链接加载失败，请优先使用 **ghfast.top** 镜像；如仍无法访问，请检查本地网络或稍后重试。



---



## 🚀 快速开始





1. 自建更新

```bash

git clone https://github.com/zy-xyz/hosts-new.git

cd hosts-new

python3 main.py          # 生成最新规则

```

## 最后插播一条广告
欢迎大家使用我的自建 DNS ，在去广告的基础上同时含义加速 steam 、Google 、github ，以及分流等功能，欢迎使用
DoH：
https://dns.acezy.top/dns-query //edgeone 加速家宽服务器
https://ali.acezy.top:444/dns-query //阿里云服务器成都节点
DOT: 
tls://ali.acezy.top
DOQ:
quic://ali.acezy.top 
同时服务器维护不易，还请各位多多支持
![微信](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/mm_facetoface_collect_qrcode_1759930989054.png)
![支付宝](https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/1759930373305.jpg)

