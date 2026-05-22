import requests # pyright: ignore[reportMissingModuleSource]

res = requests.get("https://github.com/RishavVerma0/Journey-To-AI-Engineer")

print(dir(res))