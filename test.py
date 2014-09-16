from plytex import Document, Header, Environment, Block
import yaml

settings_path = "settings.yaml"

with open(settings_path, 'r') as settings_file:
    settings = yaml.load(settings_file)['report']

doc = Document()
doc.loadTemplate("default.tex")

doc.Header(type='section', name='Chapter 1')
doc.Image(path = "test.png", label='img1', caption = "Image 1")

tableHeader = ['First', 'Second', 'Third']
rows = [
    ["row1" , " Other Text" , "Other Text 2"] ,
    ["row2" , "" , ""] ,
    ["row3" , "Other Text 4" , ""] ,
    ["row4" , " Other Text 6" , "Other Text"] ,
    ["row5" , "" ] ,
    ["row6" , " Other Text 9" , ""] ,
    ]

doc.Table(tableHeader, rows)
doc.blocks.append(Block(body = 'THIS IS SOME TEXT'))

print doc.renders(settings)

doc.render(settings, "/home/ubuntu/output.pdf")



