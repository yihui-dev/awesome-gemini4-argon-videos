#!/usr/bin/env python3
"""Validate catalog provenance, publication cutoff, and public-media verification."""
import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
load = lambda name: json.loads((ROOT / 'data' / name).read_text())
videos = load('videos.json')
posts = {p['id']: p for p in load('source-posts.json')}
collection = load('collection.json')
verification = load('verification.json')
objects = {o['url']: o for o in verification['objects']}
cutoff = dt.datetime.fromisoformat(collection['publicationCutoffUtc'].replace('Z', '+00:00'))
assert videos and len(videos) == collection['videoCount']
assert len({v['id'] for v in videos}) == len(videos)
assert len({v['sourceSha256'] for v in videos}) == len(videos), 'Duplicate original files'
assert len({v['mediaId'] for v in videos}) == len(videos)
assert len(objects) == len(videos) * 3 == verification['objectCount']
for v in videos:
    post_id = v['id'].split('-')[0]
    p = posts[post_id]
    published = dt.datetime.fromisoformat(v['publishedAt'].replace('Z', '+00:00'))
    assert published > cutoff
    assert published.timestamp() == p['publishedTimestamp']
    assert abs(((int(post_id) >> 22) + 1288834974657) / 1000 - published.timestamp()) < 2
    assert dt.datetime.fromisoformat(v['publishedAtBeijing']) == published
    assert v['originalPost'] == p['text'] and v['author']['handle'] == p['author']['handle']
    assert v['sourceUrl'] == p['url'] and post_id in v['sourceUrl']
    assert (ROOT / 'prompts' / (v['id'] + '.md')).exists()
    assert v['category'] in {'motion', '3d', 'interactive', 'comparison', 'workflow'}
    assert bool(v['prompt']) == bool(v['promptSourceUrl'])
    if v['prompt']:
        assert v['promptStatus'].startswith('verbatim')
    else:
        assert v['promptStatus'] == 'not_published_in_reviewed_sources'
    for field in ['videoUrl', 'posterUrl', 'previewUrl']:
        url = v[field]
        assert url.startswith('https://media.skillry.dev/gemini-4-argon/' + v['id'] + '/')
        assert objects[url]['publicReadback'] == 'passed'
    video = objects[v['videoUrl']]
    assert video['sha256'] == v['sourceSha256'] and video['bytes'] == v['bytes']
    assert video['byteRange'].startswith('206;')
assert collection['sourceAccountCount'] == len({v['author']['handle'] for v in videos})
assert collection['publicPromptCount'] == sum(bool(v['prompt']) for v in videos)
for name in ['README.md', 'README.zh-CN.md']:
    text = (ROOT / name).read_text()
    assert text.count('<td width="33%"') == len(videos)
    assert 'utm_campaign=awesome-gemini4-argon-videos' in text
    assert '/Users/' not in text and '/Volumes/' not in text
print(f'PASS: {len(videos)} videos; exact source text and authors; strict Beijing cutoff; {len(objects)} verified R2 assets.')
