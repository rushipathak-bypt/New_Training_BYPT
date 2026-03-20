text = input("Enter a String: ").lower()
count = 0
for i in text:
    if i in "aeiou":
        count += 1
print(f"Number of vowels in {text} are {count}")
