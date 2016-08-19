# Program to create dictionary
# from 2 lists & added "None" when no key to value

keys = ['key1', 'key2', 'key3', 'key4', 'key5']
values = [1, 2, 3]
result = {}
for i  in range(len(keys)):
    try:
        result [keys[i]] = values [i]
    except:
        result[keys[i]]="None"
print(result)
