import os, requests, shutil, re, glob, ipaddress, functools

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

links = [
        "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt",
        "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt",
    	"https://perflyst.github.io/PiHoleBlocklist/SmartTV-AGH.txt",
        "https://easylist-downloads.adblockplus.org/easylist.txt",
  	"https://easylist-downloads.adblockplus.org/easylistchina.txt",
   	"https://easylist-downloads.adblockplus.org/easyprivacy.txt",
  	"https://raw.githubusercontent.com/Noyllopa/NoAppDownload/master/NoAppDownload.txt",
        "https://raw.githubusercontent.com/sjhgvr/oisd/main/abp_small.txt",
        "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
        "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt",
        "https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt",
	"https://easylist-downloads.adblockplus.org/easylist.txt",
	"https://filters.adtidy.org/windows/filters/224_optimized.txt",
	"https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt",
	"https://easylist.to/easylist/fanboy-annoyance.txt",
	"https://easylist.to/easylist/easyprivacy.txt",
	"https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt",
	"https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
 	"https://malware-filter.gitlab.io/malware-filter/urlhaus-filter-hosts-online.txt",
 	"https://raw.githubusercontent.com/lingeringsound/10007/main/all",
	"https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts",
	"https://raw.githubusercontent.com/crazy-max/WindowsSpyBlocker/master/data/hosts/spy.txt",
 	"https://easylist-downloads.adblockplus.org/antiadblockfilters.txt",
	"https://easylist-downloads.adblockplus.org/easylistchina.txt",
	"https://filters.adtidy.org/android/filters/15_optimized.txt",
	"https://filters.adtidy.org/extension/ublock/filters/224.txt",
	"https://filters.adtidy.org/extension/ublock/filters/11.txt",
	"https://github.com/Potterli20/file/releases/download/github-hosts/Accelerate-Hosts.txt",
	"https://anti-ad.net/easylist.txt",
	"https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts",
	"https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockfilters.txt",
	"https://raw.githubusercontent.com/pboymt/Steam520/main/hosts",
	"https://raw.githubusercontent.com/rentianyu/Ad-set-hosts/master/adguard",
	"https://lingeringsound.github.io/adblock_auto/Rules/adblock_auto.txt",
	"https://lingeringsound.github.io/adblock_auto/Rules/adblock_auto_lite.txt",
	"https://raw.fgit.ml/lingeringsound/adblock/master/Toutiao_block.txt",
	"https://raw.githubusercontent.com/uniartisan/adblock_list/master/adblock_plus.txt",
	"https://raw.githubusercontent.com/uniartisan/adblock_list/master/adblock_privacy.txt",
	"https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt",
	"https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt",
	"https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt",
	"https://raw.githubusercontent.com/banbendalao/ADgk/master/kill-baidu-ad.txt",
	"https://raw.githubusercontent.com/jianboy/github-host/master/hosts",
	"https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt",
	"https://raw.githubusercontent.com/zsakvo/AdGuard-Custom-Rule/master/rule/zhihu-strict.txt",
	"https://small.oisd.nl/",
	"https://raw.githubusercontent.com/francis-zhao/quarklist/master/dist/quarklist.txt",
	"https://raw.githubusercontent.com/neodevpro/neodevhost/master/lite_adblocker",
	"https://raw.githubusercontent.com/Cats-Team/AdRules/main/adblock_lite.txt",
	"https://gitlab.com/ineo6/hosts/-/raw/master/next-hosts",
	"https://raw.hellogithub.com/hosts",
	"https://raw.githubusercontent.com/Noyllopa/NoAppDownload/master/NoAppDownload.txt",
	"https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts",
	"https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
	"https://cdn.jsdelivr.net/gh/sbwml/halflife-list@master/ad.txt",
	"https://raw.githubusercontent.com/596546419/ad-filters-subscriber/main/rule/local-rule.txt",
	"https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/adblock.txt",
	"https://raw.githubusercontent.com/8680/GOODBYEADS/master/data/rules/allow.txt",
	"https://raw.githubusercontent.com/zsokami/ACL4SSR/main/hosts",
	"https://raw.githubusercontent.com/Clov614/SteamHostSync/main/Hosts",
	"https://github.com/entr0pia/fcm-hosts/raw/fcm/fcm-hosts",
	"https://raw.githubusercontent.com/JohyC/Hosts/refs/heads/main/hosts.txt",
	"https://raw.githubusercontent.com/geoisam/FuckScripts/main/adfuck.txt"    
]
dead_hosts = [
    "https://git.acezy.top/https://raw.githubusercontent.com/notracking/hosts-blocklists-scripts/master/domains.dead.txt",
    "https://git.acezy.top/https://raw.githubusercontent.com/notracking/hosts-blocklists-scripts/master/hostnames.dead.txt"
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
    try:
        open(path, "wb").write(requests.get(url, timeout=10).content)
    except Exception:
        pass

def run_fetch():
    clear_cache()
    tasks = ([(url, f"{CACHE}/host-{i}") for i, url in enumerate(links, 1)] +
             [(url, f"{CACHE}/dead_host-{i}") for i, url in enumerate(dead_hosts, 1)])
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        for url, path in tasks:
            pool.submit(fetch, url, path)

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
        if not stripped or stripped.startswith(('#', '!', '[', '<')):
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

# ---------- 2. 纯 CPU 的处理放进进程池 ----------
def _process_chunk(lines: list, black: set) -> tuple[list, list]:
    """
    纯函数：给进程池执行，返回 (acc_hosts, easylist)
    """
    acc, easy, adblock = [], [], []
    for line in lines:
        line = line.strip()
        if not line or line.startswith(('#', '!', '[', '<')):
            continue
        line = re.sub(r'^(0\.0\.0\.0|::)\s+', '127.0.0.1 ', line)

        # 黑名单快速过滤：先粗后细
        if any(d in line for d in black):
            continue

        parts = line.split()
        if len(parts) >= 2:
            try:
                ipaddress.ip_address(parts[0])
                # 只要是以 127.0.0.1 打头的 hosts 行，都转成 ||domain^
                if parts[0] == '127.0.0.1':
                    domain = parts[1]
                    if domain not in black:
                        easy.append(f'||{domain}^')
                # 其它 IP（如 0.0.0.0）想保留就放到 acc，不想保留可删除
                else:
                    acc.append(line)
                continue
            except ValueError:
                pass

        # 其余情况
        if line.endswith('^') and (line.startswith('||') or line.startswith('@@||')):
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

if __name__ == "__main__":
    run_fetch()
    build()