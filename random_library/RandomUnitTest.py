from Random import Random

random = Random(error=0.05)

print("---- 1. random() ----")
r = random.random()
print("Random single:", r, "OK" if 0 <= r < 1 else "FAIL")

seq = random.random(10)
print("Random sequence:", seq, "OK" if len(seq) == 10 and all(0 <= x < 1 for x in seq) else "FAIL")


print("\n---- 2. uniform() ----")
r = random.uniform(5, 10)
print("Uniform single float:", r, "OK" if 5 <= r <= 10 else "FAIL")

r = random.uniform(5, 10, integer=True)
print("Uniform single integer:", r, "OK" if isinstance(r, int) and 5 <= r <= 10 else "FAIL")

seq = random.uniform(1, 5, n=20)
print("Uniform sequence float:", seq)

seq = random.uniform(1, 5, n=20, integer=True)
print("Uniform sequence integer:", seq)


print("\n---- 3. normal() ----")
r = random.normal(0, 1)
print("Normal single:", r,)

seq = random.normal(0, 1, n=50)
print("Normal sequence: ",seq )



print("\n---- 5. choice() ----")
seq = ["a", "b", "c", "d"]
ok = True
for _ in range(20):
    choice = random.choice(seq)
    if choice not in seq:
        ok = False
print("Choice test:", "OK" if ok else "FAIL")
