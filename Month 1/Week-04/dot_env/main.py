from dotenv import load_dotenv 
import os

load_dotenv()

name = os.getenv("NAME")
age = os.getenv("AGE")
city = os.getenv("CITY")

print(name)
print(age)
print(city)