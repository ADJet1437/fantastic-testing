class Entry:

    def __init__(self, prefix, price):
        self.prefix = prefix
        self.price = price
        self.children = []

    def find_child(self, entry):
        return entry.prefix.startswith(self.prefix)

    def add_child(self, new_entry):
        for child in self.children:
            if child.find_child(new_entry):
                child.add_child(new_entry)
                return
            if new_entry.find_child(child):
                new_entry.add_child(child)
        for each in new_entry.children:
            if each in self.children:
                self.children.remove(each)
        self.children.append(new_entry)

    def find_entry(self, phone_number):
        # find a better entry in its children
        for child in self.children:
            if phone_number.startswith(child.prefix):
                return child.find_entry(phone_number)
        # if none of child matches, return itself
        return self


class Operator:

    def __init__(self, name, filepath):
        self.name = name
        self.root_entry = Entry(None, None)
        self.init_price_tree(filepath)

    def add_entry(self, entry):
        self.root_entry.add_child(entry)

    def init_price_tree(self, filepath):
        with open(filepath) as f:
            for line in f:
                prefix, price = line.strip().split()
                self.add_entry(Entry(prefix, price))

    def find_entry(self, phone_number):
        entry = self.root_entry.find_entry(phone_number)
        # print("Best route: ", entry.prefix, entry.price)
        return entry


class Router:

    operators = []

    def add_operator(self, name, price_file):
        self.operators.append(Operator(name, price_file))

    def route(self, phone_number):

        best_entry = {"name": None, "prefix": None, "price": None}

        for operator in self.operators:
            entry = operator.find_entry(phone_number)
            # operator not available
            if entry.price is None:
                continue
            # first found operator or find better result
            if best_entry["price"] is None or entry.price < best_entry["price"]:
                best_entry = {"name": operator.name, "prefix": entry.prefix, "price": entry.price}

        return best_entry


if __name__ == "__main__":
    router = Router()
    router.add_operator("A", "price_lists/test1.txt")
    router.add_operator("B", "price_lists/test2.txt")
    # enter the number that the area code fits in the price lists, e.g. 23, 155, 1546 ...
    result = router.route("231556098")
    print(result["name"], result["prefix"], result["price"])
