message = input('>')
digits_map = {
    "1" : "One",
    "2" : "Two",
    "3" : "Three"
}
output = None #None = null
for i in message:
    output = (digits_map.get(i, "x"))
    print(output)
print('fim')

emojis = {
    ":)" : ""
}