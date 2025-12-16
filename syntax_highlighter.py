reserved = [
"if", "elif", "else",
"while", "for",
"def", "return", "global",
"import", "from",
"continue", "break",
"del",
"in", "not", "or", "and", "is",
"raise",
"class",
]
spaceinstring = "space in string"
whitespace = [" ", "\n"]
quotes = ["'", '"']
nums = "0123456789"
abc = "abcdefghijklmnoprstuvyzwxq"
abc += abc.upper() + "_"
operators = ["=", "<", ">", "+", "-", "=", "/", "*", "?", "<=", ">=", "==", "!", "!=", "%"]
named_tokens = {
  ",": "comma",
  ".": "dot",
  "[": "bracked_begin",
  "]": "bracket_end",
  "(": "paran_begin",
  ")": "paran_end",
  "{": "curly_begin",
  "}": "curly_end",
  ";": "semicolon",
  ":": "colon",
}
quote_escape = chr(92)
reserved_identifiers = ["None", "True", "False"]

def seek_new_token():
  i = tokenizer["i"]
  if tokenizer["char"] in quotes:
    tokenizer["current_quote"] = tokenizer["char"]
    tokenizer["token"] = {"type": "string", "starts": i, "ends": i+1}
    tokenizer["tokens"].append(tokenizer["token"])
  elif tokenizer["char"] in operators:
    tokenizer["token"] = {"type": "operator", "starts": i, "ends": i+1}
    tokenizer["tokens"].append(tokenizer["token"])
  elif tokenizer["char"] in nums:
    tokenizer["token"] = {"type": "number", "starts": i, "ends": i+1}
    tokenizer["tokens"].append(tokenizer["token"])
  elif tokenizer["char"] in abc:
    tokenizer["token"] = {"type": "identifier", "starts": i, "ends": i+1}
    tokenizer["tokens"].append(tokenizer["token"])
  elif tokenizer["char"] in named_tokens:
    tokenizer["tokens"].append({"type": named_tokens[tokenizer["char"]], "starts": i, "ends": i+1})
  elif tokenizer["char"] == "#":
    tokenizer["token"] = {"type": "comment", "starts": i, "ends": i+1}
    tokenizer["tokens"].append(tokenizer["token"])
  elif tokenizer["char"] in whitespace:
    tokenizer["token"] = {"type": "whitespace", "starts": i, "ends": i+1}
    tokenizer["tokens"].append(tokenizer["token"])

tokenizer = {
  "i": 0,
  "current_quote": None,
  "token": None,
  "tokens": [],
  "char": None
}

def reset():
  tokenizer["i"] = 0
  tokenizer["current_quote"] = None
  tokenizer["token"] = None
  tokenizer["tokens"] = []
  tokenizer["char"] = None

def tokenize(text):
  reset()
  while tokenizer["i"] < len(text):
    tokenizer["char"] = text[tokenizer["i"]]
    if tokenizer["token"]:
      token_next = text[tokenizer["token"]["starts"]: tokenizer["i"]+1]
      if tokenizer["token"]["type"] == "string":
        tokenizer["token"]["ends"] += 1
        if tokenizer["char"] == tokenizer["current_quote"] and text[tokenizer["i"]-1] != quote_escape:
          tokenizer["token"] = None
          tokenizer["current_quote"] = None
      elif tokenizer["token"]["type"] == "operator":
        if token_next in operators:
          tokenizer["token"]["ends"] += 1
        else:
          tokenizer["token"] = None
          seek_new_token()
      elif tokenizer["token"]["type"] == "number":
        if tokenizer["char"] in nums:
          tokenizer["token"]["ends"] += 1
        else:
          tokenizer["token"] = None
          seek_new_token()
      elif tokenizer["token"]["type"] in ("identifier", "reserved", "reserved-identifier"):
        if tokenizer["char"] in abc or tokenizer["char"] in nums:
          tokenizer["token"]["ends"] += 1
          if token_next in reserved_identifiers:
            tokenizer["token"]["type"] = "reserved-identifier"
          elif token_next in reserved:
            tokenizer["token"]["type"] = "reserved"
          else:
            tokenizer["token"]["type"] = "identifier"
        else:
          tokenizer["token"] = None
          seek_new_token()
      elif tokenizer["token"]["type"] == "comment":
        if tokenizer["char"] == "\n":
          tokenizer["token"] = None
          seek_new_token()
        else:
          tokenizer["token"]["ends"] += 1
      elif tokenizer["token"]["type"] == "whitespace":
        if tokenizer["char"] in whitespace:
          tokenizer["token"]["ends"] += 1
        else:
          tokenizer["token"] = None
          seek_new_token()
    else:
      seek_new_token()
    tokenizer["i"] += 1
  return tokenizer["tokens"]