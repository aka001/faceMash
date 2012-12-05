
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def index():
    ###########
    #Defining the Elo Rating Computing Function
    ###########
##EloRatingFunction

    def __calculate_elo_rank(player_a_rank=1600, player_b_rank=1600, winner= 1, penalize_loser=True, PLAYER_A = 1, PLAYER_B = 2):
	import math

	if winner is PLAYER_A:
	    winner_rank, loser_rank = player_a_rank, player_b_rank
	else:
	    winner_rank, loser_rank = player_b_rank, player_a_rank
	rank_diff = winner_rank - loser_rank
	exp = (rank_diff * -1) / 400
	odds = 1 / (1 + math.pow(10, exp))
	if winner_rank < 2100:
	    k = 32
	elif winner_rank >= 2100 and winner_rank < 2400:
	    k = 24
	else:
	    k = 16
	new_winner_rank = round(winner_rank + (k * (1 - odds)))
	if penalize_loser:
	    new_rank_diff = new_winner_rank - winner_rank
	    new_loser_rank = loser_rank - new_rank_diff
	else:
	    new_loser_rank = loser_rank
	if new_loser_rank < 1:
	    new_loser_rank = 1
	if winner is PLAYER_A:
	    return (new_winner_rank, new_loser_rank)
	return (new_loser_rank, new_winner_rank)  
    
    args = request.args
    isValid = True
    myMashId = ""
    
    if(len(args)>0):
        r = db(db.mash.url_handle==args[0]).select().first()
        if r:
            myMashId = r.id
        else:
            isValid = False
            return dict(isValid = isValid)
        """
    else:
        #redirect to the Home Page
        redirect("YourMash","home")
        """
    
    
    ##Check for private mash to be done here

    ##Check for private mash done

    rows = db(db.face.mash_id==myMashId).select(limitby=(0,2), orderby='<random>')
        
    if(len(rows)!=2):
        return dict(isValid=False, mash_id=myMashId)
    else:
        response.menu.append((T('Rank List'), False, URL('YourMash', 'rankList', args=myMashId), []))
        form = FORM(INPUT(_name="face1", value=str(rows[0].id), _type="hidden"),
                    INPUT(_name="face2", value=str(rows[1].id), _type="hidden"),
                    INPUT(_name="selection", _id="mySelection", requires=IS_NOT_EMPTY(), _type="hidden"),
                    INPUT(_type='submit', _id="mySubmit"))

        if form.accepts(request,session):

            face1 = request.vars.face1
            face2 = request.vars.face2

            selection = request.vars.selection


            if selection not in [face1, face2]:
                exit()
            else:
                #update DB

                face1_row = db(db.face.id == int(face1)).select()[0]
                face2_row = db(db.face.id == int(face2)).select()[0]

                
                if face1 == selection:
                    face1_row.won = int(face1_row.won) + 1
                    face2_row.lost = int(face2_row.lost) + 1
                        
                    (face1_row.elo_rating, face2_row.elo_rating) = __calculate_elo_rank(float(face1_row.elo_rating),float(face2_row.elo_rating), winner=face1, penalize_loser=True, PLAYER_A = face1, PLAYER_B = face2)
                else:
                    face2_row.won = int(face2_row.won) + 1
                    face1_row.lost = int(face1_row.lost) + 1
                        
                    (face1_row.elo_rating, face2_row.elo_rating) = __calculate_elo_rank(float(face1_row.elo_rating),float(face2_row.elo_rating), winner=face2, penalize_loser=True, PLAYER_A = face1, PLAYER_B = face2)

                    
                face1_row.update_record()
                face2_row.update_record()
                    
                response.flash = "Whoz your pick !!" ##Replace this by random cheesy lines

        elif form.errors:
                response.flash = "You are trying to do something funny there !! Go try that sumwhere else.."
        else:
                response.flash = "Whoz your pick !!"

        return dict(rows=rows, form=form, isValid = isValid)


def rankList():
    args = request.args

    if(len(args)>0):
        r = db(db.mash.url_handle==args[0]).select().first()
        if r:
            mash_id = r.id
        else:
            return dict(isValid = False)
        
        #Check for private mash_id to be inserted here
        
        rows = db(db.face.mash_id == mash_id).select(orderby=~db.face.elo_rating)
        
        response.menu.append((T('Mash'), False, URL('YourMash', 'index', args=mash_id), []))
        return dict(isValid = True, rows = rows)
    else:
        return dict(isValid = False)

def home():
    return dict()
    

        
