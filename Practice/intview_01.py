
def addToList(val, list=[]):
 list.append(val)
 return list

list1 = addToList(1)
print ("list1 = %s" % list1)
list2 = addToList(123,[])
list3 = addToList("a")
print ("list1 = %s" % list1)
print ("list2 = %s" % list2)
print ("list3 = %s" % list3)