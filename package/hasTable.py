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

    def _hash(self, key):
        return hash(key) % self.inventory

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

    def returnline(self, a):
        index = self._hash(a)
        apple = self.table[index]
        self.remove(apple.key)
        return str(apple.key)

    def to_array(self):
        elements = []
        for i in range(self.inventory):
            current = self.table[i]
            while current:
                elements.append((current.key, current.value))
                current = current.next
        return elements

    def search(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        return False

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

    def contains(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False
