@auth.requires_login()
def create():
    """
    Function to create a new mash
    """
    def on_Accept_func(form):
        ##Enter the mash_id to Big ID mapping into the database here

        ##Look for all values in mash table which donot have a mapping in mashID_to_bigID_map table, and update them

        print db.executesql("SELECT MAX(id) FROM mash")
        
        pass
    
    form = crud.create(db.mash, onaccept = on_Accept_func, message="Mash Created !! Now Add Faces to it :)")
    return dict(form = form)

@auth.requires_login()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires_login()
def list():
    """
    Function to list all mashes owned by the current user
    """
    isAuthorized = True
    
    args = request.args
    if(len(args)>0) and args[0].isdigit():
        #Case When only one mash is to be  read and shown

        ##Check if the User is the owner of the mash

        mash_id = args[0]
        row = db(db.mash.created_by==auth.user_id and db.mash.id==mash_id).select()        
        if(len(row)==0): #User doesnot have permissions to do this 
            return dict(isAuthorized = False)
        else:
            
            ##List Basic Mash Details, the "row" object will hold all the data
            
            ##List Images it holds with appropriate links
            for r in row:
                childFaces = db(db.face.mash_id==r.id).select(orderby=~db.face.elo_rating)

                
                # Obtain urlHandle for the particular mash_id
                r = db(db.mash.id == mash_id).select().first()
                mash_url_handle = ""
                if r:
                    mash_url_handle = r.url_handle
            
            return dict(isAuthorized = True, row=r, childFaces = childFaces, perID= True, mash_url_handle = mash_url_handle, mash_id = mash_id)

        
    response.menu.append((T('Create a Mash'), False, URL(request.application,"mash","create"), []))

    rows = db(db.mash.created_by==auth.user_id).select()
    return dict(isAuthorized = True, rows=rows, perID = False)


@auth.requires_login()
def ajaxMashUrlHandleSearch():
    response.headers['Content-Type'] = "application/json"
    
    partialstr = request.args

    if len(partialstr)>0:
        partialstr = partialstr[0]
    else:
        redirect(URL("YourMash","home"))
    
    query = db.mash.url_handle==partialstr
    row = db(query).select()
    if row:
        return "false"
    else:
        return "true"

        
    
    
    
