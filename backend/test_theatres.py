import re
html = open('bms_test_failure.html', 'r', encoding='utf-8').read()
# Theatres are usually in an element with class name containing 'venue' or similar. 
# We'll just look for strong elements or something.
# Let's extract all text from div>div>div... it's a bit complex.
# We know the theatre list has a structure.
matches = re.findall(r'<a class=".*?__venue-name".*?>(.*?)</a>', html)
if matches:
    print("Theatres:", set(matches))
else:
    # Another approach: find all occurrences of "Cinepolis"
    for i, m in enumerate(re.finditer(r'Cinepolis', html)):
        start = max(0, m.start() - 100)
        end = min(len(html), m.end() + 500)
        print(f"Match {i}:", html[start:end])
