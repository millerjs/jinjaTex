import jinja2
from jinja2 import Template

class Block:
    
    def __init__(self, blockType = None, **kwargs):
        self.children = []
        self.blockType = blockType

        self.vars = {
            'args': [],
            'type': "",
            'body': ""
            }

        for key, value in kwargs.iteritems():
            self.vars[key] = value
        
        self.body = ""

    def __getitem__(self, key):
        if key in self.vars:
            return self.vars[key]
        else:
            return ""

    def __setitem__(self, key, value):
        if key in self.vars:
            self.vars[key] = value
        else:
            return 
    
class Header(Block):

    def __init__(self, **kwargs):
        Block.__init__(self, 'header', **kwargs)

    def __repr__(self):
        return "<PlyTeX Header %s>" % hash(self)

class Environment(Block):

    def __init__(self, **kwargs):
        Block.__init__(self, 'environment', **kwargs)

    def __repr__(self):
        return "<PlyTeX Environment %s>" % hash(self)
    
class Document:

    def __init__(self, templateVars = None):

        self.vars = {
            "envPath": "templates/",
            }

        self.blocks = []
        self.addVars(templateVars)

        self.body = []
        self.template = None

        self.templateLoader = jinja2.FileSystemLoader(self['envPath'])
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)

    def getSection(self, name):
        return None

    def Header(self, **kwargs):
        header = Header(**kwargs)
        self.blocks.append(header)
        return header

    def Environment(self, **kwargs):
        environment = Environment(**kwargs)
        self.blocks.append(environment)
        return environment


    def loadTemplate(self, template_path):
        try:
            self.template = self.templateEnv.get_template(template_path)
        except Exception, msg:
            raise Exception("Unable to load template file: " + str(msg))

    def __setitem__(self, key, value):
        self.vars[key] = value
        return self

    def __getitem__(self, key):
        if key in self.vars:
            return self.vars[key]
        else:
            return None

    def setVars(self, templateVars):
        self.templateVars = templateVars


    def addVars(self, templateVars):
        if templateVars:
            for key, value in templateVars:
                self.vars[key] = value

    def renders(self, templateVars = None):

        if templateVars:
            self.templateVars = templateVars

        if self.template:
            return self.template.render(self.templateVars, document = self)

    def __repr__(self):
        return "<PlyTeX Document %s>" % hash(self)
    

