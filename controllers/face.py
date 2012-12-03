def create():
    """
    Function to add a new face to a mash

    /face/create/[:mash_id]
    """

    ## Checking if the mash_id has been passed in the URL and is a valid mash_id and the current useris the owner of the mash
    
    args = request.args
    if(len(args)>0 and args[0].isdigit()) and len(db(db.mash.created_by==auth.user_id and db.mash.id==args[0]).select())>0:
        isAuthorized = True
    else:
        isAuthorized = False
        return dict(isAuthorized = isAuthorized)

    db.face.mash_id.default = args[0]    
    form = crud.create(db.face)

    return dict(isAuthorized = isAuthorized, form = form)

def delete():
    """
    Function to delete a new face from a mash
    /face/delete/[:mash_id]/[:face_id]
    """
    
    ## Checking if the mash_id, face_id has been passed in the URL and is a valid mash_id and face_id and the current useris the owner of the mash
    
    args = request.args

    if(len(args)>=2 and args[0].isdigit() and args[1].isdigit() and len(db(db.mash.created_by==auth.user_id and db.mash.id==args[0]).select())>0 and len(db(db.face.id==args[1] and db.face.mash_id==args[0]).select())>0 and len(db(db.face.id==args[1]).select())>0 and len(db(db.face.mash_id == args[0]).select())):
       isAuthorized = True
    else:
        isAuthorized = False
        return dict(isAuthorized = isAuthorized)
    
    ##Delete Record Here
    db(db.face.id == args[1]).delete()
    return dict(isAuthorized = isAuthorized)
