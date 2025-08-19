class Soldier:
    def __init__(self,ID:int,first_name:str,last_name:str,phone_number:str,rank:str):
        self.ID = ID
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.rank = rank
    def to_dict(self):
        return {"ID":self.ID,
                "first_name":self.first_name,
                "last_name":self.last_name,
                "phone_number":self.phone_number,
                "rank":self.rank}