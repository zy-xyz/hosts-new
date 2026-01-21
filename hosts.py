import os, requests, shutil, re, glob, ipaddress, functools
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


links = [
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/ChineseFilter/sections/adservers.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/ChineseFilter/sections/allowlist.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/ChineseFilter/sections/antiadblock.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/ChineseFilter/sections/general_elemhide.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/ChineseFilter/sections/general_url.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/ChineseFilter/sections/general_elemhide.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/adservers.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/allowlist.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/allowlist_stealth.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/banner_sizes.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/antiadblock.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/banner_sizes.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/general_elemhide.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/general_url.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/refs/heads/master/BaseFilter/sections/general_elemhide.txt",
    "https://raw.githubusercontent.com/geoisam/FuckScripts/main/adsfuck.txt",
    "https://easylist-downloads.adblockplus.org/easylistchina.txt",
    "https://perflyst.github.io/PiHoleBlocklist/SmartTV-AGH.txt",
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt",
    "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt",
    "https://filters.adtidy.org/windows/filters/224_optimized.txt",
    "https://raw.githubusercontent.com/lingeringsound/10007/main/all",
    "https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts",
    "https://github.com/Potterli20/file/releases/download/github-hosts/Accelerate-Hosts.txt",
    "https://github.com/Potterli20/file/releases/download/github-hosts/gfw-hosts.txt",
    "https://anti-ad.net/easylist.txt",
    "https://raw.githubusercontent.com/jianboy/github-host/master/hosts",
    "https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt",
    "https://raw.githubusercontent.com/zsakvo/AdGuard-Custom-Rule/master/rule/zhihu-strict.txt",
    "https://raw.githubusercontent.com/ineo6/hosts/refs/heads/master/hosts",
    "https://raw.hellogithub.com/hosts",
    "https://raw.githubusercontent.com/zsokami/ACL4SSR/main/hosts",
    "https://raw.githubusercontent.com/Clov614/SteamHostSync/main/Hosts",
    "https://raw.githubusercontent.com/entr0pia/fcm-hosts/fcm/fcm-hosts",
    "https://raw.githubusercontent.com/JohyC/Hosts/refs/heads/main/hosts.txt",
    "https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/allow.txt",
    "https://raw.githubusercontent.com/zy-xyz/hosts-new/refs/heads/main/diy.txt",
    "https://github-hosts.tinsfox.com/hosts",
    "https://github.com/laylavish/uBlockOrigin-HUGE-AI-Blocklist/raw/refs/heads/main/list.txt",
    "https://github.com/laylavish/uBlockOrigin-HUGE-AI-Blocklist/raw/refs/heads/main/noai_hosts.txt",
    "https://raw.githubusercontent.com/obgnail/chinese-internet-is-dead/master/blocklist.txt",
    "https://raw.githubusercontent.com/geoisam/FuckScripts/main/adfuck.txt"      
]
dead_hosts = [
    "https://raw.githubusercontent.com/notracking/hosts-blocklists-scripts/master/domains.dead.txt",
    "https://raw.githubusercontent.com/notracking/hosts-blocklists-scripts/master/hostnames.dead.txt"
]

CACHE = "cache"
OUTPUT = "hosts"
MAX_WORKERS = 8
MAX_PROC_WORKERS = os.cpu_count()

def clear_cache():
    if os.path.exists(CACHE):
        shutil.rmtree(CACHE)
    os.makedirs(CACHE)

def fetch(url, path):
    """下载单个链接，返回 (是否成功, url, 错误信息)"""
    s = Session()
    s.mount('https://', HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1)))
    try:
        response = s.get(url, timeout=10)
        response.raise_for_status()  # 检查HTTP状态码
        open(path, 'wb').write(response.content)
        return True, url, None
    except Exception as e:
        return False, url, str(e)

