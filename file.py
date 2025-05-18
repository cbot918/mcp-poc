
file_name = "a.txt"

try: 
    with open(file_name) as file:
        print(file.read())
except Exception as e:
    print(f"Exception:{e}")
else:
    print("successful")
finally:
    print("complete")