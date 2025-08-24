import os, requests, shutil, re, glob
from concurrent.futures import ThreadPoolExecutor

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
        line = re.sub(r'\s+', ' ', line.strip())
        if not line or line.startswith(('#', '!', '[', '<')) or '.' not in line:
            continue
        line = re.sub(r'^(0\.0\.0\.0|::)\s+', '127.0.0.1 ', line)
        domain = line.split()[-1]
        if domain not in black:
            cleaned.append(line)
    return list(dict.fromkeys(cleaned))

def build():
    hosts, dead = load()
    with open(OUTPUT, "w", encoding='utf-8') as f:
        f.write("\n".join(clean_lines(hosts, dead)))

if __name__ == "__main__":
    run_fetch()
    build()