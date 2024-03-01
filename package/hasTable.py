class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HasTable:
    def __init__(self, inventory):
        self.inventory = inventory
        self.size = 0
        self.table = [None] * inventory

    # Process : Takes the key, hashes it, and ensures that the resulting hash value is within the hash table size
    # Flow : hash the key modulo it by the self.inventory then return it.
    def _hash(self, key):
        return hash(key) % self.inventory

    # Process : inserts multiple items into the hash table from an array passed to the method.
    # Flow : for i in array check that i's address isn't 4001 South 700 East. If it is not then get
    # Flow : i's id and insert it and i's value into the table
    def multi_insert(self, arraya):
        for i in arraya:
            if i.get_address() != "4001 South 700 East":
                self.insert(i.get_id(), i)

    # Process : uses the key variable passed to it insert a value into the hash table
    # Flow : set index to the hash value of the key. If the table is empty then insert the key/value as the first item
    # Flow : and increase the size. Else, set the current pointer to the value at that index
    # Flow : while there are items in the list check if any key in the table matches the key passed into the method
    # Flow : return if there is a matching key. If not set the pointer to current.next. Create a new node using the
    # Flow : key and value passed into the method. Set the new node to the position at table[index]. Set the next ptr
    # Flow : for the new node to self.table[index]. Increase the size by 1
    def insert(self, key, value):
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            new_node = Node(key, value)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

    # Process : accepts a key then searches the hash table for the key and returns its value
    # Flow : sets the index to be the hash value of the key variable. Set the pointer to the key at that index
    # Flow : Loop through the hash table. If the current.key == key then return the value at that key
    # Flow : if no key currently matches a key in the table then return false
    def search(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        return False

    # Loops through each key starting from the top. When the matching Key is found it checks if it is previous
    # If yes then sets previous.next to current.next else self.table[index] = current.next. Decrease self.size by 1
    # If key can't be found the raises  KeyError
    def remove(self, key):
        index = self._hash(key)

        previous = None
        current = self.table[index]

        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

        raise KeyError(key)

    def __len__(self):
        return self.size
