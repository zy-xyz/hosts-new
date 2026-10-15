package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"
)

const (
	cacheDir = "cache"
	statsDir = "docs/static/data"
	workers  = 32
)

func main() {
	full := flag.Bool("full", false, "use the extended source list (links_full.txt)")
	outDir := flag.String("out", ".", "directory to write the three output files into")
	noGate := flag.Bool("no-gate", false, "skip the output-ratio safety gate")
	flag.Parse()

	linksFile, suffix := "links.txt", ""
	if *full {
		linksFile, suffix = "links_full.txt", "_full"
	}

	urls := stripComments(readLines(linksFile))
	if len(urls) == 0 {
		log.Fatalf("no sources in %s", linksFile)
	}
	fmt.Printf("sources=%d full=%v\n", len(urls), *full)

	start := time.Now()
	results := fetchAll(urls, cacheDir, workers)

	var all []string
	diyn := 0
	for i := range results {
		if results[i].Err != nil || results[i].Path == "" {
			continue
		}
		ls := readLines(results[i].Path)
		results[i].Domains = countDomains(ls)
		all = append(all, ls...)
	}
	diy := stripComments(readLines("diy.txt"))
	diyn = len(diy)
	all = append(all, diy...)
	fmt.Printf("raw_lines=%d diy=%d\n", len(all), diyn)

	fetchElapsed := time.Since(start)

	acc, easy, ad := classify(all)

	// Diff exclusion: a domain may never be accelerated and blocked at once.
	blocked := domainSet(easy)
	for d := range domainSet(ad) {
		blocked[d] = struct{}{}
	}
	kept, conflicts := acc[:0], 0
	for _, l := range acc {
		if _, bad := blocked[domainOf(l)]; bad {
			conflicts++
			continue
		}
		kept = append(kept, l)
	}
	acc = kept
	fmt.Printf("acc_conflicts_removed=%d\n", conflicts)

	acc, easy, ad = dedupe(acc), dedupe(easy), dedupe(ad)
	buckets := BucketStats{Accelerate: len(acc), Easylist: len(easy), Adblock: len(ad)}

	// Safety gate: refuse to publish a run that lost over half of any bucket.
	prev, havePrev := previousCounts(suffix)
	if !*noGate && havePrev {
		for _, c := range []struct {
			name      string
			now, then int
		}{
			{"accelerate", buckets.Accelerate, prev.Accelerate},
			{"easylist", buckets.Easylist, prev.Easylist},
			{"adblock", buckets.Adblock, prev.Adblock},
		} {
			if c.then > 100 && c.now < c.then/2 {
				log.Fatalf("GATE: %s.txt dropped from %d to %d lines (%.1f%% loss) — refusing to publish",
					c.name, c.then, c.now, 100*(1-float64(c.now)/float64(c.then)))
			}
		}
	}

	files := map[string][]string{
		"accelerate" + suffix + ".txt": acc,
		"easylist" + suffix + ".txt":   easy,
		"adblock" + suffix + ".txt":    ad,
	}
	for name, lines := range files {
		if err := writeOutput(filepath.Join(*outDir, name), lines); err != nil {
			log.Fatalf("write %s: %v", name, err)
		}
	}

	st := buildStats(*full, results, buckets, len(all), time.Since(start))
	if err := writeStats(statsDir, st); err != nil {
		log.Fatalf("stats: %v", err)
	}
	if err := appendHistory(statsDir, st); err != nil {
		log.Fatalf("history: %v", err)
	}

	failed := len(st.FailedSources)
	fmt.Printf("fetch=%.1fs total=%.1fs failed=%d\n", fetchElapsed.Seconds(), st.DurationS, failed)
	fmt.Printf("accelerate=%d easylist=%d adblock=%d\n", buckets.Accelerate, buckets.Easylist, buckets.Adblock)
	for i, f := range st.FailedSources {
		if i >= 5 {
			fmt.Printf("  ... and %d more failed sources\n", failed-5)
			break
		}
		fmt.Printf("  FAILED %s\n", f)
	}
}

// readLines reads a text file, tolerating CRLF and a leading BOM.
func readLines(path string) []string {
	f, err := os.Open(path)
	if err != nil {
		return nil
	}
	defer f.Close()
	sc := bufio.NewScanner(f)
	sc.Buffer(make([]byte, 0, 64*1024), 4*1024*1024)
	var out []string
	for sc.Scan() {
		s := strings.TrimSuffix(strings.TrimPrefix(sc.Text(), "\ufeff"), "\r")
		if s != "" {
			out = append(out, s)
		}
	}
	return out
}

func stripComments(lines []string) []string {
	out := lines[:0]
	for _, l := range lines {
		if t := strings.TrimSpace(l); t != "" && !strings.HasPrefix(t, "#") {
			out = append(out, t)
		}
	}
	return out
}

// countDomains counts distinct domain tokens in one source's lines.
func countDomains(lines []string) int {
	seen := make(map[string]struct{}, 256)
	for _, l := range lines {
		if d := domainOf(l); d != "" {
			seen[d] = struct{}{}
		}
	}
	return len(seen)
}

func domainSet(lines []string) map[string]struct{} {
	m := make(map[string]struct{}, len(lines))
	for _, l := range lines {
		if d := domainOf(l); d != "" {
			m[d] = struct{}{}
		}
	}
	return m
}

// previousCounts reads the last history record so the gate can compare runs.
func previousCounts(suffix string) (BucketStats, bool) {
	name := "history.jsonl"
	if suffix == "_full" {
		name = "history_full.jsonl"
	}
	f, err := os.Open(filepath.Join(statsDir, name))
	if err != nil {
		return BucketStats{}, false
	}
	defer f.Close()
	sc := bufio.NewScanner(f)
	sc.Buffer(make([]byte, 0, 1<<20), 16*1024*1024)
	last := ""
	for sc.Scan() {
		if t := strings.TrimSpace(sc.Text()); len(t) > 2 {
			last = t
		}
	}
	if last == "" {
		return BucketStats{}, false
	}
	var s Stats
	if json.Unmarshal([]byte(last), &s) != nil {
		return BucketStats{}, false
	}
	return s.Buckets, true
}
