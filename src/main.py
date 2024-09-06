import os
import gencrl

os.makedirs("crl", exist_ok=True)
for i in os.listdir("data"):
    if i == "example":
        continue
    with open(os.path.join("crl", i + ".crl"), "wb") as f:
        f.write(gencrl.invoke(os.path.join("data", i)))
