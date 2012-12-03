

def create():
    """
    Function to create a new mash
    """
    form = crud.create(db.mash)
    return dict(form = form)

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def list():
    """
    Function to list all mashes owned by the current user
    """
    isAuthorized = True
    
    args = request.args
    if(len(args)>0) and args[0].isdigit():
        #Case When only one mash is to be  read and shown

        ##Check if the User is the owner of the mash
        row = db(db.mash.created_by==auth.user_id and db.mash.id==args[0]).select()        
        if(len(row)==0): #User doesnot have permissions to do this 
            return dict(isAuthorized = False)
        else:
            
            ##List Basic Mash Details, the "row" object will hold all the data
            
            ##List Images it holds with appropriate links
            for r in row:
                childFaces = db(db.face.mash_id==r.id).select(orderby=~db.face.elo_rating)
                        
            return dict(isAuthorized = True, row=r, childFaces = childFaces, perID= True)
    else:
            return dict(isAuthorized = False)

        
    
    rows = db(db.mash.created_by==auth.user_id).select()
    return dict(isAuthorized = True, rows=rows)


    
    
