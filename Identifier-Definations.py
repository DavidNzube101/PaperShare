# DEAR Future DEVS,
# This is the definations of some of the short (also UN-UNDERSTANDABLE, super CONCISE, really LIGHTWEIGHT, really 
# EASY to type, really FAST to type) identifiers such as 
# variables, functions and classes

definations = {
  "": "No identifier mentioned!",
  "pt": "Payment Type",
  "SJI": "School Joined ID"
  # ...like 50 more to go 😭😭
}

# Usage:
try:
  identifier = "mmm" # Replace with the identifier you find confusing
  print(definations[f'{identifier}'])

except (KeyError, Exception) as you:
  print(f"Invalid Identifier: {you}\nOops, looks like the identifier doesn't exist. Remember the identifier(s) are case-sensitive.")