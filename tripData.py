class activity:
    def __init__(self, name:str, location:str, cost:int, booked:bool, category:str, link):
        self.name = name
        self.location = location
        self.cost= cost
        self.booked = booked
        self.category = category
        self.link = link   
class dest:
    def __init__(self, locations:list[str], cost:int):
        self.locations = locations
        self.cost= cost
class hotel:
    def __init__(self, name:str, location:str, cost:int, booked:bool, rating:int, link):
        self.name = name
        self.location = location
        self.cost= cost
        self.booked = booked
        self.rating = rating
        self.link = link
class hotels:
    def __init__(self, hotelList:list[hotel]):
        self.hotelList = hotelList
class activities:
    def __init__(self, activityList:list[activity]):
        self.activityList = activityList
class transport:
    def __init__(self, type:str, fromLocation:str, toLocation:str, cost:int, booked:bool, link, departureTime:str="", arrivalTime:str=""):
        self.type = type
        self.fromLocation = fromLocation
        self.toLocation = toLocation
        self.cost= cost
        self.booked = booked
        self.link = link
        self.departureTime = departureTime
        self.arrivalTime = arrivalTime
class transportations:
    def __init__(self, transportList:list[transport]):
        self.transportList = transportList
class trip:
    def __init__(self, tripName:str, dest:dest, hotels:hotels, activities:activities, transportations:transportations, totalCost:int,startDate:str, endDate:str):
        self.tripName = tripName
        self.dest = dest
        self.hotels = hotels
        self.activities = activities
        self.transportations = transportations
        self.startDate = startDate
        self.endDate = endDate
        self.totalCost = totalCost
        def calculateTotalCost(self):
            total = 0
            for hotel in self.hotels.hotelList:
                total += hotel.cost
            for activity in self.activities.activityList:
                total += activity.cost
            for transport in self.transportations.transportList:
                total += transport.cost
            self.totalCost = total
            return total
class projects:
    def __init__(self, tripList:list[trip],ImgURLs:list[str]):
        self.tripList = tripList