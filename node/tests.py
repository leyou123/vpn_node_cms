from django.test import TestCase
# Create your tests here.

str1 ="中国,"

str2 = str1.split(",")
test = [i for i in str2 if i != '']


str2 ="中国,"

str4 = str2.split(",")
test1 = [i for i in str4 if i != '']



res = list(set(test).intersection(set(test1)))

print(test)


print("".join(res))
