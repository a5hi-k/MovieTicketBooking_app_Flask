from applications.config import Create_ticketbookingapplicaton



app,api=Create_ticketbookingapplicaton()



from applications.api import VenueAPI,ShowAPI

api.add_resource(VenueAPI,"/api/venue/<int:venue_id>","/api/venue")

api.add_resource(ShowAPI,"/api/show/<int:show_id>","/api/show")




if __name__ == '__main__':

    app.run(debug=True)    