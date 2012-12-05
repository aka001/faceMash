@auth.requires_login()
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


        

    mash_id = args[0]

    def onAccept(form):
        #Increment the number of images in the mash entry here
        rec = db(db.mash.id==args[0]).select().first()
        rec.num_of_images += 1
        rec.update_record()

        ##Resize uploaded Image here
        def resizeImage(imageName, box):
            #imageName : Name of the imageFile in the uploads directory
            # box : number containing the one edge in pixels of bounding box of the scaled image (always a square)
            import os
            import Image
            
            im = Image.open(request.folder + "uploads/" + imageName)
            w,h = im.size

            if w>h:
                k = box/float(w)
                h = int(k*h)
                w = int(box)
            else :
                k = box/float(h)
                w = int(k*w)
                h = int(box)

            
            im = im.resize((int(w),int(h)),Image.ANTIALIAS)
            im.save(request.folder + "uploads/" + imageName, "JPEG")

            return
            
            

        resizeImage(form.vars.image, 250)
        redirect(URL("mash","list",args=mash_id)) #As currently mash/list/[:mash_id] has the only interface to enter images to a mash
        
    
    db.face.mash_id.default = mash_id
    form = crud.create(db.face, onaccept=onAccept)
    form['_action'] = URL("face","create",args=mash_id)
    
    return dict(isAuthorized = isAuthorized, form = form, mash_id = mash_id)

@auth.requires_login()
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

    ##Delete the file
    r = db(db.face.id == args[1]).select().first()
    if r:
        import os
        os.remove(request.folder + "uploads/" + r.image)
    
    ##Delete Record Here
    db(db.face.id == args[1]).delete()

    #Update num of images in mash database here
    rec = db(db.mash.id==args[0]).select().first()
    rec.num_of_images -= 1
    if rec.num_of_images <0 :
        rec.num_of_images = 0
    rec.update_record()

    ##Redirect to the listing page of the mash_id
    redirect(URL("mash","list",args=args[0]))
    
    return dict(isAuthorized = isAuthorized)
