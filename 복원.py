import base64

with open("decode_csv.b64", "r") as f:
    encoded = f.read()

decoded = base64.b64decode(encoded)

with open("data/sample_data.csv", "wb") as f:
    f.write(decoded)

print("✅ sample_data.csv 복원 완료")
