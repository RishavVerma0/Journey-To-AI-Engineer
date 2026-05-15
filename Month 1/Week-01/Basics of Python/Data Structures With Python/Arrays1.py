# 1. Let us say your expense for every month are listed below,
# i. January - 2200
# ii. February - 2350
# iii. March - 2600
# iv. April - 2130
# v. May - 2190
# Create a list to store these monthly expenses and using that find out,
# -
# 口
# 盛習Paused
# X
# :
# 1. In Feb, how many dollars you spent extra compare to January?
# 2. Find out your total expense in first quarter (first three months) of the year.
# 3. Find out if you spent exactly 2000 dollars in any month
# 4. June month just finished and your expense is 1980 dollar. Add this item to our monthly expense list
# 5. You returned an item that you bought in a month of April and got a refund of 200$. Make a correctibn to your monthly expense list based on this

#List of our monthly Expenses
expenses = [2200,2350,2600,2130,2190]

# 1. In Feb, how many dollars you spent extra compare to January?
extra_feb = expenses[1] - expenses[0]
print("1.In the month of February, you spent extra ${} compared to January.".format(extra_feb))

# 2. Find out your total expense in first quarter (first three months) of the year.

quater_sum = expenses[0] + expenses[1] + expenses[2]
print("2.The total expence for the first Quater is ${}.".format(quater_sum))

# 3. Find out if you spent exactly 2000 dollars in any month

print("3.If you spent exactly 2000 dollars in any month?", 2000 in expenses)

# 4. June month just finished and your expense is 1980 dollar. Add this item to our monthly expense list

expenses.append(1980)
print("4. Expenses after adding June:",expenses)

# 5. You returned an item that you bought in a month of April and got a refund of 200$. Make a correctibn to your monthly expense list based on this

expenses[3] = expenses[3] - 200
print("5. Corrected expenses list:", expenses)