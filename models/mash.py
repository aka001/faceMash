"""
Mash Table Defination
"""

db.define_table('mash',
                Field('name','string',length=40, notnull=True),
                Field('description', 'text', length=200, notnull=True),
                Field('created_on','datetime',default=request.now, readable=False, writable=False),
                Field('created_by',db.auth_user, default=auth.user_id , readable=False, writable=False ),
                Field('upload_addr', 'string', default=request.env.remote_addr, readable=False, writable=False),
                Field('num_of_images','integer',default=0,readable=False, writable=False),
                Field('is_private', 'boolean', default = False, readable = False, writable = True),
                Field('is_private_password', 'password', readable = False, writable = True ),
                format = '%(name)s(%(id)s)',
                )


"""
Face Table Defination
"""

db.define_table('face',
                 Field('name', 'string', length=40, required=True),
                 Field('image', 'upload', required=True, requires=IS_IMAGE(extensions=('bmp','gif','jpeg','png'), maxsize=(300,300), minsize=(0,0))),
                 Field('created_on','datetime',default=request.now, readable=False, writable=False),
                 Field('created_by',db.auth_user, default=auth.user_id , readable=False, writable=False ),
                 Field('upload_addr', 'string', default=request.env.remote_addr, readable=False, writable=False),
                 Field('mash_id',db.mash, readable=False, writable=False, required=True),
                 Field('won','integer',default=0,readable=False , writable=False),
                 Field('lost','integer',default=0,readable=False, writable=False),
                 Field('elo_rating','decimal(6,4)',readable=False, default=1600.00,writable=False),
                 )
