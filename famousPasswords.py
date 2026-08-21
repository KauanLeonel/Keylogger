import hashlib

hashes_md5 = [
    "9a1f30943126974075dbd4d13c8018ac",
    "978f6f608df5279d4d85e700d83ac873"
]

hash_sha1 = "250e77f12a5ab6972a0895d290c4792f0a326ea8"

with open("500worst.txt", "r", encoding="utf-8") as arquivo:

    for linha in arquivo:
        palavra = linha.strip()

        md5 = hashlib.md5(palavra.encode()).hexdigest()
        sha1 = hashlib.sha1(palavra.encode()).hexdigest()

        if md5 in hashes_md5:
            print("MD5 encontrado:")
            print(palavra, "->", md5)

        if sha1 == hash_sha1:
            print("SHA1 encontrado:")
            print(palavra, "->", sha1)