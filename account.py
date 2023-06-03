import streamlit as st
class Account(object):
    def __init__(self, name, value, cstruc=None) -> None:
        self.name=name
        self.value=value
        self.cstruc=cstruc
        
class Collection(object):
    def __init__(self, type, **kwargs) -> None:
        self.type=type
        self.collection = kwargs
        self.count = len(self.collection.items())
        self.valid = self.validate()
        self.value = sum([x.value for x in self.collection.values()])
        
    def validate(self):
        return False if '' in [x for x in self.collection.keys()] else True
            
    def express_collection(self):
        st.write(self.collection)
        # for k, v in self.collection.items():
        #     # print(f"{k} -> {v.value}")
        #     st.write(f"{k} -> {v.value}")