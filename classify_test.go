package main

import "testing"

// one returns the single routed line, or "" when the input is dropped.
func one(t *testing.T, in string) (Bucket, string) {
	t.Helper()
	rs := routeLine(in)
	if len(rs) == 0 {
		return -1, ""
	}
	return rs[0].Bucket, rs[0].Line
}

func TestRouting(t *testing.T) {
	cases := []struct {
		in     string
		bucket Bucket
		want   string
	}{
		// hosts syntax
		{"127.0.0.1 ads.example.com", BucketEasylist, "||ads.example.com^"},
		{"0.0.0.0 ads.example.com", BucketEasylist, "||ads.example.com^"},
		{"0.0.0.0\tads.example.com", BucketEasylist, "||ads.example.com^"},
		{"  0.0.0.0 ads.example.com  ", BucketEasylist, "||ads.example.com^"},
		{"0.0.0.0 Ads.Example.COM", BucketEasylist, "||ads.example.com^"}, // lowercase
		{":: ads.example.com", BucketEasylist, "||ads.example.com^"},
		{"::1 owu.se", BucketEasylist, "||owu.se^"}, // ::1 is a sink, not accelerate
		{"1.2.3.4 ad-maven.com", BucketAccelerate, "1.2.3.4 ad-maven.com"},
		{"0.0.0.0 ads.example.com # trailing note", BucketEasylist, "||ads.example.com^"},

		// reserved / invalid -> never emitted
		{"::1 ip6-localhost", -1, ""},
		{"127.0.0.2 localhost", -1, ""},
		{"0.0.0.0 broadcasthost", -1, ""},
		{"0.0.0.0 com", -1, ""},

		// adblock syntax routing by consumer
		{"||domain.com^", BucketEasylist, "||domain.com^"},
		{"@@||domain.com^", BucketEasylist, "@@||domain.com^"},
		{"||domain.com^$important", BucketEasylist, "||domain.com^$important"},
		{"@@||good.com^$important", BucketEasylist, "@@||good.com^$important"},
		{"||domain.com^$dnsrewrite=1.2.3.4", BucketEasylist, "||domain.com^$dnsrewrite=1.2.3.4"},
		{"||domain.com^$third-party", BucketAdblock, "||domain.com^$third-party"},
		{"@@||domain.com^$generichide", BucketAdblock, "@@||domain.com^$generichide"},
		{"||domain.com/path.js$important", BucketAdblock, "||domain.com/path.js$important"},
		{"||*.doubleclick.net^", BucketAdblock, "||*.doubleclick.net^"},
		{"||at*.doubanio.com", BucketAdblock, "||at*.doubanio.com"},
		{"/adframe[0-9]+/", BucketEasylist, "/adframe[0-9]+/"},
		{"example.org##.ad", BucketAdblock, "example.org##.ad"},
		{"! a comment", -1, ""},
		{"# a comment", -1, ""},
	}
	for _, c := range cases {
		gotBucket, gotLine := one(t, c.in)
		if gotBucket != c.bucket || gotLine != c.want {
			t.Errorf("routeLine(%q) = (%v,%q), want (%v,%q)", c.in, gotBucket, gotLine, c.bucket, c.want)
		}
	}
}

func TestMultiHostExpansion(t *testing.T) {
	rs := routeLine("127.0.0.1 a.com b.com c.com")
	if len(rs) != 3 {
		t.Fatalf("got %d rules, want 3: %v", len(rs), rs)
	}
	for i, want := range []string{"||a.com^", "||b.com^", "||c.com^"} {
		if rs[i].Line != want {
			t.Errorf("rule %d = %q, want %q", i, rs[i].Line, want)
		}
	}
}

func TestDomainOf(t *testing.T) {
	cases := map[string]string{
		"||a.com^":         "a.com",
		"@@||b.com^":       "b.com",
		"@@||c.com^$x":     "c.com",
		"1.2.3.4 d.com":    "d.com",
		"||e.com/path$y":   "e.com",
		"example.org##.ad": "",
	}
	for in, want := range cases {
		if got := domainOf(in); got != want {
			t.Errorf("domainOf(%q) = %q, want %q", in, got, want)
		}
	}
}

func TestDedupe(t *testing.T) {
	got := dedupe([]string{"a", "b", "a", "", "c", "b"})
	want := []string{"a", "b", "c"}
	if len(got) != len(want) {
		t.Fatalf("got %v, want %v", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Errorf("index %d = %q, want %q", i, got[i], want[i])
		}
	}
}
