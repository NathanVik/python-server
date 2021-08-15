from data import data



def test_forloop():
    for i in range(10):
        print(i)


def print_titles():
    #method for FOR loops in python
    for prod in data:
        print(prod["title"])

def print_sum():
    sum = 0
    for item in data:
        sum += item["price"]

    print(f"the sum is: {sum}")
    
def print_test2(limit):
    #method to print title of items that cost more than 2 bucks
    for item in data:
        if(item["price"] > limit):
            print(f"{item['title']} - Price: ${item['price']}")


def print_category_list():
    results = []
    for item in data:
        cat = item["category"]

        if cat not in results:
            results.append(cat)
    print(results)

def run_test():
    print("running tests")


    #test_forloop()
    #print_titles()
    #print_sum() #Print sum of all prices in catalog
    #print_test2(3)
    print_category_list() #print list of unique categories



run_test()