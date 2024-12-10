# from collections import defaultdict
# from pathlib import Path

from progman.platforms.windowsshortcutcollector import WindowsShortcutCollector
from progman.core import Tags

w = WindowsShortcutCollector()
links = w.collect_links()
for i in links:
    if Tags.HIDDEN.value not in i.tags:
        print(f"{i.name:<55}", i.target_path)

# icon_types = defaultdict(int)
# for link in links:
#     stripped_icon_path = (link.icon_path.split(",")[0] if "," in link.icon_path else link.icon_path) or link.target_path
#     path = Path(stripped_icon_path)
#     # print(path, link.icon_path.split(",")[1] if ',' in link.icon_path else '')
#     icon_types[path.suffix.lower()] += 1

# print("Summary:\n========")
# for key in sorted(icon_types, key=lambda k: icon_types[k], reverse=True):
#     print(f"{key}: {icon_types[key]/len(links) * 100:.0f}%")
