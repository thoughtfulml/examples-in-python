Rationales behind some changes:

1. Change package names like 'naive-bayes' to valid Python identifiers.
The package with invalid name can be imported only with special code like:

```naive_bayes = __import__('naive-bayes')```

instead of

```import naive_bayes```

when package  name is a valid Python identifier.

2. Pre-2.1 Python classes are not used, because they are not properly integrated into type system.

3. EmailObject.file is removed, because it creates useless entanglement

4. The variable name 'file' is not used because overrides the built-in function 'file'.

5. 'file' is not closed by EmailObject, because it violates SRP (the 'file' object is owned and opened by caller).

6. The standard Python idiom `with open('name') as fp:` used because it provides
  exceptional stability (it closes file if any exception occurs inside the block).
  
This 
  
```
with open('name') as fp:
    do_something(fp)
```

is short equivalent (approximately) of:
  
```
try:
    fp = open('name')
    do_something(fp)
finally:
    fp.close()
```

