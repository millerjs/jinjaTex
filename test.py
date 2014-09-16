from plytex import Document, Header, Environment
import yaml

settings_path = "settings.yaml"

with open(settings_path, 'r') as settings_file:
    settings = yaml.load(settings_file)['report']

doc = Document()
doc.loadTemplate("default.tex")

doc.Header(type='section', name='Chapter 1')
doc.Environment(type="verbatim")



print doc.renders(settings)



