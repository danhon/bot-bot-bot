import re

text = "A post with a #hashtag in it and #another one."
parts = re.split(r'(#\w+)', text)

result = [part for part in parts if part]

# for fragment in result:
#     print(fragment)
#     if re.match(r'#\w+', fragment):
#         print(f"Found hashtag: {fragment}")

print(result)

for fragment in result:
    if re.match(r'#\w+', fragment):
        print("start hashtag + ", fragment, " + end")
    else:
        print(fragment)

