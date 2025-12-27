from functions.run_python_file import run_python_file

test1_args = ["calculator", "main.py"]
test2_args = ["calculator", "main.py", ["3 + 5"]]
test3_args = ["calculator", "tests.py"]
test4_args = ["calculator", "../main.py"]
test5_args = ["calculator", "nonexistent.py"]
test6_args = ["calculator", "lorem.txt"]

test1 = run_python_file(test1_args[0], test1_args[1])
test2 = run_python_file(test2_args[0], test2_args[1], test2_args[2])
test3 = run_python_file(test3_args[0], test3_args[1])
test4 = run_python_file(test4_args[0], test4_args[1])
test5 = run_python_file(test5_args[0], test5_args[1])
test6 = run_python_file(test6_args[0], test6_args[1])

print(f"Test 1:\nArguments:\n{test1_args}\nOutput:\n{test1}\n")
print(f"Test 2:\nArguments:\n{test2_args}\nOutput:\n{test2}\n")
print(f"Test 3:\nArguments:\n{test3_args}\nOutput:\n{test3}\n")
print(f"Test 4:\nArguments:\n{test4_args}\nOutput:\n{test4}\n")
print(f"Test 5:\nArguments:\n{test5_args}\nOutput:\n{test5}\n")
print(f"Test 6:\nArguments:\n{test6_args}\nOutput:\n{test6}\n")