def run_fetch():
    """并发下载所有链接并统计结果"""
    clear_cache()
    tasks = ([(url, f"{CACHE}/host-{i}") for i, url in enumerate(links, 1)] +
             [(url, f"{CACHE}/dead_host-{i}") for i, url in enumerate(dead_hosts, 1)])
    
    success_urls = []
    failed_urls = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        # 提交所有任务
        future_to_url = {
            pool.submit(fetch, url, path): url 
            for url, path in tasks
        }
        
        # 逐个获取结果（使用as_completed可以边下载边显示）
        for future in as_completed(future_to_url):
            success, url, error = future.result()
            if success:
                success_urls.append(url)
                print(f"✓ 成功: {url}")
            else:
                failed_urls.append((url, error))
                print(f"✗ 失败: {url} - {error}")
    
    # 打印汇总报告
    print("\n" + "="*60)
    print(f"下载完成！总计: {len(tasks)} | 成功: {len(success_urls)} | 失败: {len(failed_urls)}")
    print("="*60)
    
    if success_urls:
        print("\n[成功的链接]")
        for url in success_urls:
            print(f"  - {url}")
    
    if failed_urls:
        print("\n[失败的链接]")
        for url, error in failed_urls:
            print(f"  - {url}")
            print(f"    错误: {error}")
    
    return success_urls, failed_urls

def load() -> tuple[list, set]:
    hosts, dead = [], []
    for pat, dst in (("host-*", hosts), ("dead_host-*", dead)):
        for f in glob.glob(os.path.join(CACHE, pat)):
            with open(f, encoding='utf-8', errors='ignore') as fp:
                dst.extend(fp.read().splitlines())
    return hosts, set(dead)

def clean_lines(hosts: list, black: set) -> list:
    cleaned = []
    for line in hosts:
        stripped = line.strip()
        if not stripped or stripped.startswith(( '!', '[', '<')):
            continue
        line = re.sub(r'^(0\.0\.0\.0|::)\s+', '127.0.0.1 ', line)
        # 检查是否包含黑名单中的域名
        if any(domain in stripped for domain in black):
            continue
        cleaned.append(line)
    return list(dict.fromkeys(cleaned))

IPV4_RE = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}$')
IPV6_RE = re.compile(r'^(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$')

def is_ip(addr: str) -> bool:
    try:
        ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False

def _process_chunk(lines: list, black: set) -> tuple[list, list, list]:
    acc, easy, adblock = [], [], []
    for line in lines:
        line = line.strip()
        if not line or line.startswith(('#', '!', '[', '<')):
            continue
        line = re.sub(r'^(0\.0\.0\.0|::)\s+', '127.0.0.1 ', line)

        parts = line.split()
        if len(parts) >= 2:
            try:
                ipaddress.ip_address(parts[0])
                if parts[0] == '127.0.0.1':
                    domain = parts[1]
                    if domain not in black:
                        easy.append(f'||{domain}^')
                else:
                    acc.append(line)
                continue
            except ValueError:
                pass

        if line.endswith('^') and (line.startswith('||') or line.startswith('@@||')):
            domain = line[2:-1].split('/', 1)[0]
            if domain not in black:
                easy.append(line)
        else:
            adblock.append(line)

    return acc, easy, adblock

def parallel_classify(all_lines: list, black: set) -> tuple[list, list, list]:
    chunk_size = max(1, len(all_lines) // MAX_PROC_WORKERS)
    chunks = [all_lines[i:i + chunk_size] for i in range(0, len(all_lines), chunk_size)]

    with ProcessPoolExecutor(max_workers=MAX_PROC_WORKERS) as pool:
        results = pool.map(
            functools.partial(_process_chunk, black=black),
            chunks
        )

    acc_total, easy_total, ad_total = [], [], []
    for acc, easy, ad in results:
        acc_total.extend(acc)
        easy_total.extend(easy)
        ad_total.extend(ad)
    return acc_total, easy_total, ad_total

def build():
    hosts, dead = load()
    acc_hosts, easylist, adblock = parallel_classify(hosts, dead)

    with open("accelerate.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(acc_hosts))
    with open("easylist.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(easylist))
    with open("adblock.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(adblock))

    # 打印文件统计
    print(f"\n成功生成文件:")
    print(f"  - accelerate.txt: {len(acc_hosts)} 行")
    print(f"  - easylist.txt: {len(easylist)} 行")
    print(f"  - adblock.txt: {len(adblock)} 行")

if __name__ == "__main__":
    success_urls, failed_urls = run_fetch()
    build()
