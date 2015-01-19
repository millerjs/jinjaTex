import jinja2
import tempfile
import atexit
import shutil
import os
import subprocess


def filter_braced(text):
    return "{%s}" % text


def newline(text):
    return text + "\\\\"


class Block:

    def __init__(self, blockType="", **kwargs):
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


class Image(Block):
    def __init__(self, **kwargs):

        args = {
            "path": "",
            "label": "",
            "width": .9,
            "caption": "",
        }

        args.update(kwargs)
        Block.__init__(self, blockType='image', **args)

    def __repr__(self):
        return "<PlyTeX Image %s>" % hash(self)


class Header(Block):
    def __init__(self, **kwargs):
        Block.__init__(self, blockType='header', **kwargs)

    def __repr__(self):
        return "<PlyTeX Header %s>" % hash(self)


class Table(Block):
    def __init__(self, **kwargs):
        Block.__init__(self, blockType='table', **kwargs)

    def __repr__(self):
        return "<PlyTeX Header %s>" % hash(self)


class Environment(Block):
    def __init__(self, **kwargs):
        Block.__init__(self,  blockType='table', **kwargs)

    def __repr__(self):
        return "<PlyTeX Environment %s>" % hash(self)


class Document:

    def __init__(self, templateVars=None):

        atexit.register(self.__cleanup__)

        self.vars = {
            "envPath": "templates/",
        }

        self.blocks = []
        self.addVars(templateVars)

        self.body = []
        self.template = None

        self.templateLoader = jinja2.FileSystemLoader(self['envPath'])
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)

        self.temporaryPath = None
        self.temporaryDir = tempfile.mkdtemp()
        self.templateEnv.filters['braced'] = filter_braced
        self.templateEnv.filters['newline'] = newline

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

    def Image(self, **kwargs):

        if 'path' not in kwargs:
            raise Exception("Please specify image kwarg 'path'")

        path = kwargs['path']
        directory = self.temporaryDir

        dst = os.path.join(directory, os.path.basename(os.path.normpath(path)))
        shutil.copyfile(path, dst)

        print "Copied file %s to %s" % (path, dst)

        image = Image(**kwargs)
        self.blocks.append(image)
        return image

    def Table(self, header, rows, **kwargs):
        kwargs['cols'] = len(header)

        convertedRows = []
        for i in range(len(rows)):
            if len(rows[i]) < len(header):
                rows[i] += [""] * (len(header) - len(rows[i]))
                print len(rows[i])
            convertedRows.append(" & ".join(rows[i]) + " \\\\ \hline ")

        for i in range(len(header)):
            header[i] = "\\textbf{%s}" % header[i]

        kwargs['header'] = " & ".join(header)
        kwargs['rows'] = convertedRows

        table = Table(**kwargs)
        self.blocks.append(table)
        return table

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

    def renders(self, templateVars=None):

        if templateVars:
            self.templateVars = templateVars

        if self.template:
            return self.template.render(self.templateVars, document=self)

    def render(self, templateVars=None, output=None, temporary=True):

        text = self.renders(templateVars)
        directory = self.temporaryDir

        path = tempfile.mktemp(dir=directory, suffix=".tex")
        if temporary:
            self.temporaryPath = path
        print "made file: ", path

        local = os.path.basename(os.path.normpath(path))

        if templateVars['preamble']:
            preamble = templateVars['preamble'] + ".tex"
            dst = os.path.join(
                directory, os.path.basename(os.path.normpath(preamble)))
            shutil.copyfile(preamble, dst)

        with open(path, 'w') as latex:
            latex.write(text)

        latex_proc = subprocess.Popen(["pdflatex", local],
                                      cwd=directory,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        latex_proc = subprocess.Popen(["pdflatex", local],
                                      cwd=directory,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)

        for line in latex_proc.stdout:
            print line,

        err = latex_proc.stderr.read()

        if latex_proc.returncode == 0:
            print "PlyTex SUCCESS"

        else:
            print "*** PlyTex might have failed ***"
            print err

        try:
            shutil.copyfile(path.replace('.tex', '.pdf'), output)

            print "Copied to %s" % output
        except Exception, msg:
            print "Unable to copy file to required location", msg

        if self.template:
            return self.template.render(self.templateVars, document=self)

    def __cleanup__(self):
        if self.temporaryDir:
            shutil.rmtree(self.temporaryDir)
            print "deleted", self.temporaryDir

        elif self.temporaryPath:
            os.remove(self.temporaryPath)

    def __repr__(self):
        return "<PlyTeX Document %s>" % hash(self)
