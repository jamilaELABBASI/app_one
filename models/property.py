from odoo import models, fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta

class Property(models.Model):
    _name = "property"
    _description = "Property"
    _inherit=['mail.thread','mail.activity.mixin']
    # 1️⃣ mail.thread
    # ➡️ Ajoute le chatter
        # historique des messages
        # suivi des changements (tracking)
        # log automatique des champs suivis

    # 2️⃣ mail.activity.mixin
    # ➡️ Ajoute les activités
        # To Do
        # Call
        # Email
        # deadlines
        # rappels

    # Tu obtiens automatiquement dans le form view :
        # un bouton “Activities”
    # possibilité de :
        # ajouter une activité
        # choisir le type (To Do, Call…)
        # assigner à un utilisateur
        # mettre une date limite
        # 👉 Sans écrire de code supplémentaire.
    ref=fields.Char(default='New',readonly=True)
    name = fields.Char(required=True,default='Nom',size=12)
    description = fields.Text(tracking=True)
    postcode = fields.Char()
    date_availability = fields.Date(tracking=True)
    expected_selling_date= fields.Date(tracking=True)
    is_late=fields.Boolean()
    expected_price = fields.Float()
    #(digits=(0,5)))
    selling_price = fields.Float()
    diff=fields.Float(compute='_compute_diff')
    # 👉 compute sert à calculer automatiquement la valeur d’un champ à partir d’autres champs.
    # ➡️ Tu ne remplis pas ce champ à la main, Odoo le fait pour toi.
    # compute le champss ne sera ni cree ni stocke dans la base de donnees
    # si vous ajouter , store=1 le champs sera cree et stocke sur la BD
    # champs sera en mode lecture seul si vous ajouter readonly=0 sera changer en mode ecriture car par defaut il est en mode lecture
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups="app_one.property_manager_group")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    #, default='north'
    owner_id=fields.Many2one("owner")
    owner_adresse=fields.Char(related='owner_id.address',readonly=False,store=True) # on tourne readonly false si on veut mettre le champs changable related field as computer ne sera pas stocker dans la base de donnees si on le veut stocker on doit utiliser store
    # 1️⃣ related='owner_id.address'
        # owner_adresse devient un champ lié (related) à owner_id.address.
        # Toute modification de owner_adresse peut se répercuter sur owner_id.address si readonly=False.
        # owner_id doit être un Many2one existant dans ce modèle.
    # 2️⃣ readonly=False
        # Par défaut, les champs related sont readonly=True.
        # Ici, tu dis que tu veux pouvoir modifier le champ directement.
        # Odoo écrit alors sur le champ lié (owner_id.address) quand tu modifies owner_adresse.
    # 3️⃣ store=True
        # Le champ est stocké en base.
        # Permet de :
        # le filtrer dans un search ou domain
        # l’afficher dans un tree view
        # Sans store=True :
        # le champ est calculé à la volée
        # pas possible de le rechercher facilement
    # 🧠 Points importants
        # Si readonly=False et que l’utilisateur modifie owner_adresse :
        # Odoo met à jour le champ réel owner_id.address
        # Peut impacter d’autres enregistrements si la relation n’est pas unique
        # Si store=False :
        # Tu ne peux pas faire de filtre dans le tree ou search
    # Bonnes pratiques :
        # related + store=True pour filtrer/rechercher
        # readonly=False seulement si tu veux vraiment modifier le champ lié depuis le parent
    owner_phone=fields.Char(related='owner_id.phone',readonly=False) # readonly false on autorisela modification de la valeur
    tag_ids=fields.Many2many("tag")
    state=fields.Selection([
        ( 'draft','Draft'),
        ( 'pending','Pending'),
        ( 'sold','Sold'),
        ( 'closed','Closed'),
    ],default='draft')

    # pour activer l'archivage
    active=fields.Boolean(default=True)

    # 1️⃣ 'unique_name'
        # Nom de la contrainte
        # Obligatoire, sert à identifier la contrainte dans la base de données.
    # 2️⃣ 'unique(name)'
        # Type de contrainte SQL : ici, UNIQUE sur le champ name
        # Cela empêche la création de deux enregistrements avec le même name.
    # 3️⃣ 'This name already exists. Please choose another.'
        # Message d’erreur affiché à l’utilisateur si la contrainte est violée.

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'This name already exists. Please choose another.')
    ]

    line_ids=fields.One2many("property.line","property_id")
    create_time=fields.Datetime(default=fields.Datetime.now())
    next_time=fields.Datetime(compute='_compute_next_time')

    # depends on utilise toujours avec les champs compute
    # 'owner_id.phone' ca veux dire quand le phone change executer pour moi cette method
    # depends can take the view fields and model fields or relationnal fields as owner_id.phone because is a field in owner model
        # C’est utilisé avant une méthode compute.
        # Indique à Odoo quand recalculer le champ calculé.
        # 🔹 Fonctionnement
        # expected_price ou selling_price change → Odoo déclenche le calcul.
        # owner_id.phone change → Odoo déclenche aussi le calcul.
        # ➡️ Même si phone est dans un modèle lié (Many2one), le compute sera mis à jour automatiquement.
    @api.depends('expected_price','selling_price','owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print('inside _compute_diff method')
            rec.diff=rec.expected_price - rec.selling_price

    # field doit etre simple c'est a dire existe sur la vue
    # onchange can take just the view fields means just fields displayed in the form
    # une fois la valeur d'expected_price change la method sera executer
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec) # va afficher newId ca veux dire ???
            # et lorsqu'on a afficher rec dans method depens on voir lid de record enregistrer
            print('inside _onchange_expected_price method')
            # si l'utilisateur entrer une valeur negative on va lui afficher un msg d'erreur
        return{
            'warning':{'title':'warning','message':'negative value','type':'notification'}
        }

    @api.constrains('bedrooms')
    def _check_bedrooms_greator_zero(self):
        for property in self:
            if property.bedrooms==0:
                print('not valid')
                raise ValidationError('please add valiid number of bedrooms')

    """
    # CRUD operations
    # cest methodes sont deja definit au niveau du model qui ete herite par notre model Property

    #Ovveride redifinir la methode create
    # Create method
    @api.model_create_multi
    def create(self, vals_list):
        # recuperer la methode a partie de resource
        res = super(Property, self).create(vals_list)
        #res=super().create(self,vals)  # 2 eme ecriture de la methode

        print("inside create method")
        # your custom logic
        return res

    #Read
    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, **kwargs):
        print("inside search method")
        # Forward all arguments safely to super
        res = super(Property, self)._search(domain, offset=offset, limit=limit, order=order, **kwargs)
        # Logic
        return res

    #Update
    def write(self, vals):
        res = super(Property,self).write(vals)
        print("inside write method")
        return res

    #Delete
    def unlink(self):
        res=super(Property,self).unlink()
        print('inside unlike method')
        return res

"""
    def action_state(self):
        for rec in self:
            print('inside state action method')
            if rec.state=='draft':
                rec.state='pending'
            elif rec.state=='pending':
                rec.state='sold'
            else:
                rec.state='draft'


    def action_draft(self):
        for rec in self:
            self.create_history_record(rec.state,"draft",'action_draft_method')
            #print('inside draft action method')
            rec.state="draft"
            # on peut aussi changer la valeur de la variable via la methode de update rec.write({'state':'draft'})

    def action_pending(self):
        for rec in self:
            #print('inside draft action method')
            self.create_history_record(rec.state,"pending",'action_pending_method')
            rec.state = "pending"
            # on peut aussi changer la valeur de la variable via la methode de update rec.write({'state':'draft'})

    def action_sold(self):
        for rec in self:
            self.create_history_record(rec.state,"sold",'action_sold_method')
            #print('inside draft action method')
            rec.state = "sold"
            # on peut aussi changer la valeur de la variable via la methode de update rec.write({'state':'draft'})

    def action_closed(self):
        for rec in self:
            self.create_history_record(rec.state,"closed",'action_closed_method')
            #print('inside action_closed method')
            rec.state="closed"

    def check_expected_selling_date(self):
        #print('inside check_expected_selling_date method')
        #print(self)
        property_ids=self.search([]) # recuperer tooous  les enregistrements equivalent de select * from property;
        #print(property_ids)
        for rec in property_ids:
            #print(rec)
            #verifier si rec.expected_selling_date  a une valeur est elle est pas nul
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late=True

    # env pour acceder a nimport quel model ex user , company ...
    def action(self):
        # domaine sous forme dune liste
        #[("name","=","Villa"),("","",""),("","","")] # operator > < in =  != like(il contient la chaine de caratere meme si elle est en majuscule) ilike
        #print(self.env['property'].search([("name","!=","Villa"),("bedrooms","=",2)]))
        print(self.env['property'].search(['!',("name","!=","Villa"),("bedrooms","=",2)]))
        print(self.env['property'].search(['&',("name","!=","Villa"),("bedrooms","=",2)])) # par defaut cest le AND tous les conditions doivent etre verifiees
        print(self.env['property'].search(['|',("name","!=","Villa"),("bedrooms","=",2)])) # OR

        """
        print('******************* User Infos *******************')
        print(self.env.user)
        print(self.env.user.login)
        print(self.env.user.name)
        print(self.env.user.email)
        print(self.env.user.phone) """
        print('******************* Company Infos *******************')
        """print(self.env.company.street)
        print(self.env.company.partner_id)
        print(self.env.context)
        print('******************* Object *******************')
        print(self.env['owner'].create({'name':'name two','phone':'0661243562'}))
        print(self.env['owner'].search([]))
        print(self.env['owner'].search([('id', '=', 1)], limit=1))
        print(self.env['owner'].browse([('id','=',1)]))
         """

    @api.model
    def create(self,vals):
        res=super(Property,self).create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('property_seq')
        return res


    def create_history_record(self,old_state,new_state,reason):
        for rec in self:
            rec.env['property.history'].create({
                'user_id':rec.env.uid,
                'property_id':rec.id,
                'old_state':old_state,
                'new_state':new_state,
                'reason':reason or "",      # si reason n'a pas de valeur va prendre une chain evide
                'line_ids':[(0,0,{'description':line.description,'area':line.area }) for line in rec.line_ids],
   })

    """
            # env contient l'environnement d'execution complet (tous les infos sur user(utilisateur courant),context,cr(connexion , db))
    env =   ├── Modèles ORM(env['model'])
            ├── Utilisateur(env.user, env.uid)
            ├── Contexte(env.context)
            ├── Société(env.company, env.companies)
            ├── Base de données(env.cr)
            ├── Langue(env.lang)
            ├── Sécurité(sudo, is_superuser)
            ├── Références XML(env.ref)
            └── Mécanismes internes(registry, cache)
    """


    def action_open_change_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.property_change_state_wizard_window_action') #nom de lapp.id du record de window action
        action['context']={'default_property_id':self.id} # cest le lien entre le wizard et property
        return action

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time=rec.create_time+timedelta(hours=6)
            else:
                rec.next_time =False







class PropertyLine(models.Model):
    _name ="property.line"
    property_id=fields.Many2one('property')
    area=fields.Float()
    description=fields.Char()


    # 1️⃣ @api.depends
        # 🔹 But
        # Pour les champs calculés (compute).
        # Indique à Odoo quand recalculer le champ automatiquement.

    # 2️⃣ @api.onchange
        # 🔹 But
        # Pour réagir à un changement dans le formulaire.
        # Affecte l’interface avant de sauvegarder.
        # Utile pour :
            # remplir un champ automatiquement
            # afficher un warning
            # modifier des valeurs dans le form

    #  3️⃣ @api.constrains
        # 🔹 But
        # Pour vérifier des règles métier avant sauvegarde.
        # Lève une erreur si la condition n’est pas respectée.