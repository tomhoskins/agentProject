from functions.get_file_content import get_file_content
from utils.config import MAX_CHARS

test1_content = get_file_content("calculator", "lorem.txt")
test1_length = len(test1_content)
test1_truncate_string_present = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]' in test1_content
print(f"Test 1: Length of returned content: {test1_length}. Truncation string present: {test1_truncate_string_present}.")

test2 = get_file_content("calculator", "main.py")
test3 = get_file_content("calculator", "pkg/calculator.py")
test4 = get_file_content("calculator", "/bin/cat") 
test5 = get_file_content("calculator", "pkg/does_not_exist.py")

print(test2)
print(test3)
print(test4)
print(test5)