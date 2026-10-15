package main

import (
	"os"
	"strings"
)

// dedupe removes duplicate lines while preserving first-seen order.
func dedupe(lines []string) []string {
	seen := make(map[string]struct{}, len(lines))
	out := lines[:0:0]
	for _, l := range lines {
		if l == "" {
			continue
		}
		if _, ok := seen[l]; ok {
			continue
		}
		seen[l] = struct{}{}
		out = append(out, l)
	}
	return out
}

// writeOutput dedupes, sorts stably and appends a trailing newline.
func writeOutput(path string, lines []string) error {
	lines = dedupe(lines)
	if len(lines) == 0 {
		return os.WriteFile(path, nil, 0o644)
	}
	return os.WriteFile(path, []byte(strings.Join(lines, "\n")+"\n"), 0o644)
}

// domainOf extracts the hostname token a consumer would act on.
func domainOf(line string) string {
	s := line
	if i := strings.Index(s, "@@||"); i == 0 {
		s = s[4:]
	} else if strings.HasPrefix(s, "||") {
		s = s[2:]
	} else {
		f := strings.Fields(s)
		if len(f) >= 2 {
			return strings.ToLower(f[1])
		}
		return ""
	}
	if i := strings.IndexAny(s, "^/$"); i >= 0 {
		s = s[:i]
	}
	return strings.ToLower(s)
}
